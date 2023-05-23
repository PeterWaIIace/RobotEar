# RobotEar

This is repository of proof of concept implementation for voice command processing for robot with minimal example of chain of thoughts and operating system command execution.

https://github.com/PeterWaIIace/RobotEar/assets/40773550/685dc83e-c718-4cb8-b73c-b4e83d2e9a00

Minimal example of Chain of Thoughts - CoT

## Architecture

The RobotEar is based on several python libraries and few custom parts, allowing it to listen to microphone, detect speech, execute preprogrammed commands, interact with host operating system, and respond with LLM generated text sythetised by python voice sythetiser. Entire project is based on pyaudio which uses nonblocking callbacks to read microphone data and save it to .wav temporary file, speech is extracted with local base model of whisper developed by OpenAI. User text extracted from speech is processed by OpenAI twice allowing LLM to execute commands on operating system as well as reflect on own response before giving it to user. Response from LLM is sythetised with `pyttsx3`.

LLM interacts with OS via command manager block, which holds preprogrammed list of commands LLM can access - this limits unexpected behaviours, allow LLM to search through list of available commands to guess from unintelligible speech. Commands can be easily extended addapting to system requirements.

Following design and relations between components can be seen on picture below: 

![RobotEarDesign](https://github.com/PeterWaIIace/RobotEar/assets/40773550/00f12b0a-4f04-4609-a467-e503c5a7730a)

#### Minimal Chain of Thoughts - mCoT

During operation, every user input acts on LLM twice - this is called in this project Minimal Chain of Thoughts mCoT. As real chain of thoughts allows LLM to process complicated problems by being prompted itself, minimal implementation in RobotEar allows it to reflect on its own response, and take into account output from execution of command on operating system. This is far from chain of thoughts, however it implements very basic CoT behaviour.  

#### Adding new commands

System can be editted and expanded with new commands via simply editing `command.py`. It contains dictionary with commands names, which are used by LLM to filter user input, and instructions how to call commands use imperatively from python script (LLM has no access to it). 

This is example of dictionary for Windows:
```
self.config = {
    "get_time"   : "time /T",
    "get_date"   : "date /T"
}
```

## How to use it - Windows

##### 1. Install python dependencies: 
```
pip install -r requirements.txt
```
##### 2. Create config file and fill it with your OpenAi API keys
`config.json` - this file should be in same directory as main.py
```
{
    "apiKey": "somekey",
    "organization" : "someorg"
}
```

##### 3. Run script `main.py`:

```
python3 main.py
```
After running wait for downloading whisper model. Script should ask you which audio input you want to use for, choose the one which is the most suitable for your application.

## How to use it - Raspian [WiP]

It is still work in progress, code can run on raspberryPi4 64bit but I do not have microphone to test it with.

##### 1. Get RaspbianOS 64bit:

To use whispher which is based on pytorch, you will need 64bit operating system. It can be easily obtained with rapsberrypi imager https://www.raspberrypi.com/software/. 

##### 2. In raspbian install following requirements:
```
sudo apt-get install python3-pyaudio
sudo apt install espeak
```

##### 3. Install python dependencies: 
```
pip install -r requirements.txt
```
##### 4. Create config file and fill it with your OpenAi API keys
`config.json` - this file should be in same directory as main.py
```
{
    "apiKey": "somekey",
    "organization" : "someorg"
}
```

##### 5. Run script `main.py`:

```
python3 main.py
```
After running wait for downloading whisper model. Script should ask you which audio input you want to use for, choose the one which is the most suitable for your application.
