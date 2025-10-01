import _thread, time, array
from machine import Pin
import rp2

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
sm = rp2.StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(PIN_NUM))
sm.active(1)

def led_thread():
    while True:
        ar = array.array("I", [0x100000]*NUM_LEDS)
        sm.put(ar, 8)
        time.sleep(0.5)
        ar = array.array("I", [0x001000]*NUM_LEDS)
        sm.put(ar, 8)
        time.sleep(0.5)

_thread.start_new_thread(led_thread, ())
while True:
    print("Main core free!")
    time.sleep(1)
