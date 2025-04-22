import os
import pandas as pd
import numpy as np

def compute_rms(data):
    return np.sqrt(np.mean(np.square(data)))

def extract_rms(filepath):
    # extract x,y,z axis data
    x_data, y_data, z_data = [], [], []

    with open(filepath, 'r') as f:
        for line in f:
            if line.strip() == '':
                continue
            parts = line.strip().split('\t')
            if len(parts) != 3:
                continue
            x,y ,z = map(float, parts)
            x_data.append(x)
            y_data.append(y)
            z_data.append(z)

    return [
        compute_rms(x_data),
        compute_rms(y_data),
        compute_rms(z_data)
    ]

def extract_features(test_folder):
    results = []
    filenames = sorted(os.listdir(test_folder))

    print(f"RMS_x, RMS_y, RMS_z")
    for filename in filenames:
        if not filename.endswith('.txt'):
            continue
        filepath = os.path.join(test_folder, filename)
        rms_values = extract_rms(filepath)
        results.append(rms_values + [filename])
        print(f"{rms_values[0]}, {rms_values[1]}, {rms_values[2]}")

    return results

def save_to_csv(data, output_file):
    data = pd.DataFrame(data, columns=["RMS_x", "RMS_y", "RMS_z", "filename"])
    data.to_csv(output_file, index=False)
    print(f"\n{output_file} saved!")

if __name__ == "__main__":
    folder_path = "test"
    output_csv = "T4_test_features.csv"
    features = extract_features(folder_path)
    save_to_csv(features, output_csv)
    input("Press Enter to exit...")