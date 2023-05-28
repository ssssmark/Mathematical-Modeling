import numpy as np
import random
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

# 遗传算法
def genetic_algorithm(pop_size, elite_size, mutation_prob, max_iter):
    # 初始化种群
    population = [np.random.permutation(len(coords)) for _ in range(pop_size)]
    for i in range(max_iter):
        # 计算适应度
        fitness = [1/path_length(p) for p in population]
        # 选择
        elite_indices = np.argsort(fitness)[-elite_size:]
        elite_population = [population[i] for i in elite_indices]
        # 交叉
        children = []
        while len(children) < pop_size - elite_size:
            parent1, parent2 = random.sample(elite_population, 2)
            child = np.zeros(len(coords), dtype=int) - 1
            start, end = sorted(random.sample(range(len(coords)), 2))
            child[start:end+1] = parent1[start:end+1]
            for i in range(len(parent2)):
                if parent2[i] not in child:
                    j = np.where(child == -1)[0][0]
                    child[j] = parent2[i]
            children.append(child)
        # 变异
        for j in range(elite_size, pop_size):
            if random.random() < mutation_prob:
                k, l = random.sample(range(len(coords)), 2)
                population[j][k], population[j][l] = population[j][l], population[j][k]
        # 更新种群
        population = elite_population + children

    best_path = elite_population[-1]
    best_length = path_length(best_path)
    return best_path, best_length

# 使用遗传算法求解最短路径
pop_size = 100
elite_size = 50
mutation_prob = 0.5
max_iter = 100
best_path, best_length = genetic_algorithm(pop_size, elite_size, mutation_prob, max_iter)
print(f'Best path found by genetic algorithm: {best_path}')
print(f'Length of the path: {best_length}')