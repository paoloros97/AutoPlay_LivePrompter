# AutoPlay for LivePrompter


<!-- GETTING STARTED -->
## Installation

### Install Python

* <a href="https://www.python.org/downloads/">Download</a> and install Python.

### Install Visual Studio Build Tools

* <a href="https://visualstudio.microsoft.com/downloads/?q=build+tools">Download</a> and install Visual Studio.
Install then the Visual Studio Build Tools.
(This is necessary to install python-rtmidi)

 <p align="center"><img src="images/VisualStudio.PNG" alt="avvia" width="550"></p>

### Install libreries

Copy and paste the following commands into the Command Prompt:

```
pip install mido
```
```
pip install python-rtmidi
```


### Lunch App
Double click on the Python file "AutoPlayer.py"
<p align="center"><img src="images/AutoPlayScreenShot.PNG" alt="avvia" width="550"></p>

When it receive a MIDI command, the message will be forwarded, and added a play command.
(Look into the code to change the MIDI name ports)

<p align="center"><img src="images/AutoPlayScreenShot_withsignal.PNG" alt="avvia" width="550"></p>

