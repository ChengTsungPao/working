import numpy as np
import matplotlib.pylab as plt
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense, Activation


def get_data(path):
    health = np.load(path+"health.npz")["r"]
    unhealth = np.load(path+"unhealth.npz")["r"]
    X = np.array(health.tolist() + unhealth.tolist())
    Y = np.array([[0., 1.] for _ in range(len(health))] + [[1., 0.] for _ in range(len(unhealth))])
    return X, Y


c = 0.1
path = "./erythrocyte/"
X, Y = get_data(path)
X_train, Y_train, X_test, Y_test = X[:int(len(X)*(1-c))], Y[:int(len(X)*(1-c))], X[int(len(X)*(1-c)):], Y[int(len(X)*(1-c)):]

model = Sequential([
    Dense(4, input_dim=8),
    Activation('relu'),
    Dense(2),
    Activation('softmax'),
])
print(model.summary())

print('\nTraining ------------')
sgd = optimizers.SGD(lr=0.00001)
model.compile(optimizer=sgd, loss='categorical_crossentropy',  metrics=['accuracy'])
H = model.fit(X_train, Y_train, epochs=100000, batch_size=32)

loss, accuracy = model.evaluate(X_test, Y_test)
print('\nTesting ------------')
print('test loss: ', loss)
print('test accuracy: ', accuracy)

plt.subplot(121)
plt.plot(range(len(H.history["loss"])), H.history["loss"], "o", label = "loss")
plt.subplot(122)
plt.plot(range(len(H.history["accuracy"])), H.history["accuracy"], "o", label = "accuracy")
plt.legend()
plt.show()
