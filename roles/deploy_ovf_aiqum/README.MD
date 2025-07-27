deploy_ovf_aiqum
================================

Deploys ActiveIQ Unified Manager virtual appliances to a vSphere infrastructure.

Requirements
------------

Requires the ActiveIQUnifiedManager.ova virtual appliance downloaded from NetApp.com.  Store the archive in either the role's files directory, or the playbook's files directory.
Requires the community.vmware ansible galaxy collection.
Requires pyvmoni.

Role Variables
--------------

| Variable                | Required | Default           | Example                       | Comments                                                               |
|-------------------------|----------|-------------------|-------------------------------|------------------------------------------------------------------------|
| vm_name                 | yes      |                   | "sgws-storage1"               | a valid VM name                                                        |
| vm_datastore            | yes      |                   | "datastore1"                  | the VMware datastore where the node will be placed                     |
| vm_network              |          |                   |                               |                                                                        |
| vm_disk_provisioning    |          | "thin"            |                               | Virtual Disk provisioning mode                                         |
| vcenter_address         | yes      |                   | "vc.demo.lab"                 | The hostname or IP address of the vCenter server                       |
| vcenter_username        | yes      |                   | "administrator@vsphere.local" | A vcenter username with rights to deploy the OVA                       |
| vcenter_password        | yes      |                   | "ChangeMe2!"                  | The password for the vcenter user                                      |
| vcenter_datacenter      | yes      |                   | "Datacenter 1"                | vCenter datacenter where the node will be deployed                     |
| vcenter_cluster         |          |                   |                               |                                                                        |
| ovf_version             | no       | "9.9"             | "9.9"                         | The StorageGrid OVF version                                            |
| ovf_file                | no       |                   | "/files/aiqum.ova"            | optional explicit path to the AIQUM OVA file                           |
| vm_fqdn                 |          |                   |                               | The fully qualified domain name for the ActiveIQ Unified Manager VM    |
| vm_address              |          |                   |                               |                                                                        |
| vm_netmask              |          |                   |                               |                                                                        |
| vm_gateway              |          |                   |                               |                                                                        |
| vm_primary_dns          |          |                   |                               |                                                                        |
| vm_secondary_dns        |          |                   |                               |                                                                        |
| timer1                  | no       | 420               | 480                           | the seconds to wait for the timezone prompt                            |
| timer2                  | no       | 300               | 360                           | the seconds to wait for the username/password prompt                   |
| vm_username             | no       | "admin"           |                               |                                                                        |
| vm_username             | no       | "ChangeMe2!"      |                               |                                                                        |
| vm_timezone_geo         | no       | "12"              |                               | #12 = US                                                               |
| vm_timezone_region      | no       | "10"              |                               | #10 = Pacific                                                          |

Dependencies
------------

Example Playbook
----------------

    ---
    - name: Build AIQUM from OVA
      hosts: localhost
      gather_facts: false
      vars:   
        vcenter_address: vcenter.demo.lab
        vcenter_username: administrator@vsphere.local
        vcenter_password: ChangeMe2!
        vcenter_datacenter: "Datacenter 1"
        vm_datastore: "datastore1"
      tasks:
        - include_role: 
            name: deploy_ovf_aiqum
          vars:
            # ovf_file: "files/AIQUM/ActiveIQUnifiedManager-9.8.ova"          
            vm_name:          "aiqum"
            vm_fqdn:          "aiqum.demo.lab"
            vm_username:      "admin"
            vm_password:      "ChangeMe2!"        
            vm_network:       "VM Network"
            vm_address:       "192.168.0.99"
            vm_netmask:       "255.255.255.0"
            vm_gateway:       "192.168.0.1"
            vm_primary_dns:   "192.168.0.21"
            vm_secondary_dns: "192.168.0.1"



Author Information
------------------

Sean Hatfield
sean.hatfield@netapp.com
github.com/madlabber
