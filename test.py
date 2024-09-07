import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import pandas as pd


model = tf.keras.models.load_model("unsw_nb15_cyber_threat_detection_model.h5")


data_file = "D:/hackmaggadon/UNSW_NB15_training-set.csv"
data = pd.read_csv(data_file, encoding='ISO-8859-1', low_memory=False)


sample_data = data.iloc[[100]] 

columns_to_drop = ['swin', 'attack_cat', 'label']
sample_features = sample_data.drop(columns=columns_to_drop)


sample_features_processed = LabelEncoder.preprocessor.transform(sample_features)


prediction = model.predict(sample_features_processed)
predicted_label = LabelEncoder.inverse_transform([prediction.argmax()])


predicted_attack_cat = LabelEncoder.attack_cat_encoder.inverse_transform([sample_data['attack_cat_encoded'].values[0]])

print(f"Predicted Attack Name: {predicted_label[0]}")
print(f"Actual Attack Type: {predicted_attack_cat[0]}")
