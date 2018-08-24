import sys
from time import sleep

import requests
from gpiozero import LEDBoard
from gpiozero import StatusBoard


def is_website_up(url, error_text=None):
    """
    Check that a website is responding without error and does not contain error_text
    :param error_text:  return False if response contains this text
    :param url: URL to check
    :return: True if 200 response is received - False in all other circumstances
    """
    try:
        search = error_text is None

        if search:
            r = requests.head(url)
            return r.ok
        else:
            r = requests.get(url)

            if not r.ok:
                return False

            return r.text.find(error_text) == -1

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


def launch_sequence():
    """
    Test that all the leds are operating.
    """

    # Manually configure the leds as PWM compatible
    # Each number is a GPIO pin number
    with LEDBoard(17, 22, 9, 5, 13, pwm=True) as green_leds:
        # Ensure everything is off to start
        green_leds.off()

    with LEDBoard(4, 27, 10, 11, 6, pwm=True) as red_leds:
        # Ensure everything is off to start
        red_leds.off()

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


def update_strip_status(strip, url, error_text):
    """
    Update the leds on the strip to indicate the status of the given url
    :param strip: StatusBoard strip to update
    :param url: url to test
    """
    #  Flash the currently lit LED to indicate activity
    if strip.lights.red.is_lit:
        current_led = strip.lights.red
    else:
        current_led = strip.lights.green
    current_led.blink(0.1, 0.1)
    #  Check the website
    switch_leds(strip, is_website_up(url, error_text))


def monitor_websites():
    """
    Continuously update the led to reflect status of websites.
    """
    urls = [
        ('https://google.com/', None),
        ('https://stackoverflow.com/', None),
        ('https://github.com/ErrorActionPreference/', None),
        ('https://azure.microsoft.com/en-us/status/feed/', 'UK South'),
        ('https://grantadesign.com/', 'Software Engineer'),
    ]

    with StatusBoard() as status_board:
        #  Status board is upside down so run from top to bottom
        updates = [
            (status_board.five, 'https://www.google.com/', None),
            (status_board.four, 'https://stackoverflow.com/', None),
            (status_board.three, 'https://github.com/ErrorActionPreference/', None),
            (status_board.two, 'https://azure.microsoft.com/en-us/status/feed/', 'UK South'),
            (status_board.one, 'https://grantadesign.workable.com/', 'Software Engineer'),
        ]

        while True:
            for strip, url, error_text in updates:
                update_strip_status(strip, url, error_text)
                sleep(6)

            sleep(30)


if __name__ == "__main__":
    launch_sequence()
    monitor_websites()
