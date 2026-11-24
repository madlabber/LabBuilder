#!/usr/bin/env python3
"""Add an ESXi host to a vCenter cluster, and give it a datastore.

The host's certificate thumbprint comes from vCenter itself: the host is added without one, and
the thumbprint from the SSLVerifyFault vCenter answers with is used to add it again. So it works
whether or not the machine running it can reach the host (community.vmware.vmware_host connects
to the host to read the thumbprint).

With DATASTORE given, it also makes sure the host has a datastore of that name: if it has none,
the largest empty disk is formatted as VMFS 6 (ESXi 8 keeps its boot disk for itself, so the
lab gives the host a separate data disk).

Usage: add_esx_host.py VCENTER DATACENTER CLUSTER ESX_FQDN [DATASTORE]
Passwords come from the environment: VC_USER, VC_PASSWORD, ESX_USER, ESX_PASSWORD.
Prints "added" or "present" (already in the cluster), then "datastore created" if it made one;
errors exit 1.
"""
import os
import ssl
import sys
import time

from pyVim.connect import Disconnect, SmartConnect
from pyVmomi import vim


def wait(task):
    while task.info.state in (vim.TaskInfo.State.queued, vim.TaskInfo.State.running):
        time.sleep(3)
    if task.info.state != vim.TaskInfo.State.success:
        raise task.info.error
    return task.info.result


def ensure_datastore(host, name):
    """Format the host's largest empty disk as VMFS 6 named `name`, unless it already has `name`."""
    if any(ds.name == name for ds in host.datastore):
        return
    storage = host.configManager.storageSystem
    storage.RescanAllHba()                                 # a disk added while the host was running
    dss = host.configManager.datastoreSystem
    disks = sorted(dss.QueryAvailableDisksForVmfs(), key=lambda d: d.capacity.block * d.capacity.blockSize)
    if not disks:
        raise RuntimeError(f'{host.name} has no datastore "{name}" and no empty disk to create one on')
    disk = disks[-1]
    options = dss.QueryVmfsDatastoreCreateOptions(devicePath=disk.devicePath, vmfsMajorVersion=6)
    spec = options[0].spec
    spec.vmfs.volumeName = name
    dss.CreateVmfsDatastore(spec=spec)
    print('datastore created')


def main():
    vc, dc_name, cl_name, esx = sys.argv[1:5]
    ds_name = sys.argv[5] if len(sys.argv) > 5 else ''
    si = SmartConnect(host=vc, user=os.environ['VC_USER'], pwd=os.environ['VC_PASSWORD'],
                      sslContext=ssl._create_unverified_context())
    try:
        content = si.RetrieveContent()
        dc = next(d for d in content.rootFolder.childEntity if isinstance(d, vim.Datacenter) and d.name == dc_name)
        cluster = next(c for c in dc.hostFolder.childEntity if isinstance(c, vim.ClusterComputeResource) and c.name == cl_name)
        host = next((h for h in cluster.host if h.name.lower() == esx.lower()), None)
        if host:
            print('present')
        else:
            spec = vim.host.ConnectSpec(hostName=esx, userName=os.environ['ESX_USER'],
                                        password=os.environ['ESX_PASSWORD'], force=True)
            try:
                host = wait(cluster.AddHost_Task(spec=spec, asConnected=True))
            except vim.fault.SSLVerifyFault as fault:
                spec.sslThumbprint = fault.thumbprint
                host = wait(cluster.AddHost_Task(spec=spec, asConnected=True))
            print('added')
        if ds_name:
            ensure_datastore(host, ds_name)
    finally:
        Disconnect(si)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:  # report the vSphere fault text, not a traceback
        print(f'error: {getattr(e, "msg", None) or e}', file=sys.stderr)
        sys.exit(1)
