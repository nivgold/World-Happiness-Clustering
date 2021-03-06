from sklearn.cluster import KMeans

# do the cluster operation
def cluster(dataset, num_of_runs, num_of_clusters):
    df_no_country = dataset.drop(['country'], axis=1)
    labels = KMeans(n_clusters=num_of_clusters, n_init=num_of_runs, random_state=4).fit_predict(df_no_country)
    dataset["Cluster"] = labels
