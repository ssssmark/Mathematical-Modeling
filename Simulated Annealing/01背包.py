import random
import math

# 物品列表（每个物品表示为一个元组，包括物品编号、价值和重量）
items = [(1, 5, 2), (2, 10, 5), (3, 13, 18), (4, 4, 3), (5, 3, 2), (6, 11, 5),
         (7, 13, 10), (8, 10, 4), (9, 8, 11), (10, 16, 7), (11, 7, 14), (12, 4, 6)]

# 包的最大允许质量
CAPACITY = 46

# 初始温度
INITIAL_TEMPERATURE = 1000

# 冷却速率
COOLING_RATE = 0.99

# 迭代次数
ITERATIONS = 10000


def evaluate(solution):
    """
    计算方案的总价值和总重量
    """
    total_value = sum(items[i][1] for i in range(len(solution)) if solution[i])
    total_weight = sum(items[i][2] for i in range(len(solution)) if solution[i])

    return total_value, total_weight


def get_neighbor(solution):
    """
    获取一个邻居方案，即随机选取一个物品进行翻转（加入或移除）
    """
    neighbor = solution[:]
    i = random.randint(0, len(neighbor) - 1)
    neighbor[i] = not neighbor[i]
    return neighbor


def acceptance_probability(current_value, new_value, temperature):
    """
    计算接受新方案的概率，根据模拟退火算法的公式
    """
    if new_value > current_value:
        return 1.0
    else:
        return math.exp((new_value - current_value) / temperature)


def simulated_annealing():
    """
    模拟退火算法求解问题
    """
    # 随机生成一个初始方案
    current_solution = [random.choice([True, False]) for _ in range(len(items))]

    # 初始化温度
    temperature = INITIAL_TEMPERATURE

    # 迭代搜索
    for i in range(ITERATIONS):
        # 生成一个邻居方案
        neighbor = get_neighbor(current_solution)

        # 计算当前方案和邻居方案的总价值和总重量
        current_value, current_weight = evaluate(current_solution)
        neighbor_value, neighbor_weight = evaluate(neighbor)

        # 判断是否接受邻居方案

        if acceptance_probability(current_value, neighbor_value, temperature) > random.random() and neighbor_weight<CAPACITY:
            current_solution = neighbor

        # 降低温度
        temperature *= COOLING_RATE

    # 返回最终的最优方案及其总价值和总重量
    best_solution = current_solution
    best_value, best_weight = evaluate(best_solution)
    return best_solution, best_value, best_weight


# 调用模拟退火算法求解问题
best_solution, best_value, best_weight = simulated_annealing()

# 输出结果
print("最优方案：", [i+1 for i in range(len(best_solution)) if best_solution[i]])
print("总价值：", best_value)
print("总重量：", best_weight)