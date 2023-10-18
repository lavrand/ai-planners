import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load the data
data = pd.read_csv('output_full_norm.csv')

# Separate the features and target variables
X = data[['deadline1', 'deadline2', 'deadline3', 'deadline4', 'deadline5']]
y_disp = data['disp']
y_nodisp = data['nodisp']

# Splitting data into training and testing sets (80% train, 20% test)
X_train, X_test, y_disp_train, y_disp_test = train_test_split(X, y_disp, test_size=0.2, random_state=42)
_, _, y_nodisp_train, y_nodisp_test = train_test_split(X, y_nodisp, test_size=0.2, random_state=42)

# Linear Regression for 'disp'
model_disp = LinearRegression().fit(X_train, y_disp_train)
predictions_disp = model_disp.predict(X_test)

# Linear Regression for 'nodisp'
model_nodisp = LinearRegression().fit(X_train, y_nodisp_train)
predictions_nodisp = model_nodisp.predict(X_test)

# Evaluate the models
mse_disp = mean_squared_error(y_disp_test, predictions_disp)
mse_nodisp = mean_squared_error(y_nodisp_test, predictions_nodisp)

print(f"MSE for disp: {mse_disp}")
print(f"MSE for nodisp: {mse_nodisp}")
