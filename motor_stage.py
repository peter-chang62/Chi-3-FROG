import serial
import struct


class Stage:
    def __init__(self, port):
        # serial port with 1 minute timeout
        self.ser = serial.Serial(port=port, timeout=60)

        self._max_pos = 1066667
        self._max_range = 50.8

        self._cmd_home = 1
        self._cmd_move_absolute = 20
        self._cmd_move_relative = 21
        self._cmd_move_at_constant_speed = 22
        self._cmd_stop = 23
        self._cmd_return_current_position = 60

    @property
    def device(self):
        # assume only one zaber stage is connected (no daisy chain)
        return 1

    def send_message(self, command_number, data=None):
        if data is None:
            msg = struct.pack("<6B", self.device, command_number, 0, 0, 0, 0)
        else:
            msg = struct.pack("<2Bl", self.device, command_number, data)

        self.ser.write(msg)

    def receive_message(self):
        msg = self.ser.read(6)
        command_number = msg[1]
        msg_received = msg[2:]

        assert command_number != 255, "error occured"
        return command_number, msg_received

    def home(self):
        self.send_message(self._cmd_home)

    def move_absolute(self, pos):
        self.send_message(self._cmd_move_absolute, pos)

    def move_relative(self, step):
        self.send_message(self._cmd_move_relative, step)

    def move_at_constant_speed(self, vel):
        self.send_message(self._cmd_move_at_constant_speed, vel)

    def stop(self):
        self.send_message(self._cmd_stop)

    def return_current_position(self):
        self.send_message(self._cmd_return_current_position)
        cmd_num, msg = self.receive_message()
        return struct.unpack("l", msg)

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
        self.send_message(54)
        msg = self.ser.read(6)
        return struct.unpack("2Bl", msg)
