ODBLib
======
[![Build Status](https://travis-ci.org/k2r79/ODBLib.svg?branch=develop)](https://travis-ci.org/k2r79/ODBLib) [![Coverage Status](https://coveralls.io/repos/k2r79/ODBLib/badge.png?branch=develop)](https://coveralls.io/r/k2r79/ODBLib?branch=develop)

ODB II library that allows to connect and interact with a Bluetooth ELM327.

<b style='color:red'>Warning: this project is tested on Linux because it uses PyBlue (Linux / Windows support only)</b>

Features
---
This library is still in a development stage and includes :
- bluetooth connection to an ODB device (tested on an ELM327 Bluetooth)
- a command line testing tool
- AT command submission according to a mode and PID
- live engine RPM reading

Installation
---
Go to your local workspace
```
cd /path/to/your/workspace/
```

Clone the project from Github
``` 
git clone https://github.com/k2r79/ODBLib.git
```

Go to the cloned directory
```
cd ODBLIb
```

First install ***libbluetooth-dev*** on your system
````
sudo apt-get install libbluetooth-dev
```

Then install the project's pip dependencies
```
pip install -r requirements.txt
```

Check that everything works
```
nosetests
```

Licence
---
This project is under [MIT License](http://opensource.org/licenses/MIT), feel free to use and modify it.
