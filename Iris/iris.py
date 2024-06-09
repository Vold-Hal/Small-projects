import numpy as np

weights = np.zeros((3, 4 + 1)) # +1 for the bias

# def Dot(arr):
#     score = 0
#     for i, x in enumerate(arr[:-1]):
#         score += x * weights[i]
#     return score


ITERATIONS = 2000
LEARNING_RATE = 0.0001

# Specify the file path
file_path = "iris.data.txt"

# Read the data from the text file
data = np.genfromtxt(file_path, delimiter='\t')
data = np.array([[1.0] + row.tolist() for row in data])
#Structure of each array in data: [1, x1, x2, x3, x4, class]
np.random.shuffle(data)  


print("############### MULTICLASS PERCEPTRON CLASSIFIER ###############")
#TRAINING
for iteration in range(ITERATIONS):
    wrong = 0
    for object in data:
        x = object[:-1]
        y = object[-1] - 1

        predicted = np.argmax(np.dot(weights, x))

        if predicted != y :
            wrong += 1
            weights[int(y)] += LEARNING_RATE * x
            weights[int(predicted)] -= LEARNING_RATE * x
    if (iteration + 1) % (ITERATIONS/10) == 0:
        print("iteration " , iteration + 1, ", errors: ", wrong)

print("############### ONE-VS-ALL PERCEPTRON CLASSIFIER ###############")

for iteration in range(ITERATIONS):
    wrong = 0

    for i, object in enumerate(data):
        x = object[:-1]
        y = object[-1] - 1

        max_score = -100000
        max_num = -1
        for num, weight in enumerate(weights):
            score = np.dot(weight, x)

            if max_score < score:
                max_score = score
                max_num = num

            if score <= 0 and num == y:
                weight += LEARNING_RATE * x
            elif score > 0 and num != y:
                weight -= LEARNING_RATE * x
        
        if max_num != y:
            wrong += 1

    if (iteration + 1) % (ITERATIONS/10) == 0:
        print("iteration " , iteration + 1, ", errors: ", wrong)