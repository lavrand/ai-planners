import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import tensorflow as tf

# Step 1: Data Loading
# Load the data
file_path = 'output_full_norm_pressure.csv'  # make sure this points to your file
data = pd.read_csv(file_path)

# Step 2: Data Preprocessing
# Drop unnecessary columns
data = data.drop(columns=['experiment', 'File', 'nodisp', 'nodisp-disp'])

# Check for and handle missing values
missing_values = data.isnull().sum()
if missing_values.any():
    imputer = SimpleImputer(strategy='mean')
    data = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)

# Separate features and target variable
X = data.drop(columns=['disp'])
y = data['disp']

# Normalize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=42)

# Step 3: Model Building
model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)  # Output layer for regression, no activation function
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')  # MSE for regression

# Step 4: Training
history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test), verbose=1)

# Step 5: Evaluation
train_loss = history.history['loss'][-1]
val_loss = history.history['val_loss'][-1]

print(f"Final training loss: {train_loss}")
print(f"Final validation loss: {val_loss}")

# Optional: Save the model for later use
model.save('my_trained_model.h5')
