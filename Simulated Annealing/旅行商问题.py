import random
import numpy as np

# 坐标数据
coords = np.array([[1304, 2312], [3639, 1315], [4177, 2244], [3712, 1399], [3488, 1535], [3326, 1556], [3238, 1229], [4196, 1004], [4312, 790], [4386, 570], [3007, 1970], [2562, 1756], [2788, 1491], [2381, 1676], [1332, 695], [3715, 1678], [3918, 2179], [4061, 2370], [3780, 2212], [3676, 2578], [4029, 2838], [4263, 2931], [3429, 1908], [3507, 2367], [3394, 2643], [3439, 3201], [2935, 3240], [3140, 3550], [2545, 2357], [2778, 2826], [2370, 2975]])

# 表示一条路径
path = np.arange(len(coords))

# 计算路径长度
def path_length(path):
    dist = 0
    for i in range(len(path) - 1):
        dist += np.linalg.norm(coords[path[i]] - coords[path[i+1]])
    dist += np.linalg.norm(coords[path[-1]] - coords[path[0]])
    return dist

# 模拟退火算法
def simulated_annealing(init_path, init_temp, alpha, max_iter):
    current_path = init_path.copy()
    current_length = path_length(current_path)
    best_path = current_path.copy()
    best_length = current_length
    for i in range(max_iter):
        # 降温
        temp = init_temp * (1 - alpha) ** i
        # 随机扰动路径
        new_path = current_path.copy()
        j, k = random.sample(range(len(new_path)), 2)
        new_path[j], new_path[k] = new_path[k], new_path[j]
        new_length = path_length(new_path)
        # 判断是否接受新路径
        if new_length < current_length:
            current_path = new_path.copy()
            current_length = new_length
            if new_length < best_length:
                best_path = new_path.copy()
                best_length = new_length
        else:
            delta = new_length - current_length
            p = np.exp(-delta / temp)
            if random.random() < p:
                current_path = new_path.copy()
                current_length = new_length
        print(f'Iteration {i}: length={best_length}')
    return best_path, best_length

# 使用模拟退火算法求解最短路径
init_path = np.arange(len(coords))
init_temp = 1000
alpha = 0.99
max_iter = 10000
best_path, best_length = simulated_annealing(init_path, init_temp, alpha, max_iter)
print(f'Best path found by simulated annealing: {best_path}')
print(f'Length of the path: {best_length}')