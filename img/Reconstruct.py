from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2
from sympy import *
import random
import scipy.io as scio
import sys

pos_array = np.load("mask_concave_pos_array.npy")
gradient_array = np.load("mask_concave_gradient_array.npy")

# 前36项Zernike多项式
x, y = symbols('x, y')
Zernike_Ploy = np.array(([[
        1, x, y, -1+2*(x*x+y*y),

        x*x-y*y, 2*x*y, (-2+3*x*x+3*y*y)*x, (-2+3*x*x+3*y*y)*y,

        1-6*(x*x+y*y)+6*(x*x+y*y)**2, x**3-3*x*y*y, 3*x*x*y-y**3]]))


# a = np.array(([[ 0.00000000e+00,  1.18103958e-07, -9.08159177e-08,  4.70057552e-08,
#   -3.28452416e-06, -8.99055948e-07,  3.59975965e-05, -2.83824912e-05,
#    7.57180355e-06,  1.41369990e-05,  3.50138262e-05, -1.45772457e-06,
#    1.13310966e-05,  2.74055631e-07,  3.41010545e-07,  2.81789554e-09,
#    1.72132907e-06,  1.28389584e-06,  7.18981379e-09,  3.34430092e-09,]]), dtype=np.double) #20隔5

# a = np.array(([[ 0.00000000e+00 , 1.31399954e-07 ,-9.95428583e-08 ,-4.47747081e-07,
#   -3.76217944e-06, -7.22069095e-07,  3.22139238e-05, -1.99335911e-05,
#    8.32246892e-06,  2.95469280e-05,  4.65408699e-05, -8.28335512e-07,
#    1.00188541e-05,  2.82568027e-07,  3.36005753e-07,  2.84180269e-09,]]), dtype=np.double) #16隔5

a = np.array(([[ 0.00000000e+00,  1.13521661e-02, -9.11508827e-03,  9.63433581e-03,
  -5.27327014e-03,  1.64783995e-02,  2.12979545e-04,  3.00103978e-04,
   1.15968247e-06, -1.49209777e-04,  4.65696670e-05]]), dtype=np.double) #13隔1  

fig = plt.figure()  # 定义新的三维坐标轴
ax3 = plt.axes(projection='3d')
# 定义三维数据
xx = np.arange(450, 750, 1)
yy = np.arange(750, 1070, 1)
X, Y = np.meshgrid(xx, yy)

# 保存多项式的计算结果
Z_list = []

# 带系数的多项式表达式
Z = np.dot(a, Zernike_Ploy.T)[0][0]

# 第一次计算，将计算结果保存下来
def Calculate_first():
    z_min = sys.maxsize
    z_max = -sys.maxsize-1
    for p_y in yy:
        list1 = []
        for p_x in xx:
            g_x = pos_array[p_x][p_y][0]
            g_y = pos_array[p_x][p_y][1]
            print(p_y, p_x)
            if g_x != 0 and g_y != 0:  # 点在镜面上
                res = Z.subs({x: g_x, y: g_y})  # 将x、y值带入多项式
                if res > z_max:  # 寻找结果的最大、最小值
                    z_max = res
                if res < z_min:
                    z_min = res
            else:  # 点不在镜面上，将结果赋值为0
                res = nan
            # print(res)
            list1.append(res)
        Z_list.append(list1)
    print(z_min, z_max)
    Z_array = np.array(Z_list, dtype=np.double)
    ax3.plot_surface(X, Y, Z_array, cmap='rainbow')
    plt.show()
    np.save("11隔1.npy",Z_array) # 保存结果

# 以后的计算，直接调用第一次的结果
def Calculate_next():
    Z_array = np.load("m11隔1.npy")
    # 将非镜面点的值变成最大值，便于观察
    for i in range(len(Z_array)):
        for j in range(len(Z_array[i])):
            if Z_array[i][j] == 0:
                Z_array[i][j] = nan
    # ax3.set_zlim(-2 , 8)    # 设置Z轴范围
    ax3.plot_surface(X, Y, Z_array, cmap='rainbow')
    plt.show()


# Calculate_first()
Calculate_next()