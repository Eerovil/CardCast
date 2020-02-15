#! /usr/bin/env python
# -*- coding: utf-8 -*-


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
    def __init__(self, chromecast_name):
        self.chromecast_name = chromecast_name

    def cast(self, search_term):

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
        vc.device.startActivity(
            "com.netflix.mediaclient/com.netflix.mediaclient.ui.launch.NetflixComLaunchActivity"
        )

        vc.dump(window="-1", sleep=2)

        def _cast(**kwargs):
            vc.dump(window="-1", sleep=1)
            vc.findViewById("com.netflix.mediaclient:id/ab_menu_cast_item").touch()
            vc.dump(window="-1", sleep=1)
            vc.findViewWithTextOrRaise(re.compile(self.chromecast_name)).touch()

        loop_until(_cast, seconds=5, nofail=True)

        def _search(firstrun):
            vc.dump(window="-1", sleep=2)
            if not firstrun:
                vc.findViewWithContentDescriptionOrRaise(re.compile(u"""Haku""")).touch()
                vc.dump(window="-1", sleep=2)

            vc.setText((vc.findViewByIdOrRaise("android:id/search_src_text")), search_term)
            vc.device.shell("input keyevent KEYCODE_BACK")

        loop_until(_search)

        def _clicksearch(**kwargs):
            vc.dump(window="-1", sleep=1)
            vc.findViewById("com.netflix.mediaclient:id/search_result_img").touch()

        loop_until(_clicksearch)

        def _play(**kwargs):
            vc.dump(window="-1", sleep=1)
            vc.findViewById("com.netflix.mediaclient:id/video_img").touch()

        loop_until(_play)

        vc.dump(window="-1", sleep=2)
