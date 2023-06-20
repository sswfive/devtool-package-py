"""
@Time    : 2023/6/20
@Author  : ssw
@File    : ftp.py
@Desc    :
"""

import shutil
import os
import time
import ftplib
import ftputil


# import socket


class FtpHelper:
    # socket.setdefaulttimeout(999999)
    ftp = ftplib.FTP(timeout=999999)
    IsDir = False
    path = ""

    def __init__(self, host, port=21):
        self.host = host
        # self.ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
        # self.ftp.set_pasv(0)      #0主动模式 1 #被动模式
        self.ftp.connect(host, port)

    def login(self, user, passwd):
        # self.pool.submit(self.ftp.login,user, passwd)
        print(self.ftp.login(user, passwd))
        # self.ftp_host = self.pool.submit(ftputil.FTPHost,self.host, user, passwd).result()
        self.ftp_host = ftputil.FTPHost(self.host, user, passwd)

    def download_file(self, local_file, remote_file):
        file_handler = open(local_file, 'wb')
        self.ftp.retrbinary(f"RETR: {remote_file}", file_handler.write)
        file_handler.close()
        return True

    def upload_file(self, local_file, remote_file):
        if os.path.isfile(local_file) is False:
            return False
        file_handler = open(local_file, "rb")
        self.ftp.storbinary(f'STOR: {remote_file}', file_handler, 4096)
        file_handler.close()
        return True

    def upload_file_tree(self, local_dir, remote_dir):
        if os.path.isdir(local_dir) is False:
            return False
        local_names = os.listdir(local_dir)
        # 先在远端创建目录
        self.ftp.mkd(remote_dir)
        self.ftp.cwd(remote_dir)
        for loc in local_names:
            src = os.path.join(local_dir, loc)
            if os.path.isdir(src):
                self.upload_file_tree(src, loc)
            else:
                self.upload_file(src, loc)

        self.ftp.cwd("..")
        return

    def download_file_tree(self, local_dir, remote_dir):
        if os.path.isdir(local_dir) is False:
            os.makedirs(local_dir)
        self.ftp.cwd(remote_dir)
        remote_names = self.ftp.nlst()
        for file in remote_names:
            loc = os.path.join(local_dir, file)
            print(self.is_dir(file))
            if self.is_dir(file):
                self.download_file_tree(loc, file)
            else:
                self.download_file(loc, file)
        self.ftp.cwd("..")
        return

    def synchro_file_tree_2_ftp(self, local_dir, remote_dir):
        if os.path.isdir(local_dir) is False:
            return False
        local_names = os.listdir(local_dir)
        try:
            self.ftp_host.rmtree(remote_dir)
        except:
            print("删除失败")
        self.ftp.mkd(remote_dir)
        self.ftp.cwd(remote_dir)
        for loc in local_names:
            src = os.path.join(local_dir, loc)
            if os.path.isdir(src):
                self.upload_file_tree(src, loc)
            else:
                self.upload_file(src, loc)

        self.ftp.cwd("..")

        return

    def synchro_file_tree_2_local(self, local_dir, remote_dir):
        if os.path.isdir(local_dir) is False:
            os.makedirs(local_dir)
        else:
            shutil.rmtree(local_dir)
            os.makedirs(local_dir)
        self.ftp.cwd(remote_dir)
        remote_names = self.ftp.nlst()
        for file in remote_names:
            loc = os.path.join(local_dir, file)
            if self.is_dir(file):
                self.download_file_tree(loc, file)
            else:
                self.download_file(loc, file)
        self.ftp.cwd("..")
        return

    def get_dic_size(self, path):
        size = 0
        for i in self.ftp_host.listdir(path):
            if self.is_dir(path + '/' + i):
                size += self.get_dic_size(path + '/' + i)
            else:
                size += self.ftp_host.lstat(path + '/' + i).st_size
        return size

    def get_file_dic(self):
        ftp_file_dic = {}
        for f in self.ftp_host.listdir("."):
            if self.is_dir(f):
                print(f)
                info = self.ftp_host.lstat(f)
                ftp_file_dic[f] = [info.st_mtime, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info.st_mtime)),
                                   self.get_dic_size(f)]
            else:
                info = self.ftp_host.lstat(f)
                # print(self.ftp_host.lstat(f))
                ftp_file_dic[f] = [info.st_mtime, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info.st_mtime)),
                                   info.st_size]
        return ftp_file_dic

    def is_dir(self, path):
        if self.ftp_host.path.isdir(path):
            return True

    def close(self):
        self.ftp.quit()


if __name__ == "__main__":
    ftp = FtpHelper('10.16.10.128')
    ftp.login('ft', 'password')
    print(ftp.get_dic_size('del'))
    # ftp.get_file_dic()
    # print(ftp.ftp_host.stat('dir4'))

    # 下载时候远端地址不需要/
    # ftp.DownLoadFileTree('file/del', 'del')  # ok
    # 上传时候远端地址要用绝对地址
    # ftp.UpLoadFileTree('file/dir1', "dir1")
    # print(ftp.isDir('del'))
