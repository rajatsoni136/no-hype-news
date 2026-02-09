import pandas as pd
import numpy as np
from langchain_openai import OpenAIEmbeddings
from sklearn.cluster import DBSCAN
from dotenv import load_dotenv

# 1. LOAD ENV & DATA
load_dotenv()
df = pd.read_csv("processed_news.csv")

# 2. GENERATE EMBEDDINGS
# We convert text -> numbers so math can work on them.
print("Generating embeddings for clustering...")
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small") # Cheap & fast

# We cluster based on the NEW factual titles (cleaner signal)
titles = df['new_title'].tolist()
embeddings = embeddings_model.embed_documents(titles)
embeddings_array = np.array(embeddings)

# 3. CLUSTER WITH DBSCAN
# eps = distance threshold (lower = stricter duplicates, higher = looser grouping)
# min_samples = 1 means even a single article can be a "cluster" (no grouping)
# metric = cosine distance is best for text
print("Clustering articles...")
dbscan = DBSCAN(eps=0.4, min_samples=1, metric='cosine')
clusters = dbscan.fit_predict(embeddings_array)

# 4. ASSIGN CLUSTERS TO DATAFRAME
df['cluster_id'] = clusters

# 5. GROUP BY CLUSTER
# We take the first article in each cluster as the "Representative"
unique_stories = df.sort_values('hype_score').groupby('cluster_id').first().reset_index()

print(f"Original Article Count: {len(df)}")
print(f"Unique Stories Count: {len(unique_stories)}")
print(f"Reduction: {len(df) - len(unique_stories)} duplicates removed.")

# 6. SAVE
unique_stories.to_csv("final_feed.csv", index=False)
print("Saved clean feed to final_feed.csv")

# Preview Duplicates
print("\n--- Duplicate Check ---")
duplicate_clusters = df['cluster_id'].value_counts()
duplicate_clusters = duplicate_clusters[duplicate_clusters > 1]

for cluster_id in duplicate_clusters.index[:3]: # Show top 3 groups
    print(f"\nCluster {cluster_id}:")
    print(df[df['cluster_id'] == cluster_id]['new_title'].values)