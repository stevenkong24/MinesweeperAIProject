import tensorflow
from tensorflow.keras.layers import Conv2D, Dense, Flatten, Reshape, BatchNormalization, Input, MaxPooling2D, UpSampling2D, Dropout
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.optimizers import Adam, SGD
EarlyStopping = tensorflow.keras.callbacks.EarlyStopping
from matplotlib import pyplot as plt

Sequential = tensorflow.keras.models.Sequential
from sklearn.model_selection import train_test_split

from game import board

def accuracy(real, output):
    ans = real.copy()
    for i in range(len(real)):
        for j in range(len(real[0])):
            ans[i][j] = f'r{real[i][j]} o{output[i][j]}'
    return ans

import sys
import os
# sys.path.append(os.path.abspath('..'))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from data.data_io import get_data_and_labels
# from data.data_io import get_data_and_labels
from data.data_io import get_data_and_labels

print("Num GPUs Available: ", len(tensorflow.config.list_physical_devices('GPU')))

coverage_mask = False

def build_model():
    board_height, board_width = 30, 16
    model = Sequential([
        Input(shape=(board_height, board_width, 1)),  # Add channel dimension for grayscale input
        Conv2D(32, kernel_size=(3, 3), activation='sigmoid', padding='same'),
        MaxPooling2D(pool_size=(2, 2)),
        BatchNormalization(),
        Conv2D(64, kernel_size=(3, 3), activation='sigmoid', padding='same'),
        MaxPooling2D(pool_size=(2, 2)),
        BatchNormalization(),
        Flatten(),
        Dense(128, activation='sigmoid'),
        Dense(board_height * board_width, activation='sigmoid'),  # Output probabilities
        Reshape((board_height, board_width))  # Reshape back to grid
    ])

    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss=BinaryCrossentropy(),
        metrics=['accuracy', 'auc']
    )

    return model

def create_tf_dataset(data, labels, train_split=0.8, batch_size=32):
    dataset = tensorflow.data.Dataset.from_tensor_slices((data, labels))

    # Calculate split sizes
    total_size = len(data)
    train_size = int(train_split * total_size)

    # Shuffle and split
    train_dataset = dataset.take(train_size).shuffle(train_size).batch(batch_size).prefetch(tensorflow.data.AUTOTUNE)
    test_dataset = dataset.skip(train_size).batch(batch_size).prefetch(tensorflow.data.AUTOTUNE)

    return train_dataset, test_dataset

data, labels = get_data_and_labels('../data/board_dataset.npz', '../data/labels.npz', '../data/coverage_mask.npz', coverage_mask)
data = tensorflow.squeeze(data, axis=1)
labels = tensorflow.squeeze(labels, axis=[1, -1])
train, test = create_tf_dataset(data, labels)

# data, labels = get_data_and_labels('../data/board_dataset.npz', '../data/labels.npz')
# x, xtest, y, ytest = train_test_split(data, labels, test_size=0.2, train_size=0.8)
print(f'dshape: {data.shape}, dtype: {data.dtype}')
model = build_model()
print(f'model shape: {model.input_shape}')
history = model.fit(
    train,
    epochs=20,
    batch_size=32,
    validation_data=test,
    verbose=1,
)
model.save('msmodel.keras')

e = board.generateForData(30, 16, 99)
c = board.random_coverage(e)

feed = board.set_dimensions(c)
ans = model.predict(feed)
print(ans.shape)
ans = [[round(float(val), 2) for val in row] for row in ans.squeeze()]
print('----Grid Fed In-------------------------------------------------------------------')
for r in c:
    frmt = "{:>10}" * len(r)
    print(frmt.format(*r))
print('----Grid Fed In Uncovered-------------------------------------------------------------------')
for r in e:
    frmt = "{:>10}" * len(r)
    print(frmt.format(*r))
print('-------Result----------------------------------------------------------------')
for r in ans:
    frmt = "{:>10}" * len(r)
    print(frmt.format(*r))
print('------Accuracy Grid-----------------------------------------------------------------')
for r in accuracy(board.create_label_grid(e), ans):
    frmt = "{:>10}" * len(r)
    print(frmt.format(*r))

#plot
plt.plot(history.history['accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train'], loc='upper left')
plt.show()

# t1 = model.predict(xtest[0])
# print(t1)
# print(ytest[0])
