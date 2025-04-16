# Task 2: Extract RMS from each axis of each axis of each data and generate the feature vector for training
# 从act01, act02, act03文件夹中读取每个文件，提取三个轴的RMS值，生成特征向量矩阵

import os
import math
import csv

# 计算 RMS 函数
def compute_rms(data):
    n = len(data)
    return math.sqrt(sum(x**2 for x in data) / n)

# 从文件中提取 x/y/z 并计算 RMS
def extract_rms(filepath):
    x_data, y_data, z_data = [], [], []
    try:
        with open(filepath, 'r') as file:
            for line in file:
                if line.strip() == "":
                    continue
                parts = line.strip().split()
                if len(parts) != 3:
                    print(f"skip line: {line.strip()} in {filepath}")
                    continue
                x, y, z = map(float, parts)
                x_data.append(x)
                y_data.append(y)
                z_data.append(z)

        # each file has 101 lines
        if len(x_data) != 101:
            print(f"there are {len(x_data)} lines in {filepath}")

        return [compute_rms(x_data), compute_rms(y_data), compute_rms(z_data)]

    except FileNotFoundError:
        print(f"{filepath} not found")
        return None

def main():
    activities = {
        "walking": "act01",
        "sitting": "act02",
        "jogging": "act03"
    }

    output_rows = [["RMS_x", "RMS_y", "RMS_z", "label"]]

    print(f"RMS_x, RMS_y, RMS_z, label")
    for label, folder in activities.items():
        # 01.txt - 07.txt
        for i in range(1,8):
            filename = f"{i:02d}.txt"
            filepath = os.path.join(folder, filename)
            rms_values = extract_rms(filepath)
            if rms_values:
                print(f"{rms_values[0]}, {rms_values[1]}, {rms_values[2]}, {label}")
                output_rows.append([*rms_values, label])
            else:
                print(f"{label} {filename} not found")

    # save as .csv file
    with open("T2_training_features.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(output_rows)

    print("\nT2_training_features.csv saved")

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")