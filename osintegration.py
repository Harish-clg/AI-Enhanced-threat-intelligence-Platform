import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
import tensorflow as tf

data_file = "D:/hackmaggadon/UNSW_NB15_training-set.csv"


data = pd.read_csv(data_file, encoding='ISO-8859-1', low_memory=False)


print(data.head())


categorical_columns = ['proto', 'service', 'state']
numerical_columns = [col for col in data.columns if col not in categorical_columns + ['label', 'id', 'attack_cat']]


data['attack_cat'] = data['attack_cat'].fillna('Unknown') 
attack_cat_encoder = LabelEncoder()
data['attack_cat_encoded'] = attack_cat_encoder.fit_transform(data['attack_cat'])


numerical_columns.append('attack_cat_encoded')


label_encoder = LabelEncoder()
data['label'] = label_encoder.fit_transform(data['label'])


columns_to_drop = [col for col in ['label', 'id', 'attack_cat'] if col in data.columns]
X = data.drop(columns=columns_to_drop)


preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_columns),
        ('cat', OneHotEncoder(), categorical_columns)]
)


X_processed = preprocessor.fit_transform(X)
y = data['label']


X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)


model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])


model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))


loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy:.2f}")


model.save("unsw_nb15_cyber_threat_detection_model.h5")


model = tf.keras.models.load_model("unsw_nb15_cyber_threat_detection_model.h5")


sample_data = X_test[0:1]  
prediction = model.predict(sample_data)
predicted_label = label_encoder.inverse_transform([prediction.argmax()])

print(f"Predicted Threat Type: {predicted_label[0]}")


