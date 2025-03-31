# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 10:06:34 2019

The communications protocol used in the Thorlabs controllers is based on the
message structure that always starts with a fixed length, 6-byte message header
which, in some cases, is followed by a variable length data packet. The header
part of the message always contains information that indicates whether or not a
data packet follows the header and if so, the number of bytes that the data
packet contains.

The 6 bytes in the message header are shown below:

                    Byte:   byte 0  byte 1  byte 2  byte 3  byte 4  byte 5
no data packet to follow    message ID      param1  param2  dest    source
data packet to follow       message ID      data length     dest    source

The meaning of some of the fields depends on whether or not the message is
followed by a data packet. This is indicated by the most significant bit in
byte 4, called the destination byte, therefore the receiving process must first
check if the MSB of byte 4 is set. If this bit is not set, then the message is
a header-only message and the interpretation of the bytes is as follows:
message ID: describes what the action the message requests
param1: first parameter (if the command requires a parameter, otherwise 0)
param2: second parameter (if the command requires a parameter, otherwise 0)
dest: the destination module
source: the source of the message

In all messages, where a parameter is longer than a single character, the bytes
are encoded in the Intel format, least significant byte first.

In non-card-slot type of systems the source and destination of messages is
always unambiguous, as each module appears as a separate USB node in the
system. In these systems, when the host sends a message to the module, it uses
the source identification byte of 0x01 (meaning host) and the destination byte
of 0x50 (meaning “generic USB unit”). In messages that the module sends back to
the host, the content of the source and destination bytes is swapped.

In card-slot (bay) type of systems, there is only one USB node for a number of
sub-modules, so this simple scheme cannot be used. Instead, the host sends a
message to the motherboard that the sub-modules are plugged into, with the
destination field of each message indicating which slot the message must be
routed to. Likewise, when the host receives a message from a particular
sub-module, it knows from the source byte which slot is the origin of the
message.

0x01    Host controller (i.e control PC)
0x11    Rack controller, motherboard in a card slot system or comms router board
0x21    Bay 0 in a card slot system
0x22    Bay 1 in a card slot system
0x23    etc.
0x24    etc.
0x25    etc.
0x26    etc.
...
0x2A    Bay 9 in a card slot system
0x50    Generic USB hardware unit

"""

import serial
import time
from functools import wraps
import struct


def _auto_connect(func):
    """A function decorator that handles automatic connections.

    If "auto connect" is enabled the communications port is enabled before the
    function execution and disabled afterwards. If the internal "connected"
    flag is true, the connection/disconnection procedure is ignored and the
    function executes as normal.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """Wrapped function"""
        if self.auto_connect and not self.connected:
            try:
                self.open_port()
                result = func(self, *args, **kwargs)
                return result
            finally:
                self.close_port()
        else:
            result = func(self, *args, **kwargs)
            return result

    return wrapper


class APTDevice:
    def __init__(
        self, port, timeout=1.0, serial_number=None, source=0x01, destination=0x50
    ):
        assert isinstance(port, str)

        self.auto_connect = True
        self.connected = False

        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = 115200
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = timeout

        self.src = source  # 0x01 = host controller
        self.dst = destination  # 0x50 = generic usb device

        if serial_number is not None:
            assert serial_number == self.hardware_info()["serial"]

        self.send_update_messages(update=False)

    def open_port(self):
        """Opens the serial port for read/write access"""
        if not self.ser.is_open:
            self.ser.open()
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            self.connected = True

    def close_port(self):
        """Closes the serial port from read/write access"""
        if self.ser.is_open:
            self.ser.close()
            self.connected = False

    def read(self, msg_id_0, msg_id_1, req_buffer=None):
        """Read and discard messages until the requested message ID is found.
        Returns the full buffer of the message or an error if the message is
        not found
        """
        msg_found = False
        while not msg_found:
            read_buffer = self.ser.read(6)
            if len(read_buffer) == 6:
                header = struct.unpack("<BBBBBB", read_buffer)
                # Check for data packet
                if bool(header[4] & 0x80):
                    packet_length = struct.unpack("<H", read_buffer[2 : 3 + 1])[0]
                    data_buffer = self.ser.read(packet_length)
                    read_buffer = read_buffer + data_buffer
                # Check msg_id
                # print("Message ID {:X},{:X} found.".format(header[0], header[1]))
                if msg_id_0 == header[0] and msg_id_1 == header[1]:
                    msg_found = True
                    return read_buffer
                else:
                    print(
                        "Message not found, trying again. {:X},{:X}".format(
                            header[0], header[1]
                        )
                    )
            elif req_buffer is not None:
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()
                self.write(req_buffer)
                print("Message not found, trying again.")
                time.sleep(0.1)
            else:
                raise ValueError(
                    "Message {:X},{:X} not found".format(msg_id_0, msg_id_1)
                )

    def write(self, buffer):
        """Writes buffer to serial port"""
        self.ser.write(buffer)

    @_auto_connect
    def identify(self):
        """Causes the cube's LED screen to blink"""
        # MGMSG_MOD_IDENTIFY
        buffer = struct.pack("<BBBBBB", 0x23, 0x02, 0x00, 0x00, self.dst, self.src)
        self.write(buffer)

    @_auto_connect
    def enable(self, enable=None, channel=1):
        """Enable or disable the selected channel"""
        channel = {1: 0x01, 2: 0x02, 3: 0x04, 4: 0x08}[channel]
        if enable is None:
            # Check if the channel is enabled
            # MGMSG_MOD_REQ_CHANENABLESTATE
            write_buffer = struct.pack(
                "<BBBBBB", 0x11, 0x02, channel, 0x00, self.dst, self.src
            )
            self.write(write_buffer)
            # MGMSG_MOD_GET_CHANENABLESTATE
            read_buffer = self.read(0x12, 0x02, req_buffer=write_buffer)
            result = struct.unpack("<BBBBBB", read_buffer)
            enable_state = {0x01: True, 0x02: False}[result[3]]
            return enable_state
        else:
            enable_state = {True: 0x01, False: 0x02}[bool(enable)]
            # MGMSG_MOD_SET_CHANENABLESTATE
            write_buffer = struct.pack(
                "<BBBBBB", 0x10, 0x02, channel, enable_state, self.dst, self.src
            )
            self.write(write_buffer)

    @_auto_connect
    def hardware_info(self):
        """Reports the hardware info of the connected cube"""
        # MGMSG_HW_REQ_INFO
        write_buffer = struct.pack(
            "<BBBBBB", 0x05, 0x00, 0x00, 0x00, self.dst, self.src
        )
        self.write(write_buffer)
        # MGMSG_HW_GET_INFO
        read_buffer = self.read(0x06, 0x00, req_buffer=write_buffer)
        result = struct.unpack("<BBBBBBL8sH4b60sHHH", read_buffer)
        return {
            "serial": result[6],
            "model": result[7].decode("ascii").strip("\x00"),
            "type": result[8],
            "firmware": "{:}.{:}.{:}.{:}".format(*result[9 : 12 + 1]),
            "hardware": result[14],
            "modification": result[15],
            "channels": result[16],
        }

    @_auto_connect
    def send_update_messages(self, update=False, rate=0):
        """Enable or disable a constant stream of status update messages"""
        if update is False:
            # MGMSG_HW_STOP_UPDATEMSGS
            write_buffer = struct.pack(
                "<BBBBBB", 0x12, 0x00, 0x00, 0x00, self.dst, self.src
            )
            self.write(write_buffer)
        else:
            # MGMSG_HW_START_UPDATEMSGS
            write_buffer = struct.pack(
                "<BBBBBB", 0x11, 0x00, rate, 0x00, self.dst, self.src
            )
            self.write(write_buffer)


class KST201(APTDevice):
    # Conversion Factors
    ENC_CNT_MM = 24 * 2048 * 400 / 9  # encoder counts per degree
    VEL_SCL_FCT = 107824097.5  # encoder counts per (degrees per second)
    ACC_SCL_FCT = 22097.3  # encoder counts per (degrees per second**2)

    def __init__(self, port, timeout=1, serial_number=None):
        super().__init__(port, timeout=timeout, serial_number=serial_number)

        # Suspend "End of Move Messages"
        self.suspend_EoM_msgs(False)

    @_auto_connect
    def suspend_EoM_msgs(self, suspend):
        """Sent to disable or resume all unsolicited end of move messages and
        error messages returned by the controller:
            MGMSG_MOT_MOVE_STOPPED
            MGMSG_MOT_MOVE_COMPLETED
            MGMSG_MOT_MOVE_HOMED

        The command also disables the error messages that the controller sends
        when an error conditions is detected:
            MGMSG_HW_RESPONSE
            MGMSG_HW_RICHRESPONSE

        The messages are enabled by default when the controller is powered up.
        """
        suspend = bool(suspend)
        if suspend:
            # MGMSG_MOT_SUSPEND_ENDOFMOVEMSGS
            write_buffer = struct.pack(
                "<BBBBBB", 0x6B, 0x04, 0x00, 0x00, self.dst, self.src
            )
            self.write(write_buffer)
        else:
            # MGMSG_MOT_RESUME_ENDOFMOVEMSGS
            write_buffer = struct.pack(
                "<BBBBBB", 0x6C, 0x04, 0x00, 0x00, self.dst, self.src
            )
            self.write(write_buffer)

    @_auto_connect
    def status(self):
        # MGMSG_MOT_REQ_USTATUSUPDATE
        write_buffer = struct.pack(
            "<BBBBBB", 0x90, 0x04, 0x01, 0x00, self.dst, self.src
        )
        self.write(write_buffer)
        # MGMSG_MOT_GET_STATUSUPDATE
        read_buffer = self.read(0x81, 0x04, req_buffer=write_buffer)

        # MGMSG_MOT_ACK_DCSTATUSUPDATE
        # needed to keep the stage responding or else it will stop responding
        # after ~50 status update requests are received
        ack_buffer = struct.pack("<BBBBBB", 0x92, 0x04, 0x00, 0x00, self.dst, self.src)
        self.write(ack_buffer)

        # Unpack Read Buffer
        result = struct.unpack("<BBBBBBHlHHL", read_buffer)
        position = result[7]
        velocity = result[8]
        status_bits = {
            "forward hardware limit": bool(result[10] & 0x00000001),
            "reverse hardware limit": bool(result[10] & 0x00000002),
            "moving forward": bool(result[10] & 0x00000010),
            "moving reverse": bool(result[10] & 0x00000020),
            "jogging forward": bool(result[10] & 0x00000040),
            "jogging reverse": bool(result[10] & 0x00000080),
            "homing": bool(result[10] & 0x00000200),
            "homed": bool(result[10] & 0x00000400),
            "tracking": bool(result[10] & 0x00001000),
            "settled": bool(result[10] & 0x00002000),
            "motion error": bool(result[10] & 0x00004000),
            "motor current limit": bool(result[10] & 0x01000000),
            "channel enabled": bool(result[10] & 0x80000000),
        }
        return {"position": position, "velocity": velocity, "flags": status_bits}

    @_auto_connect
    def home(self, home=None):
        if home is None:
            # Check if the device has been homed
            status_bits = self.status()["flags"]
            return {"homed": status_bits["homed"], "homing": status_bits["homing"]}
        elif home is True:
            # MGMSG_MOT_MOVE_HOME
            write_buffer = struct.pack(
                "<BBBBBB", 0x43, 0x04, 0x01, 0x00, self.dst, self.src
            )
            self.write(write_buffer)

    @_auto_connect
    def return_current_position(self):
        # Get the current position
        # MGMSG_MOT_REQ_POSCOUNTER 0x0411
        write_buffer = struct.pack(
            "<BBBBBB", 0x11, 0x04, 0x01, 0x00, self.dst, self.src
        )
        self.write(write_buffer)
        # MGMSG_MOT_GET_POSCOUNTER 0x0412
        read_buffer = self.read(0x12, 0x04, req_buffer=write_buffer)
        result = struct.unpack("<BBBBBBHl", read_buffer)
        position = result[7]
        return position

    @_auto_connect
    def move_absolute(self, pos):
        # Calculate the encoder value
        # MGMSG_MOT_MOVE_ABSOLUTE
        write_buffer = struct.pack(
            "<BBBBBBHl",
            0x53,
            0x04,
            0x06,
            0x00,
            self.dst | 0x80,
            self.src,
            0x0001,
            pos,
        )
        self.write(write_buffer)

    @_auto_connect
    def move_relative(self, step):
        # MGMSG_MOT_MOVE_RELATIVE
        write_buffer = struct.pack(
            "<BBBBBBHl",
            0x48,
            0x04,
            0x06,
            0x00,
            self.dst | 0x80,
            self.src,
            0x0001,
            step,
        )
        self.write(write_buffer)

    @_auto_connect
    def stop(self):
        write_buffer = struct.pack("<6B", 0x65, 0x04, 0x01, 0x02, self.dst, self.src)
        self.write(write_buffer)

    @property
    def is_in_motion(self):
        status = self.status()["flags"]
        return not status["settled"]
