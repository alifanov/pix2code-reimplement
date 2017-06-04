import numpy as np

from os import listdir
from os.path import isfile, join

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import LSTM
from keras.layers import Merge
from keras.layers import RepeatVector
from keras.layers.merge import concatenate
from keras.layers.wrappers import TimeDistributed
from keras.preprocessing.sequence import pad_sequences

VOC_SIZE = 16
MAX_LEN = 11


def get_dataset(path='images/'):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    seq_dataset = []
    img_dataset = []
    for f in files:
        if 'npy' in f:
            code_seq = [np.eye(VOC_SIZE)[int(c):int(c)+1] for c in f[:-4].split('-')]
            ndata = np.load(join(path, f))
            img_dataset.append(ndata)
            seq_dataset.append(code_seq)
    return img_dataset, seq_dataset

img_dataset, seq_dataset = get_dataset()
img_dataset = np.array(img_dataset)
pad_sequences(seq_dataset, maxlen=MAX_LEN, padding='post')
seq_dataset = np.array(seq_dataset)
seq_dataset = np.reshape(seq_dataset, (seq_dataset.shape[0], seq_dataset.shape[1], VOC_SIZE))
# print('Tags shape: ', seq_dataset.shape)
# print('Images shape: ', img_dataset.shape)

model_cnn = Sequential()
model_cnn.add(Conv2D(32, kernel_size=(3, 3), input_shape=[256, 256, 3]))
model_cnn.add(Conv2D(64, kernel_size=(3, 3)))
model_cnn.add(MaxPooling2D())
model_cnn.add(Conv2D(128, kernel_size=(3, 3)))
model_cnn.add(Flatten())
model_cnn.add(Dense(1024, name='cnn_dense_1024'))
model_cnn.add(Dense(128, activation='relu', name='cnn_dense_128'))
model_cnn.add(RepeatVector(MAX_LEN))

model_rnn_1 = Sequential()
model_rnn_1.add(LSTM(128, input_shape=(MAX_LEN, VOC_SIZE), return_sequences=True))
model_rnn_1.add(TimeDistributed(Dense(128, name='rnn_dense_128')))

model = Sequential()
merged = Merge([model_cnn, model_rnn_1], mode='concat')
model.add(merged)
model.add(LSTM(512, return_sequences=True))
model.add(LSTM(512, return_sequences=False))
model.add(Dense(VOC_SIZE, activation='softmax', name='final_dense_16'))

model.compile(optimizer='adam', loss='categorical_crossentropy')

y = np.zeros((seq_dataset.shape[0], seq_dataset.shape[2]))
y[:, 8] = 1 # ohe for 9 (</body)

model.fit([img_dataset, seq_dataset], y, batch_size=1, epochs=5)
