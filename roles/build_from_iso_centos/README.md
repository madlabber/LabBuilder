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
| state                   | **present**,absent,force  | present creates VMs, absent deletes them, force recreates them|
| vm_name                 | **SimulateONTAP**   | a valid VM name |
| **vm_datastore**        | **datastore1**      | the VMware datastore where the node will be placed |


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
