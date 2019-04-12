import os
import sys
import time
import copy
import signal
import paramiko

class SSHClient:
    def __init__(self, host_name, num_cuda, filename, config):
        self.git_url = config['git_url']
        self.pj_root = config['pj_root']
        self.pj_name = self.git_url.split('/')[-1].split('.')[0]
        self.exec_file = filename
        self.data_dir = config['data_dir']
        self.origin_data = config['origin_data']
        self.num_cuda = num_cuda
        self.git_branch = config['git_branch']
        self.kronos_path = config['kronos_path']

        self.client = self.get_ssh_client(host_name, config['ssh_config_path'])


    def get_ssh_client(self, host_name, ssh_config_path):
        conf = paramiko.SSHConfig()
        conf.parse(open(os.path.expanduser(ssh_config_path)))
        host = conf.lookup(host_name)
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            host['hostname'], username=host['user'],
            # key_filename=host['identityfile'],
            sock=paramiko.ProxyCommand(host.get('proxycommand'))
        )
        
        print('CREATE SSH CLIENT')

        return client


    def set_project(self):
        is_pj_existing = self.check_pj_dir()
        if is_pj_existing[0] == False:
            self.send_command(['mkdir {}'.format(self.pj_root)])

        commands = self.create_base_command()

        if is_pj_existing[1]:
            self.delete_cuda_setting()
            commands.extend([
                'cd {}'.format(self.pj_name),
                'git pull origin {}'.format(self.git_branch)
                ])
        else:
            commands.extend([
                'git clone {}'.format(self.git_url),
                'cd {}'.format(self.pj_name)
                ])

            if self.data_dir == '' or self.data_dir is None:
                commands.extend([
                    'mkdir {}'.format(self.data_dir),
                    'cp -r {} {}'.format(self.origin_data, self.data_dir)
                    ])

        self.send_command(commands)
        self.insert_cuda_setting()


    def execute(self):
        signal.signal(signal.SIGINT, self.handler)

        commands = self.create_base_command()
        commands.extend([
            'cd {}'.format(self.pj_name),
            '{} run --gpu {}'.format(self.kronos_path, self.exec_file)
            ])
        self.send_command(commands)
        self.delete_cuda_setting()
        self.client.close()


    def create_base_command(self):
        base_commands = ['cd {}'.format(self.pj_root)]
        base_commands.append('. /home/tanimu/.profile'.format(self.exec_file))
        base_commands.append('. /home/tanimu/.bashrc'.format(self.exec_file))
        commands = copy.deepcopy(base_commands)

        return commands


    def check_pj_dir(self):
        check_dirs = [
                'cd {} && ls'.format(self.pj_root),
                'cd {}/{} && ls'.format(self.pj_root, self.pj_name)
                ]
        is_pj_existing = []
        for check in check_dirs:
            stdin , stdout, stderr = self.client.exec_command(check)
            if stdout.readlines() == []:
                is_pj_existing.append(False)
            else:
                is_pj_existing.append(True)
        
        return is_pj_existing


    def send_command(self, commands):
        command = ' && '.join(commands)
        print('Execute: {}'.format(command))
        try:
            stdin , stdout, stderr = self.client.exec_command(command, get_pty=True)
            for line in iter(stdout.readline, ""): 
                print(line, end="") 
        except:
            raise RuntimeError('cannot execute {}'.format(command))



    def delete_cuda_setting(self):
        exec_file_path = '/'.join([self.pj_root, self.pj_name, self.exec_file])
        ftp = self.client.open_sftp()
        file = ftp.file(exec_file_path, "r", -1)
        content = file.readlines()
        while True: 
            if (content[0] == '##### BEGIN CUDA SETTING BY KRONOS #####\n') and (
                    content[4] == '###### END CUDA SETTING BY KRONOS ######\n'):
                del content[0:6]
            else:
                break
        file = ftp.file(exec_file_path, "w", -1)
        file.writelines(content)
        file.flush()
        ftp.close()


    def insert_cuda_setting(self):
        exec_file_path = '/'.join([self.pj_root, self.pj_name, self.exec_file])
        ftp = self.client.open_sftp()
        file = ftp.file(exec_file_path, "r", -1)
        content = file.readlines()
        content.insert(0, 
                '##### BEGIN CUDA SETTING BY KRONOS #####\n' +
                'import os\n' + 
                'os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"\n' +
                'os.environ["CUDA_VISIBLE_DEVICES"] = "{}"\n'.format(
                    ', '.join(map(str, self.num_cuda))) +
                '###### END CUDA SETTING BY KRONOS ######\n' +
                '\n'
                )
        file = ftp.file(exec_file_path, "w", -1)
        file.writelines(content)
        file.flush()
        ftp.close()


    def handler(signal, frame):
        print('WARNING: CUDA SETTING is inserted to the head of execution file such as main.py in the remote server.' +
        'Please check, if you operate DIRECTLY it without using "kronos job" again.')
        sys.exit(0)

