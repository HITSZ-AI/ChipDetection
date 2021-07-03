import os
import cv2

#工具类，如导出TXT函数、保存图片等功能函数
def is_number(s):
    if s == '':
        return False
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包
        for i in s:
            unicodedata.numeric(i)  # 把一个表示数字的字符串转换为浮点数返回的函数
            # return True
        return True
    except (TypeError, ValueError):
        pass
    return False


def converStr2float(s):
    if is_number(s):
        return float(s)
    else:
        return -1.0


def converStr2Int(s):
    if is_number(s):
        return int(float(s))
    else:
        return -1


def CreateTxtFileTail(imgPath):
    with open(imgPath, 'a') as file_handle:
        file_handle.write('ENDSTR')  # 开始写入数据
        file_handle.write('\n')  # 自动换行
        file_handle.write('ENDLIB')
        file_handle.write('\n')
    return 0


def CreateTxtFile(imgPath,row_index, col_index, col_end):

    vertex1 = str(col_index) + ':' + str(row_index)
    vertex2 = str(col_end) + ':' + str(row_index)
    with open(imgPath, 'a') as file_handle:
        # file_handle.write('BOUNDARY')  # 开始写入数据
        file_handle.write('\n')  # 自动换行
        file_handle.write('PATH\n')
        file_handle.write('LAYER 50\n')
        file_handle.write('DATATYPE 0\n')
        # 给甲方的时候 WIDTH=10 ,WIDTH=1代表0.002um 一个像素点对应0.02um
        file_handle.write('WIDTH 1\n')
        file_handle.write('XY' + ' ' + vertex1)  # 左上角顶点
        file_handle.write('\n')
        file_handle.write(vertex2)  # 右上角顶点
        file_handle.write('\n')
        file_handle.write('ENDEL')
        file_handle.write('\n')
    return 0

def CreateTxtFileHead(imgPath):
    with open(imgPath, 'w') as file_handle:
        file_handle.write('HEADER 600 ')  # 开始写入数据
        file_handle.write('\n')  # 自动换行
        file_handle.write('BGNLIB 3/10/2021 17:35:23 3/10/2021 17:35:23 ')
        file_handle.write('\n')
        file_handle.write('LIBNAME DEFAULT')
        file_handle.write('\n')
        file_handle.write('UNITS 0.001 1e-009')
        file_handle.write('\n')
        file_handle.write('         ')
        file_handle.write('\n')
        file_handle.write('BGNSTR 3/10/2021 17:35:23 3/10/2021 17:35:23 ')
        file_handle.write('\n')
        file_handle.write('STRNAME VIA1')
        file_handle.write('\n')
        file_handle.write('         ')
        file_handle.write('\n')
    return 0

def SaveBinaryImage(image,path):
    content, tempfilename = os.path.split(path)
    # 拼接文件名
    filename, extension = os.path.splitext(tempfilename)
    filename = filename + str('_binary') + extension
    content=content+"/BinaryImg"
    if not os.path.exists(content):  # 如果不存在路径，则创建这个路径
        os.makedirs(content)
    filepath = os.path.join(content, filename)
    filepath = filepath.replace('\\', '/')
    print(filepath)
    cv2.imwrite(filepath, image)
    return filepath

def SaveBinaryLocalityImage(image,path):
    content, tempfilename = os.path.split(path)
    # 拼接文件名
    filename, extension = os.path.splitext(tempfilename)
    filename = filename + str('_binary_locality') + extension
    content = content + "/LocalBinaryImg"
    if not os.path.exists(content):  # 如果不存在路径，则创建这个路径
        os.makedirs(content)
    filepath = os.path.join(content, filename)
    filepath = filepath.replace('\\', '/')
    print(filepath)
    cv2.imwrite(filepath, image)
    return filepath

def SaveRGBDiffImage(image,path):
    content, tempfilename = os.path.split(path)
    # 拼接文件名
    filename, extension = os.path.splitext(tempfilename)
    filename = filename + str('_RGBDiff') + extension
    content=content+"/RGBImg"
    if not os.path.exists(content):  # 如果不存在路径，则创建这个路径
        os.makedirs(content)
    filepath = os.path.join(content, filename)
    filepath = filepath.replace('\\', '/')
    print(filepath)
    cv2.imwrite(filepath, image)
    return filepath

def SaveRGBDiffLocalityImage(image,path):
    content, tempfilename = os.path.split(path)
    # 拼接文件名
    filename, extension = os.path.splitext(tempfilename)
    filename = filename + str('_RGBDiff_locality') + extension
    content=content+"/RGBLocalImg"
    if not os.path.exists(content):  # 如果不存在路径，则创建这个路径
        os.makedirs(content)
    filepath = os.path.join(content, filename)
    filepath = filepath.replace('\\', '/')
    print(filepath)
    cv2.imwrite(filepath, image)
    return filepath

def SaveHSVTractImage(image,path):
    content, tempfilename = os.path.split(path)
    print(content)
    # 拼接文件名
    filename, extension = os.path.splitext(tempfilename)
    filename = filename + str('_HSVTract') + extension
    #filepath = os.path.join(content,"/HsvImg")
    content=content+"/HsvImg"
    if not os.path.exists(content):  # 如果不存在路径，则创建这个路径
        os.makedirs(content)
    filepath=os.path.join(content,filename)
    filepath = filepath.replace('\\', '/')
    print(filepath)
    cv2.imwrite(filepath, image)
    return filepath

def SaveHSVTractLocalityImage(image,path):
    content, tempfilename = os.path.split(path)
    # 拼接文件名
    filename, extension = os.path.splitext(tempfilename)
    filename = filename + str('_HSCTract_locality') + extension
    content = content + "/LocalHSVImg"
    if not os.path.exists(content):  # 如果不存在路径，则创建这个路径
        os.makedirs(content)
    filepath = os.path.join(content, filename)
    filepath = filepath.replace('\\', '/')
    print(filepath)
    cv2.imwrite(filepath, image)
    return filepath

def Save_RGB_Image(image,path):
    content, tempfilename = os.path.split(path)
    # 拼接文件名
    filename, extension = os.path.splitext(tempfilename)
    filename = filename + str('_binary') + extension
    filepath = os.path.join("../images/ImgSave", filename)
    filepath = filepath.replace('\\', '/')
    print(filepath)
    cv2.imwrite(filepath, image)