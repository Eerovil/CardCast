import hid
import time


# enumerate USB devices
class Reader():
    def __init__(self, vendor, product):
        self.h = None
        self.vendor = vendor
        self.product = product
        for d in hid.enumerate():
            keys = list(d.keys())
            keys.sort()
            for key in keys:
                print("%s : %s" % (key, d[key]))
            print()
    
    def __enter__(self):
        try:
            print("Opening the device")

            self.h = hid.device()
            self.h.open(self.vendor, self.product)  # VendorID/ProductID

            print("Manufacturer: %s" % self.h.get_manufacturer_string())
            print("Product: %s" % self.h.get_product_string())
            print("Serial No: %s" % self.h.get_serial_number_string())

            # enable non-blocking mode
            self.h.set_nonblocking(1)

            # write some data to the device
            print("Write the data")
            self.h.write([0, 63, 35, 35] + [0] * 61)
            return self

        except IOError as ex:
            print(ex)
            print("You probably don't have the hard coded device. Update the hid.device line")
            print("in this script with one from the enumeration list output above and try again.")
            raise

    def __exit__(self, type, value, traceback):
        print("Closing the device")
        self.h.close()

    def read():
        try:
            while True:
                time.sleep(0.001)
                d = self.h.read(64)
                if d:
                    return d
                else:
                    continue
        except KeyboardInterrupt:
            pass
        print(counter, end="\r")
        # print(INPUT)

