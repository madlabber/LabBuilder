# LabBuilder
 A collection of playbooks and tooling for building labs

main.yml - provisions labs from inventory files
vars/main.yml - variable related to the lab hosting environment
defaults/ - task level default variables
test_ - playbooks that demonstrate how to use the tasks


2 ways to use this library:
1. build a playbook that calls the roles and tasks to assemble a lab, 
2. build an inventory file that describes lab and pass it to main.yml
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

