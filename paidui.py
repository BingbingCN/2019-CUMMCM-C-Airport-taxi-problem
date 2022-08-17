# 排队论

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'

total_time = 10  # 总时间
N = 10000000000  # 最大队列长度
# 到达率与服务率
lambd = 10
mu = 6

arr_mean = 1/lambd
ser_mean = 1/mu
arr_num = round(total_time*lambd*2)

# 按负指数分布产生各顾客达到时间间隔
customer_time = np.random.exponential(arr_mean, arr_num)
# 各顾客的到达时刻等于时间间隔的累积和
customer_time = np.array(np.cumsum(customer_time))
# 按负指数分布产生各顾客服务时间
serve_time = np.random.exponential(ser_mean, arr_num)
customer_num = np.sum(customer_time <= total_time)

# 计算第 1个顾客的信息
wait_time = np.zeros(customer_num)
wait_time[0] = 0
# 其离开时刻等于其到达时刻与服务时间之和
all_time = np.zeros(customer_num)
all_time[0]= customer_time[0] + wait_time[0]
# 此时系统内共有
system_customer = np.zeros(customer_num)
system_customer[0] = 1
member = [0]
number=0
for i in range(1, arr_num):
    # 如果第 i个顾客的到达时间超过了仿真时间，则跳出循环
    if customer_time[i] > total_time:
        break
    else:
        for j in member:
            #已经服务乘客的数量
            if all_time[j] > customer_time[i]:
                number = number + 1
        # 系统已满
        if number >= N+1:
            system_customer[i] = 0
        # 系统未满
        else:
            if number == 0:
                wait_time[i] = 0
                all_time[i] = customer_time[i] + serve_time[i]
                system_customer[i] = 1
                member.append(i)
            else:
                len_men = len(member)
                wait_time[i] = all_time[member[len_men-1]] - customer_time[i]
                all_time[i] = all_time[member[len_men-1]] + serve_time[i]
                system_customer[i] = number + 1
                member.append(i)

len_men = len(member)

# 绘图
y = np.arange(0, len_men, 1)
plt.plot(customer_time[0:len_men], y, 'b', label='arrive time')
plt.plot(all_time, y, 'r4--', label='leave time')
plt.legend()
plt.grid()
plt.show()
plt.plot(wait_time,'y', label='wait time')
plt.plot(serve_time[0:len_men] + wait_time, 'g4--', label='stop time')
plt.legend()
plt.grid()
plt.show()
