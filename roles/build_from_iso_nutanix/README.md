# build_from_iso_nutanix

Builds Nutanix Community Edition 2.1 (AHV) nodes as nested VMs on vCenter, then creates the cluster.
It doesn't support PVE yet.

## What it needs
* `files/phoenix.x86_64-fnd_5.6.1_patch-aos_6.8.1_ga.iso`, the CE 2.1 ISO (about 7 GB). The role makes an unattended copy of it next to it (see below) and uploads that once to `iso_datastore`.
* An inventory group (default `nutanix`). Each host sets `ip_address` (the AHV host) and `cvm_address`.
* A lab gateway that forwards a WAN port to the first CVM's SSH. LabBuilder creates the cluster through it:
  ```yaml
  rdp_jumphost: ""          # otherwise it replaces nat_rules
  nat_rules:
    - { name: "SSH to the first CVM", external_port: "2222", internal_port: "22", protocol: "tcp", target_ip: 192.168.0.61 }
  ```
See `inventories/lab_nutanix.yml` (1 node) and `inventories/lab_nutanix3.yml` (3 nodes).

## How the install is automated
No keystrokes: the CE installer runs unattended from an answer file, the same way Nutanix Foundation drives phoenix.

1. **Unattended ISO** (`tasks/vmw/make_install_iso.yml`, once per controller): xorriso rebuilds the CE ISO in `files/` as `<install_iso>-unattended.iso` (about 15 minutes, then reused). Two changes:
   * the CE Installer boot line gets `AZ_HINT=<UUID>`. With it, phoenix mounts the volume with that UUID, reads `arizona.cfg` from it and installs without the GUI;
   * the AOS installer, split on the ISO into `.tar.p00` and `.tar.p01`, is joined into one `.tar`, because the unattended installer checks it as a tar file.
   All nodes share one copy on `iso_datastore`.
2. **Seed ISO per node** (`tasks/vmw/make_seed_iso.yml`): `templates/arizona.cfg.j2` becomes the node's answer file (AHV and CVM addresses, disks, EULA accepted, and the AOS and AHV images as `file://` paths on the installer CD, which the CE boot leaves mounted at `/mnt/iso`, each as `{url, md5sum}`; phoenix needs that form, and an empty `md5sum` skips the check for files that are already local). It goes on a small ISO, `<vm_name>-arizona.iso`, attached as the VM's second CD. Every seed has the same volume UUID (`nutanix_az_volume_date`), so the one boot line finds each node's own file.
3. **Power on.** The installer images AHV and the CVM and reboots on its own; the VM boots from disk first, so it comes up in AHV.

The answer file assigns the disks by name, and the VM is built to match. VMware paravirtual disks report as SSD:

| Disk | Device | Size | Used for |
|---|---|---|---|
| scsi0:0 | sda | 64 GB | AHV boot (`nutanix_hyp_boot_disk`) |
| scsi0:1 | sdb | 500 GB | CVM boot, at least 200 GB (`nutanix_cvm_boot_disks`) |
| scsi0:2 | sdc | 250 GB | data (`nutanix_cvm_data_disks`) |

`disk.EnableUUID=TRUE` gives the disks serial numbers, which the installer and the CVM need. CPU virtualization is exposed to the guest. The controller needs `xorriso` (install-requirements.yml installs it).

Re-running the playbook leaves installed nodes alone. To rebuild a node, run with `state=force`.

## Cluster creation (`tasks_from: create_cluster.yml`, run once)
1. Finds the gateway's WAN IP in vCenter. Each CVM command then runs from LabBuilder over `WAN:2222` as `nutanix`, through `files/cvm_ssh.py`. That helper uses paramiko, so `sshpass` isn't needed, and it retries until the command succeeds, because the CVM reboots once during its first boot.
2. Waits until genesis (port 2100) answers on every CVM.
3. Runs `cluster -s <all CVM IPs> create`, with `--redundancy_factor=1` when there's one node, plus the cluster name, virtual IP, DNS and NTP.
4. Tries to set the Prism `admin` password to `nutanix_admin_password`, which is the lab password in `main.yml`. Prism's rules are stricter than the four character classes: no dictionary words, and no more than 2 identical characters in a row. If Prism refuses the password, the role prints the reason and `admin` keeps the CE default `nutanix/4u`. Prism then asks for a new one at the first sign-in.

The first Prism sign-in still asks for a Nutanix .NEXT account (my.nutanix.com), so the lab needs internet access through the gateway.

## Lab VM network (`tasks/lab_network.yml`)
Once the cluster exists, the role can create a managed AHV network on the lab LAN (VLAN 0, IP management on, the lab's DNS and domain), e.g. as the target network for VMs that Nutanix Move migrates:
```yaml
nutanix_lab_network: lab-lan
nutanix_lab_network_pool_start: 192.168.0.100   # outside the gateway's DHCP range
nutanix_lab_network_pool_end:   192.168.0.120
```

## The Move demo lab
`inventories/lab_nutanix_move.yml` (1 node) adds a VMware source next to the cluster: vCenter 8.0 U3 (`vc01`) and one ESXi host (`esx01`, with a data disk for `datastore1`), plus an **Ansible VM** (`ansible`, AlmaLinux 9). The last play runs **stage 2** on that VM, inside the lab (roles/stage2): it prepares `vc01` (roles/vcenter_prep), puts Windows Server 2019 and Debian 12 ISOs on `datastore1`, and deploys Move from its OVA on `esx01` with "Deploy OVF files". Users then build a small Windows VM and a small Linux VM and migrate both; `lab-lan` is the target network on the cluster. The Move guide documents the OVA for ESXi-to-ESXi, and Move 6.3.3 is qualified with AOS 6.10 while CE 2.1 runs AOS 6.8.1; the lab guide notes both and walks through the migration.

## Timing
| Variable | Default | Meaning |
|---|---|---|
| `nutanix_cluster_wait` | 5400 s | how long to wait for the CVMs before giving up |
