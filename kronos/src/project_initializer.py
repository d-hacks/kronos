import yaml


def init_project_prompt():
    data = {
        'dependencies': [],
        'hardware': []
    }

    print("Python `2` or `3`?")
    python_version = input("> ")
    data['dependencies'].append('python=={}'.format(python_version))

    print("Use OpenCV? (e.g. `3.1` or `n`)")
    opencv_version = input("> ")
    if opencv_version is not "n":
        data['dependencies'].append('opencv=={}'.format(opencv_version))

    print("Number of GPUs (Titan V)? (e.g. `2` or `0`)")
    num_gpu = input("> ")
    data['hardware'].append('gpu=={}'.format(num_gpu))

    with open('kronosspec.yml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


if __name__ == "__main__":
    init_project_prompt()
