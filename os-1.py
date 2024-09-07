import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from tensorflow.keras.utils import to_categorical
import tensorflow as tf

# Load the specified CSV file with a specified encoding
data_file = "D:/hackmaggadon/UNSW_NB15_training-set.csv"

# Reading the CSV file with 'ISO-8859-1' encoding to handle special characters
data = pd.read_csv(data_file, encoding='ISO-8859-1', low_memory=False)

# Inspect the dataset
print(data.head())

# Define categorical and numerical columns
categorical_columns = ['proto', 'service', 'state']
numerical_columns = [col for col in data.columns if col not in categorical_columns + ['label', 'id', 'attack_cat']]

# Label encoding for the 'attack_cat' column
data['attack_cat'] = data['attack_cat'].fillna('Unknown')  # Handle missing values if any
attack_cat_encoder = LabelEncoder()
data['attack_cat_encoded'] = attack_cat_encoder.fit_transform(data['attack_cat'])

# Combine 'attack_cat_encoded' with numerical features
numerical_columns.append('attack_cat_encoded')

# Label encoding for the target variable 'label'
label_encoder = LabelEncoder()
data['label'] = label_encoder.fit_transform(data['label'])

# Ensure only existing columns are dropped
columns_to_drop = [col for col in ['label', 'id', 'attack_cat'] if col in data.columns]
X = data.drop(columns=columns_to_drop)

# Apply transformations
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_columns),
        ('cat', OneHotEncoder(), categorical_columns)]
)

# Fit and transform the data
X_processed = preprocessor.fit_transform(X)
y = to_categorical(data['label'])  # One-hot encode the labels

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

# Build the model
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(len(label_encoder.classes_), activation='softmax')  # Output layer with softmax
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Predict on new data
sample_data = X_test[0:1]  # Using the first example from the test set as a sample
prediction = model.predict(sample_data)
predicted_label = label_encoder.inverse_transform([prediction.argmax()])

print(f"Predicted Threat Type: {predicted_label[0]}")
