import logging
import os
import shutil
import oyaml as yaml

logger = logging.getLogger(__name__)


def get_src_path(dir=''):
    path = os.path.dirname(__file__).split('/')
    path.pop(-1)
    path = '/' + os.path.join(*path)
    return path


def copy_file_to_working_dir(filename, working_dir):
    src_path = get_src_path()
    shutil.copy(
        os.path.join(
            src_path, filename), os.path.join(
            working_dir, filename))


def load_kronos_config():
    f = open(os.path.join(os.getcwd(), "kronos-config.yml"), "r+")
    config = yaml.safe_load(f)
    return config


def change_imgname(project_dir):
    path = project_dir.split('/')
    project_name = path[-1]
    inp = input(
            'Docker image name [default: {}]:'.format(project_name)).lower()
    if inp != "":
        imgname = inp
    else:
        imgname = project_name

    for device in ['cpu', 'gpu']:
        yml_path = os.path.join(
            project_dir,
            'docker',
            'docker-compose-{}.yml'.format(device))
        with open(yml_path, 'r') as f:
            dcyml = yaml.safe_load(f)

        dcyml['services']['experiment']['image'] = imgname
        with open(yml_path, 'w') as f:
            yaml.safe_dump(dcyml, f)


def copy_files_to_working_dir(filename_list, working_dir):
    for filename in filename_list:
        copy_file_to_working_dir(filename, working_dir)


def base_command(use_gpu):
    if use_gpu:
        return ['docker-compose', '-f', '{}/docker-compose-gpu.yml'.format(
            load_kronos_config()['docker_path'])]
    return ['docker-compose', '-f', '{}/docker-compose-cpu.yml'.format(
        load_kronos_config()['docker_path'])]


def run_command(use_gpu):
    args = base_command(use_gpu)
    args.append('run')

    return args


def check_dir(dir):
    if dir is not None:
        os.mkdir(dir)
        return os.path.join(os.getcwd(), dir)
    else:
        while True:
            inp = input(
                'Do you create docker files in current dir? [Y/n]: ').lower()
            if inp in ['y', 'ye', 'yes', '']:
                return os.getcwd()
            elif inp in ['n', 'no']:
                return False


def send_files(project_dir):
    gitignore = os.path.join(project_dir, '.gitignore')
    if os.path.exists(gitignore):
        while True:
            inp = input(
                'Do you want to overwrite the current gitignore with the default python gitignore? [Y/n]: ').lower()
            if inp in ['y', 'ye', 'yes', '']:
                return ['.gitignore', 'kronos-config.yml']
            elif inp in ['n', 'no']:
                return ['kronos-config.yml']
    else:
        return ['.gitignore', 'kronos-config.yml']
