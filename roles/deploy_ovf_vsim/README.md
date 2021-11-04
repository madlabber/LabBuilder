deploy_ovf_vsim
================================

Deploys NetApp ONTAP Simulator (vsims) virtual appliances.

Requirements
------------

- Requires the vsim-netapp-DOT{{ ovf_version }}-cm_nodar.ova virtual appliance downloaded from NetApp.com.  
Store the archive in either the role's files directory, or the playbook's files directory.

- Requires the community.vmware ansible galaxy collection.

- Requires pyvmoni.

Installation
------------

`ansible-galaxy role install -f -p ./roles git+https://github.com/madlabber/deploy_ovf_vsim.git,main`


Role Variables
--------------

| Variable                | **Default**/Example | Comments  |
|-------------------------|---------------------|-----------|
| state                   | **present**,absent  | present creates VMs, absent deletes them.|
| vm_name                 | **SimulateONTAP**   | a valid VM name |
| **vm_datastore**        | **datastore1**      | the VMware datastore where the node will be placed |
| data_network            | **"VM Network"**    | The vSphere portgroup used for ONTAP data and mgmt traffic |
| cluster_network         | **"VM Network"**    | The vSphere portgroup used the for ONTAP cluster network |
| vm_disk_provisioning    | **"thin"**          | Virtual Disk provisioning mode |
| vm_num_cpus             | **"2"**             | number of vCPUs to assign to the VM |
| vm_memory_mb            | **"8192"**          | amount of memory, in MB, to assign to the VM |
| vm_num_nics             | **"4"**, 6, 8, 10   | number of nics to create on the VM (4-10) |
| **vcenter_address**     | "vc.demo.lab"       | The hostname or IP address of the vCenter server |
| **vcenter_username**    | **"administrator@vsphere.local"** | A vcenter username with rights to deploy the OVA |
| **vcenter_password**    | "ChangeMe2!"        | The password for the vcenter user |
| **vcenter_datacenter**  | "Datacenter 1"      | vCenter datacenter where the node will be deployed |
| vcenter_cluster         |                     | |
| ovf_version             | **"9.9.1"**         | The vsim OVF version|
| ovf_file                | | default: "{{role_path}}/files/vsim-netapp-DOT{{ ovf_version }}-cm_nodar.ova" |
| sys_serial_number       | **"4082368-50-7"**, "4034389-06-2" | must match an available license key set. |
| nvram_sysid             | "4082368507"        | if omitted a random sysid will be used. |
| vdevinit                | **"34:14:0,34:14:1"** | simulated disk configuration.  see vars/main.yml for details |
| ontap_node_mgmt_ip      | "192.168.0.91"      | If specified, node setup will be attempted. |
| ontap_netmask           | "255.255.255.0"     | Subnet mask for the data network |
| ontap_gateway           | "192.168.0.1"       | Gateway IP for the data network |
| ontap_cluster_mgmt_ip   | "192.168.0.90"      | If specified, cluster setup will be attempted |
| ontap_cluster_name      | "democluster"       | ONTAP cluster name |
| ontap_password          | **"netapp123"**     | ONTAP admin password |
| ontap_dns_domain        |                     | DNS domain | 
| ontap_dns_server        |                     | DNS Server on the data/mgmt network |
| ontap_location          |                     | optional ONTAP SNMP location value used for cluster setup |
| add_nodes_by_serial     | "4034389-06-2"      | serial number of a node to add into the cluster |
| disk_model              | **"vha"**, "vscsi"  | vha uses simulated disk, vscsi uses virtual disks |
| shelf0_disk_count       | "14"                | (1-14) Number of disks to create on shelf 0 |
| shelf0_disk_size        | "4000"              | valid sizes are 500,1000,2000,4000, or 9000 |
| shelf0_disk_type        |                     | valid type from 'vsim_makedisks -h'. See defaults/main.yml for examples. |
| shelf1_disk_count       | "14"                | (1-14) Number of disks to create on shelf 1 |
| shelf1_disk_size        | "4000"              | valid sizes are 500,1000,2000,4000, or 9000 |
| shelf1_disk_type        |                     | valid type from 'vsim_makedisks -h'. See defaults/main.yml for examples. |
| shelf2_disk_count       | "14"                | (1-14) Number of disks to create on shelf 2 |
| shelf2_disk_size        |                     | valid sizes are 500,1000,2000,4000, or 9000 |
| shelf2_disk_type        | "23"                | valid type from 'vsim_makedisks -h'. See defaults/main.yml for examples. |
| shelf3_disk_count       |                     | (1-14) Number of disks to create on shelf 3 |
| shelf3_disk_size        |                     | valid sizes are 500,1000,2000,4000, or 9000 |
| shelf3_disk_type        |                     | valid type from 'vsim_makedisks -h'. See defaults/main.yml for examples. |
| force                   | **False**, True     | If true, existing VMs will be deleted and recreated |
| node_setup_delay        | **60**              | Seconds to wait before attempting node setup |

Default Configuration(s)
------------------------  
This role does some adjustments to the default config from NetApp:
  * Default storage config:
    * Populating the first 2 shelfs, resulting in 28 total drives
    * Leveraging 4 GB FCAL style drives
  * Expanded `aggr0` & `vol0` 


Dependencies
------------

Example Playbook
----------------
    ---
    - hosts: localhost 
      name: Deploy a single node ONTAP Simulator cluster
      gather_facts: false
      vars: 
        vcenter_address:  vcenter.demo.lab
        vcenter_username: administrator@vsphere.local
        vcenter_password: ChangeMe2!
        vcenter_datacenter: "Datacenter"
        vcenter_cluster:    "Cluster1"
      tasks:
        - include_role: 
            name: deploy_ovf_vsim
          vars:
            vm_name:               "vsim1-01"
            vm_datastore:          "datastore1"
            ontap_node_mgmt_ip:    "192.168.0.81"
            ontap_netmask:         "255.255.255.0"
            ontap_gateway:         "192.168.0.1"
            ontap_cluster_name     "vsim1" 
            ontap_cluster_mgmt_ip: "192.168.0.80"

    ---
    - hosts: localhost 
      name: Deploy a single node ONTAP Simulator cluster with additional storage
      gather_facts: false
      vars: 
        vcenter_address:  vcenter.demo.lab
        vcenter_username: administrator@vsphere.local
        vcenter_password: ChangeMe2!
        vcenter_datacenter: "Datacenter"
        vcenter_cluster:    "Cluster1"
      tasks:
        - include_role: 
            name: deploy_ovf_vsim
          vars:
            vm_name:               "vsim1-01"
            vm_datastore:          "datastore1"
            ontap_node_mgmt_ip:    "192.168.0.81"
            ontap_netmask:         "255.255.255.0"
            ontap_gateway:         "192.168.0.1"
            ontap_cluster_name     "vsim1" 
            ontap_cluster_mgmt_ip: "192.168.0.80"
            shelf0_disk_count:     14  
            shelf0_disk_size:      4000
            shelf0_disk_type:      31 
            shelf1_disk_count:     14  
            shelf1_disk_size:      4000
            shelf1_disk_type:      31
            shelf2_disk_count:     14  
            shelf2_disk_size:      4000
            shelf2_disk_type:      31
            shelf3_disk_count:     14  
            shelf3_disk_size:      4000
            shelf3_disk_type:      31  
  
    ---
    - hosts: localhost 
      name: Deploy a 2-node ONTAP Simulator cluster
      gather_facts: false
      vars: 
        vcenter_address:  vcenter.demo.lab
        vcenter_username: administrator@vsphere.local
        vcenter_password: ChangeMe2!
        vcenter_datacenter: "Datacenter"
        vcenter_cluster:    "Cluster1"
      tasks:
        # Deploy the second node first
        - include_role: 
            name: deploy_ovf_vsim
          vars:
            vm_name:            "vsim2-02"  
            vm_datastore:       "datastore1"
            data_network:       "VM Network"
            cluster_network:    "VM Network 2"
            sys_serial_number:  "4034389-06-2"
            ontap_node_mgmt_ip: "192.168.0.92"  
            ontap_netmask:      "255.255.255.0"
            ontap_gateway:      "192.168.0.1"
      
        # Deploy the first node last
        - include_role: 
            name: deploy_ovf_vsim
          vars:
            vm_name:               "vsim2-01"
            vm_datastore:          "datastore1"
            data_network:          "VM Network"
            cluster_network:       "VM Network 2"
            sys_serial_number:     "4082368-50-7"
            add_nodes_by_serial:   "4034389-06-2"
            ontap_node_mgmt_ip:    "192.168.0.91"
            ontap_netmask:         "255.255.255.0"
            ontap_gateway:         "192.168.0.1"
            ontap_cluster_name     "vsim2" 
            ontap_password:        "netapp123"
            ontap_cluster_mgmt_ip: "192.168.0.90"    


NOTES
-----
* Reference either `vsim_makedisks -h` or table comment in `defaults\main.yml` to adjust type, size, & count of disks
* Leverage both the `data_network` & `cluster_network` for creating a 2 node cluster
* setup second node first to leverage `add_nodes_by_serial`  
* `add_nodes_by_serial` only supports adding 1 additional node


Author Information
------------------

Sean Hatfield\
sean.hatfield@netapp.com\
github.com/madlabber
