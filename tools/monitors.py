import os
from time import sleep
import threading
import signal

try:
    import pyudev
except ModuleNotFoundError:
    os.system(f"notify-send \"monitors.py no module pyudev. Exiting\"")
    exit(0)


monitors = {
    "eDP-1": {
        "primary": True,
        "config": "preferred, auto, 2",
        "drm_path": "/sys/class/drm/card1-eDP-1",
        "status": "unknown"
    },
    "DP-1": {
        "primary": False,
        "config": "preferred, auto, 1",
        "drm_path": "/sys/class/drm/card1-DP-1",
        "status": "unknown",
    },
    "DP-2": {
        "primary": False,
        "config": "preferred, auto, 1",
        "drm_path": "/sys/class/drm/card1-DP-2",
        "status": "unknown",
    },
    "DP-3": {
        "primary": False,
        "config": "preferred, auto, 1",
        "drm_path": "/sys/class/drm/card1-DP-3",
        "status": "unknown",
    },
}

MON_CONF = "hypr/monitor.conf"

class UdevMonitor():
    def __init__(self):
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='drm')  # Change this to match the subsystem you need
        self.check_symlink()
        self.update_mon_state()
        self.write_mon_conf()

    def blocking_wait_events(self):
        for device in iter(self.monitor.poll, None):
            sleep(5)
            cd = self.check_mon_state()
            if len(cd) > 0:
                print("detected monitor change updating config")
                self.write_mon_conf()

    def update_mon_state(self):
        for k,v in monitors.items():
            if (v["primary"] != False):
                continue
            with open(v["drm_path"]+'/status', 'rb') as f:
                v["status"] = f.read().decode("utf-8").strip('\n')

    def check_mon_state(self):
        changed_displays = []
        for k,v in monitors.items():
            if (v["primary"] != False):
                continue
            with open(v["drm_path"]+'/status', 'rb') as f:
                newstatus = f.read().decode("utf-8").strip('\n')
                if v["status"] != newstatus:
                    changed_displays.append(k)
                v["status"] = newstatus
        return changed_displays
    
    def write_mon_conf(self):

        # TODO make ext mon choosable
        for k,v in monitors.items():
            if v["primary"]:
                int_mon = k

        connected = False
        for k,v in monitors.items():
            if v["primary"]:
                continue
            ext_mon = k
            if monitors[ext_mon]["status"] == "connected":
                connected = True

        if connected:
            sleep(30)
            with open(MON_CONF, 'w') as f:
                f.write(f"monitor={int_mon}, disable\n")
                for k,v in monitors.items():
                    if v["primary"]:
                        continue
                    ext_mon = k
                    f.write(f"monitor={ext_mon}, {monitors[ext_mon]["config"]}\n")
            return
        with open(MON_CONF, 'w') as f:
            f.write(f"monitor={int_mon}, {monitors[int_mon]["config"]}\n")
            for k,v in monitors.items():
                if v["primary"]:
                    continue
                ext_mon = k
                f.write(f"monitor={ext_mon}, disable\n")

    def check_symlink(self):
        if os.path.islink(MON_CONF):
            os.unlink(MON_CONF)



def main():
    mon = UdevMonitor()
    mon.blocking_wait_events()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        os.system(f"notify-send \"monitors.py is dead.\n Reason {e}\"")
        raise e
        exit(-1)

