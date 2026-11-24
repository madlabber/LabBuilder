# vcenter_prep

Prepares a freshly deployed vCenter: creates the datacenter and cluster, adds the ESXi hosts, creates a datastore on the first host, and uploads installer ISOs to it. Run by the "Prepare vCenter" play for hosts in the `vcenter_prep` group, which stage 2 blueprints (roles/stage2) generate for a lab's own vCenter.

- **Cluster:** `vmware.vmware.cluster` (`community.vmware.vmware_cluster` is gone in community.vmware 6).
- **Hosts:** `files/add_esx_host.py` (pyVmomi) adds each host, taking its certificate thumbprint from vCenter's SSL fault, so it works whether or not the host itself is reachable.
- **Datastore:** ESXi 8 keeps its whole boot disk for itself (OSData), so give the host a separate data disk with `create_local_vmfs: 'False'`. The helper formats the first host's largest empty disk as VMFS 6 named `vcenter_prep_datastore` (default `datastore1`), unless it already has one. Make the data disk bigger to give users more room.
- **ISOs:** `vcenter_prep_isos` (files in `files/`) go to `[datastore1] ISO/`, uploaded with a 2-hour timeout; ISOs already there are left alone.

Variables: see `defaults/main.yml`; the play in `main.yml` maps them from the stage 2 vars file.
