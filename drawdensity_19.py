# -*- coding: utf-8 -*-
import psycopg2
import matplotlib.pyplot as plt

# 查看属性数据分布散点图
# 连接到 PostgreSQL 数据库
conn = psycopg2.connect(database="shi", user="postgres", password="yangguang821.", host="localhost", port="5432")
cur = conn.cursor()


# 从数据库中获取 density_19 值
cur.execute("SELECT r_densit_3 FROM cities")
density_values_tuple = cur.fetchall()

# 提取实际的 density_19 值
density_values = [value[0] for value in density_values_tuple]


# 计算最小值和最大值
min_value = min(density_values)
max_value = max(density_values)

# # 归一化处理
# normalized_values = [(value - min_value) / (max_value - min_value) for value in density_values]

# 绘制一维坐标
x = range(len(density_values))
plt.scatter(x, density_values)
plt.xlabel('Index')
plt.ylabel('Normalized Density')
plt.title('Density Distribution')
plt.show()

