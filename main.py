from machine import Pin, SPI
import tm1637

import max7219

import time

from utime import sleep_ms

spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)

segmentDisplay=tm1637.TM1637(clk=Pin(6), dio=Pin(7))

button = Pin(16, Pin.IN, Pin.PULL_UP)
button_pressed = False
presses = 0

display = max7219.Matrix8x8(spi, ss, 1)

display.brightness(15)

def wait_pin_change(pin):
    cur_value = pin.value()
    active = 0
    while active < 5:
        if pin.value() != cur_value:
            active += 1
        else:
            active = 0
        sleep_ms(1)

def button_pressed(change):
    global button_pressed
    button_pressed = True

button.irq(handler=button_pressed, trigger=Pin.IRQ_FALLING)

while True:

    if (button_pressed == True):
        print("button_pressed")
        presses += 1
        wait_pin_change(button)
        button_pressed = False
    
    display.fill(0)

    display.hline(1,0,6,1)

    display.vline(0,1,6,1)
    display.vline(7,1,6,1)

    display.hline(1,7,6,1)

    display.pixel(2,4,1)
    display.pixel(3,5,1)
    display.pixel(4,5,1)
    display.pixel(5,4,1)

    display.pixel(2,2,1)
    display.pixel(5,2,1)
        
    display.show()

    segmentDisplay.number(presses)
      
    time.sleep(0.1)
 
