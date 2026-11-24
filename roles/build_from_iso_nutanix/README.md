# build_from_iso_nutanix

Builds Nutanix Community Edition 2.1 (AHV) nodes as nested VMs on vCenter, then creates the cluster.
It doesn't support PVE yet.

## What it needs
* `files/phoenix.x86_64-fnd_5.6.1_patch-aos_6.8.1_ga.iso`, the CE 2.1 ISO (about 7 GB). It's uploaded once to `iso_datastore`.
* An inventory group (default `nutanix`). Each host sets `ip_address` (the AHV host) and `cvm_address`.
* A lab gateway that forwards a WAN port to the first CVM's SSH. LabBuilder creates the cluster through it:
  ```yaml
  rdp_jumphost: ""          # otherwise it replaces nat_rules
  nat_rules:
    - { name: "SSH to the first CVM", external_port: "2222", internal_port: "22", protocol: "tcp", target_ip: 192.168.0.61 }
  ```
See `inventories/lab_nutanix.yml` (1 node) and `inventories/lab_nutanix3.yml` (3 nodes).

## How the install is automated
The CE installer (`init=/ce_installer`, phoenix `gui.CEGui`) has no answer file. The role types into the VM console with `vmware_guest_sendkey`, the same way `build_from_iso_esx` does:

1. **Page 1:** Tab past Hypervisor (AHV only) and Disk selection (the defaults are used). Then it types the Host IP, CVM IP, Subnet Mask and Gateway, and selects Next Page.
2. **Page 2:** it scrolls the EULA to the end (the installer checks this), ticks Accept, and selects Start.
3. After `installer_image_wait` it answers the "enter 'Y' to reboot" prompt.

The installer picks the disks itself, so the VM is built to match its defaults. VMware paravirtual disks report as SSD, so the largest disk becomes the CVM disk:

| Disk | Size | Used for |
|---|---|---|
| scsi0:0 | 64 GB | AHV boot (smallest disk) |
| scsi0:1 | 500 GB | CVM boot (largest SSD, at least 200 GB) |
| scsi0:2 | 250 GB | data |

`disk.EnableUUID=TRUE` gives the disks serial numbers, which the installer and the CVM need. CPU virtualization is exposed to the guest.

Only a VM that this run creates gets the keystrokes. Re-running the playbook leaves installed nodes alone. To rebuild a node, run with `state=force`.

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

## Nutanix Move on AHV (`tasks/deploy_move.yml`)
Optional, and not what `lab_nutanix_move` uses (see below). This is the layout the Move guide documents for migrations to AHV: the qcow2 from the Move package for AHV (`move-<version>.zip`), on the target cluster. Put the qcow2 in `files/`, set `nutanix_lab_network` as above, then:
```yaml
nutanix_move_image: "move-<version>.qcow2"   # blank skips Move
nutanix_move_ip: 192.168.0.70                # fixed address on nutanix_lab_network
```
It runs on the first CVM, through the same SSH forward:
1. Copies the image to the CVM (`files/cvm_put.py`, SFTP).
2. Imports it with `acli image.create` from a web server on the CVM's own loopback, then deletes the copy. LabBuilder's firewall isn't involved.
3. Creates the `move` VM as the Move guide specifies (2 vCPU x 2 cores, 8 GB, legacy BIOS, disk cloned from the image) on `nutanix_lab_network` with the fixed address, powers it on, and waits for its web UI.

It's skipped when a VM named `move` already exists. In a lab that leaves cluster creation to the user, run the lab build again after the cluster is created: the nodes are left alone and Move is deployed.

## The Move demo lab
`inventories/lab_nutanix_move.yml` (1 node) adds a VMware source next to the cluster: vCenter 8.0 U3 (`vc01`) and one ESXi host (`esx01`, with a data disk for `datastore1`), plus an **Ansible VM** (`ansible`, AlmaLinux 9). The last play runs **stage 2** on that VM, inside the lab (roles/stage2): it prepares `vc01` (roles/vcenter_prep), puts Windows Server 2019 and Debian 12 ISOs on `datastore1`, and deploys Move from its OVA on `esx01` with "Deploy OVF files". Users then build a small Windows VM and a small Linux VM and migrate both; `lab-lan` is the target network on the cluster. The Move guide documents the OVA for ESXi-to-ESXi, and Move 6.3.3 is qualified with AOS 6.10 while CE 2.1 runs AOS 6.8.1; the lab guide notes both and walks through the migration.

## Timing
| Variable | Default | Meaning |
|---|---|---|
| `installer_boot_wait` | 300 s | power-on until the installer screen is up (about 3 minutes in testing) |
| `installer_image_wait` | 1500 s | Start until imaging finishes |
| `nutanix_cluster_wait` | 5400 s | how long to wait for the CVMs before giving up |
