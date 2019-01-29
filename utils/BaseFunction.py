__author__ = "JentZhang"

import os


def get_filePath_fileName_fileExt(fileUrl):
    """
    获取文件路径， 文件名， 后缀名
   :param fileUrl:
   :return:
    """
    filepath, tmpfilename = os.path.split(fileUrl)
    shotname, extension = os.path.splitext(tmpfilename)

    return filepath, shotname, extension


def get_random_code(length=6):
    """
    生成数字随机验证码
    :param length:验证码的长度
    :return:
    """
    import random
    res = ''
    for i in range(length):
        res += str(random.randint(1, 9))
    return res


if __name__ == '__main__':
    filepath, shotname, extension = get_filePath_fileName_fileExt('test.txt')
    print(filepath)
    print(shotname)
    print(extension)
