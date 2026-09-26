import evdev
import socket
# Finds a device by it's human readable name and returns it as an InputDevice or returns None if not available.
def findDevice(name: str):
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device.path, device.name, device.phys)
        if device.name==name:
            print(u"Device Found {}".format(device.name))
            return device
        return None

# Takes the device from findDevice and returns the barcode as a string (delinated through an extra space provided by the scanner input)
def readCode(dev:evdev.InputDevice) -> str:
    # Key map to process key input
    code=""
    scancodes = {
        # Scancode: ASCIICode
        0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
        10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
        20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
        30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
        40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
        50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57:u'SPACE', 100: u'RALT'
    }


    ## Event Input
    for event in dev.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
                data = evdev.categorize(event)
                if data.keystate == 1:
                    key_lookup = scancodes.get(data.scancode) or u'UNKNOWN:{}'.format(data.scancode)
                    # print(u'You pressed the {} key'.format(key_lookup))
                    if key_lookup != 'SPACE':
                            print(key_lookup)
                            code = code + key_lookup
                    else:
                            print(u'The code is: {}'.format(code))
                            return code

def outputCode(addr:str,port:int,code:str):
     HOST = addr
     PORT = port
     message = code
     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST,PORT))
            s.send(message)
        except Exception as inst:
             print(u"An error occured: {}".format(inst))



if __name__ == "__main__":
    while True:
        dev = findDevice("Pixel 7 Pro")
        if dev != None:
            try:
                code=readCode(dev)
            except Exception as inst:
                print(u"Something went wrong: {}".format(inst))
            outputCode("192.168.1.84",3225,code)


