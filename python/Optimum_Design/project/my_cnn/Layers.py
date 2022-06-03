import numpy as np


def softmax(x):
    return np.array([np.exp(xi) / np.sum(np.exp(xi), axis=0) for xi in x])

def cross_entropy(x):
    return -np.log(x)

# def cross_entropy(x):
#     return np.array([-np.log(xi) for xi in x])

# def leakyReLU(x, alpha=0.001):
#     return np.array([xi * alpha if xi < 0 else xi for xi in x])

# def leakyReLU_derivative(x, alpha=0.01):
#     return np.array([alpha if xi < 0 else 1 for xi in x])

def leakyReLU(x, alpha=0.001):
    return x * alpha if x < 0 else x

def leakyReLU_derivative(x, alpha=0.01):
    return alpha if x < 0 else 1

def lr_schedule(learning_rate, epoch):
    if epoch <= 5:
        return learning_rate
    else:
        return learning_rate * 0.1


class Convolutional:

    def __init__(self, name, num_filters=16, stride=1, size=3, activation=None):
        self.name = name
        self.filters = np.random.randn(num_filters, 3, 3) * 0.1
        self.stride = stride
        self.size = size
        self.activation = activation
        self.last_input = None
        self.leakyReLU = np.vectorize(leakyReLU)
        self.leakyReLU_derivative = np.vectorize(leakyReLU_derivative)

    def forward(self, images):
        self.last_input = images 

        batch_size = images.shape[0]
        input_dimension = images.shape[2]                                          
        output_dimension = int((input_dimension - self.size) / self.stride) + 1      

        outputs = np.zeros((batch_size, self.filters.shape[0], output_dimension, output_dimension))  
                                                                                                    
        for b in range(batch_size):
            for f in range(self.filters.shape[0]):    
                inputY = outputY = 0                          
                while inputY + self.size <= input_dimension:
                    inputX = outputX = 0
                    while inputX + self.size <= input_dimension:
                        patch = images[b, :, inputY: inputY + self.size, inputX: inputX + self.size]
                        outputs[b, f, outputY, outputX] += np.sum(self.filters[f] * patch)
                        inputX += self.stride
                        outputX += 1
                    inputY += self.stride
                    outputY += 1

        if self.activation == 'relu':               
            self.leakyReLU(outputs)
        return outputs

    def backward(self, din, learning_rate):
        batch_size = self.last_input.shape[0]
        input_dimension = self.last_input.shape[2] 

        if self.activation == 'relu':                      
           self.leakyReLU_derivative(din)

        dout = np.zeros(self.last_input.shape)           
        dfilt = np.zeros(self.filters.shape)        

        for b in range(batch_size):
            for f in range(self.filters.shape[0]):        
                inputY = outputY = 0
                while inputY + self.size <= input_dimension:
                    inputX = outputX = 0
                    while inputX + self.size <= input_dimension:
                        patch = self.last_input[b, :, inputY: inputY + self.size, inputX: inputX + self.size]
                        dfilt[f] += np.sum(din[b, f, outputY, outputX] * patch, axis=0)
                        dout[b, :, inputY: inputY + self.size, inputX: inputX + self.size] += din[b, f, outputY, outputX] * self.filters[f]
                        inputX += self.stride
                        outputX += 1
                    inputY += self.stride
                    outputY += 1

        self.filters -= learning_rate * dfilt / batch_size      
        return dout                                      

    def get_weights(self):
        return np.reshape(self.filters, -1)


class Pooling:                                            
    def __init__(self, name, stride=2, size=2):
        self.name = name
        self.last_input = None
        self.stride = stride
        self.size = size

    def forward(self, image):
        self.last_input = image                           

        batch_size, num_channels, h_prev, w_prev = image.shape
        h = int((h_prev - self.size) / self.stride) + 1    
        w = int((w_prev - self.size) / self.stride) + 1

        downsampled = np.zeros((batch_size, num_channels, h, w))        

        for b in range(batch_size):
            for i in range(num_channels):                 
                inputY = outputY = 0                        
                while inputY + self.size <= h_prev:           
                    inputX = outputX = 0
                    while inputX + self.size <= w_prev:       
                        patch = image[b, i, inputY: inputY + self.size, inputX: inputX + self.size]
                        downsampled[b, i, outputY, outputX] = np.max(patch)    
                        inputX += self.stride                          
                        outputX += 1
                    inputY += self.stride
                    outputY += 1

        return downsampled
        
    def backward(self, din, learning_rate):
        batch_size, num_channels, orig_dim, *_ = self.last_input.shape   

        dout = np.zeros(self.last_input.shape) 

        for b in range(batch_size):
            for c in range(num_channels):
                inputY = outputY = 0
                while inputY + self.size <= orig_dim:
                    inputX = outputX = 0
                    while inputX + self.size <= orig_dim:
                        patch = self.last_input[b, c, inputY: inputY + self.size, inputX: inputX + self.size] 
                        (x, y) = np.unravel_index(np.nanargmax(patch), patch.shape)                  
                        dout[b, c, inputY + x, inputX + y] += din[c, outputY, outputX]
                        inputX += self.stride
                        outputX += 1
                    inputY += self.stride
                    outputY += 1

        return dout

    def get_weights(self):        
        return 0


class FullyConnected:                               # fully-connected layer
    def __init__(self, name, nodes1, nodes2, activation):
        self.name = name
        self.weights = np.random.randn(nodes1, nodes2) * 0.1
        self.biases = np.zeros(nodes2)
        self.activation = activation
        self.last_input_shape = None
        self.last_input = None
        self.last_output = None
        self.leakyReLU = np.vectorize(leakyReLU)
        self.leakyReLU_derivative = np.vectorize(leakyReLU_derivative)

    def forward(self, input):
        self.last_input_shape = input.shape       
                                                   
        input = np.array([x.flatten() for x in input])
        output = np.array([np.dot(x, self.weights) + self.biases for x in input])

        if self.activation == 'relu':                      
            self.leakyReLU(output)

        self.last_input = input                  
        self.last_output = output

        return output

    def backward(self, din, learning_rate):
        if self.activation == 'relu':                        
           self.leakyReLU_derivative(din)

        batch_size = len(din)
        
        for b in range(batch_size):
            last_input = self.last_input[b]
            d = din[b]

            last_input = np.expand_dims(last_input, axis=1)
            d = np.expand_dims(d, axis=1)

            dw += np.dot(last_input, np.transpose(d))          
            db += np.sum(d, axis=1).reshape(self.biases.shape)     

        self.weights -= learning_rate * dw / batch_size                
        self.biases -= learning_rate * db / batch_size

        dout = np.array([np.dot(self.weights, x) + self.biases for x in din])
        return dout.reshape(self.last_input_shape)

    def get_weights(self):
        return np.reshape(self.weights, -1)


class Dense:                                        # dense layer with softmax activation
    def __init__(self, name, nodes, num_classes):
        self.name = name
        self.weights = np.random.randn(nodes, num_classes) * 0.1
        self.biases = np.zeros(num_classes)
        self.last_input_shape = None
        self.last_input = None
        self.last_output = None

    def forward(self, input):
        self.last_input_shape = input.shape        

        input = np.array([x.flatten() for x in input])
        output = np.array([np.dot(x, self.weights) + self.biases for x in input])

        self.last_input = input         
        self.last_output = output

        return softmax(output)

    def backward(self, din, learning_rate=0.005):
        batch_size = len(din)

        dw = db = 0
        dout = np.zeros((batch_size, self.weights.shape[0]))
        for b in range(batch_size):
            
            last_input = self.last_input[b]
            last_output = self.last_output[b]

            for i, gradient in enumerate(din[b]):
                if gradient == 0:                
                    continue                   

                t_exp = np.exp(last_output)                 
                dout_dt = -t_exp[i] * t_exp / (np.sum(t_exp) ** 2)
                dout_dt[i] = t_exp[i] * (np.sum(t_exp) - t_exp[i]) / (np.sum(t_exp) ** 2)

                dt = gradient * dout_dt
                dout[b] = self.weights @ dt

                # update weights and biases
                dw += np.transpose(last_input[np.newaxis]) @ dt[np.newaxis]
                db += dt
                break
        
        dout = np.array(dout)
        self.weights -= learning_rate * dw / batch_size
        self.biases -= learning_rate * db / batch_size

        return dout.reshape(self.last_input_shape)  

    def get_weights(self):
        return np.reshape(self.weights, -1)
