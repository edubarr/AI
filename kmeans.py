"""
Implementação do algoritmo K-means para agrupamento. Os dados utilizados são gerados aleatoriamente idade e renda e com isso calculado um score de crédito. 
A classificação é feita tendo como base os 3 dados.
A quantidade de dados gerados pode ser alterado modificando o argumento da chamada k_mean.generate_records(X), trocando X pelo número de dados. 
Assim como a quantidade de Clusters na chamada k_mean.initiate_cluster_and_centroid(X)
Após execução é exibido os registros classificados e os Clusters com os centroides das regiões.
"""
from math import sqrt
import random
import sys

class record:
    def __init__(self, id, age, income, score):
        self.id = id
        self.age = age
        self.income = income
        self.score = score
        self.cluster_number = None

    def to_string(self):
        return "Record [id=" + str(self.id) + ", age=" + str(self.age) + ", income=" + str(self.income) + ", score=" + str(self.score) + ", cluster=" + str(self.cluster_number) + "]"
    
class cluster:
    def __init__(self, cluster_number, age_centroid, income_centroid, score_centroid):
        self.cluster_number = cluster_number
        self.age_centroid = age_centroid
        self.income_centroid = income_centroid
        self.score_centroid = score_centroid
        
    def to_string(self):
        return "Cluster [ageCentroid=" + str(self.age_centroid) + ", incomeCentroid=" + str(self.income_centroid) + ", scoreCentroid=" + str(self.score_centroid) + ", cluster=" + str(self.cluster_number) + "]"
    
    def calculate_euclidean(self, record):
        return sqrt(pow(self.age_centroid - record.age, 2) + pow(self.income_centroid - record.income, 2) + pow(self.score_centroid - record.score, 2))
    
    def update_centroids(self, record):
        self.age_centroid = (self.age_centroid + record.age) / 2
        self.income_centroid = (self.income_centroid + record.income) / 2
        self.score_centroid = (self.score_centroid + record.score) / 2
        
class kmeans:
    def __init__(self):
        self.records = []
        self.clusters = []
        self.cluster_records = []
        
    def generate_records(self, qnt):
        for i in range(qnt):
            age = random.randint(18, 99)
            income = random.randint(1300, 10000)
            score = (age * income) / 1000
            self.records.append(record(i, age, income, score))
         
    def initialize_cluster(self, clusternumber, record):
        c = cluster(clusternumber, record.age, record.income, record.score)
        self.clusters.append(c)
        cluster_record = []
        cluster_record.append(record)
        self.cluster_records.append([c, cluster_record])
        
            
    def initiate_cluster_and_centroid(self, qnt):
        counter = 0
        for record in self.records:
            if counter < qnt:
                record.cluster_number = counter
                self.initialize_cluster(counter, record)
                counter = counter + 1
            else:
                # Printa o estado atual dos clusters antes de cada atualização
                # print(record.to_string())
                # print("*** Cluster Information ***")
                # for cluster in self.clusters:
                #     print(cluster.to_string())
                # print("**********")
            
                min_distance = sys.maxsize
                which_cluster = None
                
                for cluster in self.clusters:
                    distance = cluster.calculate_euclidean(record)
                    if min_distance > distance:
                        min_distance = distance
                        which_cluster = cluster
                        
                record.cluster_number = which_cluster.cluster_number
                which_cluster.update_centroids(record)
                
                for i, item in enumerate(self.cluster_records):
                    if item == which_cluster:
                        self.cluster_records[i].append(record)
            
            # Printa o estado atual dos clusters após cada atualização
            # print("*** Cluster Information ***")
            # for cluster in self.clusters:
            #     print(cluster.to_string())
            # print("***************")
            
    def print_records(self):
        print("*** Each Record Info ***")
        for record in self.records:
            print(record.to_string())
            
    def print_clusters(self):
        print("*** Final Clusters ***")
        for cluster in self.clusters:
            print(cluster.to_string())
            
k_mean = kmeans()
k_mean.generate_records(300)
k_mean.initiate_cluster_and_centroid(4)
k_mean.print_records()
print()
k_mean.print_clusters()