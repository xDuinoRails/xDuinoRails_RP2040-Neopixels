from machine import SPI, Pin
import time

# Mapping: '1' bit = '110', '0' bit = '100'
bit_to_spi = {0: 0b100, 1: 0b110}

def color_to_spi_bytes(r,g,b):
    spi_bits = []
    for byte in [g,r,b]:
        for bit in range(8):
            v = (byte >> (7-bit)) & 1
            spi_bits.append(bit_to_spi[v])
    # Pack bits into bytes
    spi_bytes = bytearray()
    for i in range(0, len(spi_bits), 8):
        val = 0
        for j in range(8):
            if i+j < len(spi_bits):
                val = (val << 3) | spi_bits[i+j]
        spi_bytes.append(val)
    return spi_bytes

spi = SPI(0, baudrate=2400000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(3), mosi=Pin(4))

while True:
    spi.write(color_to_spi_bytes(16,0,0))  # Red
    time.sleep(0.05)
