import array, time
from machine import Pin
import rp2

# PIO program for WS2812
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)           .side(0) [T3 - 1]
    jmp(not_x, "do_zero").side(1) [T1 - 1]
    jmp("bitloop")      .side(1) [T2 - 1]
    label("do_zero")
    nop()               .side(0) [T2 - 1]
    wrap()

NUM_LEDS = 8
PIN_NUM = 16

# State machine setup
sm = rp2.StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(PIN_NUM))
sm.active(1)

def show(colors):
    ar = array.array("I", colors)
    sm.put(ar, 8)

# Example usage
while True:
    show([0x100000]*NUM_LEDS)  # Red
    time.sleep(0.5)
    show([0x001000]*NUM_LEDS)  # Green
    time.sleep(0.5)
