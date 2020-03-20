import numpy as np
import matplotlib.pylab as plt
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense, Activation
from sklearn.model_selection import train_test_split


def get_data(path):
    health = np.load(path+"health.npz")["r"]
    unhealth = np.load(path+"unhealth.npz")["r"]
    X = np.array(health.tolist() + unhealth.tolist())
    Y = np.array([[0., 1.] for _ in range(len(health))] + [[1., 0.] for _ in range(len(unhealth))])
    return X, Y


path = "./erythrocyte/"
X, Y = get_data(path)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, shuffle=True)

model = Sequential([
    Dense(10, input_dim=16),
    Activation('relu'),
    Dense(2),
    Activation('softmax'),
])
print(model.summary())

print('\nTraining ------------')
sgd = optimizers.SGD(lr=0.01)
adam = optimizers.Adam(lr=0.001)
model.compile(optimizer=adam, loss='categorical_crossentropy',  metrics=['accuracy'])
H = model.fit(X_train, Y_train, epochs=100, batch_size=8, validation_data=(X_test, Y_test), shuffle=True)

loss, accuracy = model.evaluate(X_test, Y_test)
print('\nTesting ------------')
print('test loss: ', loss)
print('test accuracy: ', accuracy)


plt.plot(range(len(H.history["accuracy"])), H.history["accuracy"], "o", label = "accuracy")
plt.legend()
plt.show()

plt.plot(range(len(H.history["loss"])), H.history["loss"], "o", label = "loss")
plt.plot(range(len(H.history["val_loss"])), H.history["val_loss"], "o", label = "val_loss")
plt.legend()
plt.show()
