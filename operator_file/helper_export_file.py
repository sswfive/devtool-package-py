"""
# @Time     : 2022/3/1 8:03 上午
# @Author   : ssw
# @File     : helper_export_file.py
# @Desc      : 导出文件
"""
import hashlib
import os
import zipfile
from shutil import rmtree, move


class File:

    def export_zip_files(self, dirpath):
        """查询导出文件"""
        import os
        import zipfile
        from io import BytesIO
        try:
            memory_file = BytesIO()
            dsplit = dirpath.split('\\')
            dname = None
            if len(dsplit) >= 2:
                dname = dsplit[-2]
            with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
                for path, dirnames, filenames in os.walk(dirpath):
                    if dname:
                        hr = path.split(dname, 1)
                        for filename in filenames:
                            zf.write(os.path.join(path, filename), os.path.join(*hr[1].split('\\'), filename))
                    else:
                        for filename in filenames:
                            zf.write(os.path.join(path, filename))
                # zf.setpassword("kk-123456".encode('utf-8'))
            memory_file.seek(0)
            return memory_file, None
        except Exception as e:
            return None, str(e)



def read_file(file_path):
    """读取文本文件内容"""
    all_line = None
    try:
        if exists(file_path):
            fsock = open(file_path, "r")
            all_line = fsock.readlines()
            fsock.close()
    except:
        pass
    return all_line


# # 这个好像有点问题，无法执行也不报错！！！！！
# def read_file_line(file_path, encoding='utf-8'):
#     # print('路径:', file_path)
#     if not exists(file_path):
#         return
#     with open(file_path, 'r', encoding=encoding) as f:
#         while True:
#             block = f.readline()
#             # print(block)
#             if not block.find('android-qingtingfm'):
#                 print(block)
#             if block:
#                 yield block
#             else:
#                 return


def save_file(file_path, content, encoding='utf-8'):
    """保存内容到文件里"""
    try:
        file_object = open(file_path, 'a', encoding=encoding)
        file_object.write(content)
        file_object.close()
        return True
    except Exception as e:
        return False


def remove_file(file_path):
    """删除文件"""
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            return True
    except:
        pass
    return False


def remove_all_file(file_list):
    """批量删除文件"""
    try:
        for file_path in file_list:
            remove_file(file_path)
    except:
        pass


def exists(file_path):
    """检查文件是否存在"""
    return os.path.exists(file_path)


# def read_file_line(ssss,sds):
#     print('暑促',ssss)

def get_file_path_name_ext(file_path):
    """
    获取文件路径， 文件名， 后缀名
    :param file_path:
    :return:
    """
    filepath, tmpfilename = os.path.split(file_path)
    shotname, extension = os.path.splitext(tmpfilename)
    return filepath, shotname, extension


# 解压单个文件到目标文件夹
def unzip_file(src_file, dest_dir, password=None):
    result = []

    if password:
        password = password.encode()
    zf = zipfile.ZipFile(src_file)

    temp_path = dest_dir + "/__temp"
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    try:
        for file_path in zf.namelist():
            # apple cache skip
            if zf.getinfo(file_path).file_size <= 0 or "__MACOSX" in file_path:
                continue

            # get the real path
            try:
                file_path_final = file_path.encode('cp437').decode('utf-8')
            except:
                file_path_final = file_path.encode('cp437').decode('gbk', 'ignore')
            file_path_final = dest_dir + "/" + file_path_final

            # extract
            file_path = zf.extract(file_path, temp_path)

            # move to real path
            if not os.path.exists(os.path.dirname(file_path_final)):
                os.makedirs(os.path.dirname(file_path_final))
            move(file_path, file_path_final)

            result.append(file_path_final)
        return result
    finally:
        # delete temp file
        rmtree(temp_path)
        zf.close()


def zip_dir(dirpath, outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()


# 判断文件目录是否存在，不存在则创建
def create_if_dir_no_exists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def enum_path_files(path):
    """
     遍历目录（子目录），返回所有文件路径
    :param path: file path
    :return: file list
    """
    file_paths = []
    if not os.path.isdir(path):
        print('Error:"', path, '" is not a directory or does not exist.')
        return
    list_dirs = os.walk(path)
    for root, dirs, files in list_dirs:
        for f in files:
            file_paths.append(os.path.join(root, f))
    return file_paths

# url 路径拼接
def url_join(par_url, sub_url):
    if par_url.endswith("/"):
        if sub_url.startswith(("/")):
            sub_url = sub_url[1:]
    else:
        if not sub_url.startswith(("/")):
            sub_url = "/" + sub_url
    return par_url + sub_url


# 获取md5代码
def get_MD5_code(str):
    hash_md5 = hashlib.md5()
    # 计算
    str = str.encode('utf-8', errors='ignore')
    hash_md5.update(str)
    # 获取计算结果(16进制字符串，32位字符)
    md5_str = hash_md5.hexdigest()
    # 打印结果
    # print(md5_str)
    return md5_str

if __name__ == '__main__':
    print('sdfsdfs')
    # read_file_linessssssssssss('4485.log', 'utf-8')