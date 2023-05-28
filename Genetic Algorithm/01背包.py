import random
import math

# 定义物品质量和价值
weights = [2, 5, 18, 3, 2, 5, 10, 4, 11, 7, 14, 6]
values = [5, 10, 13, 4, 3, 11, 13, 10, 8, 16, 7, 4]
#基因长度
gene_length=len(weights)
# 背包最大容量
max_weight = 46
# 迭代次数
iterations=100
def GA():
    # 种群大小
    population_size=100

    # 交叉率和变异率
    crossover_rate=0.5
    mutation_rate=0.5

    # 初始化种群，生成population_size个长度与weight相同的二进制串，表示货物i是否入选
    population=[[random.randint(0,1) for _ in range(len(weights))] for _ in range(population_size)]

    # 适应度函数为背包内商品的总价值
    fitness=[]
    for j in range(population_size):
        fitness.append(sum(values[i]*population[j][i] for i in range(len(values))))
    for _ in range(iterations):
        # 选择父母
        parents=[]
        for _ in range(population_size):
            index1, index2 = random.sample(range(population_size), 2)
            parent1 = population[index1] if fitness[index1] > fitness[index2] else population[index2]
            index3, index4 = random.sample(range(population_size), 2)
            parent2 = population[index3] if fitness[index3] > fitness[index4] else population[index4]
            parents.append((parent1, parent2))

        # 交叉产生下一代
        new_population=[]
        for i in range(population_size//2):
            parent1, parent2 = parents[i]
            child1 = parent1[:]
            child2 = parent2[:]
            if random.random() < crossover_rate:
                index = random.randint(1, len(weights) - 2)
                #交叉
                child1[index:], child2[index:] = child2[index:], child1[index:]
            new_population.append(child1)
            new_population.append(child2)

        #变异
        for i in range(population_size):
            for j in range(len(weights)):
                if random.random()<mutation_rate:
                    # 以一定概率变异，1变成0,0变成1
                    new_population[i][j]=1-new_population[i][j]
        # 把祖先和生成的子类放在一起进行排序，选出50个适合度最好的作为进化优胜者，作为下一轮迭代的新祖先
        population+=new_population
        # 删除不符合要求的元素
        for gene in population:
            if sum(weights[j]*gene[j] for j in range(gene_length))>max_weight:
                population.remove(gene)
        # 计算每一行的value之和
        row_values = [sum([population[i][j] * values[j] for j in range(gene_length)]) for i in range(population_size)]
        sorted_population = [x for _, x in sorted(zip(row_values, population), key=lambda pair: pair[0], reverse=True)]
        #按照排名生成下一代种群
        population=sorted_population[:population_size]

    fitness = [sum([values[i] * population[j][i] for i in range(len(values))]) for j in range(population_size)]
    allweight=[sum([weights[i] * population[j][i] for i in range(len(values))]) for j in range(population_size)]
    max_correct=0
    bestindex=0
    for i in range(population_size):
        if allweight[i]<=max_weight:
            if max_correct<fitness[i]:
                bestindex=i
                max_correct=fitness[i]

    best_solution=population[bestindex]
    best_weight = sum([weights[i] * best_solution[i] for i in range(len(weights))])
    best_value = sum([values[i] * best_solution[i] for i in range(len(values))])

    return best_solution,best_weight,best_value

print("Genetic Algorithm:")

solution, weight, value = GA()
print("Selected Items:", [i + 1 for i in range(len(solution)) if solution[i]])
print("Total Weight:", weight)
print("Total Value:", value)

