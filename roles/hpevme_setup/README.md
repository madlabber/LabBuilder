# hpevme_setup

Sets up HPE VM Essentials from inside a lab. It runs in the stage 2 LabBuilder run on the lab's
Ansible VM (`roles/stage2`), because the HVM hosts and the ONTAP sim are only reachable on the lab
LAN. The stage 2 blueprint puts the HVM hosts in group `hpevme`, reached over SSH as the install
user (paramiko, password), and the "Set up HPE VM Essentials" play in `main.yml` runs this role.

| Step | File | Turned off by |
|---|---|---|
| Wait for each host's unattended install, hvmcli and `vs0` | `main.yml` | (always) |
| ONTAP SVM `svm_vme`: NFS LIF, an iSCSI LIF per node, NFS volume `/vme_nfs`, iSCSI LUN `vme_gfs2` mapped to every host's IQN | `ontap.yml` | `hpevme_ontap: false` |
| Manager VM on the first host with `hvmcli deploy manager`, from the qcow2.gz on the Manager ISO (a CD on that host) | `manager.yml` | `hpevme_manager: false` |
| First-time setup, license (if given), group, the lab's vCenter as a cloud | `manager_api.yml` | `hpevme_setup_manager: false` |
| HVM cloud and cluster from the three hosts, NFS datastore | `cluster.yml` | `hpevme_create_cluster: false` |

`lab_hpevme_manual` keeps only the ONTAP step, so the user deploys the Manager and builds the
cluster with the lab guide.

## Status

- The host install and `hvmcli` flags were checked against HPE's 26.04 ISO and the 9.1.0-3 Manager
  README; the installer-config format against HPE's `configure_mgmt_ip.sh`.
- `cluster.yml` follows the Morpheus API docs, but hasn't been run against 9.1.0-3: it looks up the
  cluster type, cloud type and layout by name and shows the API's message if the Manager refuses
  the request. The GFS2 datastore on the iSCSI LUN is left to the user (it needs the cluster's
  heartbeat setup).
- Without `hpevme_license` the Manager runs unlicensed, and may refuse cluster creation until a
  license is applied.
