# RobotEar

This is repository of proof of concept implementation for voice command processing for robot with minimal example of chain of thoughts and operating system command execution.

https://github.com/PeterWaIIace/RobotEar/assets/40773550/685dc83e-c718-4cb8-b73c-b4e83d2e9a00

Minimal example of Chain of Thoughts - CoT

## Architecture

## How to use it - Windows

1. Install python dependencies: 
```
pip install -r requirements.txt
```
2. Create config file and fill it with your OpenAi API keys
`config.json` - this file should be in same directory as main.py
```
{
    "apiKey": "somekey",
    "organization" : "someorg"
}
```

3. Run script `main.py`:

```
python3 main.py
```
After running wait for downloading whisper model. Script should ask you which audio input you want to use for, choose the one which is the most suitable for your application.

## How to use it - Raspian [WiP]

It is still work in progress, code can run on raspberryPi4 64bit but I do not have microphone to test it with.

1. Get RaspbianOS 64bit:

To use whispher which is based on pytorch, you will need 64bit operating system. It can be easily obtained with rapsberrypi imager https://www.raspberrypi.com/software/. 

2. In raspbian install following requirements:
`sudo apt-get install python3-pyaudio `
`sudo apt install espeak`

3. Install python dependencies: 
```
pip install -r requirements.txt
```
4. Create config file and fill it with your OpenAi API keys
`config.json` - this file should be in same directory as main.py
```
{
    "apiKey": "somekey",
    "organization" : "someorg"
}
```

5. Run script `main.py`:

```
python3 main.py
```
After running wait for downloading whisper model. Script should ask you which audio input you want to use for, choose the one which is the most suitable for your application.
