import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd


model = tf.keras.models.load_model("unsw_nb15_cyber_threat_detection_model.h5")


data_file = "D:/hackmaggadon/UNSW_NB15_training-set.csv"
data = pd.read_csv(data_file, encoding='ISO-8859-1', low_memory=False)


attack_cat_encoder = LabelEncoder()
data['attack_cat'] = data['attack_cat'].fillna('Unknown')  
data['attack_cat_encoded'] = attack_cat_encoder.fit_transform(data['attack_cat'])


columns_to_drop = ['id', 'attack_cat', 'label']
columns_to_drop = [col for col in columns_to_drop if col in data.columns]
sample_features = data.drop(columns=columns_to_drop)


categorical_columns = ['proto', 'service', 'state']
numerical_columns = [col for col in data.columns if col not in categorical_columns + ['label', 'attack_cat', 'attack_cat_encoded']]


preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_columns),
        ('cat', OneHotEncoder(), categorical_columns)
    ]
)


preprocessor.fit(data.drop(columns=columns_to_drop))


sample_data = data.iloc[[100]]  


sample_features_processed = preprocessor.transform(sample_features)


prediction = model.predict(sample_features_processed)
predicted_label = attack_cat_encoder.inverse_transform([prediction.argmax()])


actual_attack_cat = attack_cat_encoder.inverse_transform([sample_data['attack_cat_encoded'].values[0]])

print(f"Predicted Attack Name: {predicted_label[0]}")
print(f"Actual Attack Type: {actual_attack_cat[0]}")
