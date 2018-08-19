from gpiozero import LEDBoard
from gpiozero import StatusBoard
import requests
from time import sleep


def pulse_leds(leds, fade_in=0, fade_out=0.7, pause=.25):
    for led in leds:
        led.pulse(fade_in, fade_out, 1, True)
        if pause > 0:
            sleep(pause)

green_leds = LEDBoard(17, 22, 9, 5, 13, pwm=True)
red_leds = LEDBoard(4, 27, 10, 11, 6, pwm=True)

red_leds.off()
green_leds.off()

pulse_leds(red_leds, fade_in=2, pause=0)

sleep(1)

for repeat in range(5):
    pulse_leds(red_leds)
    pulse_leds(reversed(red_leds))

red_leds.close()
green_leds.close()


status_board = StatusBoard('google', 'stackoverflow', 'github', 'azure', 'granta', )

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

statuses = {
    status_board.google:        'https://google.com/',
    status_board.stackoverflow: 'https://stackoverflow.com/',
    status_board.github:        'https://github.com/ErrorActionPreference/',
    status_board.azure:         'https://azure.microsoft.com/',
    status_board.granta:        'https://grantadesign.com/',
}
