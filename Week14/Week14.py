# Exercise 2 use meanshift on the iris dataset

#     1. load 'iris_data.csv' into a dataframe
#     2. get unique labels (Species column)
#     3. plot with a scatter plot each iris flower sample colored by label (3 different colors)
#     4. use: MeanShift and estimate_bandwidth from sklearn.cluster to first estimate bandwidth and then get the clusters 
#        (HINT: estimate_bandwidth() takes an argument: quantile set it to 0.2 for best result
#     5. print out labels, cluster centers and number of clusters (as returned from the MeanShift function)
#     6. create a new scatter plot where each flower is colored according to cluster label
#     7. add a dot for the cluster centers
#     8. Compare the 2 plots (colored by actual labels vs. colored by cluster label)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import estimate_bandwidth
from sklearn.cluster import MeanShift
from itertools import cycle

#     1. load 'iris_data.csv' into a dataframe
def get_data():
    iris_data = pd.read_excel("iris_data.xlsx")
    # print("iris data:\n")
    # print(iris_data)
    return iris_data

#     2. get unique labels (Species column)
def get_species():
    iris_data = get_data()
    print("\n")
    print(iris_data["Species"])

#     3. plot with a scatter plot each iris flower sample colored by label (3 different colors)
def create_plot_data(leaf_type):
    dataframe = get_data()
    g1 = dataframe.loc[dataframe['Species'] == "I. setosa"]
    g2 = dataframe.loc[dataframe['Species'] == "I. versicolor"]
    g3 = dataframe.loc[dataframe['Species'] == "I. virginica"]
    
    if leaf_type == "sepal":
        setosa_sepal = (g1["Sepal length"].values, g1["Sepal width"].values)
        versicolor_sepal = (g2["Sepal length"].values, g2["Sepal width"].values)
        virginica_sepal = (g3["Sepal length"].values, g3["Sepal width"].values)
        data_sepal = (setosa_sepal, versicolor_sepal, virginica_sepal)
        return data_sepal
    elif leaf_type == "petal":
        setosa_petal = (g1["Petal length"].values, g1["Petal width"].values)
        versicolor_petal = (g2["Petal length"].values, g2["Petal width"].values)
        virginica_petal = (g3["Petal length"].values, g3["Petal width"].values)
        data_petal = (setosa_petal, versicolor_petal, virginica_petal)
        return data_petal
    else:
        print("Leaf type has to be either 'petal' or 'sepal'")
        return None

def scatter_plot_iris(data, leaf_type):
    colors = ("red", "green", "blue")
    groups = ("setosa", "versicolor", "virginica")

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for data, color, group in zip(data, colors, groups):
        x, y = data
        ax.scatter(x, y, alpha=0.8, c=color, edgecolors='none', s=30, label=group)

    plt.title('Iris data {}'.format(leaf_type))
    plt.legend(loc=2)
    plt.show()

# data = create_plot_data("sepal")
# scatter_plot_iris(data, "sepal")
# data = create_plot_data("petal")
# scatter_plot_iris(data, "petal")

#     4. use: MeanShift and estimate_bandwidth from sklearn.cluster to first estimate bandwidth and then get the clusters 
#        (HINT: estimate_bandwidth() takes an argument: quantile set it to 0.2 for best result

def est_bandwidth(data, quantile):
    bw = estimate_bandwidth(data, quantile=quantile)
    return bw

data = get_data()
data = pd.get_dummies(data, columns=["Species"])
bandwidth = est_bandwidth(data, 0.2)
print("Bandwidth: {}".format(str(bandwidth)))

def get_clusters(data, bandwidth):
    analyzer = MeanShift(bandwidth=bandwidth) 
    return analyzer.fit(data)

clusters = get_clusters(data, bandwidth)
print(clusters)


#     5. print out labels, cluster centers and number of clusters 
#       (as returned from the MeanShift function)

def get_labels_and_centers(clusters):
    labels = clusters.labels_
    # print(labels)
    centers = clusters.cluster_centers_
    n_clusters = len(np.unique(labels))
    return labels, centers, n_clusters

labels, centers, n_clusters = get_labels_and_centers(clusters)
print("Labels")
print(labels)
print("Cluster centers")
print(centers)
print("Number of clusters")
print(n_clusters)

def create_cluster_labels(data, labels):
    data["cluster_group"] = np.nan
    data_length = len(data)
    for i in range(data_length):
        data.iloc[i, data.columns.get_loc("cluster_group")] = labels[i]

create_cluster_labels(data, labels)

def group_and_count_flowers(data):
    cluster_data = data.groupby(["cluster_group"]).mean()
    cluster_data["Counts"] = pd.Series(data.groupby(["cluster_group"]).size())
    return cluster_data

cluster_data = group_and_count_flowers(data)
print(cluster_data)


print("\n______________________________\n")

#labels, cluster_centers, n_clusters = MeanShift(data)

#     6. create a new scatter plot where each flower is colored according to cluster label

# I don't understand this exercise

#     7. add a dot for the cluster centers

# plot_data = create_plot_data("sepal")

def create_plot_w_cluster_centers(data, n_clusters, labels, cluster_centers):
    plt.figure(1)
    plt.clf()

    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters), colors):
        my_members = labels == k
        cluster_center = cluster_centers[k]
        plt.plot(data.iloc[my_members, 0], data.iloc[my_members, 1], col + '.')
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=14)
    plt.title('Estimated number of clusters: %d' % n_clusters)
    plt.show()

create_plot_w_cluster_centers(data, n_clusters, labels, centers)
