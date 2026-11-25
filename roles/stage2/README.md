# stage2

Runs LabBuilder a second time **inside a lab**, on the lab's Ansible VM, where the lab's own vCenter and ESXi hosts are reachable directly. Used by the last play in `main.yml` ("Stage 2 inside the pod") for hosts in the `stage2` group.

From outside (stage 1, LabBuilder):
1. Finds the lab gateway's WAN address, which forwards `stage2_ssh_port` (2223) to the Ansible VM's port 22.
2. Makes a dedicated SSH key (`~/.ssh/labbuilder_stage2`) if needed, and puts its public key in the Ansible VM's `/root/.ssh/authorized_keys` through the outer vCenter's guest operations (root can only log in with a key).
3. Over SSH through the gateway: sets up a Python 3.12 venv on the VM (`/root/venv-labbuilder`: ansible-core, pyVmomi, `community.vmware`, `vmware.vmware`; AlmaLinux 9's own Python 3.9 is too old for current pyVmomi), and copies LabBuilder to `/root/LabBuilder`, **without** `files/`, `vars/`, `inventories/` or `.git`. Then it copies only the binaries stage 2 needs (`stage2_isos`, `stage2_ovas`).
4. Generates the stage 2 **blueprint** (`inventories/stage2.yml`) and **vars file** (`vars/stage2.yml`, `vars/stage2-credentials.yml`) for the lab's own vCenter. They hold only the lab password; the outer `vars/` never enters the lab.
5. Runs the venv's `ansible-playbook main.yml -i inventories/stage2.yml -e mainvars=vars/stage2.yml -e credentials=vars/stage2-credentials.yml` on the VM, waits for it, and fails if it fails. The log stays on the VM: `/root/LabBuilder/stage2.log`.

An OVA can be marked `fix_ovf: true`: `files/fix_ovf.py` unpacks it on the runner and moves each VirtualSystem's `<Info>`/`<Name>` to the front, where the OVF standard puts them, and updates the manifest. Nutanix Move 6.3's OVF has them after its sections; the vSphere Client accepts that, but vCenter's import API (and so `vmware_deploy_ovf`) refuses it with "Missing child element 'Info'".

The generated blueprint uses existing plays: `vsphere_prep` (roles/vsphere_prep: datacenter, cluster, hosts, datastore, ISOs) and `ovf` ("Deploy OVF files").

```yaml
centos:                       # the Ansible VM (roles/build_from_iso_centos)
  hosts:
    ansible: { ip_address: 192.168.0.22, distro: alma, version: "9", install_ansible: true }
stage2:
  hosts:
    ansible:
  vars:
    stage2_vcenter: vc01          # inventory name of the lab's vCenter
    stage2_esx_hosts: [esx01]
    stage2_isos: [ <file in files/>, ... ]
    stage2_ovas: [ { name: move, ova: Nutanix-Move.ova, fix_ovf: true } ]   # optional: networks, properties
```
The gateway needs the forward (with `rdp_jumphost: ""`, since that replaces `nat_rules`):
```yaml
nat_rules:
  - { name: "SSH to the Ansible VM", external_port: "2223", internal_port: "22", protocol: "tcp", target_ip: 192.168.0.22 }
```
See `inventories/lab_nutanix_move.yml`.
