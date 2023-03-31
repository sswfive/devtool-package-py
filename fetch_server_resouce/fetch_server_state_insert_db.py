"""
@Time    : 2023/3/31
@Author  : ssw
@File    : fetch_server_state_insert_db.py
@Desc    : 实时获取服务器信息（1分钟轮询一次）并写入pg数据库
"""

import socket
import time
import psutil
import pynvml
import pg8000.native


TIME_INTERVAL = 60 * 1
pgdb_conn = pg8000.connect(host="127.0.0.1", user="test", password="test", port=5432,  database="dbtest")


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


def main():

    os_resource = OSResource()

    while True:
        device_info = os_resource.fetch_server_info
        print(f"device_info: {device_info}")
        cpu_info = os_resource.fetch_cpu_state
        print(f"cpu_info: {cpu_info}")
        mem_info = os_resource.fetch_memory_state
        print(f"mem_info: {mem_info}")
        disk_info = os_resource.fetch_disk_state
        print(f"disk_info: {disk_info}")
        gpu_info = os_resource.fetch_gpu_state
        print(f"gpu_info: {gpu_info}")

        # 插入到数据库
        cur = pgdb_conn.cursor()
        #print(f"获取到的cur:{cur}")
        # cpu_percent = None
        # memory_percent = mem_info.get('mem_percent')
        # disk_percent = disk_info.get('disk_percent')
        # device_ip = device_info.get('host_ip')
        # cur.execute("INSERT INTO equipment_monitor_info (cpu_percent, memory_percent, disk_percent, gpu_info, device_ip) VALUES (%s, %s, %s, %s, %s)", (cpu_percent, memory_percent, disk_percent, json.dumps(gpu_info), device_ip))
        # pgdb_conn.commit()

        time.sleep(TIME_INTERVAL)


if __name__ == '__main__':
    main()