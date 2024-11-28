import tensorflow
from tensorflow.keras.layers import Conv2D, Dense, Flatten, Reshape, BatchNormalization, Input
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.optimizers import Adam, SGD

Sequential = tensorflow.keras.models.Sequential
from sklearn.model_selection import train_test_split

import sys
import os
# sys.path.append(os.path.abspath('..'))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from data.data_io import get_data_and_labels
# from data.data_io import get_data_and_labels
from data.data_io import get_data_and_labels

def build_model():
    x, y = 30, 16
    model = Sequential([
        Input(shape=(x, y, 1)),
        Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same'),
        #BatchNormalization(),
        Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'),
        #BatchNormalization(),
        Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same'),
        # BatchNormalization(),
        Conv2D(1, kernel_size=(1, 1), activation='sigmoid')
    ])

    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss=BinaryCrossentropy(),
        metrics=['accuracy']
    )

    return model

data, labels = get_data_and_labels('data/board_dataset.npz', 'data/labels.npz')
# data, labels = get_data_and_labels('../data/board_dataset.npz', '../data/labels.npz')
x, xtest, y, ytest = train_test_split(data, labels, test_size=0.2, train_size=0.8)

model = build_model()
model.fit(
    x,
    y,
    epochs=30,
    batch_size=32,
    verbose=1
)
model.save('msmodel.keras')

print("Test:")
test_loss, test_accuracy = model.evaluate(xtest, ytest)

# t1 = model.predict(xtest[0])
# print(t1)
# print(ytest[0])
