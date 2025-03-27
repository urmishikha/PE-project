import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
columns = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 
           'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
           'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
           'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login', 
           'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
           'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 
           'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
           'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
           'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
           'dst_host_srv_rerror_rate', 'attack', 'last_flag']

# Load dataset
df = pd.read_csv("/Users/urmisikhadash/KDD.txt", names=columns)

# Encode categorical variables
encoder = LabelEncoder()
df['protocol_type'] = encoder.fit_transform(df['protocol_type'])
df['service'] = encoder.fit_transform(df['service'])
df['flag'] = encoder.fit_transform(df['flag'])

# Encode attack labels (1 = attack, 0 = normal)
df['attack'] = df['attack'].apply(lambda x: 0 if x == 'normal' else 1)

# Normalize numeric features
scaler = StandardScaler()
features = df.drop(columns=['attack'])
labels = df['attack']
features_scaled = scaler.fit_transform(features)

# Split data
X_train, X_test, y_train, y_test = train_test_split(features_scaled, labels, test_size=0.2, random_state=42)

print(f"Training set size: {X_train.shape}, Testing set size: {X_test.shape}")

from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, classification_report

# Train Isolation Forest model
model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
model.fit(X_train)

# Predict anomalies
y_pred = model.predict(X_test)
y_pred = np.where(y_pred == -1, 1, 0)  # Convert -1 (anomalies) to 1, others to 0

# Evaluate model
print("Classification Report:")
print(classification_report(y_test, y_pred))
import joblib

# Save the trained model
print("Saving model...")
joblib.dump(model, 'models/anomaly_model.pkl')

# Save the scaler
print("Saving scaler...")
joblib.dump(scaler, 'models/anomaly_model_scaler.pkl')

print("Both files saved successfully!")

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

# Example training data (replace with your dataset)
X_train = np.random.rand(1000, 10)  # 1000 samples, 10 features

# Build the autoencoder
input_dim = X_train.shape[1]
autoencoder = Sequential([
    Dense(14, activation='relu', input_shape=(input_dim,)),
    Dense(input_dim, activation='sigmoid')
])
autoencoder.compile(optimizer='adam', loss='mean_squared_error')

# Train the autoencoder
autoencoder.fit(X_train, X_train, epochs=50, batch_size=256, shuffle=True)

# Save the autoencoder
autoencoder.save('models/autoencoder.h5')
print("Autoencoder saved.")