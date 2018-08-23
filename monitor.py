from gpiozero import LEDBoard
from gpiozero import StatusBoard
import requests
from time import sleep


def is_website_up(url):
    """
    Check that a website is responding without error.
    :param url: URL to check
    :return: True if 200 response is received - False in all other circumstances
    """
    try:
        r = requests.get(url)
        return r.ok
    except:
        return False


def pulse_leds(leds, fade_in=1.0, fade_out=1.0, pause=0.0):
    """
    Fade leds in and out.
    :param leds: Collection of leds to pulse
    :param fade_in: Time in seconds to spend fade the led up
    :param fade_out: Time in seconds to fade the led down
    :param pause: Interval (in seconds) between pulsing each led
    """
    for led in leds:
        led.pulse(fade_in, fade_out, 1, True)
        if pause > 0:
            sleep(pause)


def switch_leds(strip, green):
    """
    Turn green led on, red led off or vice versa on a given strip.
    :param strip: StatusBoard strip
    :param green: if True turn the green on, red off.  Otherwise green off, red on
    """
    red_led = strip.lights.red
    green_led = strip.lights.green

    if green:
        green_led.on()
        red_led.off()
    else:
        green_led.off()
        red_led.on()


def test_sequence():
    """
    Test that all the leds are operating.
    """

    # Manually configure the leds as PWM compatible
    # Each number is a GPIO pin number
    green_leds = LEDBoard(17, 22, 9, 5, 13, pwm=True)
    red_leds = LEDBoard(4, 27, 10, 11, 6, pwm=True)

    try:
        # Ensure everything is off to start
        red_leds.off()
        green_leds.off()

        # Pulse greed LEDs on
        pulse_leds(red_leds)
        sleep(3)

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
    finally:
        green_leds.close()
        red_leds.close()


def monitor_websites():
    """
    Continuously update the led to reflect status of websites.
    """
    urls = [
        'https://google.com/',
        'https://stackoverflow.com/',
        'https://github.com/ErrorActionPreference/',
        'https://azure.microsoft.com/',
        'https://grantadesign.com/',
    ]

    status_board = StatusBoard()

    try:
        while True:
            #  Status board is upside down so run from top to bottom
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
    finally:
        status_board.close()


test_sequence()
monitor_websites()
