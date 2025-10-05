# SPDX-FileCopyrightText: 2021 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time

import board
import microcontroller
import rp2pio
import array

import adafruit_pioasm

# NeoPixels are 800khz bit streams. We are choosing zeros as <312ns hi, 936 lo>
# and ones as <700 ns hi, 556 ns lo>.
# The first two instructions always run while only one of the two final
# instructions run per bit. We start with the low period because it can be
# longer while waiting for more data.
program = """
.program ws2812
loop:
   set pins 1  [2]    ; 350ns - Drive 'HIGH'
   out pins 1  [4]    ; 550ns - Drive data
   set pins 0  [2]    ; 350ns - Drive 'LOW'
"""

assembled = adafruit_pioasm.assemble(program)

NEOPIXEL   = board.D6
NUM_PIXELS = 20

sm = rp2pio.StateMachine(
      assembled
    , frequency       = 8_000_000  # Go for 50ns step size
    , first_out_pin   = NEOPIXEL
    , first_set_pin   = NEOPIXEL
    , out_shift_right = False
    , auto_pull       = True
    , pull_threshold  = 24
)
print("real frequency", sm.frequency)

while True:
    pixel_buffer = array.array('L', [0xF00000 << 8, 0xF00000 << 8, 0xF00000 << 8]) 
    # sm.write(pixel_buffer)                 # Send data using one CPU
    sm.background_write(once=pixel_buffer) # Send data using non-blocking DMA
    time.sleep(1)

    pixel_buffer = array.array('L', [0x00F000 << 8, 0x000000 << 8, 0x00F000 << 8])
    # sm.write(pixel_buffer)                 # Send data using one CPU
    sm.background_write(once=pixel_buffer) # Send data using non-blocking DMA
    time.sleep(.2)

    pixel_buffer = array.array('L', [0x0000F0 << 8])
    # sm.write(pixel_buffer)                 # Send data using one CPU
    sm.background_write(once=pixel_buffer) # Send data using non-blocking DMA
    time.sleep(.2)

