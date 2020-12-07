import time
import Adafruit_GPIO.I2C as I2C

'''
PCA9685 settings
ref:
    https://cdn-shop.adafruit.com/datasheets/PCA9685.pdf
    https://github.com/adafruit/Adafruit_Python_PCA9685
    https://github.com/jetsonhacks/JHPWMDriver
'''

# specs
RESOLUTION       = 4096     # 12bits
OSCILLATOR_CLOCK = 25000000 # 25MHz
MIN_FREQ         = 40
MAX_FREQ         = 1000

# Registers:
MODE1            = 0x00
MODE2            = 0x01
PRE_SCALE        = 0xFE
LED0_ON_L        = 0x06
LED0_ON_H        = 0x07
LED0_OFF_L       = 0x08
LED0_OFF_H       = 0x09
ALL_LED_ON_L     = 0xFA
ALL_LED_ON_H     = 0xFB
ALL_LED_OFF_L    = 0xFC
ALL_LED_OFF_H    = 0xFD

# Bits:
ALLCALL          = 0x01
OUTDRV           = 0x04
RESTART          = 0x80
SLEEP            = 0x10
INVRT            = 0x10


def val_low(val):
    return val & 0xFF


def val_high(val):
    return val >> 8


class PCA9685:

    def __init__(self, address=0x40, busnum=1, **kwargs):

        # Setup I2C interface for the device.
        self.device = I2C.get_i2c_device(address, busnum=busnum, **kwargs)

        self.reset()
        self.wake()

    def wake(self):
        mode1 = self.device.readU8(MODE1)
        mode1 = mode1 & ~SLEEP
        self.device.write8(MODE1, mode1)
        time.sleep(0.005)

    def reset(self):
        self.set_all_pwm(0, 0)
        self.device.write8(MODE2, OUTDRV)
        self.device.write8(MODE1, ALLCALL)
        time.sleep(0.005)

    def set_pwm_freq(self, freq):
        freq = min(max(freq, MIN_FREQ), MAX_FREQ)
        prescale = int(OSCILLATOR_CLOCK / RESOLUTION / freq - 0.5)
        old_mode = self.device.readU8(MODE1)
        new_mode = (old_mode & 0x7F) | SLEEP
        self.device.write8(MODE1, new_mode)
        self.device.write8(PRE_SCALE, prescale)
        self.device.write8(MODE1, old_mode)
        time.sleep(0.005)
        self.device.write8(MODE1, old_mode | RESTART)

    def set_pwm(self, channel, on_val, off_val):
        self.device.write8(LED0_ON_L + 4*channel,  val_low(on_val))
        self.device.write8(LED0_ON_H + 4*channel,  val_high(on_val))
        self.device.write8(LED0_OFF_L + 4*channel, val_low(off_val))
        self.device.write8(LED0_OFF_H + 4*channel, val_high(off_val))

    def set_all_pwm(self, on_val, off_val):
        self.device.write8(ALL_LED_ON_L,  val_low(on_val))
        self.device.write8(ALL_LED_ON_H,  val_high(on_val))
        self.device.write8(ALL_LED_OFF_L, val_low(off_val))
        self.device.write8(ALL_LED_OFF_H, val_high(off_val))

    def set_duty_cycle(self, channel, duty):
        duty = min(max(duty, 0), 100)
        self.set_pwm(channel, 0, int(duty / 100 * (RESOLUTION-1)))

    def toggle_pwm(self, channel, toggle):
        if toggle:
            self.set_pwm(channel, 0, RESOLUTION - 1)
        else:
            self.set_pwm(channel, 0, 0)
