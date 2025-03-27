from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
import joblib

def build_autoencoder(input_dim):
    """
    Build and compile an Autoencoder model.
    """
    autoencoder = Sequential([
        Dense(14, activation='relu', input_shape=(input_dim,)),  # Encoder
        Dense(input_dim, activation='sigmoid')  # Decoder
    ])
    autoencoder.compile(optimizer='adam', loss='mean_squared_error')
    return autoencoder

def train_autoencoder(X_train, epochs=50, batch_size=256):
    """
    Train the Autoencoder model.
    """
    input_dim = X_train.shape[1]
    autoencoder = build_autoencoder(input_dim)
    autoencoder.fit(X_train, X_train, epochs=epochs, batch_size=batch_size, shuffle=True)
    return autoencoder

import numpy as np

def detect_anomaly_autoencoder(features, autoencoder, threshold=0.1):
    """
    Detect anomalies using the trained Autoencoder.
    """
    # Ensure features are in the correct shape
    features = np.array(features).reshape(1, -1)
    
    # Reconstruct the input
    reconstructed = autoencoder.predict(features)
    
    # Calculate the mean squared error (MSE)
    mse = np.mean(np.power(features - reconstructed, 2), axis=1)
    
    # Return True if the MSE exceeds the threshold (anomaly detected)
    return mse > threshold

def save_autoencoder(autoencoder, filepath):
    """
    Save the Autoencoder model to a file.
    """
    autoencoder.save(filepath)
    print(f"Autoencoder saved to {filepath}")

def load_autoencoder(filepath):
    """
    Load the Autoencoder model from a file.
    """
    from tensorflow.keras.models import load_model
    autoencoder = load_model(filepath)
    print(f"Autoencoder loaded from {filepath}")
    return autoencoder


import numpy as np

# Example training data (replace with your dataset)
X_train = np.random.rand(1000, 10)  # 1000 samples, 10 features

# Train the Autoencoder
autoencoder = train_autoencoder(X_train)

# Save the Autoencoder
save_autoencoder(autoencoder, 'models/autoencoder.h5')