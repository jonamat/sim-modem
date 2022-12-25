import serial
import time


class SerialComm:
    def __init__(
        self,
        address,
        baudrate=460800,
        timeout=5,
        at_cmd_delay=0.1,
        on_error=None,
        byte_encoding="ISO-8859-1",
    ):
        self.at_cmd_delay = at_cmd_delay
        self.on_error = on_error
        self.byte_encoding = byte_encoding
        self.modem_serial = serial.Serial(
            port=address,
            baudrate=baudrate,
            timeout=timeout,
        )

    def send(self, cmd) -> str or None:
        self.modem_serial.write(cmd.encode(self.byte_encoding) + b"\r")
        time.sleep(self.at_cmd_delay)

    def send_raw(self, cmd):
        self.modem_serial.write(cmd)
        time.sleep(self.at_cmd_delay)

    def read_lines(self) -> list:
        read = self.modem_serial.readlines()
        for i, line in enumerate(read):
            read[i] = line.decode(self.byte_encoding).strip()
        return read

    def read_raw(self, size: int):
        return self.modem_serial.read(size)

    def close(self):
        self.modem_serial.close()
