# RobotUnicornAttack
A deep reinforcement learning based bot that masters the flash game Robot Unicorn attack

<https://www.crazygames.com/game/robot-unicorn-attack>




## Getting started

1. Clone this repository
2. Run `./do venv` to create a python virtual environment
3. Activate virtual environment by running from project root directory `source venv/bin/activate`
4. Update your pip via `python -m pip install --upgrade pip`
5. Run `./do install_requirements` to install all project requirements


If you have not worked with Selenium before, please make sure to download a Chromedriver
### Download Chromedriver

<https://chromedriver.chromium.org/downloads> (Make sure you are using the same version as your Chrome)

#### Install on Mac & Linux

Unzip downloaded chromedriver
`unzip chromedriver_mac64.zip`

Give it the right permissions
`xattr -d com.apple.quarantine chromedriver`

Move the driver to the /usr/local/bin folder
`mv chromedriver /usr/local/bin` 

## Training model

```
python3 main.py -m "Train"
```

## Running model

```
python3 main.py -m "Run"
```