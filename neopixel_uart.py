from machine import UART, Pin
import time

uart = UART(0, baudrate=2400000, tx=Pin(0))

def encode_byte(byte):
    result = bytearray()
    for i in range(8):
        if (byte & (1 << (7-i))):
            result.append(0xF8)
        else:
            result.append(0xC0)
    return result

def send_color(r,g,b):
    data = encode_byte(g) + encode_byte(r) + encode_byte(b)
    uart.write(data)

while True:
    send_color(16,0,0)  # Red
    time.sleep(0.05)
