---
## TO DO List
windows:
VSIM: 
centos:
  - refresh RedHat compatibility through v9 
DC: 
DNS: 
  - add PVE support 
AIQUM:
  - done: integrate PVE into aiqum in main 
XCP-NG:
  - rewrite to use autoinstall
  - add PVE support 
storagegrid:
  - add PVE support 
esxi: 
  - find a way to deploy 9.x to PVE
OVA: 
  - find a generalized way to deploy OVA to proxmox 
  - make a seperate builder role for ONTAP Deploy

Proxmox:
  - add vlan support to all roles 
  - add pve support to prep playbook

Snippets:
# proxmox: get list of vlans in use:
for vmid in $(qm list | awk 'NR>1 {print $1}'); do qm config $vmid 2>/dev/null; done | grep -o 'tag=[0-9]\+' | cut -d= -f2 | sort -nu

# proxmox: get next unused vlan in range 1000+
for vmid in $(qm list | awk 'NR>1 {print $1}'); do qm config $vmid 2>/dev/null; done | grep -o 'tag=[0-9]\+' | cut -d= -f2 | sort -nu | awk 'BEGIN {next_vlan=1000} {if ($1 < next_vlan) {next} if ($1 == next_vlan) {next_vlan++} else if ($1 > next_vlan) {exit}} END {print next_vlan}'

