# kronos
## Overview
Kronos is a docker based command for executing machine learning projects which can automatically differenciate between a local cpu environment and a CUDA GPU environment and run accordingly.

## Installation
1. Install [pip](https://pip.pypa.io/en/stable/).
1. Install kronos via pip
```
pip install kronos-ml
```

## Command
### Introduce kronos to your project
In order to use kronos, you need to create the kronos configuration files in your project directory (current directory) by executing the following `init` command.
```
kronos init [OPTIONS]
```
The init command allows users to set the location of the project directory with the option `--dir`.
```
kronos init --dir {DIRECTORY_LOCATION}
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

### Creating a Sample Test Project
Skip this step if you already have a project that you want to implement to Kronos.

Create an empty directory to be used by kronos as a project directory and move into it.
```
mkdir test
cd test
```
Generate a sample Python file using a text editor.
```
nano sample_code.py
```
Inside the file, insert the following code.
```
import torch

a = torch.randn((3, 2))
b = torch.randn((2, 4))

c = torch.matmul(a, b)

print(c.size())
```
Save and exit. If you are using Nano, save the file by pressing Ctrl + O, and exit using Ctrl + X.

### Running the Project with kronos
Initialize the kronos project directory.
```
kronos init
```
The test directory should now have a `docker` directory, `kronos-config.yml`, and `sample_code.py`.
The next step is to let Docker/kronos know about the libraries that you will be using while running your Python file. This is done using the requirements file in the docker folder.
List all items in the docker directory.
```
ls docker
```
Out of all the files in the directory, the ones that we will be focusing on are `cpu_requirements.txt` and `gpu_requirements.txt`. Choose the requirement file based on whether your environment is using CPU or GPU processors. `cpu_requirements.txt` is used in this tutorial.
Open the text file.
```
nano docker/cpu_requirements.txt
```
This is the list of all the libraries that the Docker will be installing into its virtual environment.
Add the libraries in your project that will be used bt Python. In the context of the sample project explained above, since `sample_code.py` imports Pytorch (specified by `import torch`), Pytorch should be added to the list. Note that unnecessary libraries, such as Tensorflow in this case, should be omitted in order to reduce unnecessary install time.
The text file should now read as below.
```
torch
```
Specific versions of the library can be specified optionally.
```
torch==1.1.0
```
Save and exit.
Using the build command, build a docker container and install all libraries in it. Add `--gpu` for use in GPU environments.
```
kronos build
```
Finally, run the Python file. Add `--gpu` for use in GPU environments.
```
kronos run sample_code.py
```
