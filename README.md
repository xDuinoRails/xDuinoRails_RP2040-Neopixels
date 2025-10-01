# xDuinoRails_RP2040-Neopixels

This repository should show as many ways as possible to control Neopixels with a RP2040.

| Method | Description | Example Filename | Wokwi |
| :--- | :--- | :--- | :--- |
| PIO | Signal performed by PIO from CPU | neopixel_pio.py | [Wokwi CPU-PIO](https://wokwi.com/projects/443545796878931969) |
| DMA + PIO | Signal performed by PIO from DMA | neopixel_pio_dma.py (similar) | [Wokwi DMA-PIO](https://wokwi.com/projects/443546987878970369) |
| Bit-Banging | Manual timing via GPIO and delays | neopixel_bitbang.py | <tbd> |
| SPI | Encode WS2812 bits as SPI bytes | neopixel_spi.py | <tbd> |
| UART | Encode WS2812 bits as UART bytes | neopixel_uart.py | <tbd> |
| Multicore | Use both RP2040 cores for logic and real-time output | neopixel_multi.py | <tbd> |
