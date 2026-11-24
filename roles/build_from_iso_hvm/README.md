# build_from_iso_hvm

Builds HPE VM Essentials hosts (HVM OS 26.04) as nested VMs on vCenter, installed unattended
from HPE's own ISO (`HPE_HVM_Install_26.04_S6E64-11270.iso` in `files/`).

## How the unattended install works

HPE's ISO is Ubuntu Server with HPE's Subiquity autoinstall in `/server/user-data`. Its GRUB entry
boots `autoinstall ds=nocloud;s=/cdrom/server/`, and the user-data marks locale, identity, network
and storage as interactive. Everything else (hvmcli, the `vs0` virtSwitch, DNS, IOMMU, HPE's
repositories) already runs unattended on first boot.

1. `prepare_iso.yml` makes one copy of the ISO, `<iso>-auto.iso`, with only GRUB changed:
   `ds=nocloud` (no `s=`) so cloud-init reads its seed from a disk labelled CIDATA, and a
   3-second menu timeout. `xorriso ... -boot_image any replay` keeps HPE's BIOS and EFI boot.
   All hosts share it.
2. `seed_iso.yml` makes a small CIDATA ISO per host: HPE's user-data, read from the ISO, with
   `interactive-sections` removed and these answered:
   - `identity`: hostname, `hvm_username` (sudo) and `hvm_password` (SHA-512 hash)
   - `storage`: `direct` on the smallest disk, leaving the data disk for VM storage
   - `network`: a static address on the first NIC, matched by its fixed MAC
   - `late-commands`: writes `/opt/HPE/installer-config/00-installer-config.yaml`, which HPE's
     network screen normally writes and `configure_mgmt_ip.sh` reads on first boot to create `vs0`
3. `build_vm.yml` builds the VM (EFI, one socket, nested virtualization, two vmxnet3 NICs,
   100 GB OS disk and 200 GB data disk) with the two ISOs and any `hvm_extra_isos` as CD drives,
   boots disk-then-CD and powers it on.

LabBuilder can't reach the lab LAN, so this role doesn't wait for the install. Stage 2
(`roles/hpevme_setup`) waits for the hosts over SSH from inside the lab.

## Notes

- One socket per host: the VME eval license allows 6 sockets.
- The lab LAN portgroup must allow promiscuous mode, forged transmits and MAC changes for the VMs
  that run on the hosts (LabBuilder's `prep.yml` sets them).
- An installed host is left alone on later runs; `state=force` rebuilds it.
