import time, machine

PIN = machine.Pin(16, machine.Pin.OUT)

def send_bit(bit):
    if bit:
        PIN.value(1)
        time.sleep_us(0.8)  # T1H
        PIN.value(0)
        time.sleep_us(0.45) # T1L
    else:
        PIN.value(1)
        time.sleep_us(0.4)  # T0H
        PIN.value(0)
        time.sleep_us(0.85) # T0L

def send_byte(byte):
    for i in range(8):
        send_bit((byte << i) & 0x80)

def send_color(r,g,b):
    send_byte(g)
    send_byte(r)
    send_byte(b)

while True:
    send_color(16,0,0)  # Red
    time.sleep(0.05)
