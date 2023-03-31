"""
@Time    : 2023/3/31
@Author  : ssw
@File    : fetch_server_state_use_paramiko.py
@Desc    : 查看服务器cpu、硬盘、内存使用率，用于日常巡检
"""

import paramiko

ips = [
    '192.168.1.2',
    '192.168.1.3',
]


def get_cmd_client(ip, user="xxx", password="xxxx"):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, port=22, username=user, password=password)
    return ssh


def fetch_hostanme(ssh):
    cmd = "hostname"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    host_name = stdout.readlines()
    host_name = host_name[0]
    print(f"hostname: {host_name}")
    return host_name


def fetch_server_date(ssh):
    cmd = 'date +%T'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    curr_time = stdout.readlines()
    curr_time = curr_time[0]
    print(f"curr_time: {curr_time}")
    return curr_time


def fetch_mem_state(ssh):
    cmd = "cat /proc/meminfo|sed -n '1,4p'|awk '{print $2}'"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    mem = stdout.readlines()
    mem_total = round(int(mem[0]) / 1024)
    mem_total_free = round(int(mem[1]) / 1024) + round(int(mem[2]) / 1024) + round(int(mem[3]) / 1024)
    mem_usage = str(round(((mem_total - mem_total_free) / mem_total) * 100, 2)) + "%"
    print(f"mem_usage: {mem_usage}")


def fetch_cpu_state(ssh):
    cmd = "vmstat 1 3|sed  '1d'|sed  '1d'|awk '{print $15}'"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    cpu = stdout.readlines()
    cpu_usage = str(round((100 - (int(cpu[0]) + int(cpu[1]) + int(cpu[2])) / 3), 2)) + '%'
    print(f"cpu_usage: {cpu_usage}")


if __name__ == '__main__':
    ssh = get_cmd_client(ip="127.0.0.1", user="xxx", password="xxx")
    fetch_hostanme(ssh)
    fetch_server_date(ssh)
    fetch_mem_state(ssh)
    fetch_cpu_state(ssh)