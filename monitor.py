from gpiozero import LEDBoard
from gpiozero import StatusBoard
import requests
from time import sleep


def is_website_up(url):
    try:
        r = requests.get(url)
        return r.ok
    except:
        return False

def pulse_leds(leds, fade_in=1.0, fade_out=1.0, pause=0.0):
    for led in leds:
        led.pulse(fade_in, fade_out, 1, True)
        if pause > 0:
            sleep(pause)


def switch_leds(strip, green):
    red_led = strip.lights.red
    green_led = strip.lights.green

    if green:
        green_led.on()
        red_led.off()
    else:
        green_led.off()
        red_led.on()


green_leds = LEDBoard(17, 22, 9, 5, 13, pwm=True)
red_leds = LEDBoard(4, 27, 10, 11, 6, pwm=True)

red_leds.off()
green_leds.off()

# Pulse red LEDs on
pulse_leds(red_leds)

sleep(3)

# Swoosh up down
fade_in = 0
fade_out = 0.7
pause = 0.25

for repeat in range(5):
    pulse_leds(red_leds, fade_in, fade_out, pause)
    pulse_leds(reversed(red_leds), fade_in, fade_out, pause)

red_leds.close()
green_leds.close()

# Detect web sites
status_board = StatusBoard()

urls = [
    'https://google.com/',
    'https://stackoverflow.com/',
    'https://github.com/ErrorActionPreference/',
    'https://azure.microsoft.com/',
    'https://grantadesign.com/',
]

while True:
    for n in reversed(range(len(urls))):
        strip = status_board[n]
        url = urls[n]
        if strip.lights.red.is_lit:
            current_led = strip.lights.red
        else:
            current_led = strip.lights.green

        current_led.blink(0.1, 0.1)

        switch_leds(strip, is_website_up(url))
    sleep(60)
