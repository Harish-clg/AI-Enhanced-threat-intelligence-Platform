import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd

# Load the trained model
model = tf.keras.models.load_model("unsw_nb15_cyber_threat_detection_model.h5")

# Define preprocessing parameters
numerical_columns = [...]  # Add your numerical columns here
categorical_columns = [...]  # Add your categorical columns here

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_columns),
        ('cat', OneHotEncoder(), categorical_columns)]
)

attack_cat_encoder = LabelEncoder()
label_encoder = LabelEncoder()

def predict_threat(sample_data):
    processed_data = preprocessor.transform(sample_data)
    prediction = model.predict(processed_data)
    predicted_label = label_encoder.inverse_transform([int(prediction[0][0] > 0.5)])
    return predicted_label[0]
