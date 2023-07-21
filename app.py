#!/usr/bin/env python3

from flask import Flask
import logging
import os
import requests

# --- To be passed in to container ---
# Mandatory vars
HOST = os.getenv('HOST')
TZ = os.getenv('TZ', 'America/New_York')
ON_HOOK = os.getenv('ON_HOOK', 'onhook')
OFF_HOOK = os.getenv('OFF_HOOK', 'offhook')
EFFECT = os.getenv('EFFECT', 'Hip Hop')
BRIGHTNESS = int(os.getenv('BRIGHTNESS', 25))
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

# Optional Vars
DEBUG = int(os.getenv('DEBUG', 0))

# Version Info
VER = "0.1"
APP_VERSION = f"nanohook/{VER}"

# Setup logger
LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'
logging.basicConfig(level=LOG_LEVEL,
                    format='[%(levelname)s] %(asctime)s %(message)s',
                    datefmt='[%d %b %Y %H:%M:%S %Z]')
logger = logging.getLogger()

logger.info(f'Startup: {APP_VERSION}')


class Hooks:
    ON = ON_HOOK
    OFF = OFF_HOOK


def create_state_url(host: str, auth_token: str) -> str:
    return f"http://{host}:16021/api/v1/{auth_token}/state"


def create_effects_url(host: str, auth_token: str) -> str:
    return f"http://{host}:16021/api/v1/{auth_token}/effects"


headers = {'Content-Type': 'application/json', 'User-Agent': APP_VERSION}
app = Flask(__name__)


@app.route("/")
def index():
    return "Get Lost!"


@app.route("/hook/<command>")
def parse_hook(command):
    match command:
        case Hooks.ON:
            state_url = create_state_url(HOST, AUTH_TOKEN)
            effects_url = create_effects_url(HOST, AUTH_TOKEN)
            state_body = {'on': {'value': True}, 'brightness': {'value': BRIGHTNESS}}  # noqa: E501
            effects_body = {'select': EFFECT}
            requests.put(state_url, headers=headers, json=state_body)
            requests.put(effects_url, headers=headers, json=effects_body)
        case Hooks.OFF:
            state_url = create_state_url(HOST, AUTH_TOKEN)
            state_body = {'on': {'value': False}}
            requests.put(state_url, headers=headers, json=state_body)
        case _:
            return "Hook Not Found!"


if __name__ == "__main__":
    from waitress import serve
    serve(app, port=8080)
