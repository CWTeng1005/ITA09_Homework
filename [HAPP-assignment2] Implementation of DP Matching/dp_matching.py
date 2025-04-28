# Assignment 2: Implementation of DP Matching

import numpy as np
import matplotlib.pyplot as plt
import os

# read data
def read_data(file_path):
    # read data from txt file
    try:
        data = np.loadtxt(file_path)
        return data
    except Exception as e:
        print(f"Failed to read data from {file_path}    Error: {e}")
        return None

# calculate distance d(i,j) 局部距离 (local distance between A and B)
def local_distance(a,b):
    return np.abs(a - b)

# 计算DP Matching的累计距离矩阵
def dp_matching(m1, m2):
    # perform DP matching to compute accumulated distance matrix g and local distance matrix d
    n = len(m1)
    m = len(m2)
    g = np.full((n, m), np.inf) # 初始化累积距离矩阵g，所有元素设为无穷大
    d = np.zeros((n, m))    # 初始化局部距离矩阵d

    # initialize first point
    d[0, 0] = local_distance(m1[0], m2[0])
    g[0, 0] = d[0, 0]

    # initialize row 1
    for j in range(1, m):
        d[0, j] = local_distance(m1[0], m2[j])
        g[0, j] = d[0, j] + g[0, j-1]

    # 填充矩阵
    for i in range(1, n):
        for j in range(m):
            d[i, j] = local_distance(m1[i], m2[j])
            if j >= 2:
                # 可以从g(i-1,j), g(i-1,j-1), g(i-1,j-2)三种情况中选最小的
                g[i, j] = d[i, j] + min(g[i-1, j], g[i-1, j-1], g[i-1, j-2])
            elif j == 1:
                # 只能从g(i-1,j)或g(i-1,j-1)中选
                g[i, j] = d[i, j] + min(g[i-1, j], g[i-1, j-1])
            else:   # j == 0
                # 只能从g(i-1,j)累加
                g[i, j] = d[i, j] + g[i-1, j]

    return g, d

# 回溯寻找最佳匹配路径
def backtrack(g):
    # trace back the path from bottom-right to top-left
    i, j = np.array(g.shape) - 1  # 从最后一个点开始
    path = [(i, j)]

    while i > 0:
        if j >= 2:
            # 三种方向：上、左上、左上两格
            direction = np.argmin([g[i-1, j], g[i-1, j-1], g[i-1, j-2]])
            if direction == 0:
                i -= 1
            elif direction == 1:
                i -= 1
                j -= 1
            else: # direction == 2
                i -= 1
                j -= 2
        elif j == 1:
            # 只能考虑上或左上
            if g[i-1, j] < g[i-1, j-1]:
                i -= 1
            else:
                i -= 1
                j -= 1
        else: # j == 0
            # 只能往上
            i -= 1

        path.append((i, j))

    path.reverse()  # 逆序排列路径
    return path

# plot original signal
def plot_original(m1, m2, save_dir):
    plt.figure()
    plt.plot(m1, label = 'Signal A')
    plt.plot(m2, label = 'Signal B')
    plt.title('Original Signals')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, "original_signals.png"))
    plt.show()

# plot aligned signal
def plot_aligned(m1, m2, path, save_dir):
    new_a = []
    new_b = []
    new_time = []

    for idx, (i, j) in enumerate(path):
        new_a.append(m1[i])
        new_b.append(m2[j])
        new_time.append(idx)

    plt.figure()
    plt.plot(new_time, new_a, label = 'Signal A (aligned)')
    plt.plot(new_time, new_b, label = 'Signal B (aligned)')
    plt.title('Aligned Signals after DP Matching')
    plt.xlabel('Aligned Time')
    plt.ylabel('Amplitude')
    plt.legend()
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, "aligned_signals.png"))
    plt.show()

# main function
def main():
    # read data
    m1 = read_data('data_a.txt')
    m2 = read_data('data_b.txt')

    if m1 is None or m2 is None:
        print("Failed to read data.")
        return

    # Question 1: Plot original signal
    save_dir = "result"
    plot_original(m1, m2, save_dir)

    # Question 2: 计算DP matching
    g, d = dp_matching(m1, m2)
    # 输出DP matching总距离
    print(f"\n--- DP Matching Result ---")
    print(f"Total Matching Distance: {g[-1, -1]: .4f}")

    # Question 3:回溯并画对齐后的图
    path = backtrack(g)
    plot_aligned(m1, m2, path, save_dir)
    # 输出回溯匹配的点数
    print(f"Number of matched points: {len(path)}")
    # 简单列出部分匹配点
    print("\nSample Matched Points (A index -> B index):")
    for idx in range(0, len(path), max(1, len(path)//10)): # 每隔一点输出
        print(f"A[{path[idx][0]}] -> B[{path[idx][1]}]")

if __name__ == "__main__":
    main()
    input("Press ENTER to exit.")