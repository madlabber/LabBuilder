build_from_iso_centos
================================

Builds VMs running CentOS derivatives from ISO

Requirements
------------

- Requires the community.vmware ansible galaxy collection.

- Requires pyvmoni and pycdlib

Installation
------------



Role Variables
--------------

| Variable                | **Default**/Example | Comments  |
|-------------------------|---------------------|-----------|
| state                   | **present**,absent,force | present creates VMs, absent deletes them, force recreates them|
| vm_name                 | **centos**               | a valid VM name |
| vm_datastore            | **datastore1**           | the VMware datastore where the node will be placed |
| distro                  | **centos**,rocky,alma,rhel,stream | specifies desired linux distro |
| version                 | 7,8,8.8,8.7... | Version to be installed.  Can be just major version or can specify the minor release as well |
| vm_memory_mb            | 2048 | memory in MB |
| vm_num_cpus             | 2 | vcpu count |
| vm_disk_gb              | 40 | systeem disk size in GB |
| install_xrdp            | true,false | automatically install xRDP in the guest |
| install_ansible         | true,false | automatically install ansible in the guest |
| extra_commands          | "yum update" | a list of additional commands to run after guest installation |
| vm_hostname | | |
| vm_eth_name | **ens32** | Name of the primary network device |
| vm_address | | |
| vm_network | | VMware PortGroup Name |
| vm_password | | New root password |
| vm_netmask_cidr | | |
| vm_gateway | | |
| vm_dns_server | | |
| vm_domain | | |
| vm_password | | old root/admin password (from kickstart file)|
| rhsm_orgid | 1234567 | RHEL only: RSHM Org ID |
| rhsm_activationkey | rhelkey | RHEL only: activation key |

Dependencies
------------

Example Playbook
----------------

NOTES
-----


Author Information
------------------

Sean Hatfield\
sean.hatfield@netapp.com\
github.com/madlabber
