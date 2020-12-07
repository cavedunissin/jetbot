from .pca9685 import PCA9685


class WaveshareMotorDriver:

    # pin settings
    MOTOR_A = 0
    MOTOR_B = 1
    PINS = {
        MOTOR_A: {'PWM': 0, 'IN1': 1, 'IN2': 2},
        MOTOR_B: {'PWM': 5, 'IN1': 3, 'IN2': 4},
    }

    def __init__(self, address=0x40, busnum=1, **kwargs):

        # initialize
        self.driver = PCA9685(address, busnum, **kwargs)
        self.driver.set_pwm_freq(50)
        pass

    def move(self, motor, speed):
        # speed: -100~100
        # motor: MOTOR_A, MOTOR_B
        assert motor in list(self.PINS.keys())
        pins = self.PINS[motor]
        power = min(max(abs(speed), 0), 100)

        self.driver.set_duty_cycle(pins['PWM'], power)
        self.driver.toggle_pwm(pins['IN1'], speed >= 0)
        self.driver.toggle_pwm(pins['IN2'], speed < 0)

    def stop(self, motor):
        # motor: MOTOR_A, MOTOR_B
        assert motor in list(self.PINS.keys())
        self.move(motor, speed=0)

    def reset(self):
        self.driver.reset()
