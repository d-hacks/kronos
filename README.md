# kronos
## Overview
Kronos is a docker based command for executing machine learning projects which can automatically differenciate between a local cpu environemnt and a cuda gpu environment and run accordingly.

## Installation
1. Install [pip](https://pip.pypa.io/en/stable/).
1. Install kronos via pip
```
pip install git+https://github.com/d-hacks/kronos
```

## Command
### Introduce kronos to your project
In order to use kronos, you need to create the kronos configuration files in your project directory by executing the following `init` command.  
```
kronos init
```

### Build the container
The following commands build the docker-compose container for Python in Ubuntu 18.04 environment.
For CPU environments, type in
```
kronos build
```
For GPU environments, type in
```
kronos build --gpu
```

### Run the Python file in the docker container you built
For CPU environments, use
```
kronos run {YOUR_PYTHON_FILE.py}
```
For GPU environments, use
```
kronos run --gpu {python file}
```

## Tutorial
<!--
### Preparation
Fill in the required python packages in the {cpu/gpu}\_requirements.txt.  
The packages written int the {cpu/gpu}\_requirements.txt is install via pip.
-->
