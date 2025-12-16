import numpy as np

class NeuralNet:
    # 생성
    def __init__(self, input_nodes, hidden_nodes, output_nodes, hidden_layers=1):
        self.i_nodes = input_nodes
        self.h_nodes = hidden_nodes
        self.o_nodes = output_nodes
        self.h_layers = hidden_layers
        
        self.activations = []
        self.weights = []
        self.weights.append(np.random.uniform(-1, 1, (self.h_nodes, self.i_nodes + 1)))
        for _ in range(self.h_layers - 1):
            self.weights.append(np.random.uniform(-1, 1, (self.h_nodes, self.h_nodes + 1)))

        self.weights.append(np.random.uniform(-1, 1, (self.o_nodes, self.h_nodes + 1)))
    
    # 활성화 함수 relu
    def relu(self, x):
        return np.maximum(0, x)

    # 계산
    def predict(self, inputs_arr):
        self.activations = []

        inputs = np.append(np.array(inputs_arr), 1)
        current_outputs = inputs
        self.activations.append(np.array(inputs_arr))

        for i in range(self.h_layers):
            hidden_inputs = self.weights[i] @ current_outputs
            hidden_outputs = self.relu(hidden_inputs)
            self.activations.append(hidden_outputs)
            current_outputs = np.append(hidden_outputs, 1)

        final_inputs = self.weights[-1] @ current_outputs
        final_outputs = self.relu(final_inputs)

        self.activations.append(final_outputs)
        
        return final_outputs.tolist()

    # 복제
    def clone(self):
        clone = NeuralNet(self.i_nodes, self.h_nodes, self.o_nodes, self.h_layers)
        clone.weights = [np.copy(w) for w in self.weights]
        return clone

    # 교차 
    def crossover(self, partner):
        child = self.clone()
        for i in range(len(self.weights)):
            rows, cols = self.weights[i].shape
            rand_r = np.random.randint(rows)
            rand_c = np.random.randint(cols)
            
            for r in range(rows):
                for c in range(cols):
                    if r < rand_r or (r == rand_r and c <= rand_c):
                        pass
                    else:
                        child.weights[i][r, c] = partner.weights[i][r, c]
        return child

    # 변이
    def mutate(self, mutation_rate):
        for i in range(len(self.weights)):
            rows, cols = self.weights[i].shape
            for r in range(rows):
                for c in range(cols):
                    if np.random.rand() < mutation_rate:
                        self.weights[i][r, c] += np.random.normal() / 5
                        self.weights[i][r, c] = np.clip(self.weights[i][r, c], -1, 1)