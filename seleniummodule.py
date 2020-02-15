from time import sleep, time
import traceback
import sys

from selenium import webdriver

DATADIR = sys.argv[1] if len(sys.argv) > 1 else "/home/pi/cardcast/chromium"
CHROMEDRIVER = sys.argv[2] if len(sys.argv) > 2 else "/usr/lib/chromium-browser/chromedriver"

try:
    from pyvirtualdisplay import Display

    display = Display(visible=0, size=(800, 1000))
    display.start()
except Exception:
    print("No pyvirtualdisplay")


def loop_until(func, seconds=15, nofail=False):
    start = time()
    while True:
        try:
            print("Looping " + str(func))
            ret = func()
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


def set_chromcast_setting(browser):
    browser.get("chrome://flags")
    sleep(1)
    element = browser.find_element_by_css_selector("#load-media-router-component-extension")
    browser.execute_script("arguments[0].scrollIntoView();", element)
    browser.get_screenshot_as_file("screen1.png")
    browser.find_element_by_css_selector("#load-media-router-component-extension select").click()
    sleep(1)
    browser.find_element_by_css_selector(
        "#load-media-router-component-extension select option:nth-child(2)"
    ).click()
    sleep(1)
    browser.get_screenshot_as_file("screenflags.png")


try:
    options = webdriver.ChromeOptions()
    excludeList = ["disable-default-apps", "disable-background-networking"]
    options.add_experimental_option("excludeSwitches", excludeList)
    options.add_argument("--user-data-dir={}".format(DATADIR))

    browser = webdriver.Chrome(CHROMEDRIVER, chrome_options=options)

    set_chromcast_setting(browser)

    browser.get("https://areena.yle.fi/1-3845205")
    print(browser.title)

    def _play():
        browser.find_element_by_css_selector(".playkit-pre-playback-play-button").click()

    loop_until(_play)

    import pdb

    pdb.set_trace()

    browser.get_screenshot_as_file("screen1.png")

    def _cast():
        browser.find_element_by_css_selector(".playkit-cast-button").click()
        sleep(1)
        browser.find_element_by_css_selector(".playkit-cast-button").click()

    loop_until(_cast, 2)
    browser.get_screenshot_as_file("screen2.png")
    sleep(5)
    browser.quit()
except Exception:
    browser.get_screenshot_as_file("screenerror.png")
    traceback.print_exc()

try:
    browser.quit()
except Exception:
    traceback.print_exc()

try:
    display.stop()
except Exception:
    traceback.print_exc()
