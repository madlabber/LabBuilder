# LabBuilder
 A collection of playbooks and tooling for building labs

main.yml - provisions labs from inventory files

vars/main.yml - variable related to the lab hosting environment

defaults/ - task level default variables

test_ - playbooks that demonstrate how to use the tasks


2 ways to use this library:
1. build a playbook that calls the roles and tasks to assemble a lab, 
2. build an inventory file that describes a lab and pass it to main.yml
   
   ansible-playbook -i inventories/lab_mylabblueprint.yml main.yml


# requirements
ansible 2.14
ansible-galaxy collections:
- community.vmware
- community.general
- netapp.ontap

python libraries
- pyvmomi
- pycdlib
- pywinrm
- netapp-lib

ESXi host(s)
vCenter Server

# using alternate main vars
The default vars related to the lab hosting infrastructure are read from vars/main.yml
To load an alternate configuration, store an alternate set of vars in vars/\<altconfig\>.yml and load it at runtime with
 - -e mainvars=\<altconfig\>.yml

# Adding ISO and OVA files
The various VM build roles require installation media or OVA files.  In some cases these can be downloaded on demand, in other cases they need to be added to the files folder. 

ISO files can be prepopulated by copying them into the ISO datastore.  
Vendor OVA files need to be staged in the LabBuilder "files" folder. 

## Installation Sources that will be downloaded as needed:
 - pfsense install ISOs
 - Windows Install ISOs
 - Most linux install ISOs 

## Installation Sources that need to be added manually:
 - RedHat linux ISOs
 - Nested ESXi OVA files
 - vCenter OVA files
 - NetApp Simulator OVA files
 - NetApp ONTAP Select eval OVA files
 - NetApp StorageGrid OVA files
 - NetApp AIQUM OVA files

## PVE Notes
Most components can now build on PVE hosts, with the following general exceptions:
  - Interconnected Serial ports are not configured on PVE hosts
  - Shared virtual disks are not build on PVE hosts

## Proxmox Compatibility Status
| Component | VMware | Proxmox | Notes 
|-----------|--------|---------|-------
| centos    | YES    | YES     | 
| windows   | YES    | YES     |


