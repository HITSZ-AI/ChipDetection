import numpy as np
import cv2

#对读入的图像进行单一阈值的二值化处理
def image_binarization(image,Threshold):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #指定阈值 灰度二值化
    retval, dst = cv2.threshold(gray, Threshold, 255, cv2.THRESH_BINARY)
    # 最大类间方差法(大津算法)，thresh会被忽略，自动计算一个阈值
    #retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #中值去噪，也称为椒盐去噪
    blur = cv2.medianBlur(dst, 5)
    return blur


# 通道差值处理函数
def ChDiffExtract(img, d):
    # 遍历方法太慢，最好不要使用
    # for i in range(img.shape[0]):
    #     for j in range(img.shape[1]):

    # 按照第三维取最大数组和最小数组，用于计算标志位
    max_RGB = np.amax(img, axis=2)
    min_RGB = np.amin(img, axis=2)
    # 分别获取三个标志位矩阵，将其相乘,得到最终的标志位矩阵
    diff_RGB = ((max_RGB - min_RGB) < d)
    max_RGB = (max_RGB < 150)
    min_RGB = (min_RGB > 50)
    rec_RGB = (diff_RGB * max_RGB * min_RGB)
    # 不能用标志矩阵直接和img三维数组相乘，与numpy数组存在一定差异
    # img=(img*diff_RGB)
    img[:, :, 0] = img[:, :, 0] * rec_RGB
    img[:, :, 1] = img[:, :, 1] * rec_RGB
    img[:, :, 2] = img[:, :, 2] * rec_RGB
    # img[img > 0] = 255
    return img  # 数组参数，已经在内存中修改，返回与否不影响了

#将图像转换到HSV颜色通道上进行线路提取
def HSV_Line_Tract(image,h_1_Start,h_1_End,h_2_Start,h_2_End,s_1_Start,s_1_End,s_2_Start,s_2_End,v_1_Start,v_1_End,v_2_Start,v_2_End):
    HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    H_Channel_Flag = ((h_1_Start * 180 <= HSV[:, :, 0]) & (HSV[:, :, 0] < h_1_End * 180)) | (
                (h_2_Start * 180 <= HSV[:, :, 0]) & (HSV[:, :, 0] < h_2_End * 180))
    S_Channel_Flag = (s_1_Start * 255 <= HSV[:, :, 1]) & (HSV[:, :, 1] < s_1_End * 255) | (
                s_2_Start * 255 <= HSV[:, :, 1]) & (HSV[:, :, 1] < s_2_End * 255)
    V_Channel_Flag = (v_1_Start * 255 <= HSV[:, :, 2]) & (HSV[:, :, 2] < v_1_End * 255) | (
                (v_2_Start * 255 <= HSV[:, :, 2]) & (HSV[:, :, 2] < v_2_End * 255))

    # hsv_flag_h = (HSV[:,:, 0] > 0.5*180) & (HSV[:,:, 0] < 0.56*180)
    # hsv_flag_v =  HSV[:,:, 2] > 0.6*255
    # num_flag = np.array(~(hsv_flag_h | hsv_flag_v), dtype='uint8')

    num_flag_2 = H_Channel_Flag & V_Channel_Flag & S_Channel_Flag
    num_flag = np.array(num_flag_2, dtype='uint8')
    contextflag = np.expand_dims(num_flag, axis=2)
    HSV = HSV * contextflag
    new_image = cv2.cvtColor(HSV, cv2.COLOR_HSV2RGB)
    return  new_image