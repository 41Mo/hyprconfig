#!/bin/python
import subprocess
import os

from argparse import ArgumentParser
parser = ArgumentParser(description=__doc__)

parser.add_argument("--switch", action='store_true', default=False)

args = parser.parse_args()

BATTERY = 1
AC = 2

if __name__ == "__main__":
    try:
        s = subprocess.check_output(["tlp-stat", "-m"]).decode('UTF-8')
    except Exception as e:
        os.system(f"notify-send \"failed to run tlp-stat. {e}\"")
        exit(1)

    state = None
    if s.strip('\n').lower().startswith("battery"):
        state = BATTERY

    if s.strip('\n').lower().startswith('ac'):
        state = AC

    if state == BATTERY:
        if not args.switch:
            print("")
        else:
            try:
                s = subprocess.check_output(["sudo", "tlp", "ac"]).decode('UTF-8')
            except Exception as e:
                os.system(f"notify-send \"failed to run tlp ac. {e}\"")
                exit(1)

            try:
                subprocess.check_output(["pkill", "-36", "waybar"], )
            except Exception as e:
                os.system(f"notify-send \"tlp_status.py failed to send signal\"")
                exit(1)
    
    if state == AC:
        if not args.switch:
            print("")
        else:
            try:
                s = subprocess.check_output(["sudo", "tlp", "bat"]).decode('UTF-8')
            except Exception as e:
                os.system(f"notify-send \"failed to run tlp bat. {e}\"")
                exit(1)

            try:
                subprocess.check_output(["pkill", "-36", "waybar"], )
            except Exception as e:
                os.system(f"notify-send \"tlp_status.py failed to send signal\"")
                exit(1)
