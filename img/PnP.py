#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 20:09:04 2022

@author: heyike
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 14:39:02 2022

@author: heyike
"""


# 先求屏幕虚像坐标系与相机坐标系之间的相对姿态
# 再使用公式

import cv2
import numpy as np
import math
import scipy.io as scio
from numpy.linalg import  * 
import numba as nb


# 相机内参
camera_matrix = np.array(([[5.17815542e+03, 0.00000000e+00, 1.55127215e+03],
 						   [0.00000000e+00, 5.17299829e+03, 1.07728290e+03],
 						   [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]), dtype=np.double)

# 相机畸变
dist_coefs = np.array([[-0.04146919, 0.28286445, -0.0018283, 0.00089619, 0.27079089]], dtype=np.double)

# 读取横竖展开条纹数据
unwrpphase_hor_data = scio.loadmat(r'./pos1_h.mat')['unwrpphase12']
unwrpphase_ver_data = scio.loadmat(r'./pos1_v.mat')['unwrpphase12']

g_min = 1000

# 获取2D上4点的空间坐标，
# 300<=X<=800,  600<=Y<=1500[ 844,  476],
# @nb.jit(nopython=True)
def Calc():
	ranges = np.array([[1100, 2000], [680, 1200]])
	aaa=np.array(np.random.randint(ranges[:, 0], ranges[:, 1], size=(4000, 2)))      
	object_2d_points = np.array((aaa), dtype=np.double)
	# print(object_2d_points)

	#自动计算对应的3D坐标,默认镜面为世界坐标系z=0
	object_3d_points = np.array(
	    tuple(([unwrpphase_ver_data[int(object_2d_points[i][1]-1),int(object_2d_points[i][0]-1)],unwrpphase_hor_data[int(object_2d_points[i][1]-1),int(object_2d_points[i][0]-1)], 0] for i in range(len(object_2d_points))))
	    ,dtype=np.double)
	# print(object_3d_points)
	# 求解相机位姿
	found, rvec, tvec, _ = cv2.solvePnPRansac(object_3d_points, object_2d_points, camera_matrix, dist_coefs, flags=0)
	# 获取相机的旋转矩阵
	rotM = cv2.Rodrigues(rvec)[0]


	# print('旋转矩阵:')
	# print(rotM)
	# print('平移向量:')
	# print(tvec)

	# 选取一个点进行验证,点是图像坐标
	ranges2 = np.array([[1100, 2000], [680, 1200]])

	bbb=np.array(np.random.randint(ranges2[:, 0], ranges2[:, 1], size=(100, 2)))  
	test_point = np.array((bbb), dtype=np.double)

	#print('检测点的真实图像坐标：')
	#print(test_point)

	test_point_3d = np.array(
	    tuple(([unwrpphase_ver_data[int(test_point[i][1]-1),int(test_point[i][0]-1)],unwrpphase_hor_data[int(test_point[i][1]-1),int(test_point[i][0]-1)], 0,1] for i in range(len(test_point))))
	    ,dtype=np.float32)

	# print('误差:')
	#pixel = np.dot(camera_matrix, Out_matrix)
	#pixel1 = np.dot(pixel, test_point_3d)
	#pixel2 = pixel1/pixel1[2]    
	#print(pixel2[:-1])
	#print(object_2d_points.shape)
	error=0
	for i in range(len(test_point)):
	    b=test_point[i]
	    Out_matrix = np.concatenate((rotM, tvec), axis=1)
	    pixel = np.dot(camera_matrix, Out_matrix)
	    pixel1 = np.dot(pixel, test_point_3d[i])
	    pixel2 = pixel1/pixel1[2]
	    a=pixel2[:-1]
	    c=np.abs(b-a)
	    d=c[0]+c[1]
	    error=error+d

	error_avg=error/100    
	print(error_avg)
	return error_avg, rotM, tvec

for kk in range(1000):
	val,rotM,tvec = Calc()
	if g_min > val:
		g_min = val 
		xuanzhuan = rotM
		pingyi = tvec
print("最小值")
print(g_min)
print(rotM)
print(tvec)
