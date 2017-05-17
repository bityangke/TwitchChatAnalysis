import numpy as np
import csv
from utils import get_vectorized_comment


def batch_generator(X, y, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    # data = np.array(data)
    data_size = X.shape[0]
    num_batches_per_epoch = data_size // batch_size + 1

    for epoch in range(num_epochs):
        print("In epoch >> " + str(epoch + 1))
        print("num batches per epoch is: " + str(num_batches_per_epoch))

        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            X_shuffled = X[shuffle_indices]
            y_shuffled = y[shuffle_indices]
        else:
            X_shuffled = X
            y_shuffled = y

        for batch_num in range(num_batches_per_epoch - 1):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            X_batch = X_shuffled[start_index:end_index]
            y_batch = y_shuffled[start_index:end_index]
            batch = list(zip(X_batch, y_batch))

            yield batch


def get_input_data_from_csv(file_path, max_feature_length):
    comments = []
    classes = []
    sentiments = []
    with open(file_path) as f:
        reader = csv.DictReader(f, fieldnames=['id', 'comments', 'sentiment', 'class'])
        for i, row in enumerate(reader):
            if i > 0:
                comments.append(get_vectorized_comment(row['comments'], max_feature_length))
                sentiments.append(int(row['sentiment']) + 1)
                classes.append(int(row['class']))

    return np.asarray(comments, dtype='int32'), np.asarray(sentiments, dtype='int32'), np.asarray(classes, dtype='int32')


def get_input_data_from_text(text, sentiment, _class, max_feature_length):
    X = np.asarray([get_vectorized_comment(text)], dtype='int32')
    y_sentiment = np.asarray([int(sentiment) + 1], dtype='int32')
    y_comment = np.asarray([_class], dtype='int32')

    return X, y_sentiment, y_comment
