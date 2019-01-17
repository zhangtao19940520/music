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


if __name__ == '__main__':
    filepath, shotname, extension = get_filePath_fileName_fileExt('test.txt')
    print(filepath)
    print(shotname)
    print(extension)
