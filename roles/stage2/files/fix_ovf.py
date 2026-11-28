#!/usr/bin/env python3
"""Unpack an OVA and fix its OVF so vCenter's import accepts it.

The OVF standard puts a VirtualSystem's own <Info> and <Name> before its sections. Some
appliances (Nutanix Move 6.3 among them) put them after AnnotationSection / ProductSection;
the vSphere Client lets that through, but vCenter's import API refuses it ("Missing child
element 'Info'"). This moves those two elements to the front of each VirtualSystem, changes
nothing else, and updates the manifest's checksum for the OVF.

Usage: fix_ovf.py OVA OUT_DIR NAME
Writes OUT_DIR/NAME.ovf next to the OVA's disks and manifest. Prints "fixed" or "unchanged".
"""
import hashlib
import io
import os
import re
import sys
import tarfile
import xml.etree.ElementTree as ET

OVF_NS = 'http://schemas.dmtf.org/ovf/envelope/1'

ova, out_dir, name = sys.argv[1:4]
os.makedirs(out_dir, exist_ok=True)
with tarfile.open(ova) as tar:
    members = tar.getmembers()
    for m in members:                                   # flat archive: refuse odd paths
        if os.path.basename(m.name) != m.name or not m.isfile():
            raise SystemExit(f'error: unexpected entry in {ova}: {m.name}')
    tar.extractall(out_dir, filter='data')

ovf_name = next(m.name for m in members if m.name.endswith('.ovf'))
mf_name = next((m.name for m in members if m.name.endswith('.mf')), None)
raw = open(os.path.join(out_dir, ovf_name), 'rb').read()

# keep the file's own namespace prefixes when writing it back
for _, (prefix, uri) in ET.iterparse(io.BytesIO(raw), events=['start-ns']):
    ET.register_namespace(prefix, uri)
root = ET.fromstring(raw)

changed = False
for vs in root.iter(f'{{{OVF_NS}}}VirtualSystem'):
    children = list(vs)
    head = [c for c in children if c.tag in (f'{{{OVF_NS}}}Info', f'{{{OVF_NS}}}Name')]
    head.sort(key=lambda c: 0 if c.tag.endswith('Info') else 1)
    if children[:len(head)] != head:
        for c in head:
            vs.remove(c)
        for i, c in enumerate(head):
            vs.insert(i, c)
        changed = True

new_ovf = f'{name}.ovf'
data = ET.tostring(root, encoding='utf-8', xml_declaration=True) if changed else raw
open(os.path.join(out_dir, new_ovf), 'wb').write(data)
if new_ovf != ovf_name:
    os.remove(os.path.join(out_dir, ovf_name))

# manifest: same algorithm as the original, new OVF name and checksum
if mf_name:
    lines = []
    for line in open(os.path.join(out_dir, mf_name)).read().splitlines():
        m = re.match(r'(\w+)\((.+)\)\s*=\s*(\w+)', line)
        if m and m.group(2) == ovf_name:
            algo = m.group(1)
            digest = hashlib.new(algo.lower().replace('-', ''), data).hexdigest()
            line = f'{algo}({new_ovf})= {digest}'
        lines.append(line)
    os.remove(os.path.join(out_dir, mf_name))
    open(os.path.join(out_dir, f'{name}.mf'), 'w').write('\n'.join(lines) + '\n')

print('fixed' if changed else 'unchanged')
