import sys
import time
from win32gui import GetWindowText, GetForegroundWindow
import win32gui
from multiprocessing import Process
import logging
import datetime
import psutil, win32process
log = logging.log(logging.DEBUG, "log.txt")

file_path = r"Q:\time-tracker.txt"
default_GPS = r"2.30354785584658/48.83107313804879"

if sys.platform == "darwin":
    from AppKit import NSWorkspace
    from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID
    )


def get_active_window():
    try:
        if sys.platform == "darwin":
            app = NSWorkspace.sharedWorkspace().frontmostApplication()
            active_app_name = app.localizedName()

            options = kCGWindowListOptionOnScreenOnly
            windowList = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
            windowTitle = 'Unknown'
            for window in windowList:
                windowNumber = window['kCGWindowNumber']
                ownerName = window['kCGWindowOwnerName']
                # geometry = window['kCGWindowBounds']
                windowTitle = window.get('kCGWindowName', u'Unknown')
                if windowTitle and (
                                event_window_num == windowNumber
                        or ownerName == active_app_name
                ):
                    # log.debug(
                    #     'ownerName=%s, windowName=%s, x=%s, y=%s, '
                    #     'width=%s, height=%s'
                    #     % (window['kCGWindowOwnerName'],
                    #        window.get('kCGWindowName', u'Unknown'),
                    #        geometry['X'],
                    #        geometry['Y'],
                    #        geometry['Width'],
                    #        geometry['Height']))
                    break

            return _review_active_info(active_app_name, windowTitle)
        if sys.platform == "win32":
            pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())  # This produces a list of PIDs active window relates to
            program_name = psutil.Process(pid[-1]).name()
            print(psutil.Process(pid[-1]).name())  # pid[-1] is the most likely to survive last longer

            active_window = GetWindowText(GetForegroundWindow())
            return program_name, active_window
    except:
        log.error('Unexpected error: %s' % sys.exc_info()[0])
        log.error('error line number: %s' % sys.exc_traceback.tb_lineno)
    return 'Unknown', 'Unknown'

old_window = ""
try:
    flags, hcursor, (x,y) = win32gui.GetCursorInfo()
except Exception as e:
    print(e)
old_text = ""
old_x = ""

while True:
    program_name, active_window = get_active_window()

    if active_window != old_window:
        with open(file_path, "a", encoding="utf8") as file:
            text = str("\n" + datetime.datetime.now().astimezone().replace(microsecond=0).isoformat() + " - " + default_GPS + " - Computer" + " - " + program_name + " - " + active_window)
            print(text)
            file.write(text)
            old_text = text
        old_window = active_window

    elif x == old_x:
        if active_window == old_window:
            if "STOP" not in old_text:
                with open(file_path, "a", encoding="utf8") as file:
                    text = str("\n" + datetime.datetime.now().astimezone().replace(microsecond=0).isoformat() + " - " + default_GPS + " - " + "STOP")
                    print(text)
                    file.write(text)
    else:
        time.sleep(60)


    try:
        flags, hcursor, (old_x,old_y) = win32gui.GetCursorInfo()
    except Exception as e:
        print(e)
    time.sleep(60)
