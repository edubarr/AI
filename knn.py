# Implementação do algoritmo K-NN para predição. Algoritmo foi treinado com o dataset iris, e foi utilizado validação cruzada para calcular a acurácia média.
from random import seed
from random import randrange
from csv import reader
from math import sqrt

# Carrega o arquivo iris.csv como lista
def load_csv(filename):
    dataset = []
    with open(filename, "r") as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset


# Converte a coluna de string para float
def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())


# Converte a coluna da espécie de flor para um inteiro
def specie_to_int(dataset, column):
    class_values = [row[column] for row in dataset]
    unique = set(class_values)
    lookup = dict()
    for i, value in enumerate(unique):
        lookup[value] = i
        print("[%s] => %d" % (value, i))
    for row in dataset:
        row[column] = lookup[row[column]]
    return lookup


# Normaliza os dados em uma escala 0 - 1
def normalize_dataset(dataset, minmax):
    for row in dataset:
        for i in range(len(row)):
            row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])


# Calcula a distância euclidiana entre dois pontos
def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1) - 1):
        distance += (row1[i] - row2[i]) ** 2
    return sqrt(distance)


# Encontra os vizinhos similares
def get_neighbors(train, test_row, k):
    distances = list()
    for train_row in train:
        dist = euclidean_distance(test_row, train_row)
        distances.append((train_row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for i in range(k):
        neighbors.append(distances[i][0])
    return neighbors


# Calcula a classe
def predict_class(train, test_row, k):
    neighbors = get_neighbors(train, test_row, k)
    output_values = [row[-1] for row in neighbors]
    prediction = max(set(output_values), key=output_values.count)
    return prediction


# Divide os dados para validação cruzada
def dataset_split(dataset, n_folds):
    dataset_split = list()
    dataset_copy = list(dataset)
    fold_size = int(len(dataset) / n_folds)
    for _ in range(n_folds):
        fold = list()
        while len(fold) < fold_size:
            index = randrange(len(dataset_copy))
            fold.append(dataset_copy.pop(index))
        dataset_split.append(fold)
    return dataset_split


# Faz a avaliação do algoritmo usando a validação cruzada e retorna a lista das 5 acurácias
def test_knn(dataset, knn, n_folds, *args):
    folds = dataset_split(dataset, n_folds)
    scores = list()
    for fold in folds:
        train_set = list(folds)
        train_set.remove(fold)
        train_set = sum(train_set, [])
        test_set = list()
        for row in fold:
            row_copy = list(row)
            test_set.append(row_copy)
            row_copy[-1] = None
        predicted = knn(train_set, test_set, *args)
        actual = [row[-1] for row in fold]
        accuracy = accuracy_metric(actual, predicted)
        scores.append(accuracy)
    return scores


# Calcula a acurácia comparando as predições com os dados reais
def accuracy_metric(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            correct += 1
    return correct / float(len(actual)) * 100.0


# Executa o K-NN em todas as linhas do dataset de teste
def k_nn(train, test, k):
    predictions = list()
    for row in test:
        predictions.append(predict_class(train, row, k))
    return predictions


# Executa o algoritmo para treinar e testar a acurácia e faz uma predição
def main():
    seed(1)
    dataset = load_csv("iris.csv")  # Carrega o arquivo do dataset iris
    for i in range(len(dataset[0]) - 1):
        str_column_to_float(dataset, i)
    specie_to_int(dataset, len(dataset[0]) - 1)  # Converta as colunas para float e int
    # Define os parâmetros
    n_folds = 5
    k = 5
    # define novos dados para ser calculada a espécie
    data = [4.5, 2.3, 1.3, 0.3]
    specie = predict_class(dataset, data, k)
    print("Dados = %s, Previsão: %s\n" % (data, specie))
    accuracys = test_knn(dataset, k_nn, n_folds, k)
    print("Acurácias calculadas: %s" % accuracys)
    print("Acurácia média: %.3f%%" % (sum(accuracys) / float(len(accuracys))))


main()
