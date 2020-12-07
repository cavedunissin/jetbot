from .waveshare import WaveshareMotorDriver
from .dfrobot import DFRobotMotorDriver


class MotorDriver:

    MOTOR_A = 0
    MOTOR_B = 1

    def __init__(self, board='dfrobot', **kwargs):

        if board == 'waveshare':
            driver = WaveshareMotorDriver(**kwargs)
        elif board == 'dfrobot':
            driver = DFRobotMotorDriver(**kwargs)
        else:
            raise NotImplementedError

        for method in ['move', 'stop', 'reset']:
            setattr(self, method, getattr(driver, method))
