import numpy as np
import cv2
import scipy.io as scio

# 相机内参
camera1_matrix = np.array(([3.55115955e+03, 0.00000000e+00, 1.06319316e+03],
                         [0.00000000e+00, 3.55054293e+03, 7.91996530e+02],
                         [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]), dtype=np.double)

camera2_matrix = np.array(([3.56061034e+03, 0.00000000e+00, 1.06782843e+03],
						 [0.00000000e+00, 3.56068900e+03, 7.97767769e+02],
						 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]), dtype=np.double)
#相机外参
R_c1_scr = np.array(([ 0.97946873,  0.10918407, -0.1694693 ],
					 [-0.03375905, -0.73993377, -0.67183208],
					 [-0.19874941, 0.66375964, -0.72105604],), dtype=np.double)

T_c1_scr = np.array(([-352.66892836],
 					 [-104.98902428],
					 [ -54.63020171]), dtype=np.double)

# 相机1到相机2的旋转矩阵
R_c1_c2 = np.array(([[ 9.73160646e-01,  1.74109635e-03, -2.30120244e-01],
 					[-7.17643306e-04,  9.99989477e-01,  4.53109116e-03],
 					[ 2.30125711e-01, -4.24433535e-03,  9.73151655e-01]]), dtype=np.double)
# 相机1到相机2的平移向量
T_c1_c2 = np.array(([[82.28949171],
					 [-0.548095  ],
 					 [ 2.99858893]]), dtype=np.double)
# 相机焦距
c1_focal_length = (3.55115955e+03 + 3.55054293e+03) * 0.00345 / 2
c2_focal_length = (3.56061034e+03 + 3.56068900e+03) * 0.00345 / 2
# print(c1_focal_length)
# print(c2_focal_length)

# 读取横竖展开条纹数据
unwrpphase_hor_data = scio.loadmat(r'./unwrpphase_hor_main_pos1.mat')['unwrpphase12']
unwrpphase_ver_data = scio.loadmat(r'./unwrpphase_ver_main_pos1.mat')['unwrpphase12']

# 1、取相机1图像中心点附近的点，减少畸变
p1_pic = np.array([[1000, 600, 1]], dtype=np.int64)

# 2、计算该点在相机1坐标系下的坐标
p1_cam1 = np.dot(np.linalg.inv(camera1_matrix), p1_pic.T) * c1_focal_length
# print(p1_cam1)
# 3、待测点在直线上

best_score = 0 # 记录最好的夹角情况

for m in range(14, 1500): 
	obj_cam1 = p1_cam1 * m # 遍历直线上的点

	# 4、计算相机1图像坐标对应的屏幕坐标,并转换到c1坐标系
	s1_x = int(p1_pic[0][1])-1 
	s1_y = int(p1_pic[0][0])-1
	# s1_lcd = [[unwrpphase_ver_data[int(p1_pic[0][1]-1),int(p1_pic[0][0]-1)]],[unwrpphase_hor_data[int(p1_pic[0][1]-1),int(p1_pic[0][0]-1)]], [0]] # s1的lcd坐标

	s1_lcds = [  # s1的lcd坐标
		[[unwrpphase_ver_data[s1_x,s1_y]], [unwrpphase_hor_data[s1_x,s1_y]], [0]],
		[[unwrpphase_ver_data[s1_x,s1_y+1]], [unwrpphase_hor_data[s1_x,s1_y+1]], [0]],
		[[unwrpphase_ver_data[s1_x+1,s1_y]], [unwrpphase_hor_data[s1_x+1,s1_y]], [0]],
		[[unwrpphase_ver_data[s1_x+1,s1_y+1]], [unwrpphase_hor_data[s1_x+1,s1_y+1]], [0]],
	]
	for s1_lcd in s1_lcds:
		s1_cam1 = np.dot(R_c1_scr, s1_lcd) + T_c1_scr # s1在c1坐标系的坐标

		line_s1_obj = (obj_cam1 - s1_cam1) / np.linalg.norm(obj_cam1 - s1_cam1) # 光线s1
		line_obj_p1 = p1_cam1 / np.linalg.norm(p1_cam1) # 光线t1
		n1 = line_obj_p1 - line_s1_obj # 法线n1

		# 5、计算待测点和LCD点在c2坐标系的坐标，并且计算n2
		obj_cam2 = np.dot(R_c1_c2, obj_cam1) + T_c1_c2 # 待测点在c2坐标系坐标

		p2_pic = np.dot(camera2_matrix, obj_cam2/obj_cam2[2]).reshape(-1, 3) #待测点在c2坐标系坐标

		p2_cam2 = np.dot(np.linalg.inv(camera2_matrix), p2_pic.T) * c2_focal_length

		s2_x = int(p2_pic[0][1])-1 
		s2_y = int(p2_pic[0][0])-1

		# s2_lcd = [[unwrpphase_ver_data[int(p2_pic[0][1]-1),int(p2_pic[0][0]-1)]],[unwrpphase_hor_data[int(p2_pic[0][1]-1),int(p2_pic[0][0]-1)]], [0]] # s2的lcd坐标
	 
		s2_lcds = [  # s2的lcd坐标
			[[unwrpphase_ver_data[s2_x,s2_y]], [unwrpphase_hor_data[s2_x,s2_y]], [0]],
			[[unwrpphase_ver_data[s2_x,s2_y+1]], [unwrpphase_hor_data[s2_x,s2_y+1]], [0]],
			[[unwrpphase_ver_data[s2_x+1,s2_y]], [unwrpphase_hor_data[s2_x+1,s2_y]], [0]],
			[[unwrpphase_ver_data[s2_x+1,s2_y+1]], [unwrpphase_hor_data[s2_x+1,s2_y+1]], [0]],
		]
		for s2_lcd in s2_lcds:
			s2_cam1 = np.dot(R_c1_scr, s2_lcd) + T_c1_scr	# s2在c1坐标系的坐标
			s2_cam2 = np.dot(R_c1_c2, s2_cam1) + T_c1_c2	# s2在c坐标系的坐标

			line_s2_obj = (obj_cam2 - s2_cam2)/np.linalg.norm(obj_cam2 - s2_cam2)  # 光线s2
			line_obj_p2 = p2_cam2 / np.linalg.norm(p2_cam2) # 光线t2

			n2 = line_obj_p2 - line_s2_obj # 法线n2
			n2 = np.dot(np.linalg.inv(R_c1_c2), n2) #将n2转到c1坐标系下

			alpha = (np.dot(n1.T, n2) / (np.linalg.norm(n1)*np.linalg.norm(n2)))[0][0] # 计算n1和n2的夹角
			print(alpha)
			if alpha > best_score:
				best_score = alpha
				best_pos = obj_cam1
print("best_score: ")
print(best_score)
print("best_pos: ")
print(best_pos)