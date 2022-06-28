import serial
from interface import Interface

DEFAULT_PORT = '/dev/tty.usbserial-10'

DEFAULT_BAUD_RATE = 9_600

DEFAULT_TIMEOUT = 0.5


class Control(Interface):
    """Control syringe pump(s) via serial communication (basic mode)."""

    def __init__(self, port=DEFAULT_PORT, baud_rate=DEFAULT_BAUD_RATE, timeout=DEFAULT_TIMEOUT):
        """Constructor.

            args : 
                port
                baud_rate
                timeout

        """
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout

    def tx_cmd(self, adr : str, cmd : str):
        """Transmit the command over the serial bus"""
        msg = adr + cmd + '\r'
        tx_msg = msg.encode()
        with serial.Serial(
            port=self.port, 
            baudrate=self.baud_rate, 
            bytesize=serial.EIGHTBITS, 
            parity=serial.PARITY_NONE, 
            timeout=self.timeout
            ) as ser:
            ser.write(tx_msg)
            rx_msg = ser.readline().decode()
        return rx_msg

    def rx_cmd(self):
        """Receive the command over the serial bus"""
        with serial.Serial(
            port=self.port, 
            baudrate=self.baud_rate, 
            bytesize=serial.EIGHTBITS, 
            parity=serial.PARITY_NONE, 
            timeout=self.timeout
            ) as ser:
            rx_msg = ser.readline().decode()
        return rx_msg


if __name__=='__main__':
    pass