from sklearn.cluster import KMeans

def detect_behavior_anomaly(user_data, kmeans_model):
    cluster = kmeans_model.predict([user_data])
    if cluster not in normal_clusters:  # Define normal clusters
        return True
    return False