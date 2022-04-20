#DBScan file
###Parameters:
#Data Matrix
#Minpts
#e

###Returns:
#means
#clusters found
##Label points:
#Core
#Border
#Noise

from sklearn.datasets import make_blobs
import numpy as np
import math

#Get distance between 2 points
def distance(mean_point, distance_point):
    return math.sqrt(sum([(mean_point[index] - distance_point[index]) ** 2 for index in range(len(mean_point))]))

#Return if in neighborhood
def within_neighborhood(point_1, point_2, max_distance):
    return distance(point_1, point_2) <= max_distance

class Point():
    #Point is a tuple of point values
    def __init__(self, point):
        self.point = point
        self.label =  "noise"
        self.cluster = []

    def get_cluster(self, cluster = []):
        length = len(cluster)
        new = []
        new.append(self)
        new.append(self.cluster)
        cluster.append(self)
        cluster.append(self.cluster)
        print(len(cluster))
        cluster = list(set(cluster))
        if len(cluster) == length:
            return cluster
        for item in new:
            cluster = get_cluster(cluster)
        return cluster


def dbscan(matrix, minpts = 5, e = 10000):
    points = [Point(tuple(matrix[row,:])) for row in range(len(matrix))]
    for item in points:
        #print(item.point)
        for other in points:
            if within_neighborhood(item.point, other.point, minpts):
                item.cluster.append(other)
                other.cluster.append(item)
    for item in points:
        item.cluster = list(set(item.cluster))
        if len(item.cluster) >= minpts:
            item.label = "core"
        else:
            for other in item.cluster:
                if other.label == "core":
                    item.label = "border"
                    break
    return [point.get_cluster() for point in points]
            

#Testing Space
D, labels = make_blobs(n_samples=500, centers=3, cluster_std=.3, random_state=0)

D.shape

scan = dbscan(D, 6)
for item in scan:
    print(item)
