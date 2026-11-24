#!/usr/bin/env python3

# SLOP Warning.  Here there be vibes:

import base64
import ipaddress
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import yaml

FONT = "Calibri"
COLOR_BLUE = "#4472C4"
COLOR_ORANGE = "#ED7D31"
COLOR_CARD_BG = "light-dark(#D9D9D9,#D9D9D9)"
COLOR_BLACK = "light-dark(#000000,#000000)"

# Bus color palette for multi-LAN topologies (lan1, lan2, lan3, lan4...)
BUS_PALETTE = [
    ("#4472C4", "Data/Mgmt"),
    ("#ED7D31", "Internal/Cluster/HA"),
    ("#70AD47", "Storage/iSCSI"),
    ("#7030A0", "Replication/Backup"),
    ("#00B0F0", "DMZ/External"),
]

# Map logical icon keys to SVG filenames in your ./icons/ folder
ICON_FILES = {
    "laptop": "laptop.svg",
    "router": "router.svg",
    "arrow_badge": "arrow_badge.svg",
    "monitor": "monitor.svg",
    "windows": "windows.svg",
    "ad_dc": "ad_dc.svg",
    "ansible": "ansible.svg",
    "linux": "linux.svg",
    "ubuntu": "ubuntu.svg",
    "vcenter": "vcenter.svg",
    "server_top": "server_top.svg",
    "server_card": "server_card.svg",
    "vm_card": "vm_card.svg",
    "esxi": "esxi.svg",
    "proxmox": "proxmox.svg",
    "xcpng": "rocket_gray.svg",
    "netapp": "netapp.svg",
    "storagegrid": "storagegrid.svg",
    "aiqum": "aiqum.svg",
    "ova": "ova.svg",
    "nutanix": "nutanix.svg",
}


def load_svg_data_uri(icons_dir: Path, key: str):
    svg_path = icons_dir / ICON_FILES.get(key, "")
    if svg_path.exists():
        svg_text = svg_path.read_text(encoding="utf-8")
        if key == "server_top":
            svg_text = svg_text.replace("#595959", "#8C8C8C").replace("#595959".lower(), "#8C8C8C")
        b64 = base64.b64encode(svg_text.encode("utf-8")).decode("ascii")
        # Omit ';base64' so draw.io's style parser doesn't split on the semicolon
        return f"data:image/svg+xml,{b64}"
    return None


class DrawioBuilder:
    def __init__(self, name: str, icons_dir: Path):
        self.name = name
        self.icons_dir = icons_dir
        self._id = 2

        self.mxfile = ET.Element("mxfile", host="Electron", type="device")
        self.diagram = ET.SubElement(self.mxfile, "diagram", id="lab_diagram", name=name)
        self.model = ET.SubElement(
            self.diagram,
            "mxGraphModel",
            dx="1200",
            dy="800",
            grid="1",
            gridSize="10",
            guides="1",
            tooltips="1",
            connect="1",
            arrows="1",
            fold="1",
            page="1",
            pageScale="1",
            pageWidth="1200",
            pageHeight="850",
            background="#FFFFFF",
            math="0",
            shadow="0",
        )
        self.root = ET.SubElement(self.model, "root")
        ET.SubElement(self.root, "mxCell", id="0")
        ET.SubElement(self.root, "mxCell", id="1", parent="0")
    def next_id(self) -> str:
        val = str(self._id)
        self._id += 1
        return val

    def add_box(self, x, y, w, h, value="", style="", parent="1"):
        cid = self.next_id()
        cell = ET.SubElement(
            self.root,
            "mxCell",
            id=cid,
            value=value,
            style=style,
            vertex="1",
            parent=parent,
        )
        ET.SubElement(
            cell,
            "mxGeometry",
            x=str(x),
            y=str(y),
            width=str(w),
            height=str(h),
            **{"as": "geometry"},
        )
        return cid

    def add_icon(self, icon_key: str, x, y, w, h, fallback_label="", fallback_style=""):
        uri = load_svg_data_uri(self.icons_dir, icon_key)
        if uri:
            style = (
                "shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;"
                f"verticalAlign=top;aspect=fixed;imageAspect=1;image={uri};"
            )
            return self.add_box(x, y, w, h, "", style)
        style = fallback_style or (
            "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;"
            f"fontFamily={FONT};fontSize=9;fontStyle=1;"
        )
        return self.add_box(x, y, w, h, fallback_label or icon_key.upper(), style)

    def add_line(self, x1, y1, x2, y2, color=COLOR_BLACK, width=3, dashed=False):
        cid = self.next_id()
        dash_str = "dashed=1;" if dashed else ""
        style = f"endArrow=none;html=1;rounded=0;strokeColor={color};strokeWidth={width};{dash_str}"
        cell = ET.SubElement(self.root, "mxCell", id=cid, value="", style=style, edge="1", parent="1")
        geom = ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
        ET.SubElement(geom, "mxPoint", x=str(x1), y=str(y1), **{"as": "sourcePoint"})
        ET.SubElement(geom, "mxPoint", x=str(x2), y=str(y2), **{"as": "targetPoint"})
        return cid

    def add_text(self, text, x, y, w=80, h=24, bold=True, size=13, align="center"):
        style_bold = "fontStyle=1;" if bold else ""
        style = (
            f"text;html=1;strokeColor=none;fillColor=none;align={align};verticalAlign=middle;"
            f"whiteSpace=wrap;rounded=0;fontFamily={FONT};fontSize={size};{style_bold}fontColor={COLOR_BLACK};"
        )
        return self.add_box(x, y, w, h, text, style)

    def draw_vm_card(self, label: str, x: int, y: int, top_icon: str, bottom_icon: str, is_ova=False, label_below=False):
        w, h = 84, 136
        uri = load_svg_data_uri(self.icons_dir, "vm_card")
        if uri:
            style = (
                "shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;"
                f"verticalAlign=top;aspect=fixed;imageAspect=1;image={uri};"
            )
            self.add_box(x, y, w, h, "", style)
        else:
            card_style = (
                f"rounded=1;arcSize=18;whiteSpace=wrap;html=1;fillColor={COLOR_CARD_BG};"
                f"strokeColor={COLOR_BLACK};strokeWidth=2.5;"
            )
            self.add_box(x, y, w, h, "", card_style)
            self.add_line(x, y + 68, x + w, y + 68, COLOR_BLACK, 2)

        if label_below:
            self.add_text(label.upper(), x - 12, y + h + 4, w + 24, 22, bold=True, size=13)
        else:
            self.add_text(label.upper(), x - 12, y - 26, w + 24, 22, bold=True, size=13)

        self.add_icon(top_icon, x + 16, y + 10, 52, 48, top_icon.upper())

        if is_ova:
            ova_style = (
                f"rounded=1;arcSize=15;whiteSpace=wrap;html=1;fillColor={COLOR_BLACK};"
                f"strokeColor={COLOR_BLACK};fontColor=light-dark(#FFFFFF,#FFFFFF);fontFamily={FONT};fontSize=16;fontStyle=1;"
            )
            self.add_box(x + 12, y + 82, 60, 38, "OVA", ova_style)
        else:
            self.add_icon(bottom_icon, x + 16, y + 78, 52, 48, bottom_icon.upper())

        return x + (w // 2), y, y + h

    def draw_hypervisor_card(self, label: str, x: int, y: int, hv_icon: str):
        w, h = 84, 156
        uri = load_svg_data_uri(self.icons_dir, "server_card")
        if uri:
            style = (
                "shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;"
                f"verticalAlign=top;aspect=fixed;imageAspect=1;image={uri};"
            )
            self.add_box(x, y, w, h, "", style)
        else:
            card_style = (
                f"rounded=0;whiteSpace=wrap;html=1;fillColor={COLOR_CARD_BG};"
                f"strokeColor={COLOR_BLACK};strokeWidth=2.5;"
            )
            self.add_box(x, y, w, h, "", card_style)
            self.add_line(x, y + 78, x + w, y + 78, COLOR_BLACK, 2)
            self.add_icon("server_top", x + 16, y + 12, 52, 48, "SRV")

        self.add_icon(hv_icon, x + 16, y + 92, 52, 48, hv_icon.upper())
        self.add_text(label.upper(), x - 12, y + h + 4, w + 24, 22, bold=True, size=13)

        return x + (w // 2), y, y + h

    def to_xml_string(self) -> str:
        ET.indent(self.mxfile, space="  ")
        return ET.tostring(self.mxfile, encoding="unicode")


def octet(ip_str: str) -> str:
    val = str(ip_str).strip()
    if not val or "." not in val:
        return ""
    return f".{val.split('.')[-1]}"


def extract_subnets(all_vars: dict) -> list:
    """Detect all lab_lanX definitions (lan1, lan2, lan3, etc.) from all.vars."""
    lans = []
    for idx in range(1, 10):
        pg_key = f"lab_lan{idx}_portgroup"
        gw_key = f"lab_lan{idx}_gateway"
        cidr_key = f"lab_lan{idx}_netmask_cidr"
        if pg_key in all_vars or gw_key in all_vars:
            gw = str(all_vars.get(gw_key, ""))
            cidr = str(all_vars.get(cidr_key, "24"))
            subnet_str = ""
            if gw and "." in gw:
                try:
                    subnet_str = str(ipaddress.ip_network(f"{gw}/{cidr}", strict=False))
                except ValueError:
                    subnet_str = gw
            color, default_desc = BUS_PALETTE[(idx - 1) % len(BUS_PALETTE)]
            desc = all_vars.get(f"lab_lan{idx}_name", default_desc)
            lans.append({
                "index": idx,
                "key": f"lan{idx}",
                "subnet": subnet_str,
                "desc": desc,
                "color": color,
            })
    if not lans:
        lans.append({
            "index": 1,
            "key": "lan1",
            "subnet": "192.168.0.0/24",
            "desc": "Data/Mgmt",
            "color": COLOR_BLUE,
        })
    return lans
def detect_connected_lans(host_vars: dict, group_vars: dict, total_lans: int) -> list:
    """Determine which LAN buses (1-based indices) a host connects to."""
    merged = {**group_vars, **host_vars}
    connected = set()

    # Check ethernet_ports dict (common on esx, proxmox, xcpng)
    eth_ports = merged.get("ethernet_ports", {})
    if isinstance(eth_ports, dict):
        for target in eth_ports.values():
            t_str = str(target).lower()
            for idx in range(1, total_lans + 1):
                if f"lan{idx}" in t_str or f"net{idx}" in t_str:
                    connected.add(idx)

    # Check interfaces dict (common on pfsense)
    ifaces = merged.get("interfaces", {})
    if isinstance(ifaces, dict):
        for iface_name, target in ifaces.items():
            if str(iface_name).lower() == "wan":
                continue
            t_str = str(target).lower()
            for idx in range(1, total_lans + 1):
                if f"lan{idx}" in t_str or f"net{idx}" in t_str:
                    connected.add(idx)

    # Check explicit lanX_ip / secondary IPs
    for idx in range(1, total_lans + 1):
        if f"lan{idx}_ip" in merged or f"ip_address_lan{idx}" in merged:
            connected.add(idx)

    if not connected:
        connected.add(1)
    return sorted(connected)


def generate_diagram(yaml_path: Path, out_dir: Path, icons_dir: Path):
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "all" not in data:
        print(f"Skipping non-inventory YAML: {yaml_path}")
        return

    all_vars = data.get("all", {}).get("vars", {}) or {}
    children = data.get("all", {}).get("children", {}) or {}

    lab_name = yaml_path.stem
    lans = extract_subnets(all_vars)
    total_lans = len(lans)

    b = DrawioBuilder(lab_name, icons_dir)

    top_nodes = []
    bottom_nodes = []
    rdp_target_ip = None

    # --- PARSE ALL LABBUILDER COMPONENT GROUPS ---
    # 1. Routers / Firewalls (pfsense)
    pf_grp = children.get("pfsense", {}) or {}
    pf_gvars = pf_grp.get("vars", {}) or {}
    for hname, hvars in (pf_grp.get("hosts", {}) or {}).items():
        hvars = hvars or {}
        if not rdp_target_ip:
            rdp_target_ip = str(hvars.get("rdp_jumphost", pf_gvars.get("rdp_jumphost", "")))
        gw_ip = str(hvars.get("ip_address", all_vars.get("lab_lan1_gateway", "192.168.0.1")))
        top_nodes.append({
            "role": "gateway",
            "name": hname,
            "ip": gw_ip,
            "lans": detect_connected_lans(hvars, pf_gvars, total_lans),
        })

    # 2. Windows Desktops / Servers / Domain Controllers (winservers, dc, windows)
    for grp_name in ("winservers", "dc", "windows"):
        grp = children.get(grp_name, {}) or {}
        gvars = grp.get("vars", {}) or {}
        for hname, hvars in (grp.get("hosts", {}) or {}).items():
            hvars = hvars or {}
            is_dc = (grp_name == "dc") or ("dc" in hname.lower())
            top_nodes.append({
                "role": "dc" if is_dc else "desktop",
                "name": hname,
                "ip": str(hvars.get("ip_address", "")),
                "top_icon": "ad_dc" if is_dc else "monitor",
                "bot_icon": "windows",
                "is_ova": False,
                "lans": detect_connected_lans(hvars, gvars, total_lans),
            })

    # 3. Linux / Ansible / Ubuntu / RHEL (centos, ubuntu, linux, ansible)
    for grp_name in ("centos", "ubuntu", "linux", "ansible"):
        grp = children.get(grp_name, {}) or {}
        gvars = grp.get("vars", {}) or {}
        for hname, hvars in (grp.get("hosts", {}) or {}).items():
            hvars = hvars or {}
            merged = {**gvars, **hvars}
            is_ans = merged.get("install_ansible") or ("ansible" in hname.lower()) or (grp_name == "ansible")
            top_icon = "ansible" if is_ans else ("ubuntu" if grp_name == "ubuntu" else "server_top")
            bot_icon = "ubuntu" if grp_name == "ubuntu" else "linux"
            top_nodes.append({
                "role": "linux",
                "name": hname,
                "ip": str(hvars.get("ip_address", "")),
                "top_icon": top_icon,
                "bot_icon": bot_icon,
                "is_ova": False,
                "lans": detect_connected_lans(hvars, gvars, total_lans),
            })

    # 4. Appliances: vCenter, AIQUM, Generic OVA/OVF (vcenter, aiqum, ova, ovf)
    for grp_name in ("vcenter", "aiqum", "ova", "ovf"):
        grp = children.get(grp_name, {}) or {}
        gvars = grp.get("vars", {}) or {}
        for hname, hvars in (grp.get("hosts", {}) or {}).items():
            hvars = hvars or {}
            merged = {**gvars, **hvars}
            ovf_str = str(merged.get("ovf_file", merged.get("install_file", ""))).lower()
            is_ova = ovf_str.endswith(".ova") or grp_name == "ova"
            if grp_name == "vcenter" or "vcenter" in ovf_str:
                disp = "VCSA" if hname.lower().startswith("vc") else hname
                t_icon = "vcenter"
            elif grp_name == "aiqum" or "aiqum" in ovf_str:
                disp = hname
                t_icon = "aiqum"
            else:
                disp = hname
                t_icon = "ova"
            top_nodes.append({
                "role": "appliance",
                "name": disp,
                "ip": str(hvars.get("ip_address", "")),
                "top_icon": t_icon,
                "bot_icon": "ova",
                "is_ova": is_ova,
                "lans": detect_connected_lans(hvars, gvars, total_lans),
            })
    # 5. Hypervisors (esx, nested_esx, proxmox, pve, xcpng)
    hypervisor_map = {
        "esx": "esxi",
        "nested_esx": "esxi",
        "proxmox": "proxmox",
        "pve": "proxmox",
        "xcpng": "xcpng",
        "nutanix": "nutanix",
    }
    for grp_name, hv_icon in hypervisor_map.items():
        grp = children.get(grp_name, {}) or {}
        gvars = grp.get("vars", {}) or {}
        for hname, hvars in (grp.get("hosts", {}) or {}).items():
            hvars = hvars or {}
            hv_lans = detect_connected_lans(hvars, gvars, total_lans)
            if total_lans > 1 and hv_lans == [1] and not gvars.get("ethernet_ports"):
                hv_lans = [1, 2]
            bottom_nodes.append({
                "role": "hypervisor",
                "name": hname,
                "ip": str(hvars.get("ip_address", "")),
                "bot_icon": hv_icon,
                "lans": hv_lans,
            })

    # 6. Storage Systems (vsims, ots, ontap, sgws, storagegrid)
    for grp_name in ("vsims", "ots", "ontap", "sgws", "storagegrid"):
        grp = children.get(grp_name, {}) or {}
        gvars = grp.get("vars", {}) or {}
        for hname, hvars in (grp.get("hosts", {}) or {}).items():
            hvars = hvars or {}
            merged = {**gvars, **hvars}
            cname = merged.get("cluster_name", hname)
            cip = str(merged.get("cluster_mgmt_ip", hvars.get("ip_address", "")))
            st_icon = "storagegrid" if grp_name in ("sgws", "storagegrid") else "netapp"
            st_lans = list(range(1, total_lans + 1)) if total_lans > 1 else [1]
            bottom_nodes.append({
                "role": "storage",
                "name": cname,
                "ip": cip,
                "icon": st_icon,
                "lans": st_lans,
            })

    # Filter network bars to only LANs connected by at least one VM or hypervisor (exclude gateway & storage)
    active_lan_indices = set()
    for n in top_nodes:
        if n["role"] != "gateway":
            active_lan_indices.update(n.get("lans", []))
    for n in bottom_nodes:
        if n["role"] == "hypervisor":
            active_lan_indices.update(n.get("lans", []))

    if active_lan_indices:
        lans = [l for l in lans if l["index"] in active_lan_indices]
    else:
        lans = lans[:1]

    valid_indices = {l["index"] for l in lans}
    for n in bottom_nodes:
        if n["role"] == "storage":
            filtered = [i for i in n.get("lans", []) if i in valid_indices]
            n["lans"] = filtered if filtered else [lans[0]["index"]]

    # --- COMPUTE CANVAS & BUS GEOMETRY ---
    col_step = 135
    max_cols = max(len(top_nodes), len(bottom_nodes) + 1, 5)
    box_x = 140
    box_w = max(840, max_cols * col_step + 140)
    box_y = 30

    bus_x1 = box_x + 25
    bus_x2 = box_x + box_w - 25
    first_bus_y = 290
    bus_spacing = 46

    last_bus_y = first_bus_y + ((len(lans) - 1) * bus_spacing)
    bot_y = last_bus_y + 80
    box_h = (bot_y + 185) - box_y

    # Full-canvas white background so laptop area & PNG exports are always solid white
    canvas_bg_style = "rounded=0;whiteSpace=wrap;html=1;fillColor=light-dark(#FFFFFF,#FFFFFF);strokeColor=none;"
    b.add_box(0, 0, box_x + box_w + 40, box_y + box_h + 40, "", canvas_bg_style)

    # Outer Lab Frame (drawn FIRST with solid white fill so it sits behind bus lines and cards)
    frame_style = (
        f"rounded=1;arcSize=5;whiteSpace=wrap;html=1;fillColor=light-dark(#FFFFFF,#FFFFFF);"
        f"strokeColor={COLOR_BLACK};strokeWidth=1.5;"
    )
    b.add_box(box_x, box_y, box_w, box_h, "", frame_style)

    for idx, lan in enumerate(lans):
        by = first_bus_y + (idx * bus_spacing)
        lan["y"] = by
        b.add_line(bus_x1, by, bus_x2, by, lan["color"], 4)
        if idx == 0 and lan["subnet"]:
            b.add_text(lan["subnet"], bus_x1 + 65, by - 26, 140, 22, bold=True, size=13, align="left")
        label_str = f"{lan['desc']} ({lan['subnet']})" if (idx > 0 and lan["subnet"]) else lan["desc"]
        b.add_text(label_str, bus_x1 + 65, by + 4, 220, 22, bold=True, size=13, align="left")

    # --- RENDER TOP ROW NODES ---
    top_y = 95
    gateway_right_x = None
    rdp_target_left_x = None

    for idx, node in enumerate(top_nodes):
        if node["role"] == "gateway":
            cx = box_x + 35
            b.add_icon("laptop", 22, top_y + 42, 84, 55, "LAPTOP")
            badge_bg = "ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=light-dark(#FFFFFF,#FFFFFF);strokeColor=none;"
            b.add_box(box_x - 20, top_y + 47, 40, 40, "", badge_bg)
            b.add_icon("arrow_badge", box_x - 20, top_y + 47, 40, 40, "<->")
            r_size = 84
            r_style = (
                f"ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor={COLOR_CARD_BG};"
                f"strokeColor={COLOR_BLACK};strokeWidth=2.5;"
            )
            #b.add_box(cx, top_y + 26, r_size, r_size, "", r_style)
            b.add_icon("router", cx, top_y + 26, r_size, r_size, "GW")
            b.add_text(node["name"], cx, top_y, r_size, 22, bold=True, size=13)

            drop_x = cx + (r_size // 2)
            target_lan = lans[0]
            b.add_line(drop_x, top_y + 26 + r_size, drop_x, target_lan["y"], target_lan["color"], 3.5)
            b.add_text(octet(node["ip"]), drop_x + 2, top_y + 26 + r_size + 2, 36, 20, bold=True, size=12, align="left")
            gateway_right_x = cx + r_size
        else:
            cx = box_x + 70 + (idx * col_step)
            mid_x, _, card_bot = b.draw_vm_card(
                node["name"],
                cx,
                top_y,
                node["top_icon"],
                node["bot_icon"],
                is_ova=node.get("is_ova", False),
                label_below=False,
            )
            for l_idx_pos, lan_num in enumerate(node["lans"]):
                lan_obj = next((l for l in lans if l["index"] == lan_num), lans[0])
                offset = (l_idx_pos - (len(node["lans"]) - 1) / 2) * 14
                dx = int(mid_x + offset)
                b.add_line(dx, card_bot, dx, lan_obj["y"], lan_obj["color"], 3.5)
                if l_idx_pos == 0:
                    b.add_text(octet(node["ip"]), dx + 2, card_bot + 2, 36, 20, bold=True, size=12, align="left")

            if rdp_target_ip and node["ip"] == rdp_target_ip:
                rdp_target_left_x = cx

    # Draw RDP Connection between Gateway and Jumphost
    if gateway_right_x and rdp_target_left_x and rdp_target_left_x > gateway_right_x:
        badge_size = 40
        target_badge_x = rdp_target_left_x - (badge_size // 2)
        b.add_line(gateway_right_x, top_y + 68, target_badge_x, top_y + 68, COLOR_BLACK, 5)
        badge_bg = "ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=light-dark(#FFFFFF,#FFFFFF);strokeColor=none;"
        b.add_box(target_badge_x, top_y + 48, badge_size, badge_size, "", badge_bg)
        b.add_icon("arrow_badge", target_badge_x, top_y + 48, badge_size, badge_size, "RDP")
        mid_rdp = (gateway_right_x + target_badge_x) // 2
        b.add_text("RDP", mid_rdp - 20, top_y + 72, 40, 20, bold=True, size=12)

    # --- RENDER BOTTOM ROW NODES (Hypervisors & Storage) ---
    hv_nodes = [n for n in bottom_nodes if n["role"] == "hypervisor"]
    st_nodes = [n for n in bottom_nodes if n["role"] == "storage"]

    hv_start_x = box_x + 220
    for idx, node in enumerate(hv_nodes):
        cx = hv_start_x + (idx * 120)
        mid_x, top_edge, _ = b.draw_hypervisor_card(
            node["name"],
            cx,
            bot_y,
            node["bot_icon"],
        )
        n_lans = node["lans"]
        for pos, lan_num in enumerate(n_lans):
            lan_obj = next((l for l in lans if l["index"] == lan_num), lans[0])
            offset = (pos - (len(n_lans) - 1) / 2) * 20
            dx = int(mid_x + offset)
            b.add_line(dx, lan_obj["y"], dx, top_edge, lan_obj["color"], 3.5)
            if pos == 0:
                b.add_text(octet(node["ip"]), dx - 36, top_edge - 24, 34, 20, bold=True, size=12, align="right")

    st_start_x = hv_start_x + max(len(hv_nodes), 1) * 120 + 40
    for idx, node in enumerate(st_nodes):
        cx = st_start_x + (idx * 200)
        sw, sh = 170, 82
        st_style = (
            f"rounded=0;whiteSpace=wrap;html=1;fillColor={COLOR_CARD_BG};"
            f"strokeColor={COLOR_BLACK};strokeWidth=2.5;"
        )
        b.add_icon(node["icon"], cx, bot_y + 45, sw, sh, node["name"].upper(), st_style)
        b.add_text(node["name"].upper(), cx, bot_y + 45 + sh + 6, sw, 22, bold=True, size=13)

        top_edge = bot_y + 45
        n_lans = node["lans"]
        for pos, lan_num in enumerate(n_lans):
            lan_obj = next((l for l in lans if l["index"] == lan_num), lans[0])
            dx = cx + 55 + (pos * 35)
            b.add_line(dx, lan_obj["y"], dx, top_edge, lan_obj["color"], 3.5)
            if pos == 0:
                b.add_text(octet(node["ip"]), dx - 36, top_edge - 24, 34, 20, bold=True, size=12, align="right")

    out_file = out_dir / f"{lab_name}.drawio"
    out_file.write_text(b.to_xml_string(), encoding="utf-8")
    print(f"Generated: {out_file}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python inv2drawio.py <inventory_file_or_dir> <output_dir> [icons_dir]")
        sys.exit(1)

    src = Path(sys.argv[1])
    default_out_dir = Path(__file__).resolve().parent.parent / "diagrams/"
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else default_out_dir
    default_icons = Path(__file__).resolve().parent.parent / "diagrams/icons"
    icons_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else default_icons
    out_dir.mkdir(parents=True, exist_ok=True)

    files = [src] if src.is_file() else sorted(list(src.glob("*.yml")) + list(src.glob("*.yaml")))
    for f in files:
        generate_diagram(f, out_dir, icons_dir)


if __name__ == "__main__":
    main()
