import array, time
from machine import Pin
import rp2

NUM_LEDS = 8
PIN_NUM  = 0

# PIO program for WS2812
@rp2.asm_pio( set_init=rp2.PIO.OUT_LOW
            , out_init=rp2.PIO.OUT_LOW
            , out_shiftdir=rp2.PIO.SHIFT_LEFT
            , autopull=True
            , pull_thresh=24)
def ws2812():
    set(pins, 1)   [1]  # 2 cycles = 250ns 'HIGH'
    out(pins, 1)   [4]  # 5 clocks = 675ns DATA (HIGH or LOW)
    set(pins, 0)   [2]  # 3 cycles = 375ns 'LOW'

# 
# Frequency choice
# - Neopixel requires 800kHz per bit
# - Let's use 10 cycle per bit 
#      = 8MHz frequency
#      ~ 125ns per cycle
#
# - Use both "out" and "set" for the simple code
# 
sm = rp2.StateMachine( 0, ws2812, freq=8_000_000
                     , set_base=Pin(PIN_NUM)
                     , out_base=Pin(PIN_NUM)
                     )
sm.active(1)

def show(colors):
    ar = array.array("I", colors)
    sm.put(ar, 8)

def show_n_sleep(color):
    show(color*NUM_LEDS)  # Green
    time.sleep(0.6)

# Example usage
while True:
    show_n_sleep([0xFF0000])  # Green
    show_n_sleep([0x00FF00])  # Red
    show_n_sleep([0x0000FF])  # Blue
    show_n_sleep([0x000000])  # Black

