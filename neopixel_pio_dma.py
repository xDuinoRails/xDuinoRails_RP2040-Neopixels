import array
import time
from machine import Pin
import rp2
from rp2 import PIO
import uctypes

# --- Configuration ---
NUM_LEDS = 8
PIN_NUM  = 7

# --- PIO Program for WS2812 (NeoPixel) ---
@rp2.asm_pio(
  sideset_init = rp2.PIO.OUT_LOW,
  out_shiftdir = rp2.PIO.SHIFT_LEFT,
  autopull     = True,
  pull_thresh  = 24,
)
def ws2812():
  label("bitloop")  
  out(x, 1)             .side(0) [2] # (3 clks) Pull 1 bit from OSR 
  jmp(not_x, "do_zero") .side(1) [1] # (2 clks) Test the bit. If it's 0, jump to do_zero. Side-set high for T2

  label("do_one_if_x_one")
  jmp("bitloop")        .side(1) [4] # (5 clks) It was a 1. Keep pin high and loop

  label("do_zero")
  nop()                 .side(0) [4] # (5 clks) It was a 0. Set pin low and loop.

# --- State Machine Initialization ---
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))
sm.active(1)

# --- DMA Setup ---
ar = array.array("I", [0] * NUM_LEDS) # Our Color Buffer
dma = rp2.DMA()                       # Our DMA-Channel

def show(colors):
  """
  Updates the color buffer and triggers a non-blocking DMA transfer.
  """
  # Wait for any previous DMA transfer to finish.
  while dma.active():
    pass

  # Update the color data in the array.
  for i, color in enumerate(colors):
    # We shift it left by 8 bits to make it a 32-bit word with 8 leading zero bits
    ar[i] = color << 8

  print("Next color")

  # True  = DMA
  # False = Legacy blocking "put()"
  use_dma = True
  if not use_dma:
    sm.put(ar)
  else:
    dma.config(
        ctrl = dma.pack_ctrl( inc_write = False # Let's write to the fifo
                            , treq_sel  = 0 )   # PIO0/SM0 throttles the speed
      , read    = ar              # Source: Our color array (memory address)
      , write   = sm              # Destination: PIO SM
      , count   = NUM_LEDS        # Number of 32-bit words to transfer
      , trigger = True            # Start immediately ~"dma.active(1)"
    )

# --- Main Loop ---
print("Starting DMA-PIO NeoPixel demo...")
time.sleep_ms(100)

while True:
  # WS2812 format "GRB" (Green, Red, Blue)
  show([0xFF0000] * NUM_LEDS) # Green
  time.sleep(0.4)

  show([0x00FF00] * NUM_LEDS) # Red
  time.sleep(0.4)

  show([0x0000FF] * NUM_LEDS) # Blue
  time.sleep(0.4)

  show([0x000000] * NUM_LEDS) # Off
  time.sleep(0.4)
