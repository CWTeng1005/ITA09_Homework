import os
import matplotlib.pyplot as plt

# Signature data folder
data_folder = "SignatureSampleData"
# Image save folder
result_folder = "result"
# If "result" not exists, create
os.makedirs(result_folder, exist_ok=True)
# Whether to save the figure (True: save; False: don't save)
save_fig = True

# Read single signature data file
def read_signature_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    read_data = []
    for line in lines[1:]:
        parts = list(map(int, line.strip().split()))
        if parts[0] == -1:
            read_data.append("BREAK")
        else:
            read_data.append(parts)
    return read_data

# Plot the shape of the signature
def plot_signature_shape(shape_data, title, save_path=None):
    plt.figure(figsize=(6,4))
    x, y = [], []
    for item in shape_data:
        if item == "BREAK":
            if x and y:
                plt.plot(x, y, 'k')
            x, y = [], []
        else:
            x.append(item[0])
            y.append(-item[1]) # Reverse y-axis

    if x and y:
        plt.plot(x, y, 'k')

    plt.title(f"Signature Shape - {title}")
    plt.axis("equal")
    plt.axis("off")

    if save_path and save_fig:
        plt.savefig(save_path)
        print(f"{save_path} SAVED!!")
    plt.show()
    plt.close()

# Plot 5 variables as separate subplots (one figure)
def plot_signature_variables(var_data, title, save_path=None):
    variables = {'x':[], 'y':[], 'pressure':[], 'azimuth':[], 'altitude':[], 'time':[]}
    for item in var_data:
        if item != "BREAK":
            variables['x'].append(item[0])
            variables['y'].append(item[1])
            variables['pressure'].append(item[2])
            variables['azimuth'].append(item[3])
            variables['altitude'].append(item[4])
            variables['time'].append(item[5])

    plt.figure(figsize=(10, 10))

    var_names = ['x', 'y', 'pressure', 'azimuth', 'altitude']
    for i, var in enumerate(var_names):
        plt.subplot(5, 1, i+1) # r5c1, i+1 sub_fig
        plt.plot(variables['time'], variables[var], label=var)
        plt.ylabel(var)
        plt.grid(True)
        if i == 0:
            plt.title(f"Signature Variables over Time - {title}")
        if i == 4:
            plt.xlabel("Time")

    plt.tight_layout() # avoid sub_fig overlay

    if save_path and save_fig:
        plt.savefig(save_path)
        print(f"{save_path} SAVED!!")
    plt.show()
    plt.close()

# Main function
if __name__ == "__main__":
    files = ["001.001.000.sdt", "001.001.001.sdt"]
    for filename in files:
        filepath = os.path.join(data_folder, filename)
        data = read_signature_file(filepath)
        name = os.path.splitext(filename)[0]

        # Save paths --> result
        shape_path = os.path.join(result_folder, f"{name}_shape.png")
        vars_path = os.path.join(result_folder, f"{name}_vars.png")

        plot_signature_shape(data, title=name, save_path=shape_path)
        plot_signature_variables(data, title=name, save_path=vars_path)
    input("Press Enter to close...")