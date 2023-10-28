from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import pandas as pd
import joblib  # for saving the model
from sklearn.tree import export_graphviz  # for tree visualization
import os  # for path operations and checking
import subprocess

# Load the data
data = pd.read_csv('output_full_norm_pressure.csv')

# Define the features explicitly
features = ['deadline1', 'deadline2', 'deadline3', 'deadline4', 'deadline5']

# Prepare feature matrix (X) and target vector (y)
X = data[features]
y = data['nodisp-disp']

# Handling missing values if there are any
# For simplicity, we're filling missing values with the column mean.
# More sophisticated imputation methods can be used for more accurate results.
if X.isnull().values.any():
    X.fillna(X.mean(), inplace=True)

if y.isnull().values.any():
    y.fillna(y.mean(), inplace=True)

# Split the data into training and testing sets (75% train, 25% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Create a Random Forest Regressor model and fit it to the training data
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Predicting the target for the test data
y_pred = model.predict(X_test)

# Calculating the performance metrics
mae = mean_absolute_error(y_test, y_pred)  # Mean Absolute Error
mse = mean_squared_error(y_test, y_pred)  # Mean Squared Error
rmse = np.sqrt(mse)  # Root Mean Squared Error
r2 = r2_score(y_test, y_pred)  # R squared value

print(f"mae, mse, rmse, r2 =  {mae, mse, rmse, r2}")

plt.figure(figsize=(14, 6))

# 2. Actual vs. Predicted values plot
plt.subplot(1, 2, 1)
plt.scatter(y_test, y_pred, color='blue', alpha=0.5)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)  # Diagonal line
plt.xlabel('Actual values')
plt.ylabel('Predicted values')
plt.title('Actual vs. Predicted Values')

# 3. Residuals plot
residuals = y_test - y_pred

plt.subplot(1, 2, 2)
plt.scatter(y_pred, residuals, color='red', alpha=0.5)
plt.hlines(y=0, xmin=y_pred.min(), xmax=y_pred.max(), colors='black', linestyles='dashed', lw=2)
plt.xlabel('Predicted values')
plt.ylabel('Residuals')
plt.title('Residuals vs. Predicted Values')

plt.tight_layout()
plt.show()

# Number of random entries to generate
num_samples = 10000  # We generate a large sample space to then pick the top entries from

# Understanding the range of deadline values
deadline_min_values = X.min()
deadline_max_values = X.max()



# Generate random data within the observed range
np.random.seed(42)  # for reproducibility
random_deadlines = np.random.uniform(low=deadline_min_values, high=deadline_max_values, size=(num_samples, len(features)))

# Use the model to predict "nodisp-disp" for these random deadlines
random_nodisp_disp = model.predict(random_deadlines)

# Create a DataFrame to store this data
random_data = pd.DataFrame(random_deadlines, columns=features)
random_data['predicted_nodisp_disp'] = random_nodisp_disp

# Select the top 100 entries with the highest predicted "nodisp-disp"
top_100_entries = random_data.nlargest(100, 'predicted_nodisp_disp')

top_100_entries.head()  # Display the first few rows of the top 100 entries

# Define the path for saving the file
output_path = 'top_100_predicted_nodisp_disp.csv'

# Save the top 100 entries to a CSV file
top_100_entries.to_csv(output_path, index=False)  # The index is excluded from the saved file

# Save the model to a separate file
model_filename = 'random_forest_regressor_model.pkl'
joblib.dump(model, model_filename)
print(f"Model saved as {model_filename}")

# Extract the nth tree from the forest
n = 0  # You can choose which tree you want to visualize by changing this value
nth_tree = model.estimators_[n]

# Export as dot file
tree_export_filename = 'tree_from_random_forest.dot'
export_graphviz(nth_tree, out_file=tree_export_filename,
                feature_names = features,
                rounded = True, proportion = False,
                precision = 2, filled = True)


# Check if Graphviz is installed and in PATH
try:
    subprocess.run(['dot', '-V'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except subprocess.CalledProcessError:
    raise Exception("Graphviz not installed or not in PATH. Please install Graphviz and ensure 'dot' is available in your PATH.")

# Export as dot file
tree_export_filename = 'tree_from_random_forest.dot'
export_graphviz(nth_tree, out_file=tree_export_filename,
                feature_names = features,
                rounded = True, proportion = False,
                precision = 2, filled = True)

# Convert the dot file to a PNG image
output_image_filename = 'tree_from_random_forest.png'
subprocess.run(['dot', '-Tpng', tree_export_filename, '-o', output_image_filename], check=True)

print(f"Tree visualization saved as {output_image_filename}. You can view this image directly.")

try:
    subprocess.run(['xdg-open', output_image_filename], check=True)
except subprocess.CalledProcessError:
    print(f"Could not open the image. Please manually open '{output_image_filename}' to view the tree visualization.")

print(f"Tree visualization saved as {tree_export_filename}. You can convert it to PNG or PDF using external utilities.")

print(f"Finished successfully")

# visualize
# dot -Tpng tree_from_random_forest.dot -o tree_from_random_forest.png
