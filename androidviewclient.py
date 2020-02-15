#! /usr/bin/env python
# -*- coding: utf-8 -*-


import subprocess
import re
import traceback
from time import sleep, time

from com.dtmilano.android.viewclient import ViewClient


def loop_until(func, seconds=15, nofail=False):
    start = time()
    firstrun = True
    while True:
        try:
            print("Looping " + str(func))
            ret = func(firstrun=firstrun)
            if ret != "continue":
                break
        except Exception:
            traceback.print_exc()
            if (time() - start) > seconds:
                if nofail:
                    return
                else:
                    raise
        if (time() - start) > seconds:
            return
        sleep(0.5)
        firstrun = False


class Netflix:
    def __init__(self, chromecast_name, connect_ip=None):
        self.chromecast_name = chromecast_name
        self.connect_ip = connect_ip

    def cast(self, netflix_url):
        if self.connect_ip:
            subprocess.check_call(["adb", "connect", self.connect_ip])

        kwargs1 = {"verbose": False, "ignoresecuredevice": False, "ignoreversioncheck": False}
        device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)

        kwargs2 = {
            "forceviewserveruse": False,
            "startviewserver": True,
            "autodump": False,
            "ignoreuiautomatorkilled": True,
            "compresseddump": True,
            "useuiautomatorhelper": False,
            "debug": {},
        }
        vc = ViewClient(device, serialno, **kwargs2)
        vc.device.shell("input keyevent KEYCODE_WAKEUP")
        vc.device.shell("input keyevent KEYCODE_WAKEUP")

        vc.device.shell("am force-stop com.netflix.mediaclient")
        vc.device.shell("am start -a android.intent.action.VIEW -d {}".format(netflix_url))

        def _cast(**kwargs):
            vc.dump(window="-1", sleep=1)
            vc.findViewById("com.netflix.mediaclient:id/ab_menu_cast_item").touch()
            vc.dump(window="-1", sleep=1)
            vc.findViewWithTextOrRaise(re.compile(self.chromecast_name)).touch()

        loop_until(_cast, seconds=5, nofail=True)

        def _play(**kwargs):
            vc.dump(window="-1", sleep=1)
            vc.findViewById("com.netflix.mediaclient:id/video_img").touch()

        loop_until(_play)

        vc.dump(window="-1", sleep=2)


if __name__ == "__main__":
    netflix = Netflix("Living Room Chromecast", connect_ip="192.168.100.13")
    netflix.cast("https://www.netflix.com/watch/81101272")
