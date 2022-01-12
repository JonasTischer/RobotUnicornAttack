# RobotUnicornAttack
A deep reinforcement learning based bot that masters the flash game Robot Unicorn attack

https://www.crazygames.com/game/robot-unicorn-attack


Download Chromedriver:

<https://chromedriver.chromium.org/downloads> (Make sure you are using the same version as your Chrome)

Unzip downloaded chromedriver
`unzip chromedriver_mac64.zip`

Give it the right permissions
`xattr -d com.apple.quarantine chromedriver`

Move the driver to the /usr/local/bin folder
`mv chromedriver /usr/local/bin` 

## Getting started

1. Clone this repository
1. Run `./do venv` to create a python virtual environment
1. Activate virtual environment by running from project root directory `source venv/bin/activate`
1. Update your pip via `python -m pip install --upgrade pip`
1. Run `./do install_requirements` to install all project requirements
