from gpiozero import StatusBoard
from gpiozero.tools import negated, smoothed
import requests
from time import sleep

sb = StatusBoard('google', 'stackoverflow', 'github', 'azure', 'granta')

def website_up(url):
    while True:
        try:
            r = requests.get(url)
            print(url, r.ok)
            yield r.ok
        except:
            yield False

statuses = {
    sb.google: website_up('https://google.com/'),
    sb.stackoverflow: website_up('https://stackoverflow.com/'),
    sb.github: website_up('https://github.com/ErrorActionPreference/'),
    sb.azure: website_up('https://azure.microsoft.com/'),
    sb.granta: website_up('https://grantadesign.com/'),
}

for strip, website in statuses.items():
    strip.lights.green.source = smoothed(website, 2, any)  # allow 1 false negative out of 2
    strip.lights.green.source_delay = 60

    strip.lights.red.source = negated(strip.lights.green.values)
    strip.lights.red.source_delay = 60



input()

