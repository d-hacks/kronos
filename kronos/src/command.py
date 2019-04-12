from .modules.utils import logger, get_src_path, run_command, base_command, job_command, check_dir, copy_files_to_working_dir
import shutil
import os
import subprocess

def init(dir=None):
    src_path = get_src_path()
    target_dir = check_dir(dir)
    docker_path = os.path.join(src_path, 'docker')
    shutil.copytree(docker_path, os.path.join(target_dir, 'docker'))
    filename_list = ['.gitignore', 'kronos-config.yml']
    copy_files_to_working_dir(filename_list, target_dir)

def run(use_gpu, filename):
    args = run_command(use_gpu)
    args.extend(['experiment', 'python3', filename])
    try:
        res = subprocess.check_call(args)
        logger.info(res)
    except Exception as E:
        print(E)

def job(filename):
    try:
        job_command(filename)
    except Exception as E:
        print(E)

def shell(use_gpu):
    args = run_command(use_gpu)
    args.extend(['experiment', 'ipython'])
    try:
        res = subprocess.check_call(args)
        logger.info(res)
    except Exception as E:
        print(E)

def build(use_gpu):
    args = base_command(use_gpu)
    args.extend(['build'])
    try:
        res = subprocess.check_call(args)
        logger.info(res)
    except Exception as E:
        print(E)

def notebook(use_gpu):
    args = run_command(use_gpu)
    args.extend(['--service-ports', 'experiment', 'jupyter', 'notebook', '--ip=0.0.0.0', '--port', '8888'])
    try:
        res = subprocess.check_call(args)
        logger.info(res)
    except Exception as E:
        print(E)
