# sim-modem

Easy library for interfacing with mobile modems. Tested with Simcom SIM7600G-H on Raspberry PI Zero W. The commands could be different for other modems.

## Installation

```bash
pip install sim-modem
```

## Usage
    
```python
from sim_modem import Modem

modem = Modem('/dev/ttyUSB2')

signal_quality = modem.get_signal_quality()
print(signal_quality)

modem.send_sms('+393383928434', 'Hello World!')

```


## API

### Modem (Class)

Main class for interfacing with the modem. Each method raise an exception if the modem returns an error. If the command is successful, the function returns the response from the modem.


```python
Modem(        
    address, # Address of the device tty (e.g. "/dev/ttyUSB2")
    baudrate=460800, # Baudrate of the device. Default: 460800
    timeout=5, # Timeout for the serial connection. Default: 5
    at_cmd_delay=0.1, # Delay between AT commands. Default: 0.1
    debug=False # Log commands and responses from modem, test command support before executing them. Default: False
)
```


| Method                                        | Description                                                             |
| --------------------------------------------- | ----------------------------------------------------------------------- |
| `reconnect() -> str`                          | Reconnect to serial                                                     |
| `close() -> str`                              | Close the serial connection                                             |
| *Hardware related methods*                    |                                                                         |
| `get_model_identification() -> str`           | Get the model identification                                            |
| `get_manufacturer_identification() -> str`    | Get the manufacturer identification                                     |
| `get_serial_number() -> str`                  | Get the serial number                                                   |
| `get_firmware_version() -> str`               | Get the firmware version                                                |
| `get_volume() -> str`                         | Get the volume. The volume range is between 0 and 5                     |
| `set_volume(index: int) # 0-5`                | Set the volume. The volume range must be between 0 and 5                |
| `improve_tdd() -> str`                        | Decrease TDD Noise effect                                               |
| `enable_echo_suppression() -> str`            | Enable echo suppression                                                 |
| `disable_echo_suppression() -> str`           | Disable echo suppression                                                |
| *Network related methods*                     |                                                                         |
| `get_network_registration_status() -> str`    | Get the network registration status                                     |
| `get_network_mode() -> NetworkMode`           | Get the network mode                                                    |
| `get_network_name() -> str`                   | Get the network name                                                    |
| `get_network_operator() -> str`               | Get the network operator                                                |
| `get_signal_quality() -> str`                 | Get the signal quality                                                  |
| `get_signal_quality_db() -> int`              | Get the signal quality in dB                                            |
| `get_signal_quality_range() -> SignalQuality` | Get the signal quality as a range (see [SignalQuality](#SignalQuality)) |
| `get_phone_number() -> str`                   | Get the phone number                                                    |
| `get_sim_status() -> str`                     | Get the SIM status                                                      |
| `set_network_mode(mode: NetworkMode) -> str`  | Set the network mode                                                    |
| *Calls related methods*                       |                                                                         |
| `call(number: str) -> str`                    | Call a number                                                           |
| `answer() -> str`                             | Answer a call                                                           |
| `hangup() -> str`                             | Hangup a call                                                           |
| *SMS related methods*                         |                                                                         |
| `get_sms_list() -> list`                      | Get the list of SMS                                                     |
| `empty_sms() -> str`                          | Empty the SMS storage                                                   |
| `send_sms(number: str, message: str) -> str`  | Send an SMS                                                             |
| `get_sms(index: int) -> dict`                 | Get an SMS by ID                                                        |
| `delete_sms(index: int) -> str`               | Delete an SMS by ID                                                     |
| *GPS related methods*                         |                                                                         |
| `get_gps_status() -> str`                     | Get the GPS status                                                      |
| `start_gps() -> str`                          | Start the GPS                                                           |
| `stop_gps() -> str`                           | Stop the GPS                                                            |
| `get_gps_coordinates() -> dict`               | Get the GPS coordinates                                                 |


### SignalQuality (enum)

Signal quality expressed as ranges 

| Key                       | Description                 |
| ------------------------- | --------------------------- |
| `SignalQuality.LOW`       | Signal is under 7           |
| `SignalQuality.FAIR`      | Signal is between 7 and 15  |
| `SignalQuality.GOOD`      | Signal is between 15 and 20 |
| `SignalQuality.EXCELLENT` | Signal is over 20           |

### NetworkMode (enum)

Network mode of the modem (get/set)

| Key                       | Description |
| ------------------------- | ----------- |
| `NetworkMode.AUTOMATIC`   | Automatic   |
| `NetworkMode.GSM_ONLY`    | GSM only    |
| `NetworkMode.LTE_ONLY`    | LTE only    |
| `NetworkMode.ANY_BUT_LTE` | Any but LTE |


## License

[MIT](https://choosealicense.com/licenses/mit/)