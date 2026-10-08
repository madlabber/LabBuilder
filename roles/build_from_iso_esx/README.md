# build_from_iso_esx

## about
This role builds ESX virtual machines on VMware or Proxmox hosts

## Variables:

Virtual Machine Configuration Variables:
=========================================
| Variable      | **Default**/Example | Comments        |
|---------------|---------------------|-----------------|
| install_iso   | /path/to/esx.iso    | path to the installer iso file | 
| state         | **present**         | Creates the VM  |
|               | absent              | deletes the VM  |
|               | force               | replaces the VM |
| vm_address    | 192.168.0.51        | IPv4 address of VM |
| vm_netmask    | 255.255.255.0       | IPv4 netmask of VM |
| vm_gateway    | 192.168.0.1         | IPv4 default gateway |
| vm_dns_server | 192.168.0.11        | IPv4 DNS server |
| vm_domain     | demo.lab            | DNS domain name |
| vm_hostname   | esx1                | The hostname |
| vm_name       | vm101               | the virtual machine name |
| vm_password   | ChangeMe2!          | The root password |
| vm_network    | "VM Network"        | portgroup or bridge name |
| vm_disk_gb    | 128 | VM boot disk size |
| vm_num_nics   | 2 | Number of network adapters |
| vm_num_cpus   | 2 | Number of vCPUs |
| vm_memory_mb  | 8192 | virtual memory in MB |
| ethernet_ports |  | list of ports eth0-eth7 mapping each to a specific vm network |
| disks | | list of disks to create on the VM |



vsphere host variables:
=====================
| variable |
|-----------|
| vcenter_address |
| vcenter_username |
| vcenter_password |
| vcenter_datacenter |
| vcenter_cluster |
| vm_datastore |
| iso_datastore |

standalone esxi host variables:
===============================
| variable |
|----|
| esxi_address |
| esxi_username |
| esxi_password |
| vm_datastore |
| iso_datastore |

proxmox host variables:
========================
| variable    |             |   |
|-------------|-------------|---|
| pve_address  | 10.10.0.50 | Proxmox host address |
| pve_username | root       | Proxmox username |
| pve_password | ChangeMe2! | Proxmox password |
| vm_datastore | local-lvm  | Proxmox storage name |
| iso_datastore | local     | Proxmox ISO storage name | 
| iso_path | /var/lib/vz/template/iso | Path to the ISO folder on the Proxmox host |






