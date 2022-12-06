m,t = input("请输入星期几、几点钟(空格隔开):").split()
m = int(m)
t = int(t)
if m != 6 and m != 7:
    if t>=900 and t < 1900:
        print("工作日：工作")
    elif t>=1900 and t<2400:
        print("工作日：休息")    
    else :
        print("工作日：睡觉")
else:
    if t>=0 and t <= 1200:
        print("周末：睡觉")
    else:
        print("周末：玩儿")
