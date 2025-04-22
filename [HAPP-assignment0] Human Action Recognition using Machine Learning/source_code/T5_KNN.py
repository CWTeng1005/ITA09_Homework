import pandas as pd
# noinspection PyProtectedMember
from sklearn.neighbors import KNeighborsClassifier

def classify_test_samples(train_data_file, test_data_file, output_file):
    # read training & test data feature
    train_data = pd.read_csv(train_data_file)
    test_data = pd.read_csv(test_data_file)

    # extract training & test feature and label
    x_train = train_data[["RMS_x", "RMS_y", "RMS_z"]].values
    y_train = train_data["label"].values
    x_test = test_data[["RMS_x", "RMS_y", "RMS_z"]].values
    filenames = test_data["filename"].values

    # initialize KNN classifier
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(x_train, y_train)

    # predict test data label
    prediction = knn.predict(x_test)

    reverse_act_mapping = {
        'walking': 'act01',
        'sitting': 'act02',
        'jogging': 'act03'
    }

    results = []
    print(f"Sample | Class")
    for sample, (filename, pred) in enumerate(zip(filenames, prediction), start = 1):
        act_name = reverse_act_mapping.get(pred)
        result_str = f"{sample:02d}     | {act_name}:  {pred}"
        results.append(result_str)
        print(result_str)

    # save the result
    with open(output_file, 'w') as f:
        f.write(f"Sample | Class\n")
        for result in results:
            f.write(result +'\n')
    print(f"\n{output_file} SAVED!")


train = 'T2_training_features.csv'
test = 'T4_test_features.csv'
prediction_result = 'T5_prediction_result.txt'

classify_test_samples(train, test, prediction_result)
input("Press Enter to exit...")