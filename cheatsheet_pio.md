Hier ist ein kompaktes **Cheatsheet für die PIO (Programmable I/O) des RP2040**, das dir einen schnellen Überblick über Aufbau, Befehle und typische Anwendungen gibt:

---

## 🧠 **Grundlagen der PIO**
- **PIO = Programmable I/O**: Ermöglicht benutzerdefinierte Protokolle direkt auf dem Chip.
- Besteht aus:
  - **4 State Machines (SM)** pro PIO-Block (2 Blöcke insgesamt)
  - **Instruktionsspeicher** (32 Befehle pro Block)
  - **FIFOs** für Kommunikation mit CPU
  - **Pins**, **Interrupts**, **DMA-Unterstützung**

---

## 🏗️ **Aufbau einer PIO-Assembly**
```asm
.program my_program
loop:
    set pins, 1       ; Setzt Pin auf HIGH
    nop               ; Wartet 1 Takt
    set pins, 0       ; Setzt Pin auf LOW
    jmp loop          ; Springt zurück
```

---

## 🧾 **PIO-Befehle (Instruktionen)**

| Befehl       | Beschreibung                              |
|--------------|-------------------------------------------|
| `set`        | Setzt Register oder Pins auf einen Wert   |
| `jmp`        | Bedingter/unbedingter Sprung              |
| `wait`       | Wartet auf Ereignis (Pin, IRQ, etc.)      |
| `in`         | Liest Bits von Pins oder Register         |
| `out`        | Schreibt Bits in Pins oder Register       |
| `push`       | Schiebt Daten in RX FIFO                  |
| `pull`       | Holt Daten aus TX FIFO                    |
| `mov`        | Kopiert Daten zwischen Registern          |
| `irq`        | Setzt oder löscht Interrupts              |
| `nop`        | Keine Operation (1 Takt warten)           |

---

## 🧮 **Register**
- `x`, `y`: Allgemeine Register
- `isr`: Input Shift Register
- `osr`: Output Shift Register
- `pins`: Zugriff auf GPIOs

---

## 🔁 **Timing & Steuerung**
- Jeder Befehl dauert **1 Takt** (Standard)
- Mit `delay` kann man zusätzliche Takte hinzufügen:
  ```asm
  set pins, 1 [5]  ; Setzt Pin und wartet 5 Takte
  ```

---

## 🧰 **Typische Anwendungen**
- SPI, I²C, UART (benutzerdefiniert)
- WS2812 (NeoPixel) Ansteuerung
- PWM-Generierung
- Protokollanalyse oder -emulation

---

## 🧑‍💻 **Integration in C/C++ oder MicroPython**
- In C/C++ mit **SDK** (`pioasm`, `rp2_common_pio`)
- In MicroPython mit `rp2.StateMachine` und `@asm_pio()` Dekorator

---

Möchtest du ein Beispiel für ein konkretes Protokoll (z. B. UART oder WS2812) oder eine Visualisierung des Datenflusses in der PIO?
