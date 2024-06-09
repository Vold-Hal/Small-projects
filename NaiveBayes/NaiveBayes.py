import numpy as np
import pandas as pb
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")



data = pb.read_csv("train.csv")
test_data = pb.read_csv("test.csv")

# LOADING DATA


labels = data.iloc[:,0].values
pixels_data = data.iloc[:,1:].values

# CALCULATING PROBABILITIES
pixels_data = (pixels_data > 109).astype(int) #making pixel data into 0,1 

counts = [[0.0] * 784 for _ in range(10)] #Initialize a list to count pixels for each number
total_amount = np.zeros(10)

for i, label in enumerate(labels):
    if (i+1) % 10000 == 0:
        print("trained on samples:" , i+1 )
    total_amount[label] += 1
    counts[label] += pixels_data[i]


probabilities = counts / (total_amount[:, np.newaxis] + 1e-10)

total_occurrences = sum(total_amount)

# Calculate prior probabilities
prior_probabilities = [count / total_occurrences for count in total_amount]


###TESTING PART###


print("TEST HAS BEGUN")

# LOADING DATA


labels = test_data.iloc[:,0].values
pixels_data = test_data.iloc[:,1:].values

# # Making probabilities into log to avoid overflow
np_probabilities = np.array(probabilities)
# log_probabilities = np.log(np_probabilities)

# CALCULATING PREDICTIONS
pixels_data = (pixels_data > 109).astype(int) #making pixel data into 0,1 

# Initialize empty arrays for failed data, labels, and predictions
failed_data = np.empty((0,), dtype=np.uint8)  # Assuming 784 pixels
failed_labels = []
failed_predictions = []

right_count = 0
count = 0

for i, test_image in enumerate(pixels_data):
    if (i+1) % 1000 == 0:
        print("tested samples:" , i+1 )

    max_probability = float('-inf')
    predicted_label = None
    
    for digit in range(10):
        probability = np.log(prior_probabilities[digit] + 1e-10)  # Initialize with prior probability
        
        # Calculate likelihood of observing the test data given the class (digit)
        probability += np.sum(np.log(probabilities[digit] * test_image + (1 - probabilities[digit]) * (1 - test_image) + 1e-10))
        # Check if this class (digit) has higher probability than the current max5
        if probability > max_probability:
            max_probability = probability
            predicted_label = digit
    if labels[i] == predicted_label:
        right_count += 1
    else:
        failed_data = np.append(failed_data, pixels_data[i], axis=0)
        failed_labels.append(labels[i])
        failed_predictions.append(predicted_label)
    count += 1
    

print("Success rate is ", right_count/count * 100, "%")


np_probabilities = np_probabilities.reshape(-1, 28, 28)
failed_data = failed_data.reshape(-1, 28, 28)

for n in range(len(failed_data)):
    if n % 2 == 0:
        # Plot all heatmaps in a single figure
        cols = 3  # Number of columns in the grid
        rows = 2  # Number of rows in the grid
        fig, axes = plt.subplots(rows, cols, figsize=(12, 12))  

    current_axes = None
    if n % 2 == 0:
        current_axes = axes.flat[:3]
    else:
        current_axes = axes.flat[-3:]

    for i, ax in enumerate(current_axes):
        plot_position = i % 3
        if plot_position == 0:
            sns.heatmap(np_probabilities[failed_labels[n]], cmap='gray', cbar=False, ax=ax)
            ax.set_title(f'Expected {failed_labels[n]}')
        elif plot_position == 1:
            sns.heatmap(failed_data[n], cmap='gray', cbar=False, ax=ax)
            ax.set_title(f'Sample {failed_labels[n]}')
        elif plot_position == 2:
            sns.heatmap(np_probabilities[failed_predictions[n]], cmap='gray', cbar=False, ax=ax)
            ax.set_title(f'Expected Digit {failed_predictions[n]}')
        ax.axis('off')
    
    if n % 2 == 1:
        plt.tight_layout()
        plt.show()








