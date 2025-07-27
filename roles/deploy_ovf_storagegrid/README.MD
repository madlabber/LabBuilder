deploy_ovf_storagegrid
================================

Deploys StorageGrid node virtual appliances to a vSphere infrastructure.

Requirements
------------

Requires the storagegrid virtual appliance archive downloaded from NetApp.com.  Extract the archive into either the role's files directory, or the playbook's files directory.
Requires the community.vmware ansible galaxy collection
Requires pyvmoni

Role Variables
--------------

| Variable                | Required | Default           | Example                       | Comments                                                               |
|-------------------------|----------|-------------------|-------------------------------|------------------------------------------------------------------------|
| vm_name                 | yes      |                   | "sgws-storage1"               | a valid VM name                                                        |
| ovf_hostname            | yes      |                   | "sgws-storage1"               | a valid hostname                                                       |
| vm_datastore            | yes      |                   | "datastore1"                  | the VMware datastore where the node will be placed                     |
| vcenter_address         | yes      |                   | "vc.demo.lab"                 | The hostname or IP address of the vCenter server                       |
| vcenter_username        | yes      |                   | "administrator@vsphere.local" | A vcenter username with rights to deploy the OVA                       |
| vcenter_password        | yes      |                   | "ChangeMe2!"                  | The password for the vcenter user                                      |
| vcenter_datacenter      | yes      |                   | "Datacenter 1"                | vCenter datacenter where the node will be deployed                     |
| ovf_version             | no       | "11.5.0"          | "11.5.0"                      | The StorageGrid OVF version                                            |
| ovf_location            | no       |                   | "/files/sgws/vsphere_ovf"     | optional explicit path to the folder containing the OVF files          |
| vm_num_cpus             | no       | "8"               | "4"                           | optional override for the number of vCPUs                              |
| vm_memory_mb            | no       | "24576"           | "12288"                       | optional override for the virtual memory size in MB                    |
| storage_disk_size       | no       | "4096"            | "200"                         | optional override for the storage node's data disk size in GB          |
| node_type               | no       | "VM_Storage_Node" | "VM_Storage_Node"             | "VM_Admin_Node","VM_Storage_Node", "VM_API_Gateway", "VM_Archive_Node" |
| admin_role              | no       | "Primary"         | ""                            | Admin role for admin nodes. Options are: "Primary", "Non-Primary"      |
| admin_ip                | yes      |                   | "192.168.0.110"               | The IP address of the grid's admin node                                |
| grid_network_name       | yes      |                   | "VM Network"                  | the VMware portgroup name for the grid network                         |
| grid_network_config     | yes      | "DHCP"            | "STATIC"                      | "STATIC" or "DHCP"                                                     |
| grid_network_ip         | yes      | "0.0.0.0"         | "192.168.0.110"               | for DHCP use "0.0.0.0"                                                 |
| grid_network_mask       | yes      | "255.255.255.255" | "255.255.255.0"               | for DHCP use "255.255.255.255"                                         |
| grid_network_gateway    | yes      | "0.0.0.0"         | "192.168.0.1"                 | for DHCP use "0.0.0.0"                                                 |
| grid_network_mtu        | no       | "1400"            | "1400"                        | MTU for the grid network                                               |
| client_network_name     | no       |                   | "grid-admin-network"          | the VMware portgroup name for the client network                       |
| client_network_config   | no       | "DISABLED"        | "STATIC"                      | "DISABLED", "STATIC" or "DHCP"                                         |
| client_network_ip       | no       | "0.0.0.0"         | "192.168.1.110"               |                                                                        |
| client_network_mask     | no       | "255.255.255.255" | "255.255.255.0"               |                                                                        |
| client_network_gateway  | no       | "0.0.0.0"         | "192.168.1.1"                 |                                                                        |
| client_network_mtu      | no       | "1400"            | "1400"                        | MTU for the admin network                                              |
| admin_network_name      | no       |                   | "grid-admin-network"          | the VMware portgroup name for the admin network                        |
| admin_network_config    | no       | "DISABLED"        | "STATIC"                      | "DISABLED", "STATIC" or "DHCP"                                         |
| admin_network_ip        | no       | "0.0.0.0"         | "192.168.1.110"               |                                                                        |
| admin_network_mask      | no       | "255.255.255.255" | "255.255.255.0"               |                                                                        |
| admin_network_gateway   | no       | "0.0.0.0"         | "192.168.1.1"                 |                                                                        |
| admin_network_mtu       | no       | "1400"            | "1400"                        | MTU for the admin network                                              |
| admin_network_esl       | no       | ""                | "10.10.10.0/24,172.16.0.0/16" | a comma-separated list of subnets that will communicate with this node | 
|                         |          |                   |                               | through its admin network gateway. This list will be used to create    | 
|                         |          |                   |                               | static routes. Use CIDR notation.                                      | 


Dependencies
------------

Example Playbook
----------------

    - hosts: storagegrid
      roles:
        - role: deploy_ovf_storagegrid
          vars:
            vm_name: 'sgws-admin'
            ovf_hostname: 'sgws-admin'        
            grid_network_name: "VM Network"        
            grid_network_config: "STATIC" 
            grid_network_ip: "192.168.0.110"
            grid_network_mask: "255.255.255.0"
            grid_network_gateway: "192.168.0.1"  
        - role: deploy_ovf_storagegrid
          vars:
            vm_name: 'sgws-storage1'
            ovf_hostname: 'sgws-storage1'        
            admin_ip: "192.168.0.110"
            grid_network_name: "VM Network"        
            grid_network_config: "STATIC" 
            grid_network_ip: "192.168.0.111"
            grid_network_mask: "255.255.255.0"
            grid_network_gateway: "192.168.0.1"  
      vars:   
        vcenter_address: vcenter.demo.lab
        vcenter_username: administrator@vsphere.local
        vcenter_password: ChangeMe2!
        vcenter_datacenter: "Datacenter 1"
        vm_datastore: "datastore1"

Author Information
------------------

Sean Hatfield
sean.hatfield@netapp.com
github.com/madlabber
