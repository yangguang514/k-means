from sklearn.cluster import KMeans
import psycopg2
import math
import random
import numpy as np
from decimal import Decimal
import matplotlib.pyplot as plt
from shapely.wkb import loads
from statistics import mean


# 定义空间单元类（示例）
class SpaceUnit:
    def __init__(self, city_name, r_densit_3):
        self.city_name = city_name
        self.r_densit_3 = r_densit_3

    def __repr__(self):
        return f"SpaceUnit(city_name={self.city_name}, r_densit_3={self.r_densit_3})"


# 计算两个空间单元之间的距离（示例）
def calculate_distance(r_densit_3_1, space_unit2):
    r_densit_3_2 = space_unit2.r_densit_3

    distance = abs(r_densit_3_1 - r_densit_3_2)
    return distance


# 定义领接矩阵
def has_adjacency(city, city_set, matrix):
    for adjacency in matrix:
        if adjacency[0] == city and adjacency[1] in city_set:
            if adjacency[2]:  # 检查邻接关系是否为 True
                return True
    return False


# 更新聚类中心
def calculate_updated_cluster_centers(cluster_assignments):
    updated_centers = []
    for cluster in cluster_assignments:
        if cluster:
            assigned_space_units = [space_units[index] for index in cluster]
            updated_r_densit_3 = sum([unit.r_densit_3 for unit in assigned_space_units]) / len(assigned_space_units)
            updated_center = SpaceUnit(None, updated_r_densit_3)
            updated_centers.append(updated_center)
    return updated_centers


# 连接到 PostgreSQL 数据库
conn = psycopg2.connect(database="shi", user="postgres", password="yangguang821.", host="localhost", port="5432")
cur = conn.cursor()

# 构建空间邻接矩阵
cur.execute("SELECT * FROM city_adjacency_matrix")
adjacency_matrix = cur.fetchall()
# print(adjacency_matrix)


# 指定聚类类别数
k = 2

# 初始化聚类中心和空间单元集合
cur.execute("SELECT DISTINCT city_name,r_densit_3 FROM cities")
cities = cur.fetchall()
# 初始聚类中心
cluster_centers = []
cluster_centers.insert(0, SpaceUnit("眉山市", Decimal("13779.000000")))
cluster_centers.insert(1, SpaceUnit("呼和浩特市", Decimal("2872.000000")))
cluster_centers.insert(2, SpaceUnit("徐州市", Decimal("3340.00000")))
num_clusters = len(cluster_centers)

space_units = [SpaceUnit(city[0], city[1]) for city in cities]
for i in range(len(cluster_centers)):
    space_units.remove(next(unit for unit in space_units if unit.city_name == cluster_centers[i].city_name))


updated_cluster_centers = []
m = 0
Zmin = [None] * num_clusters
Dmin = [None] * num_clusters
for i in range(len(cluster_centers)):
    Zmin_var_name = f"Zmin{i + 1}"
    Zmin_value = [cluster_centers[i].city_name]
    locals()[Zmin_var_name] = Zmin_value
    dmin_var_name = f"Dmin{i + 1}"
    dmin_value = [cluster_centers[i].r_densit_3]
    locals()[dmin_var_name] = dmin_value

# Dmin用于存储聚类中心，Dstorage用于计算聚类均值,Dmin11/Dmin22用于计算聚类中心均值
Dmin = []
Dstorage = []
for i in range(num_clusters):
    dmin_var_name = f"Dmin{i + 1}"
    dmin_value = locals()[dmin_var_name]
    Dmin.append(dmin_value)
for i in range(len(cluster_centers)):
    Dmin_var_name = f"Dmin{(i + 1) * 11}"
    Dmin_value = [cluster_centers[i].r_densit_3]
    locals()[Dmin_var_name] = Dmin_value

# 初始化 DistMark 矩阵
DistMark = [[True] * len(space_units) for i in range(len(cluster_centers))]

# 初始化聚类中心
epsilon = 0.001  # 聚类中心的变化阈值
max_iterations = 20  # 最大迭代次数
m = 0
pre_var_dmin = 0
# 迭代聚类过程
for iteration in range(max_iterations):
    m += 1
    print('第 %d 次迭代' % m)
    # 计算距离矩阵
    while True:
        dist_matrix = []
        min_value = float('inf')
        min_index = None
        for cluster_center in Dmin:
            dist_row = []
            for unit in space_units:
                # 计算距离，根据具体情况填写距离计算公式
                dist = calculate_distance(cluster_center[0], unit)
                dist_row.append(dist)
            dist_matrix.append(dist_row)
        # 遍历距离矩阵，找到未计算过的最小距离
        for i in range(len(dist_matrix)):
            for j in range(len(dist_matrix[i])):
                if DistMark[i][j]:  # 仅考虑 DistMark 为 True 的距离
                    if dist_matrix[i][j] < min_value:
                        min_value = dist_matrix[i][j]
                        min_index = (i, j)
        # 继续迭代前准备
        if min_index is None:
            # 更新空间单元和辅助矩阵便于下次分类
            space_units = [SpaceUnit(city[0], city[1]) for city in cities]
            DistMark = [[True] * len(space_units) for _ in range(len(cluster_centers))]
            # 更新聚类中心和聚类单元
            new_var_dmin = 0
            Dmin = []
            for i in range(len(cluster_centers)):
                Zmin_var_name = f"Zmin{i + 1}"
                print('第 %d 类中有：' % (i + 1))
                print(eval(Zmin_var_name))
                locals()[Zmin_var_name] = []
                Dmin_var_name = f"Dmin{i + 1}"
                locals()[Dmin_var_name] = []
                Dminxx_var_name = f"Dmin{( i + 1 )* 11}"
                average_density = mean(eval(Dminxx_var_name))
                new_var_dmin += abs(average_density - eval(Dminxx_var_name)[0])
                Dmin_var_name = [average_density]
                Dminxx_var_name = [Dmin_var_name[0]]
                Dmin.append(Dmin_var_name)
                print(Dmin)
            break
        index_i, index_j = min_index
        min_space_units = space_units[index_j]
        Smin_i = min_space_units.city_name
        Dmin_i = min_space_units.r_densit_3
        # 对于不同的聚类中心分类讨论
        Zmin_name = 'Zmin' + str(1 + index_i)
        Dmin_name = 'Dmin' + str(1 + index_i)
        Dminxx_name = 'Dmin' + str((index_i + 1) * 11)
        if len(eval(Zmin_name)) == 0:
            eval(Zmin_name).append(Smin_i)
            space_units.remove(next(unit for unit in space_units if unit.city_name == Smin_i))
            DistMark = [[True] * len(space_units) for _ in range(len(cluster_centers))]
        elif has_adjacency(Smin_i, eval(Zmin_name), adjacency_matrix):
            eval(Zmin_name).append(Smin_i)
            eval(Dminxx_name).append(Dmin_i)
            space_units.remove(next(unit for unit in space_units if unit.city_name == Smin_i))
            DistMark = [[True] * len(space_units) for _ in range(len(cluster_centers))]
            print(len(space_units))
        else:
            DistMark[index_i][index_j] = False
    if pre_var_dmin is not None:
        if abs(new_var_dmin - pre_var_dmin) < epsilon:
            print('迭代结束，达到稳定')
            print('共迭代%d次' % m)
            print(new_var_dmin)
            break
    print('第 %d 次迭代的目标函数' % m)
    print(abs(new_var_dmin - pre_var_dmin))
    pre_var_dmin = new_var_dmin
# 关闭数据库连接
cur.close()
conn.close()
