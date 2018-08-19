from gpiozero import LEDBoard
from gpiozero import StatusBoard
import requests
from time import sleep


pause = .25
fade = .7

# green_leds = LEDBoard(17, 22, 9, 5, 13, pwm=True)
red_leds = LEDBoard(4, 27, 10, 11, 6, pwm=True)

red_leds.off()
red_leds.pulse(fade,  fade, 1, False)
sleep(pause)

for repeat in range(5):
    for led in red_leds:
        led.pulse(0, fade, 1, True)
        sleep(pause)

    for led in reversed(red_leds):
        led.pulse(0, fade, 1, True)
        sleep(pause)


red_leds.close()


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
