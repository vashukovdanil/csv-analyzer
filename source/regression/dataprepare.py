import pandas as pd
from sklearn.impute import SimpleImputer

def fillMissingValues(dataset):
    nulls = dataset.isnull().sum().reset_index()
    nulls = nulls[nulls[0] != 0]["index"].tolist()

    new_data = pd.DataFrame()
    imp = SimpleImputer(strategy='most_frequent')
    new_data = pd.DataFrame(imp.fit_transform(dataset))
    new_data.columns = dataset.columns

    for column in nulls:
        dtype = dataset[column].dtype
        dataset[column] = new_data[column]
        dataset[column] = dataset[column].astype(dtype)

    return dataset

def getIndexes(dataset, column):
    result = {}
    i = 0
    for el in dataset[column]:
        if el not in result.keys():
            result[el] = i
            i += 1
    return result

def categorialToAbsolute(dataset):
    for column in dataset.columns:
        if dataset[column].dtype == object:
            indexes = getIndexes(dataset, column)
            temp = []
            for el in dataset[column]:
                temp.append(indexes[el])
            dataset[column] = temp
    return dataset