The plan for this role is to deploy ONTAP Seleect Deploy on multiple platforms, starting with VMware and Proxmox.

The VMware version can use an OVA source.
Proxmox and others will need the ,raw.tgz source

Bifurcated workflows with a common set of configuration variables to make it as transparent as possible to the caller of the role.

Bringup and initial config on VMware can use OVF Environment variables
Bringup and initial config on Proxmox will need to use expect

Ideally, an out of band method can be found to invoke the API that creates mediators.
This would facilitate OOB stand up of OTS HA pairs.
