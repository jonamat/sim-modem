from serial_comm import SerialComm
from enum import Enum
from logging import getLogger

logger = getLogger(__name__)


class NetworkMode(Enum):
    """Network mode of the modem (get/set)"""

    AUTOMATIC = 2
    GSM_ONLY = 13
    LTE_ONLY = 38
    ANY_BUT_LTE = 48


class SignalQuality(Enum):
    """Signal quality expressed as ranges"""

    LOW = "LOW"
    FAIR = "FAIR"
    GOOD = "GOOD"
    EXCELLENT = "EXCELLENT"


class Modem:
    """Class for interfacing with mobile modem"""

    def __init__(
        self,
        address,
        baudrate=460800,
        timeout=5,
        at_cmd_delay=0.1,
        debug=False,
    ):
        self.comm = SerialComm(
            address=address,
            baudrate=baudrate,
            timeout=timeout,
            at_cmd_delay=at_cmd_delay,
        )
        self.debug = debug

        self.comm.send("ATZ")
        self.comm.send("ATE1")
        read = self.comm.read_lines()
        # ['ATZ', 'OK', 'ATE1', 'OK']
        if read[-1] != "OK":
            raise Exception("Modem do not respond", read)

        if self.debug:
            logger.debug("Modem connected, debug mode enabled")

    def reconnect(self) -> None:
        try:
            self.comm.close()
        except:
            pass

        self.comm = SerialComm(
            address=self.comm.address,
            baudrate=self.comm.baudrate,
            timeout=self.comm.timeout,
            at_cmd_delay=self.comm.at_cmd_delay,
        )

        self.comm.send("ATZ")
        self.comm.send("ATE1")
        read = self.comm.read_lines()
        # ['ATZ', 'OK', 'ATE1', 'OK']
        if read[-1] != "OK":
            raise Exception("Connection lost", read)

        if self.debug:
            logger.debug("Modem connected, debug mode enabled")

    def close(self) -> None:
        self.comm.close()

    # --------------------------------- HARDWARE --------------------------------- #

    def get_manufacturer_identification(self) -> str:
        if self.debug:
            self.comm.send("AT+CGMI=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CGMI")

        self.comm.send("AT+CGMI")
        read = self.comm.read_lines()

        if self.debug:
            logger.debug("Device responded: ", read)
        # ['AT+CGMI', 'SIMCOM INCORPORATED', '', 'OK']

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1]

    def get_model_identification(self) -> str:
        if self.debug:
            self.comm.send("AT+CGMM=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CGMM")

        self.comm.send("AT+CGMM")
        read = self.comm.read_lines()

        # ['AT+CGMM', 'SIM7000E', '', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1]

    def get_serial_number(self) -> str:
        if self.debug:
            self.comm.send("AT+CGSN=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CGSN")

        self.comm.send("AT+CGSN")
        read = self.comm.read_lines()

        # ['AT+CGSN', '89014103211118510700', '', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1]

    def get_firmware_version(self) -> str:
        if self.debug:
            self.comm.send("AT+CGMR=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CGMR")

        self.comm.send("AT+CGMR")
        read = self.comm.read_lines()

        # ['AT+CGMR', '+CGMR: LE20B03SIM7600M22', '', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1].split(": ")[1]

    def get_volume(self) -> str:
        if self.debug:
            self.comm.send("AT+CLVL=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CLVL")

        self.comm.send("AT+CLVL?")
        read = self.comm.read_lines()

        # ['AT+CLVL?', '+CLVL: 5', '', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1].split(": ")[1]

    def set_volume(self, volume: int) -> str:
        if self.debug:
            self.comm.send("AT+CLVL=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CLVL={}".format(volume))

        if volume < 0 or volume > 5:
            raise Exception("Volume must be between 0 and 5")
        self.comm.send("AT+CLVL={}".format(volume))
        read = self.comm.read_lines()

        # ['AT+CLVL=5', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1]

    def improve_tdd(self) -> str:
        if self.debug:
            self.comm.send("AT+AT+PWRCTL=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+AT+PWRCTL=0,1,3")

        # ['AT+AT+PWRCTL=?', '+PWRCTL: (0-1),(0-1),(0-3)', '', 'OK']
        self.comm.send("AT+PWRCTL=0,1,3")
        read = self.comm.read_lines()

        # ['AT+PWRCTL=0,1,3', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1]

    # def reset_module(self) -> str:
    #     self.comm.send("AT+CRESET")
    #     read = self.comm.read_lines()
    #     # ['AT+CRESET', 'OK']
    #     if read[-1] != "OK":
    #         raise Exception("Command failed")
    #     logger.debug("Connection lost")
    #     exit()

    def enable_echo_suppression(self) -> str:
        if self.debug:
            self.comm.send("AT+CECM=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CECM=1")

        self.comm.send("AT+CECM=1")
        read = self.comm.read_lines()

        # ['AT+CECM=1', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1]

    def disable_echo_suppression(self) -> str:
        if self.debug:
            self.comm.send("AT+CECM=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CECM=0")

        self.comm.send("AT+CECM=0")
        read = self.comm.read_lines()

        # ['AT+CECM=0', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1]

    # ---------------------------------- NETWORK --------------------------------- #

    def get_network_registration_status(self) -> str:
        if self.debug:
            self.comm.send("AT+CREG=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CREG?")

        self.comm.send("AT+CREG?")
        read = self.comm.read_lines()

        # ['AT+CREG?', '+CREG: 0,1', '', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1].split(": ")[1]

    def get_network_mode(self) -> NetworkMode:
        if self.debug:
            self.comm.send("AT+CNMP=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CNMP?")

        self.comm.send("AT+CNMP?")
        read = self.comm.read_lines()

        # ['AT+CNMP?', '+CNMP: 2', '', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        nm = read[1].split(": ")[1]

        return NetworkMode(int(nm))

    def get_network_name(self) -> str:
        if self.debug:
            self.comm.send("AT+COPS=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+COPS?")

        self.comm.send("AT+COPS?")
        read = self.comm.read_lines()

        # ['AT+COPS?', '+COPS: 0,0,"Vodafone D2",7', '', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1].split(",")[2].strip('"')

    def get_network_operator(self) -> str:
        if self.debug:
            self.comm.send("AT+COPS=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+COPS?")

        self.comm.send("AT+COPS?")
        read = self.comm.read_lines()

        # ['AT+COPS?', '+COPS: 0,0,"Vodafone D2",7', '', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1].split(",")[2].strip('"').split(" ")[0]

    def get_signal_quality(self) -> str:
        if self.debug:
            self.comm.send("AT+CSQ=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CSQ")

        self.comm.send("AT+CSQ")
        read = self.comm.read_lines()

        # ['AT+CSQ', '+CSQ: 19,99', '', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1].split(": ")[1]

    def get_signal_quality_db(self) -> int:
        if self.debug:
            self.comm.send("AT+CSQ=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CSQ")

        self.comm.send("AT+CSQ")
        read = self.comm.read_lines()

        # ['AT+CSQ', '+CSQ: 19,99', '', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        raw = read[1].split(": ")[1].split(",")[0]
        return -(111 - (2 * int(raw)))

    def get_signal_quality_range(self) -> SignalQuality:
        if self.debug:
            self.comm.send("AT+CSQ=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CSQ")

        self.comm.send("AT+CSQ")
        read = self.comm.read_lines()

        # ['AT+CSQ', '+CSQ: 19,99', '', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        raw = read[1].split(": ")[1].split(",")[0]
        if int(raw) < 7:
            return SignalQuality.LOW
        elif int(raw) < 15:
            return SignalQuality.FAIR
        elif int(raw) < 20:
            return SignalQuality.GOOD
        else:
            return SignalQuality.EXCELLENT

    def get_phone_number(self) -> str:
        if self.debug:
            self.comm.send("AT+CNUM=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CNUM")

        self.comm.send("AT+CNUM")
        read = self.comm.read_lines()

        # ['AT+CNUM', '+CNUM: ,"+491234567890",145', '', 'OK']
        # ['AT+CNUM', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK" or read[1] == "OK":
            raise Exception("Command failed")
        return read[1].split(",")[1].strip('"')

    def get_sim_status(self) -> str:
        if self.debug:
            self.comm.send("AT+CPIN=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CPIN?")

        self.comm.send("AT+CPIN?")
        read = self.comm.read_lines()

        # ['AT+CPIN?', '+CPIN: READY', '', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        return read[1].split(": ")[1]

    def set_network_mode(self, mode: NetworkMode) -> str:
        self.comm.send("AT+CNMP={}".format(mode.value))
        read = self.comm.read_lines()
        # ['AT+CNMP=2', 'OK']
        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1]

    # ------------------------------------ GPS ----------------------------------- #

    def get_gps_status(self) -> str:
        if self.debug:
            self.comm.send("AT+CGPS=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CGPS?")

        self.comm.send("AT+CGPS?")
        read = self.comm.read_lines()

        # ['AT+CGPS?', '+CGPS: 0,1', '', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1].split(": ")[1]

    def start_gps(self) -> str:
        if self.debug:
            self.comm.send("AT+CGPS=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CGPS=1,1")

        self.comm.send("AT+CGPS=1,1")
        read = self.comm.read_lines()

        # ['AT+CGPS=1', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1]

    def stop_gps(self) -> str:
        if self.debug:
            self.comm.send("AT+CGPS=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CGPS=0")

        self.comm.send("AT+CGPS=0")
        read = self.comm.read_lines()

        # ['AT+CGPS=0', 'OK', '', '+CGPS: 0']
        # ['AT+CGPS=0', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] == "+CGPS: 0" or read[-1] == "OK":
            raise Exception("Command failed")
        return read[1]

    def get_gps_coordinates(self) -> dict:
        if self.debug:
            self.comm.send("AT+CGPS=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CGPS=1,1")
            logger.debug("Sending: AT+CGPSINFO")

        self.comm.send("AT+CGPS=1,1")
        self.comm.send("AT+CGPSINFO")
        # self.comm.send("AT+CGPS=0")
        read = self.comm.read_lines()

        # +CGPSINFO: [lat],[N/S],[log],[E/W],[date],[UTC time],[alt],[speed],[course]
        # ['AT+CGPS=1', 'OK', 'AT+CGPSINFO', '+CGPSINFO: 1831.991044,N,07352.807453,E,141008,112307.0,553.9,0.0,113', 'OK']
        # ['AT+CGPS=1', 'OK', 'AT+CGPSINFO', '+CGPSINFO: ,,,,,,,,', '', 'OK'] # if no gps signal
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return {
            "latitude": read[3].split(": ")[1].split(",")[0]
            + read[3].split(": ")[1].split(",")[1],
            "longitude": read[3].split(": ")[1].split(",")[2]
            + read[3].split(": ")[1].split(",")[3],
            "altitude": read[3].split(": ")[1].split(",")[6],
            "speed": read[3].split(": ")[1].split(",")[7],
            "course": read[3].split(": ")[1].split(",")[8],
        }

    # ------------------------------------ SMS ----------------------------------- #

    def get_sms_list(self) -> list:
        if self.debug:
            self.comm.send("AT+CMGF=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CMGF=1")
            logger.debug('Sending: AT+CMGL="ALL"')

        self.comm.send("AT+CMGF=1")
        self.comm.send('AT+CMGL="ALL"')

        read = self.comm.read_lines()
        sms_lines = [x for x in read if x != ""]  # remove empty lines
        sms_lines = sms_lines[5 : len(sms_lines) - 1]  # remove command and OK
        tuple_list = [
            tuple(sms_lines[i : i + 2]) for i in range(0, len(sms_lines), 2)
        ]  # group sms info with message

        sms_list = []
        for i in tuple_list:
            sms_list.append(
                {
                    "index": i[0].split(":")[1].split(",")[0].strip(),
                    "number": i[0].split('READ","')[1].split('","","')[0],
                    "date": i[0].split('","","')[1].split(",")[0],
                    "time": i[0].split(",")[5].split("+")[0],
                    "message": i[1].replace("\r\n", "").strip(),
                }
            )

        # ['AT+CMGL="ALL"', '+CMGL: 1,"REC READ","+491234567890",,"12/08/14,14:01:06+32"', 'Test', '', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return sms_list

    def empty_sms(self) -> str:
        if self.debug:
            self.comm.send("AT+CMGF=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CMGF=1")
            logger.debug("Sending: AT+CMGD=1,4")

        self.comm.send("AT+CMGF=1")
        self.comm.send("AT+CMGD=1,4")
        read = self.comm.read_lines()

        # ['AT+CMGF=1', 'OK', 'AT+CMGD=1,4', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")

    def send_sms(self, recipient, message) -> str:
        if self.debug:
            self.comm.send("AT+CMGF=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CMGF=1")
            logger.debug('Sending: AT+CMGS="{}"'.format(recipient))
            logger.debug("Sending: {}".format(message))
            logger.debug("Sending: {}".format(chr(26)))

        self.comm.send("AT+CMGF=1")
        self.comm.send('AT+CMGS="{}"'.format(recipient))
        self.comm.send(message)
        self.comm.send(chr(26))
        read = self.comm.read_lines()

        # ['AT+CMGF=1', 'OK', 'AT+CMGS="491234567890"', '', '> Test', chr(26), 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[4]

    def get_sms(self, slot) -> dict:
        if self.debug:
            self.comm.send("AT+CMGF=?")
            self.comm.send("AT+CMGR=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CMGF=1")
            logger.debug("Sending: AT+CMGR={}".format(slot))

        self.comm.send("AT+CMGF=1")
        self.comm.send("AT+CMGR={}".format(slot))
        read = self.comm.read_lines()

        # ['AT+CMGF=1', 'OK', 'AT+CMGR=1', '+CMGR: "REC READ","+491234567890",,"12/08/14,14:01:06+32"', 'Test', '', 'OK']
        # ['AT+CMGF=1', 'OK'] # if empty
        if self.debug:
            logger.debug("Device responded: ", read)

        if len(read) < 3 or read[-1] != "OK":
            raise Exception("Command failed")
        return {
            "slot": read[1].split(":")[1].split(",")[0].strip(),
            "number": read[1].split('READ","')[1].split('","","')[0],
            "date": read[1].split('","","')[1].split(",")[0],
            "time": read[1].split(",")[5].split("+")[0],
            "message": read[4].replace("\r\n", "").strip(),
        }

    def delete_sms(self, slot: int) -> str:
        if self.debug:
            self.comm.send("AT+CMGF=?")
            read = self.comm.read_lines()
            if read[-1] != "OK":
                raise Exception("Unsupported command")
            logger.debug("Sending: AT+CMGF=1")
            logger.debug("Sending: AT+CMGD={}".format(slot))

        self.comm.send("AT+CMGF=1")
        self.comm.send("AT+CMGD={}".format(slot))
        read = self.comm.read_lines()

        # ['AT+CMGF=1', 'OK', 'AT+CMGD=1', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1]

    # ----------------------------------- CALLS ---------------------------------- #

    def call(self, number: str) -> str:
        if self.debug:
            logger.debug("Sending: ATD{};".format(number))

        self.comm.send("ATD{};".format(number))
        read = self.comm.read_lines()

        # ['ATD491234567890;', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1]

    def answer(self) -> str:
        if self.debug:
            logger.debug("Sending: ATA")

        self.comm.send("ATA")
        read = self.comm.read_lines()

        # ['ATA', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1]

    def hangup(self) -> str:
        if self.debug:
            logger.debug("Sending: AT+CHUP")

        self.comm.send("AT+CHUP")
        read = self.comm.read_lines()

        # ['AT+CHUP', 'OK']
        if self.debug:
            logger.debug("Device responded: ", read)

        if read[-1] != "OK":
            raise Exception("Command failed")
        return read[1]
