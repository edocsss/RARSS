import numpy as np
from sklearn.metrics import accuracy_score, f1_score
from sklearn.naive_bayes import MultinomialNB, GaussianNB

from classifier.util import data_util


def run_cv(alpha=1, data_source='', activities=None):
    kfold_data = data_util.load_kfolds_training_and_testing_data(k=5, source=data_source, activities=activities)
    accuracy_results = []
    fscore_results = []

    for i, data in enumerate(kfold_data):
        X_train = data[0]
        X_test = data[1]
        Y_train = data[2]
        Y_test = data[3]

        model = GaussianNB()
        model.fit(X_train, Y_train)

        predictions = model.predict(X_test)
        accuracy = accuracy_score(Y_test, predictions)
        accuracy_results.append(accuracy)

        fscore = f1_score(Y_test, predictions, average='weighted')
        fscore_results.append(fscore)
        # print('k = {}, accuracy = {}'.format(i + 1, accuracy))
        # print('k = {}, fscore = {}'.format(i + 1, fscore))
        # print()
        # print()

    accuracy_mean = np.mean(accuracy_results)
    accuracy_std_dev = np.std(accuracy_results)

    fscore_mean = np.mean(fscore_results)
    fscore_std_dev = np.std(fscore_results)

    print('Alpha: {}'.format(alpha))
    print('Accuracy: {}'.format(accuracy_results))
    print('Accuracy Mean: {}, Accuracy Standard deviation: {}'.format(accuracy_mean, accuracy_std_dev))
    print('F1 Score: {}'.format(fscore_results))
    print('F1 Mean: {}, F1 Standard deviation: {}'.format(fscore_mean, fscore_std_dev))
    print()
    print()
    print()

    return accuracy_mean, accuracy_std_dev, fscore_mean, fscore_std_dev


if __name__ == '__main__':
    x = []
    y = []

    alphas = [0.0005]
    activities = None

    for a in alphas:
        accuracy_mean, accuracy_std_dev, fscore_mean, fscore_std_dev = run_cv(
            alpha=a,
            data_source='sw',
            activities=activities
        )