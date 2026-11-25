# vsphere_prep

Prepares a freshly deployed vCenter: creates the datacenter and cluster, adds the ESXi hosts, creates a datastore on the first host, and uploads installer ISOs to it. Run by the "Prepare vSphere" play for hosts in the `vsphere_prep` group, which stage 2 blueprints (roles/stage2) generate for a lab's own vCenter.

- **Configuration:** the role uses the usual LabBuilder variables, with no copies of its own: `vcenter_address`, `vcenter_username`, `vcenter_password`, `vcenter_datacenter`, `vcenter_cluster`, `esxi_username` and `esxi_password` from the mainvars file (`vars/main.yml`), and `lab_vm_datastore` from the lab inventory. `esx_hosts` lists the ESXi hosts to add.
- **Cluster:** `vmware.vmware.cluster` (`community.vmware.vmware_cluster` is gone in community.vmware 6).
- **Hosts:** `files/add_esx_host.py` (pyVmomi) adds each host, taking its certificate thumbprint from vCenter's SSL fault, so it works whether or not the host itself is reachable.
- **Datastore:** ESXi 8 keeps its whole boot disk for itself (OSData), so give the host a separate data disk with `create_local_vmfs: 'False'`. The helper formats the first host's largest empty disk as VMFS 6 named `lab_vm_datastore`, unless it already has one. Make the data disk bigger to give users more room.
- **ISOs:** `isos` (files in `files/`) go to `[lab_vm_datastore] ISO/`, uploaded with a 2-hour timeout; ISOs already there are left alone. Set `isos` on the host in the inventory, or pass it as an extra var: `-e '{"isos": ["debian-12.11.0-amd64-netinst.iso"]}'`.
