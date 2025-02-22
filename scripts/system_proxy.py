#!/bin/python
import subprocess
import os
from argparse import ArgumentParser
import time

parser = ArgumentParser(description=__doc__)
parser.add_argument("--switch", action='store_true', default=False)
args = parser.parse_args()

CONNECTED = 1
DISCONNECTED = 2

def add_iptables_nat_rule(rule:list):
    base = ["iptables", "-t", "nat"]
    base.extend(rule)
    launch_proc(base, "proxy_launch.py failed to add iptables rule")

def launch_proc(cmd: list, error_notify:str):
    try:
        s = subprocess.check_output(cmd).decode('UTF-8')
        return s
    except Exception as e:
        os.system(f"notify-send \"{error_notify} | Error: {e}\"")

def add_all_rules():
    add_iptables_nat_rule(["-N", "REDSOCKS"])
    add_iptables_nat_rule(["-A", "REDSOCKS", "-d", "0.0.0.0/8", "-j", "RETURN"])
    add_iptables_nat_rule(["-A", "REDSOCKS", "-d", "10.0.0.0/8", "-j", "RETURN"])
    add_iptables_nat_rule(["-A", "REDSOCKS", "-d", "127.0.0.0/8", "-j", "RETURN"])
    add_iptables_nat_rule(["-A", "REDSOCKS", "-d", "169.254.0.0/16", "-j", "RETURN"])
    add_iptables_nat_rule(["-A", "REDSOCKS", "-d", "172.16.0.0/12", "-j", "RETURN"])
    add_iptables_nat_rule(["-A", "REDSOCKS", "-d", "192.168.0.0/16", "-j", "RETURN"])
    add_iptables_nat_rule(["-A", "REDSOCKS", "-d", "224.0.0.0/4", "-j", "RETURN"])
    add_iptables_nat_rule(["-A", "REDSOCKS", "-d", "240.0.0.0/4", "-j", "RETURN"])
    add_iptables_nat_rule(["-A", "REDSOCKS", "-p", "tcp", "-j", "REDIRECT", "--to-ports", "12345"])
    add_iptables_nat_rule(["-A", "OUTPUT", "-p", "tcp", "--dport", "443", "-j", "REDSOCKS"])
    add_iptables_nat_rule(["-A", "OUTPUT", "-p", "tcp", "--dport", "80", "-j", "REDSOCKS"])
    add_iptables_nat_rule(["-A", "PREROUTING", "-p", "tcp", "--dport", "443", "-j", "REDSOCKS"])
    add_iptables_nat_rule(["-A", "PREROUTING", "-p", "tcp", "--dport", "80", "-j", "REDSOCKS"])

def clean_nat():
    add_iptables_nat_rule(["-F"])
    add_iptables_nat_rule(["-X", "REDSOCKS"])

def check_status():
    s = launch_proc(["iptables", "-L", "-t", "nat"], "proxy_launch.py failed to check status")
    if s.find("REDSOCKS") == -1:
        return DISCONNECTED
    else:
        return CONNECTED
        return ""


if __name__ == "__main__":
    status = check_status()
    if status == DISCONNECTED:
        if not args.switch:
            print("")
        else:
            add_all_rules()
            launch_proc(["systemctl", "start", "redsocks"], "proxy_launch.py failed to run systemctl start")
            launch_proc(["pkill", "-35", "waybar"], "proxy_launch.py failed to send signal")
    else:
        if not args.switch:
            print("")
        else:
            clean_nat()
            launch_proc(["systemctl", "stop", "redsocks"], "proxy_launch.py failed to run systemctl start")
            launch_proc(["pkill", "-35", "waybar"], "proxy_launch.py failed to send signal")
