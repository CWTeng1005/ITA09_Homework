import pandas as pd
import matplotlib.pyplot as plt

def plot_3d_features(csv_file):
    # read data from csv file
    data = pd.read_csv(csv_file)

    # extract RMS data and label
    rms_x = data['RMS_x']
    rms_y = data['RMS_y']
    rms_z = data['RMS_z']
    labels = data['label']

    # color of activities
    color = {
        'walking': 'blue',
        'sitting': 'green',
        'jogging': 'red'
    }

    # create 3d figure window
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # plot each activity
    for label in color:
        idx = labels == label
        ax.scatter(rms_x[idx], rms_y[idx], rms_z[idx], c=color[label], label=label)

    # set axis label
    ax.set_xlabel('RMS_x')
    ax.set_ylabel('RMS_y')
    ax.set_zlabel('RMS_z')
    ax.set_title('3D Plot of Training Features (RMS)')
    ax.legend()

    # save pic as png file
    plt.savefig("T3_3D_Plot.png")
    print("T3_3D_Plot.png saved")

    # show the figure
    plt.show()

if __name__ == "__main__":
    plot_3d_features("T2_training_features.csv")
    input("Press Enter to exit...")