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
ansible 2.17+
ansible-galaxy collections:
- community.vmware
- community.general
- netapp.ontap
- community.proxmox

python libraries
- pyvmomi
- pycdlib
- pywinrm
- netapp-lib
- proxmoxer

Additional packages:
- mtools
- qemu-img /
  qemu-utils
- xorriso

ESXi host(s)
vCenter Server

# Usage 
## Using make
1. Install ansible, then make install:
    ``` 
    make install 
    ```
2. Configure your virtualization hosting environment variables in the main vars file:
    ```
    make configure
    ```
3. Add the ISOs and OVAs for components you intend to deploy to the files folder on the ansible controller

4. Select or customize a lab blueprint from the inventories folder, i.e. lab_test.yml

5. Prepare the environment to host the lab blueprint
    ```
    make prep lab_test
    ```
6. Build the lab blueprint
    ```
    make lab_test
    ```
### using an alternate config
You can use alternate config files to target different hosting environments.  For example you may have one environment hosted on VMware, and another environment hosted on Proxmox.

1. create the config file using the main config as a reference
   ```
   cp vars/main.yml vars/altconfig.yml
   make configure altconfig
   ```
2. use the alternate config in the make commands
   ```
   make prep lab_test config:altconfig
   make lab_test config:altconfig

### Building a portion of a blueprint
You may want to only build a portion of a blueprint, as shown in these examples:
```
make lab_test -- -l server01
make lab_test config:altconfig -- -l server02,router01
```
everything after the -- is forwarded to ansible-playbook as cli parameters.

### Printing the inventory graph of a blueprint
You may print a list of VMs included in a blueprint using make graph:
```
make graph lab_test
```

## Using ansible-playbook
1. Install ansible, then execute the install-requirements.yml playbook:
    ``` 
    ansible-playbook install-requirements.yml 
    ```
2. Configure your virtualization hosting environment variables in the main vars file:
    ```
    vars/main.yml
    ```
3. Add the ISOs and OVAs for components you intend to deploy to the files folder on the ansible controller

4. Select or customize a lab blueprint from the inventories folder

5. Run the prep.yml playbook to provision any required networking and storage defined in the blueprint
    ```
    ansible-playbook prep.yml -i inventories/lab_template.yml
    ```
6. Run the main.yml playbook to build the lab environment as defined in the blueprint
    ```
    ansible-playbook main.yml -i inventories/lab_template.yml
    ```

### using alternate main vars with ansible-playbook
The default vars related to the lab hosting infrastructure are read from vars/main.yml
To load an alternate configuration, store an alternate set of vars in vars/\<altconfig\>.yml and load it at runtime with:
    
     - -e mainvars=\<altconfig\>.yml

To make this persistent, update this entry in defaults/main.yml:
    
    mainvars: vars/main.yml


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
 - VMware ESXi ISO files
 - Nested ESXi OVA files
 - vCenter OVA files
 - NetApp Simulator OVA files
 - NetApp ONTAP Select eval OVA files
 - NetApp StorageGrid OVA files
 - NetApp AIQUM installer files

## PVE Notes
Most components can now build on PVE hosts, with the following general exceptions:
  - Interconnected Serial ports are not configured on PVE hosts
  - Shared virtual disks are not built on PVE hosts

## Proxmox Compatibility Status
| Component   | VMware | Proxmox | Notes 
|-------------|--------|---------|-------
| centos      | YES    | YES     | 
| windows     | YES    | YES     | 
| pfsense     | YES    | YES     | 
| ESX         | YES    | YES     | 
| Proxmox     | YES    | YES     | 
| Ubuntu      | YES    | YES     | 
| XCP-NG      | YES*   | NO      | *experimental: only 8.2.1 on vmware*
| Nested ESXi | YES    | NO*     | PVE: use ESX (iso) instead
| AIQUM       | YES    | YES     | Use install_file: (aiqum installer .zip)
| OTS Eval    | YES    | YES     | 
| SGWS        | YES    | NO*     | PVE: Install StorageGrid on Linux
| VCENTER     | YES    | YES*    | PVE: requires manual ip/stage2 configuration
| VSIM        | YES    | YES*    | PVE: HA pairs are rendered as non-ha nodes
| OVF         | YES    | No      | Generic OVF deployment is not working on PVE


