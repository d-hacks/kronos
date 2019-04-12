import logging
import os
import yaml
import shutil
from .ssh_client import SSHClient
from .cuda_setting import CUDASetting

logger = logging.getLogger(__name__)

def get_src_path(dir=''):
    path = os.path.dirname(__file__).split('/')
    path.pop(-1)
    path = '/' + os.path.join(*path)
    return path

def copy_file_to_working_dir(filename, working_dir):
    src_path = get_src_path()
    shutil.copy(os.path.join(src_path, filename), os.path.join(working_dir, filename))

def load_kronos_config():
    f = open(os.path.join(os.getcwd(), "kronos-config.yml"), "r+")
    config = yaml.load(f)
    return config


def copy_files_to_working_dir(filename_list, working_dir):
    for filename in filename_list:
        copy_file_to_working_dir(filename, working_dir)

def base_command(use_gpu):
    if use_gpu:
        return ['docker-compose', '-f', '{}/docker-compose-gpu.yml'.format(load_kronos_config()['docker_path'])]
    return ['docker-compose', '-f', '{}/docker-compose-cpu.yml'.format(load_kronos_config()['docker_path'])]

def run_command(use_gpu):
    args = base_command(use_gpu)
    args.append('run')

    return args


def job_command(filename):
    config = load_kronos_config()
    set_cuda = CUDASetting(config)
    using_server, using_gpu = set_cuda.select_server_and_gpu()

    ssh_client = SSHClient(using_server, using_gpu, filename, config)
    ssh_client.set_project()
    ssh_client.execute()

def check_dir(dir):
    if dir is not None:
        os.mkdir(dir)
        return os.path.join(os.getcwd(), dir)
    else:
        while True:
            inp = input('Do you create docker files in current dir? [Y/n]: ').lower()
            if inp in ['y', 'ye', 'yes', '']:
                return os.getcwd()
            elif inp in ['n', 'no']:
                return False
