"""
*Zaber stage communication protocol*:

All Binary messages consist of six bytes. They must be transmitted with less
than 10 milliseconds between each byte. If the device has received less than
six bytes and a period longer than 10 milliseconds passes, it will assume the
remaining data has been lost and will discard the previously received bytes.
We recommend that customer software behave similarly when receiving data from
devices, especially in electrically noisy environments.

The six bytes are ordered as follows:

    1. Device number
    2. Command number
    3. Data, least significant byte (LSB)
    4. Data
    5. Data
    6. Data, most significant byte (MSB)

The first byte is the device number in the daisy-chain. Generally, device
number 1 is the closest device to the computer, device 2 is next, and so on
(see Renumber (Cmd 2) to sequentially number devices in the chain). If the
number 0 is used, the command will be directed to all devices in the chain.
Each axis of a multi-axis device appears as a separate device with its own
device number.

The second byte is the command number. Bytes 3, 4, 5, and 6 can be combined to
form a signed 32-bit data value, with the least significant byte transmitted
first (see Appendix B: Message Data Conversion Algorithm for more details).
Each command interprets the data value differently.

There are four types of commands:

Action commands: Commands that cause the device to perform an action
(e.g., move). See Action Command Reference for a list of all action commands.

Set commands: Commands that set the value of a setting. See Set Command
Reference for a list of all set commands.

Return commands: Commands that return a setting’s value. See Return Command
Reference for a list of all return commands.

Reply-Only commands: Messages that are only ever sent from the device to the
user. Most are spontaneously sent by the device and are not in response to a
user command. See Reply-Only Command Reference for a list of all reply-only
commands.

Most commands elicit a reply message in the same six-byte format, with a few
minor differences. The first byte in the reply is the number of the device
that just finished executing the command, not the device number the original
message was sent to. For instance, a message addressed to 0 (i.e., all
devices) will elicit a reply from each device in the daisy-chain. The second
byte is either the number of the command that the device just executed or 255
(0xFF) if an error occurs (see Error (Cmd 255) for more information on
errors).

If desired, byte 6 can be repurposed as a message ID (in place of a byte of
data). See Message ID Mode for more information.
"""

import serial
import struct


class Stage:
    def __init__(self, port):
        self.ser = serial.Serial(port=port)

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
        return command_number, msg_received

    def home(self):
        self.send_message(1)

    def get_position(self):
        self.send_message(60)
        cmd_num, msg = self.receive_message()
        return struct.unpack("l", msg)

    def get_device_id(self):
        self.send_message(50)
        cmd_num, msg = self.receive_message()
        return struct.unpack("l", msg)
