import numpy as np

nn_architecture = [
    # input layer to hidden layer
    {
        "input_dim": 2,
        "output_dim": 2,
    },
    # hidden layer to output layer
    {
        "input_dim": 2,
        "output_dim": 1,
    },
]


def init_layers(nn_architecture, seed=23):
    np.random.seed(seed)
    params_values = {}

    for idx, layer in enumerate(nn_architecture):
        layer_idx = idx + 1
        layer_input_size = layer["input_dim"]
        layer_output_size = layer["output_dim"]

        params_values['W' + str(layer_idx)] = np.random.randn(
            layer_output_size, layer_input_size)

        params_values['b' + str(layer_idx)] = np.random.randn(
            layer_output_size, 1)

    return params_values


def sigmoid(Z):
    return 1 / (1 + np.exp(-Z))


def sigmoid_backward(dA, Z):
    sig = sigmoid(Z)
    return dA * sig * (1 - sig)


# without the bias, the study progress will take much more batches
def single_layer_forward_propagation(A_prev, W_curr, b_curr):
    Z_curr = np.dot(W_curr, A_prev) + b_curr
    return sigmoid(Z_curr), Z_curr


def full_forward_propagation(X, params_values, nn_architecture):
    memory = {}
    A_curr = X

    for idx, layer in enumerate(nn_architecture):
        layer_idx = idx + 1
        A_prev = A_curr

        W_curr = params_values["W" + str(layer_idx)]
        b_curr = params_values["b" + str(layer_idx)]
        A_curr, Z_curr = single_layer_forward_propagation(
            A_prev, W_curr, b_curr)

        memory["A" + str(idx)] = A_prev
        memory["Z" + str(layer_idx)] = Z_curr

    return A_curr, memory


# since we are using sigmod function as activation function,
# I'm using cross entropy
def get_cost_value(Y_hat, Y):
    m = Y_hat.shape[1]
    cost = -1 / m * (np.dot(Y,
                            np.log(Y_hat).T) + np.dot(1 - Y,
                                                      np.log(1 - Y_hat).T))
    return np.squeeze(cost)


def single_layer_backward_propagation(dA_curr, W_curr, b_curr, Z_curr, A_prev):
    m = A_prev.shape[1]

    dZ_curr = sigmoid_backward(dA_curr, Z_curr)
    dW_curr = np.dot(dZ_curr, A_prev.T) / m
    db_curr = np.sum(dZ_curr, axis=1, keepdims=True) / m
    dA_prev = np.dot(W_curr.T, dZ_curr)

    return dA_prev, dW_curr, db_curr


def full_backward_propagation(Y_hat, Y, memory, params_values,
                              nn_architecture):
    grads_values = {}
    m = Y.shape[1]
    Y = Y.reshape(Y_hat.shape)

    dA_prev = -(np.divide(Y, Y_hat) - np.divide(1 - Y, 1 - Y_hat))

    for layer_idx_prev, layer in reversed(list(enumerate(nn_architecture))):
        layer_idx_curr = layer_idx_prev + 1

        dA_curr = dA_prev

        A_prev = memory["A" + str(layer_idx_prev)]
        Z_curr = memory["Z" + str(layer_idx_curr)]
        W_curr = params_values["W" + str(layer_idx_curr)]
        b_curr = params_values["b" + str(layer_idx_curr)]

        dA_prev, dW_curr, db_curr = single_layer_backward_propagation(
            dA_curr, W_curr, b_curr, Z_curr, A_prev)

        grads_values["dW" + str(layer_idx_curr)] = dW_curr
        grads_values["db" + str(layer_idx_curr)] = db_curr

    return grads_values


def update(params_values, grads_values, nn_architecture, learning_rate):
    for idx, layer in enumerate(nn_architecture):
        layer_idx = idx + 1
        params_values["W" + str(
            layer_idx)] -= learning_rate * grads_values["dW" + str(layer_idx)]
        params_values["b" + str(
            layer_idx)] -= learning_rate * grads_values["db" + str(layer_idx)]

    return params_values


def train(X, Y, nn_architecture, target_error, learning_rate):
    params_values = init_layers(nn_architecture, 2)
    print('initial weights')
    print('W1', params_values['W1'])
    print('W2', params_values['W2'])
    count = 1

    # first time
    Y_hat, cashe = full_forward_propagation(X, params_values, nn_architecture)
    cost = get_cost_value(Y_hat, Y)

    grads_values = full_backward_propagation(Y_hat, Y, cashe, params_values,
                                             nn_architecture)
    params_values = update(params_values, grads_values, nn_architecture,
                           learning_rate)

    print('first batch error')
    print(cost)

    while target_error < cost:
        count = count + 1
        Y_hat, cashe = full_forward_propagation(X, params_values,
                                                nn_architecture)
        cost = get_cost_value(Y_hat, Y)

        grads_values = full_backward_propagation(Y_hat, Y, cashe,
                                                 params_values,
                                                 nn_architecture)
        params_values = update(params_values, grads_values, nn_architecture,
                               learning_rate)

    print('final weights')
    print('W1', params_values['W1'])
    print('W2', params_values['W2'])
    print('final cost :', cost)
    print('total batches', count)
    return params_values


def main():

    train_X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]).reshape(4, 2)
    train_Y = np.array([0, 1, 1, 0]).reshape(4, 1)

    TARGET_ERROR = [0.1, 0.02]
    LEARNING_RATE = range(1, 11)

    for te in TARGET_ERROR:
        for lr in LEARNING_RATE:
            print('the TARGET_ERROR is', te, 'the LEARNING_RATE is', lr / 10)
            train(train_X.T, train_Y.T, nn_architecture, te, lr)
            print('--------------------------------------------------------')


if __name__ == "__main__":
    main()