import os
import sys
from argparse import ArgumentParser

if __name__ != "__main__":
    exit(-1)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = ArgumentParser(description=__doc__)
HOME_PATH=os.environ['HOME']
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

# table in format "name": (source, dest)
links_table = {
    "hypr_desktop": (
        SCRIPT_DIR+"/hypr/desktop.conf",
        SCRIPT_DIR+"/hypr/shared.conf"
    ),
    "hypr_laptop": (
        SCRIPT_DIR+"/hypr/laptop.conf",
        SCRIPT_DIR+"/hypr/shared.conf"
    ),
    "laptop_mon": (
        SCRIPT_DIR+"/hypr/laptop_monitor.conf",
        SCRIPT_DIR+"/hypr/monitor.conf",
    ),
    "desktop_mon": (
        SCRIPT_DIR+"/hypr/desktop_monitor.conf",
        SCRIPT_DIR+"/hypr/monitor.conf",
    ),
    "hyprland_conf": (
        SCRIPT_DIR+"/hypr",
        HOME_PATH+"/.config/hypr"
    ),
    "waybar": (
        SCRIPT_DIR+"/waybar",
        HOME_PATH+"/.config/waybar"
    ),
    "qt5ct": (
        SCRIPT_DIR+"/dot_config/qt5ct.conf",
        HOME_PATH+"/.config/qt5ct/qt5ct.conf"
    ),
    "qt6ct": (
        SCRIPT_DIR+"/dot_config/qt6ct.conf",
        HOME_PATH+"/.config/qt5ct/qt6ct.conf"
    ),
    "kdeglobals": (
        SCRIPT_DIR+"/dot_config/kdeglobals",
        HOME_PATH+"/.config/kdeglobals"
    ),
    "portals": (
        SCRIPT_DIR+"/dot_config/portals.conf",
        HOME_PATH+"/.config/xdg-desktop-portal/portals.conf"
    ),
    "dolphinrc": (
        SCRIPT_DIR+"/dot_config/dolphinrc",
        HOME_PATH+"/.config/dolphinrc"
    ),
    "mon_upd": (
        SCRIPT_DIR+"/dot_config/mon_upd.service",
        HOME_PATH+"/.config/systemd/user/mon_upd.service"
    ),
    "tlp_status": (
        SCRIPT_DIR+"/scripts/tlp_status.py",
        HOME_PATH+"/.local/bin/tlp_status.py"
    ),
    "proxy": (
        SCRIPT_DIR+"/scripts/system_proxy.py",
        HOME_PATH+"/.local/bin/system_proxy.py"
    ),
    "sd-environment": (
        SCRIPT_DIR+"/dot_config/path.conf",
        HOME_PATH+"/.config/environment.d/path.conf",
    ),
    "hyprland" : ["hyprland_conf", "waybar"],
    "dotfiles" : ["qt5ct", "qt6ct", "kdeglobals", "portals", "dolphinrc"],
    "laptop" : ["hypr_laptop", "laptop_mon"],
    "desktop": ["hypr_desktop", "desktop_mon"],
}

groups = ("hyprland", "dotfiles", "laptop", "desktop")

parser.add_argument("--default_links", nargs='+', choices=links_table.keys(), default=["hyprland", "waybar"])
parser.add_argument("-f", "--force_update", action='store_true')
args = parser.parse_args()
names = [];

for n in args.default_links:
    if n in groups:
        names.extend(links_table.get(n))
    else:
        names.append(n)

for link_name in names:
    try:
        if type(links_table.get(link_name)) != tuple:
            raise Exception(f"linkname {link_name} should be tuple")
        link_src, link_dst = links_table.get(link_name)
    except TypeError:
        print(f"{bcolors.FAIL}Wrong table entry {link_name}")
        continue

    if os.path.exists(link_dst):
        if args.force_update:
            os.unlink(link_dst)
        else:
            print(f"{bcolors.WARNING}Warning: {link_dst} already exists, and would not be updated", file=sys.stderr)
            continue
    dirname = os.path.dirname(link_dst)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    print(f"{bcolors.OKGREEN}Linking: {link_dst}")
    os.symlink(link_src,link_dst)
