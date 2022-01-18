
#  importujemy biblioteke o nazwie: serial
import serial

#  importujemy biblioteke o nazwie: threading

import threading

#  importujemy biblioteke o nazwie: struct
import struct

# Importujemy z biblioteki proto_file.proto_parser metodę/klasę o nazwie: ProtobufCommParser
from proto_file.proto_parser import ProtobufCommParser

# Importujemy z biblioteki proto_file.ExampleProto_pb2 metodę/klasę o nazwie: DataPacket,
from proto_file.ExampleProto_pb2 import DataPacket, DeviceRequest, DeviceResponse

#  importujemy biblioteke o nazwie: logging
import logging



# Rozpoczynamy definicje obiektu/klasy
class ProtobufComm:

# Rozpoczynamy definicje funkcji magicznej
    def __init__(self, port: str, baudrate: int):
        self.stm = serial.Serial(port, baudrate)


# Rozpoczynamy definicje bloku warunkowego
        if not self.stm.is_open:

# Podniesienie flagi wyjątku RuntimeError(
            raise RuntimeError(
                f'Couldn\'t open port {port} with baudrate {baudrate}')

# Komentarz programisty
        # these are used for LED async task
        self.led_state = False
        self.led_timer = None
        self.led_timer_delay = 0.5



# Rozpoczynamy definicje funkcji
    def read_packet_size(self, size_data: bytes) -> int:

# Importujemy z biblioteki using metodę/klasę o nazwie: to
# Komentarz programisty
        # using struct to unpack 16-bit unsigned value from byte array

# Zwracanie z funkcji obiektu
        return struct.unpack('<H', size_data)



# Rozpoczynamy definicje funkcji
    def write_packet_size(self, packet_data: bytes) -> bytes:
# Komentarz programisty
        # similarly to read_packed_data, we use struct to pack the size into the byte array
        packet_size = len(packet_data)
        packet_data = struct.pack('<H', packet_size) + packet_data

# Zwracanie z funkcji obiektu
        return packet_data



# Rozpoczynamy definicje funkcji
    def read_packet(self) -> bytes:
# Komentarz programisty
        # First, we fetch 2 bytes of size from internal serial buffer
        msg_size_data = self.stm.read(2)
# Komentarz programisty
        #print(f"Read packet header: {msg_size_data.hex(' ')}")
        msg_len = self.read_packet_size(msg_size_data)[0]
# Komentarz programisty
        # Then, we fetch the rest of the message

# Rozpoczynamy definicje bloku warunkowego
        if msg_len > 0:
            msg_data = self.stm.read(msg_len)
# Komentarz programisty
            #print(f"Read packet data: {msg_data.hex(' ')}")

# Zwracanie z funkcji obiektu
            return msg_data
        else:
            print("Empty packet.")

# Zwracanie z funkcji obiektu
            return bytes()



# Rozpoczynamy definicje funkcji
    def read_response(self) -> DeviceResponse:
# Komentarz programisty
        # Let's try reading the packet
        msg_data = self.read_packet()
# Komentarz programisty
        # And we process it

# Zwracanie z funkcji obiektu
        return ProtobufCommParser.parse_response(msg_data)



# Rozpoczynamy definicje funkcji
    def read_data_packet(self) -> DataPacket:
# Komentarz programisty
        # very similar to above
        msg_data = self.read_packet()

# Zwracanie z funkcji obiektu
        return ProtobufCommParser.parse_data_packet(msg_data)



# Rozpoczynamy definicje funkcji
    def handle_response(self, response: DeviceResponse):

# Rozpoczynamy definicje bloku warunkowego
        if response.code == DeviceResponse.ResponseType.OK:
            print('Response OK!')
        elif response.code == DeviceResponse.ResponseType.BAD_TYPE:
            print('Bad response type!')
        elif response.code == DeviceResponse.ResponseType.PROTOBUF_ERROR:
            print('Some protobuf error happened while parsing the request on the device!')



# Rozpoczynamy definicje funkcji
    def start_data_output(self):
# Komentarz programisty
        # Let's create the request and add the size
        msg = ProtobufCommParser.create_start_request()
        msg = self.write_packet_size(msg)

# Komentarz programisty
        # And that's it, it's ready to go
        self.stm.write(msg)

# Komentarz programisty
        # Just wait until the device responds
        response = self.read_response()
        self.handle_response(response)



# Rozpoczynamy definicje funkcji
    def stop_data_output(self):
# Komentarz programisty
        # basically same as above - it could definitely be
# Komentarz programisty
        # shortened, since lots of code repeats, i just dont care about it now.
# Komentarz programisty
        # C'mon, it's just an example, no one will ever use this code in prod...
# Komentarz programisty
        # ...right?
        msg = ProtobufCommParser.create_stop_request()
        msg = self.write_packet_size(msg)

        self.stm.write(msg)

# Komentarz programisty
        #response = self.read_response()
# Komentarz programisty
        #self.handle_response(response)


# Rozpoczynamy definicje funkcji
    def start_pom(self):

# Zwracanie z funkcji obiektu
        return str(f'Value A, Value B, Value C, Constant value\n')



# Rozpoczynamy definicje funkcji
    def handle_data(self):
        data = self.read_data_packet()
        print(f'{data.valueA}, {data.valueB}, {data.valueC}, {data.constantValue}')

# Wyświetlenie informacji w konsoli
        logging.info(f'{data.valueA}, {data.valueB}, {data.valueC}, {data.constantValue}')

# Zwracanie z funkcji obiektu
        return str(f'{data.valueA}, {data.valueB}, {data.valueC}, {data.constantValue}\n')



# Rozpoczynamy definicje funkcji
    def toggle_led(self):
        print('Toggling LED!')
# Komentarz programisty
        # let's create proper message and encapsulate it into our packet
        msg = ProtobufCommParser.create_led_toggle_request(self.led_state)
        msg = self.write_packet_size(msg)

# Komentarz programisty
        # and off we go
        self.stm.write(msg)
        self.led_state = not self.led_state

# Komentarz programisty
        # we have to make sure the device responds before doing anything else
        response = self.read_response()
        self.handle_response(response)



# Rozpoczynamy definicje funkcji
    def _toggle_led_with_timer(self):
        self.toggle_led()

# Rozpoczynamy definicje nowego wątku
#  Określenie wątku, który wykona daną metodę w określonym czasie 
        self.led_timer = threading.Timer(
            self.led_timer_delay, self._toggle_led_with_timer)

# Startujemy nowy wątek
        self.led_timer.start()



# Rozpoczynamy definicje funkcji
    def start_led_toggling(self, delay: int):
        self.led_timer_delay = delay

# Rozpoczynamy definicje nowego wątku
#  Określenie wątku, który wykona daną metodę w określonym czasie 
        self.led_timer = threading.Timer(delay, self._toggle_led_with_timer)

# Startujemy nowy wątek
        self.led_timer.start()



# Rozpoczynamy definicje funkcji
    def stop_led_toggling(self):
        self.led_timer.cancel()
