import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import os

# 工具函数
def read_sdt_file(file_path):
    # 读取.sdt文件，返回stroke list，每个stroke是[(x,y ), ...]的列表
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    strokes = []
    current_stroke = []
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) != 6:
            continue
        x, y = int(parts[0]), int(parts[1])
        if x == -1:
            if current_stroke:
                strokes.append(current_stroke)
                current_stroke = []
        else:
            current_stroke.append((x,y))

    if current_stroke:
        strokes.append(current_stroke)

    return strokes

# Q1. Linear Matching 距离计算
def linear_matching_distance(linear1, linear2):
    # 计算两个字符之间的线性匹配距离
    total_distance = 0
    n_strokes = min(len(linear1), len(linear2))

    for i in range(n_strokes):
        stroke1 = linear1[i]
        stroke2 = linear2[i]
        n_points = min(len(stroke1), len(stroke2))
        stroke_distance = 0

        for j in range(n_points):
            x1, y1 = stroke1[j]
            x2, y2 = stroke2[j]
            stroke_distance += sqrt((x1 - x2)**2 + (y1 - y2)**2)

        if n_points > 0:
            total_distance += stroke_distance / n_points

    return total_distance

# Q2. Dynamic Programming Matching 距离计算
def dp_matching_distance(dp1, dp2):
    # 使用动态规划匹配两个字符的距离
    total_distance = 0
    n_strokes = min(len(dp1), len(dp2))

    for i in range(n_strokes):
        stroke1 = dp1[i]
        stroke2 = dp2[i]
        n, m = len(stroke1), len(stroke2)
        dp = np.full((n + 1, m + 1), np.inf)
        dp[0][0] = 0

        for i1 in range(1, n + 1):
            for j1 in range(1, m + 1):
                x1, y1 = stroke1[i1 - 1]
                x2, y2 = stroke2[j1 - 1]
                cost = sqrt((x1 - x2)**2 + (y1 - y2)**2)
                dp[i1][j1] = cost + min(
                    dp[i1 - 1][j1],
                    dp[i1][j1 - 1],
                    dp[i1 - 1][j1 - 1]
                )

        total_distance += dp[n][m] /max(n, m)

    return total_distance

# Q3. plot
def plot_matching(c1, c2, method="original", save_path=None):
    """
    可视化两个字符及其匹配关系
    method可选：
    - original：仅绘制两个字符
    - linear：线性匹配连线
    - dp：动态规划匹配连线
    save_path：若指定路径则保存图像
    """
    fig, ax = plt.subplots(figsize = (6, 6))

    # 画原始字符（蓝色和红色）
    for stroke in c1:
        xs, ys = zip(*stroke)
        ax.plot(xs, ys, color='blue', alpha=0.7, linewidth=1)
    for stroke in c2:
        xs, ys = zip(*stroke)
        ax.plot(xs, ys, color='red', alpha=0.7, linewidth=1)

    if method not in("linear", "dp"):
        ax.set_title("Original Characters")
    else:
        n_strokes = min(len(c1), len(c2))
        for s in range(n_strokes):
            stroke1 = c1[s]
            stroke2 = c2[s]

            if method == "linear":
                n = min(len(stroke1), len(stroke2))
                for i in range(n):
                    x1, y1 = stroke1[i]
                    x2, y2 = stroke2[i]
                    ax.plot([x1, x2], [y1, y2], color='gray', linestyle='dotted', linewidth=0.8)

            elif method == "dp":
                n, m = len(stroke1), len(stroke2)
                dp = np.full((n + 1, m + 1), np.inf)
                dp[0][0] = 0
                backtrack = {}

                for i in range(1, n + 1):
                    for j in range(1, m + 1):
                        x1, y1 = stroke1[i - 1]
                        x2, y2 = stroke2[j - 1]
                        cost = sqrt((x1 - x2)**2 + (y1 - y2)**2)
                        options = {
                            (i - 1, j): dp[i - 1][j],
                            (i, j - 1): dp[i][j - 1],
                            (i - 1, j - 1): dp[i - 1][j - 1]
                        }
                        prev, min_cost = min(options.items(), key=lambda x: x[1])
                        dp[i][j] = cost + min_cost
                        backtrack[(i, j)] = prev

                i, j = n, m
                path = []
                while (i, j) in backtrack:
                    path.append((i - 1, j - 1))
                    i, j = backtrack[(i, j)]
                path.reverse()

                for i, j in path:
                    if 0 <= i < len(stroke1) and 0 <= j < len(stroke2):
                        x1, y1 = stroke1[i]
                        x2, y2 = stroke2[j]
                        ax.plot([x1, x2], [y1, y2], color='gray', linestyle='dotted', linewidth=0.8)

        ax.set_title(f'Matching Method: {method.upper()}')

    ax.invert_yaxis()
    ax.axis('equal')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()

# 示例调用
if __name__ == "__main__":
    os.makedirs("output_images", exist_ok=True)

    # read data
    # strokes1 = read_sdt_file("SimpleData/ref.sdt")
    # strokes2 = read_sdt_file("SimpleData/test.sdt")
    strokes1 = read_sdt_file("SignatureSampleData/001.001.000.sdt")
    strokes2 = read_sdt_file("SignatureSampleData/001.001.001.sdt")

    # Q1. linear matching
    d_linear = linear_matching_distance(strokes1, strokes2)
    print(f"Linear Matching Distance: {d_linear:.2f}")

    # Q2. DP matching
    d_dp = dp_matching_distance(strokes1, strokes2)
    print(f"DP Matching Distance: {d_dp:.2f}")

    # Q3. Visualize
    plot_matching(strokes1, strokes2, method="original", save_path="output_images/original.png")
    # plot_matching(strokes1, strokes2, method="original", save_path="output_images/original_test.png")
    plot_matching(strokes1, strokes2, method="linear", save_path="output_images/linear.png")
    # plot_matching(strokes1, strokes2, method="linear", save_path="output_images/linear_test.png")
    plot_matching(strokes1, strokes2, method="dp", save_path="output_images/dp.png")
    # plot_matching(strokes1, strokes2, method="dp", save_path="output_images/dp_test.png")

    input("Press ENTER to exit...")