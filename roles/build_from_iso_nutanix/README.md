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

## Timing
| Variable | Default | Meaning |
|---|---|---|
| `installer_boot_wait` | 300 s | power-on until the installer screen is up (about 3 minutes in testing) |
| `installer_image_wait` | 1500 s | Start until imaging finishes |
| `nutanix_cluster_wait` | 5400 s | how long to wait for the CVMs before giving up |
