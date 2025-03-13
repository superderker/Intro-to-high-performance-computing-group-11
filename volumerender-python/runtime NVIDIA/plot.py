import matplotlib.pyplot as plt
import numpy as np
import os

# 设置你想要绘制的文件 (需包含 .txt 后缀)
# selected_files = ["unchanged.txt", "numba.txt", "cupy.txt", "python.txt"]
# selected_files = ["unchanged.txt", "cupy.txt", "cupyandmp.txt", "cupyanddask.txt"]
selected_files = ["unchanged.txt", "dask.txt", "daskmp.txt", "mp.txt", "daskdistributed.txt"]

# 设置每条线的颜色 (与文件列表顺序对应)
colors = ["red", "orange", "green", "blue", "yellow"]

# 设定数据目录 (修改为你的txt文件所在目录)
data_dir = "./"  # 例如 "/path/to/your/txt/files/"

# 存储数据
data = {}
angles = None

# 解析数据
for i, file in enumerate(selected_files):
    file_path = os.path.join(data_dir, file)
    method_name = file.replace(".txt", "")  # 以文件名作为方法名称

    # 读取数据
    file_data = np.loadtxt(file_path, delimiter=':', dtype=str)
    file_angles = np.array([int(row[0]) for row in file_data])
    file_means = np.array([float(row[1].split(',')[0]) for row in file_data])

    # 统一角度
    if angles is None:
        angles = file_angles

    data[method_name] = (file_means, colors[i])  # 存储数据和对应颜色

# 画图
plt.figure(figsize=(8, 6))

# 遍历所有方法数据
for method, (runtimes, color) in data.items():
    plt.plot(angles, runtimes, marker='o', label=method, color=color)

# 图表样式
plt.xlabel("Angles")
plt.ylabel("Runtime (seconds)")
plt.legend()
plt.grid(True)
plt.title("Runtime Comparison")

# 保存图片（可选）
# plt.savefig("numba+cupy+python.png", dpi=300)
# plt.savefig("cupy+cupymp+cupyanddask.png", dpi=300)
plt.savefig("dask+mp+daskmp+daskdistributed.png", dpi=300)

# 显示图表
plt.show()
