build_storagegrid_node_from_ova
================================

Deploys StorageGrid node virtual appliances to a vSphere infrastructure.

Requirements
------------

Requires the storagegrid virtual appliance archive downloaded from NetApp.com
Requires the community.vmware ansible galaxy collection
Requires pyvmoni

Role Variables
--------------

| Variable                | Required | Default | Choices                   | Comments                                 |
|-------------------------|----------|---------|---------------------------|------------------------------------------|
| vm_name                 | yes      | false   | string value              | example: "sgws-storage1"                 |
| ovf_hostname            | yes      | false   | a valid dns hostname      | example: "sgws-storage1"                 |
| vm_datastore            | yes      | false   | a valid vm datastore      | example: "datastore1"                    |
| grid_network_name       | yes      | false   | a valid vm portgroup      | example: "VM Network"                    |
| grid_network_config     | yes      | true    | "STATIC", "DHCP"          |                                          |
| grid_network_ip         | yes      | false   | a valid IP address        | example: "192.168.0.10"                  |
| grid_network_mask       | yes      | false   | a valid subnet mask       | example: "255.255.255.0"                 |
| grid_network_gateway    | yes      | false   | a valid gateway address   | example: "192.168.0.1"                   |

note: this list is incomplete.  FIXME.

Dependencies
------------

Example Playbook
----------------

    - hosts: storagegrid
      roles:
        - role: build_storagegrid_node_from_ova
          vars:
            vm_name: 'sgws-admin'
            ovf_hostname: 'sgws-admin'        
            grid_network_name: "VM Network"        
            grid_network_config: "STATIC" 
            grid_network_ip: "192.168.0.110"
            grid_network_mask: "255.255.255.0"
            grid_network_gateway: "192.168.0.1"  
        - role: build_storagegrid_node_from_ova
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
