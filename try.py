from __future__ import print_function

import hid
import time
import uinput

MAPPING = {
    'green': uinput.BTN_0,
    'red': uinput.BTN_1,
    'yellow': uinput.BTN_2,
    'blue': uinput.BTN_3,
    'orange': uinput.BTN_4,
    'tilt': uinput.BTN_SELECT,  # SELECT
    'start': uinput.BTN_START,  # START
    'select': uinput.BTN_SELECT,  # SELECT
    'whammy': uinput.ABS_X,  # WHAMMY
    'strumdown': uinput.BTN_DPAD_DOWN,
    'strumup': uinput.BTN_DPAD_UP,
}

DEVICE = uinput.Device(MAPPING.values())

# enumerate USB devices

for d in hid.enumerate():
    keys = list(d.keys())
    keys.sort()
    for key in keys:
        print("%s : %s" % (key, d[key]))
    print()

# try opening a device, then perform write and read


def diff(new_arr, old_arr):
    for i in range(len(new_arr)):
        if new_arr[i] != old_arr[i]:
            yield (i, new_arr[i]) 


try:
    print("Opening the device")

    h = hid.device()
    h.open(0x054c, 0x0268)  # VendorID/ProductID

    print("Manufacturer: %s" % h.get_manufacturer_string())
    print("Product: %s" % h.get_product_string())
    print("Serial No: %s" % h.get_serial_number_string())

    # enable non-blocking mode
    h.set_nonblocking(1)

    # write some data to the device
    print("Write the data")
    h.write([0, 63, 35, 35] + [0] * 61)

    # wait
    time.sleep(0.05)

    # read back the answer
    print("Read the data")
    previous = None
    INPUT = {
        'green': False,
        'red': False,
        'yellow': False,
        'blue': False,
        'orange': False,
        'tilt': False,
        'start': False,
        'select': False,
        'whammy': False,
        'strumdown': False,
        'strumup': False,
    }

    def set_input(key, val, tmp):
        prev = INPUT[key]
        if tmp >= val:
            tmp -= val
            INPUT[key] = True
        else:
            INPUT[key] = False

        if prev != INPUT[key]:
            # SEND EVENT
            DEVICE.emit(MAPPING[key], INPUT[key])
            pass

        return tmp

    counter = 0
    while True:
        try:
            time.sleep(0.001)
            d = h.read(64)
            counter += 1
            if d:
                if previous and d != previous:
                    for ret in diff(d, previous):
                        if ret[0] == 7:
                            DEVICE.emit(MAPPING['whammy'], ret[1])

                        if ret[0] == 2:
                            tmp = ret[1] - 128
                            tmp = set_input('strumdown', 64, tmp)
                            tmp = set_input('strumup', 16, tmp)
                            tmp = set_input('start', 8, tmp)
                            tmp = set_input('select', 1, tmp)

                        if ret[0] == 3:
                            tmp = ret[1]
                            tmp = set_input('orange', 128, tmp)
                            tmp = set_input('blue', 64, tmp)
                            tmp = set_input('red', 32, tmp)
                            tmp = set_input('yellow', 16, tmp)
                            tmp = set_input('green', 2, tmp)
                            tmp = set_input('tilt', 1, tmp)

                previous = d
            else:
                continue
        except KeyboardInterrupt:
            break
        print(counter, end="\r")
        # print(INPUT)

    print("Closing the device")
    h.close()

except IOError as ex:
    print(ex)
    print("You probably don't have the hard coded device. Update the hid.device line")
    print("in this script with one from the enumeration list output above and try again.")

print("Done")