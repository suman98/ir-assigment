import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Sample documents
sport_docs = [
    "The team scored a winning goal in the last minute of the game.",
    "The athlete broke the world record in the 100-meter sprint.",
    "The basketball team won the championship for the third consecutive year."
]

health_docs = [
    "Regular exercise and a balanced diet are essential for good health.",
    "The new vaccine has shown promising results in clinical trials.",
    "Yoga and meditation can help reduce stress and improve overall well-being."
]

business_docs = [
    "The company reported a significant increase in quarterly profits.",
    "The stock market experienced a sharp decline due to economic uncertainties.",
    "The CEO announced plans to expand into new markets."
]

# Combine all documents
all_docs = sport_docs + health_docs + business_docs
categories = ['Sport'] * len(sport_docs) + ['Health'] * len(health_docs) + ['Business'] * len(business_docs)

# Vectorize documents using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(all_docs)

# Apply K-means clustering
k = 3  # Number of clusters
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(X)

# Assign labels to clusters based on predominant category
cluster_labels = []
for i in range(k):
    indices = np.where(kmeans.labels_ == i)[0]
    cluster_categories = [categories[idx] for idx in indices]
    cluster_label = max(set(cluster_categories), key=cluster_categories.count)
    cluster_labels.append(cluster_label)

# Function to assign a new document to a cluster
def assign_to_cluster(new_doc):
    # Preprocess the new document
    new_doc_vectorized = vectorizer.transform([new_doc])

    # Predict the cluster for the new document
    predicted_cluster = kmeans.predict(new_doc_vectorized)
    return cluster_labels[predicted_cluster[0]]