# kronos
## Discription
This is the docker based command for machine learning project.  
kronos helps that you mind the difference between a local cpu environemnt and a cuda gpu environment.  

## Installation


## Preparation
Fill in the required python packages in the {cpu/gpu}\_requirements.txt.
The packages written int the {cpu/gpu}\_requirements.txt is install via pip.

## Command
### Build the container
Create the docker-compose container of python environment.  
This container provides python in Ubuntu 18.04 environment.  
If you want to create the cpu environment, please type the following commaned.
`kronos build`
If you want to create the gpu environment, please type the following commaned.
`kronos build --gpu`

### Run the python file in the built docker container
Run the python file in cpu environment
({python\_file} is the target file that you want to run)
`kronos run {python file}`
Run the python file in gpu environment
`kronos run --gpu {python file}`

## Tutorial


