import serial
import struct
from functools import wraps


def _autoconnect(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            self.open_port()
            result = func(self, *args, **kwargs)
            return result
        finally:
            self.close_port()

    return wrapper


class ZaberStage:
    """
    Please see this documentation:
    https://www.zaber.com/w/Manuals/Binary_Protocol_Manual#Set_Index_Distance_-_Cmd_79

    For newer firmware (7), please see this documentation:
    https://www.zaber.com/protocol-manual?protocol=Binary#topic_return_054_status
    """

    def __init__(self, port):
        # serial port with 1 minute timeout
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.timeout = 60

        self._max_pos = 1066667
        self._max_range = 50.8

        self._cmd_home = 1
        self._cmd_move_absolute = 20
        self._cmd_move_relative = 21
        self._cmd_move_at_constant_speed = 22
        self._cmd_stop = 23
        self._cmd_return_status = 54
        self._cmd_return_current_position = 60

        self.connected = False

    def open_port(self):
        if not self.ser.is_open:
            self.ser.open()
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            self.connected = True

    def close_port(self):
        if self.ser.is_open:
            self.ser.close()
            self.connected = False

    @property
    def device(self):
        # assume only one zaber stage is connected (no daisy chain)
        return 1

    def send_message(self, command_number, data=0):
        msg = struct.pack("<2Bl", self.device, command_number, data)
        self.ser.write(msg)

    def receive_message(self):
        msg = self.ser.read(6)
        command_number = msg[1]
        msg_received = msg[2:]

        assert command_number != 255, "error occured! perhaps command does not exist?"
        return command_number, msg_received

    @_autoconnect
    def home(self):
        self.send_message(self._cmd_home)

    @_autoconnect
    def move_absolute(self, pos):
        self.send_message(self._cmd_move_absolute, pos)

    @_autoconnect
    def move_relative(self, step):
        self.send_message(self._cmd_move_relative, step)

    @_autoconnect
    def move_at_constant_speed(self, vel):
        self.send_message(self._cmd_move_at_constant_speed, vel)

    @_autoconnect
    def stop(self):
        self.send_message(self._cmd_stop)

    @_autoconnect
    def return_current_position(self):
        self.send_message(self._cmd_return_current_position)
        cmd_num, msg = self.receive_message()
        return struct.unpack("l", msg)

    @_autoconnect
    def return_status(self):
        """
        0 - idle, not currently executing any instructions
        1 - executing a home instruction
        10 - executing a manual move in Velocity Mode (i.e. the manual control knob is turned)
        11 - executing a manual move in Displacement Mode (i.e. the manual control knob is turned)
        13 - device has stalled and stopped or been displaced while stationary (FW 6.07 and up only)
        18 - executing a move to stored position instruction
        20 - executing a move absolute instruction
        21 - executing a move relative instruction
        22 - executing a move at constant speed instruction
        23 - executing a stop instruction (i.e. decelerating)
        65 - device is parked (FW 6.02 and up only. FW 6.01 returns 0 when parked)
        78 - executing a move index instruction
        """
        self.send_message(self._cmd_return_status)
        cmd_num, msg = self.receive_message()
        return struct.unpack("l", msg)
