from .modules.utils import (logger, get_src_path, run_command, base_command, check_dir, copy_files_to_working_dir, change_imgname, send_files)
import shutil
import os
import subprocess


def init(dir):
    src_path = get_src_path()
    target_dir = check_dir(dir)
    docker_path = os.path.join(src_path, 'docker')
    shutil.copytree(docker_path, os.path.join(target_dir, 'docker'))
    filename_list = send_files(target_dir)
    copy_files_to_working_dir(filename_list, target_dir)
    change_imgname(target_dir)


def run(use_gpu, filename):
    args = run_command(use_gpu)
    args.extend(['experiment', 'python3', filename])
    try:
        res = subprocess.check_call(args)
        logger.info(res)
    except Exception as E:
        print(E)


def ipython(use_gpu):
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
    args.extend(['--service-ports', 'experiment', 'jupyter',
                 'notebook', '--allow-root', '--ip=0.0.0.0', '--port', '8888'])
    try:
        res = subprocess.check_call(args)
        logger.info(res)
    except Exception as E:
        print(E)


def lab(use_gpu):
    args = run_command(use_gpu)
    args.extend(['--service-ports', 'experiment', 'jupyter',
                 'lab', '--allow-root', '--ip=0.0.0.0', '--port', '8888'])
    try:
        res = subprocess.check_call(args)
        logger.info(res)
    except Exception as E:
        print(E)


def bash(use_gpu, name=None):
    args = run_command(use_gpu)
    if name:
        args.extend(['--name', name])
    args.extend(['experiment', '/bin/bash'])
    try:
        res = subprocess.check_call(args)
        logger.info(res)
    except Exception as E:
        print(E)
