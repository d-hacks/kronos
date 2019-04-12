# kronos
## Overview
This is the docker based command for machine learning project.  
kronos helps that you mind the difference between a local cpu environemnt and a cuda gpu environment.  

## Installation
1. Install [pip](https://pip.pypa.io/en/stable/).
1. Install kronos via pip
```
pip install git+https://github.com/d-hacks/kronos
```

## Command
### Introduce kronos to your project
In order to use kronos, you need to create the kronos configuration files in your project directory.  
In kronos, you can create that only to executing the following `init` command.  
```
kronos init
```

### Build the container
Create the docker-compose container of python environment.  
This container provides python in Ubuntu 18.04 environment.  
If you want to create the cpu environment, please type the following commaned.
```
kronos build
```
If you want to create the gpu environment, please type the following commaned.
```
kronos build --gpu
```

### Run the python file in the built docker container
Run the python file in cpu environment
({python\_file} is the target file that you want to run)
```
kronos run {python file}
```
Run the python file in gpu environment
```
kronos run --gpu {python file}
```

## Tutorial
<!--
### Preparation
Fill in the required python packages in the {cpu/gpu}\_requirements.txt.  
The packages written int the {cpu/gpu}\_requirements.txt is install via pip.
-->
