# Task 1: Read all train data. And plot figure of each data. Each figure will contain 3 axis data

import os
import numpy as np
import matplotlib.pyplot as plt

def read_signal(file_path):
    # read the data of signals in a file, each row contain 3 data (x,y,z)
    # 读取单个训练文件的信号数据，每行包含3个数字（x,y,z）
    # return x,y,z array
    # 返回：x,y,z 数组
    try:
        data = np.loadtxt(file_path)
        # each row of the data --> [x,y,z]
        # data 的每一行假设为 [x,y,z]
        x = data[:, 0]
        y = data[:, 1]
        z = data[:, 2]
        return x, y, z
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None, None

def plot_signal(x, y, z, title, save_path=None, show_plot=False):
    # plot the signal, show the data of 3 axis
    # 绘制信号图，显示三个轴的数据
    plt.figure()
    plt.plot(x, label="X-axis")
    plt.plot(y, label="Y-axis")
    plt.plot(z, label="Z-axis")
    plt.title(title)
    plt.xlabel("Sample")
    plt.ylabel("Acceleration")
    plt.legend()

    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")

    if show_plot:
        plt.show()
    else:
        plt.close()

def process_training_data(base_folders, show_plot=False):
    # Traverse each specified folder and plot signal graphs for all files.
    # 遍历文件夹，绘制每个文件的信号图
    # base_folders: list of (folder_name, label)
    for folder, label in base_folders:
        # construct folder path (in current directory)
        for i in range (1, 8):
            # 01.txt - 07.txt
            filename = f"{i:02d}.txt"
            file_path = os.path.join(folder, filename)
            x, y, z = read_signal(file_path)
            if x is None:
                continue
            # title of graph, show the action and filename
            title = f"{label}_{filename}"
            # set a directory to save the graph
            save_dir = "T1_plots"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            save_path = os.path.join(save_dir, f"{label}_{filename}.png")
            plot_signal(x, y, z, title, save_path, show_plot=show_plot)

# define the folder and corresponding label
training_folders = [
    ("act01", "Walking"),
    ("act02", "Sitting"),
    ("act03", "Jogging")
]

if __name__ == "__main__":
    # show_plot=False if you dont want show plot
    process_training_data(training_folders, show_plot=True)
    input("Press Enter to exit...")
