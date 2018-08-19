from gpiozero import LEDBoard
from gpiozero import StatusBoard
import requests
from time import sleep


def is_website_up(url):
    try:
        r = requests.get(url)
        print(url, r.ok)
        return r.ok
    except:
        return false


def website_up(url):
    while True:
        try:
            r = requests.get(url)
            print(url, r.ok)
            yield r.ok
        except:
            yield False


def pulse_leds(leds, fade_in=1.0, fade_out=1.0, pause=0.0):
    for led in leds:
        led.pulse(fade_in, fade_out, 1, True)
        if pause > 0:
            sleep(pause)


green_leds = LEDBoard(17, 22, 9, 5, 13, pwm=True)
red_leds = LEDBoard(4, 27, 10, 11, 6, pwm=True)

red_leds.off()
green_leds.off()

# Pulse red leds on
pulse_leds(red_leds)

sleep(2)

# Swoosh up down
fade_in = 0
fade_out = 0.7
pause = 0.25

for repeat in range(5):
    pulse_leds(red_leds, fade_in, fade_out, pause)
    pulse_leds(reversed(red_leds), fade_in, fade_out, pause)

# Detect web sites
green_led = green_leds[0]
red_led = red_leds[0]

green_led.blink(0.5, 0.5)
sleep(3)
if is_website_up('https://google.com'):
    green_led.on()
    red_led.off()
else:
    green_led.off()
    red_led.on()

while True:
    # Do nothing
    pass

red_leds.close()
green_leds.close()

status_board = StatusBoard('google', 'stackoverflow', 'github', 'azure', 'granta', )
statuses = {
    status_board.google: 'https://google.com/',
    status_board.stackoverflow: 'https://stackoverflow.com/',
    status_board.github: 'https://github.com/ErrorActionPreference/',
    status_board.azure: 'https://azure.microsoft.com/',
    status_board.granta: 'https://grantadesign.com/',
}
