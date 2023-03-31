"""
@Time    : 2023/3/31
@Author  : ssw
@File    : fetch_server_state_use_psutil.py
@Desc    : 获取服务器资源（cpu、mem、gpu、disk、ip）的实时信息

# package install:
    pdm add psutil
    pdm add pynvml
"""

import socket
import psutil


class OSResource:

    @property
    def fetch_server_info(self):
        hostname = socket.gethostname()
        host_ip = socket.gethostbyname(hostname)
        return {"host_ip": host_ip, "hostname": hostname}

    @property
    def fetch_memory_state(self):
        mem = psutil.virtual_memory()
        memory_state = {
            'mem_total': mem.total / (1024 * 1024),
            'mem_free': mem.available / (1024 * 1024),
            'mem_used': mem.used / (1024 * 1024),
            'mem_percent': '%s%%' % mem.percent
        }
        return memory_state

    @property
    def fetch_cpu_state(self):
        cpu = psutil.cpu_percent()
        cpu_state = round(cpu / 100, 4)
        return {"cpu_state": cpu_state}

    @property
    def fetch_disk_state(self):
        disk = psutil.disk_usage('/home')
        disk_state = {
            'disk_total': disk.total,
            'disk_used': disk.used,
            'disk_free': disk.free,
            'disk_percent': round(disk.percent / 100, 4),
        }
        return disk_state

    @property
    def fetch_gpu_state(self):
        """
        获取GPU信息
        """
        pynvml.nvmlInit()
        gpu_detail_info = []
        gpu_count = pynvml.nvmlDeviceGetCount()
        gpu_detail_info.append({"gpu_count": gpu_count})
        for i in range(gpu_count):
            gpu = pynvml.nvmlDeviceGetHandleByIndex(i)
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(gpu)
            gpu_detail_info.append({
                "index": i,
                "mem_state": {
                    "total": mem_info.total,
                    "used": mem_info.used,
                    "free": mem_info.free
                },
                "gpu_type": pynvml.nvmlDeviceGetName(gpu)
            })
        pynvml.nvmlShutdown()
        return gpu_detail_info


if __name__ == '__main__':
    os_resource = OSResource()
    print(os_resource.fetch_server_info)
    print(os_resource.fetch_memory_state)
    print(os_resource.fetch_cpu_state)
    print(os_resource.fetch_disk_state)
    print(os_resource.fetch_gpu_state)