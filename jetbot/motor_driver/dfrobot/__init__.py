from .DFRobot_RaspberryPi_DC_Motor import DFRobot_DC_Motor_IIC as Board
import time


class DFRobotMotorDriver:

    def __init__(self, address=0x10, busnum=1):

        # initialize
        self.MOTOR_A = 0
        self.MOTOR_B = 1
        self.driver = Board(busnum, address)
        self.ids = [self.driver.M1, self.driver.M2]

        # Begin and check the status
        while self.driver.begin() != self.driver.STA_OK:
            self.driver.print_board_status()
            print("board begin faild")
            time.sleep(2)
        print("board begin success")
        self.driver.set_moter_pwm_frequency(1000)

    def move(self, motor, speed):
        '''
        speed: -100~100
        motor: MOTOR_A or MOTOR_B
        '''
        power = min(max(abs(speed), 0), 100)
        orientation = self.driver.CW if speed >= 0 else self.driver.CCW
        self.driver.motor_movement([self.ids[motor]], orientation, power)

    def stop(self, motor):
        # motor: MOTOR_A or MOTOR_B
        self.driver.motor_stop([self.ids[motor]])

    def reset(self):
        # Stop all motors
        self.driver.motor_stop(self.driver.ALL)
