import math


class CUDASetting:
    def __init__(self, config):
        self.num_use_gpu = config['num_use_gpu']
        self.fix_server = config['fix_server']
        self.fix_gpu = config['fix_gpu']

        self.state = self.get_gpusinfo()
        self.servers = list(self.state.keys())
        self.align_state = {}


    def select_server_and_gpu(self):
        using_server = None
        if self.fix_server == '' or self.fix_server is None:
            using_server = self.search_available_server()
        else:
            for s in self.servers:
                s_name = s.split('.')[0]
                if s_name in self.fix_server:
                    using_server = s_name

        if using_server is None:
            raise RuntimeError('fix_server in config.py is not valid. Please select the server in ["bacchus", "chasca", "diana"].')

        print('SERVER TO USE: {}'.format(using_server))


        if self.fix_gpu == [] or self.fix_gpu == '' or self.fix_gpu == None:
            using_gpu = self.search_available_gpu(using_server)
        elif type(self.fix_gpu) == int:
            assert self.num_use_gpu == 1
            using_gpu = self.fix_gpu
        elif len(self.fix_gpu) >= 1:
            assert self.num_use_gpu == len(self.fix_gpu)
            using_gpu = self.fix_gpu
        else:
            raise RuntimeError('fix_gpu in config.py is not valid. Please specify gpu like a [0], [0, 1].')

        print('CUDA TO USE: {}'.format(using_gpu))

        return using_server.split('.')[0], using_gpu


    def search_available_server(self):
        num_available_gpu = {}
        for s in self.servers:
            self.align_state[s] = {}
            num_available_gpu[s] = 0
            gpus = self.state[s]
            for i, g in enumerate(gpus):
                used = float(g['memory.used'])
                total = float(g['memory.total'])
                ratio = (used / total) * 100
                self.align_state[s][i] = math.ceil(ratio)
                if ratio < 10:
                    num_available_gpu[s] += 1

        print('GPU USAGE %: {}'.format(self.align_state))

        min_availble_gpu = 100
        using_server = None
        for k, v in num_available_gpu.items():
            if v >= self.num_use_gpu and v < min_availble_gpu:
                min_availble_gpu = v
                using_server = k

        if using_server is None:
            raise RuntimeError('GPU is fully used')

        return using_server


    def search_available_gpu(self, using_server):
        using_gpu = [i for i in range(self.num_use_gpu)]
        usage_acending = [100 for i in range(self.num_use_gpu)]

        for k, v in self.align_state[using_server].items():
            is_this_gpu_selected = False
            for i in range(self.num_use_gpu):
                if v < usage_acending[i]:
                    for j in reversed(range(i, self.num_use_gpu)):
                        usage_acending[j] = usage_acending[j-1]
                        using_gpu[j] = using_gpu[j-1]
                    usage_acending[i] = v
                    using_gpu[i] = k
                    is_this_gpu_selected = True

                if is_this_gpu_selected:
                    break

        return using_gpu


    def get_gpusinfo(self):
        state = {
            "chasca.ht.sfc.keio.ac.jp": [
                {
                    "memory.used": "12000", 
                    "name": "TITAN X (Pascal)", 
                    "timestamp": "2018/10/11 23:22:03.405",
                    "memory.total": "12194", 
                    "uuid": "GPU-1ab15dd0-004d-5cc0-b8bd-756cee3647cf",
                    "utilization.gpu": "0", 
                    "index": "0",
                    "memory.free": "12194",
                    "utilization.memory": "0"
                }, 
                {
                    "memory.used": "0",
                    "name": "TITAN X (Pascal)",
                    "timestamp": "2018/10/11 23:22:03.406",
                    "memory.total": "12196",
                    "uuid": "GPU-ca5cd507-bd29-6a91-87ef-056333c74d9b",
                    "utilization.gpu": "3",
                    "index": "1",
                    "memory.free": "12196",
                    "utilization.memory": "0"
                }
            ], 
            "bacchus.ht.sfc.keio.ac.jp": [
                {
                    "memory.used": "0",
                    "name": "GeForce GTX 1080",
                    "timestamp": "2018/10/11 23:22:05.939",
                    "memory.total": "8117",
                    "uuid": "GPU-c609ee76-b279-a905-65af-2cd378364f80",
                    "utilization.gpu": "0",
                    "index": "0",
                    "memory.free": "8117",
                    "utilization.memory": "0"
                },
                {
                    "memory.used": "0",
                    "name": "GeForce GTX 1080",
                    "timestamp": "2018/10/11 23:22:05.940",
                    "memory.total": "8119",
                    "uuid": "GPU-e8064785-f266-9b0e-ce81-32b141754dd5",
                    "utilization.gpu": "0",
                    "index": "1",
                    "memory.free": "8119",
                    "utilization.memory": "0"
                },
                {
                    "memory.used": "0",
                    "name": "GeForce GTX 1080",
                    "timestamp": "2018/10/11 23:22:05.941",
                    "memory.total": "8119",
                    "uuid": "GPU-414401c7-a5fa-1f3e-4517-2a24764f2309",
                    "utilization.gpu": "0",
                    "index": "2",
                    "memory.free": "8119",
                    "utilization.memory": "0"
                }, 
                {
                    "memory.used": "0",
                    "name": "GeForce GTX 1080",
                    "timestamp": "2018/10/11 23:22:05.942",
                    "memory.total": "8119",
                    "uuid": "GPU-37df2e6e-eef1-260b-9910-704df9aee4f7",
                    "utilization.gpu": "2",
                    "index": "3",
                    "memory.free": "8119",
                    "utilization.memory": "0"
                }
            ]
        }
        
        return state
