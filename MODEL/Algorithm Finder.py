from lazypredict.Supervised import LazyClassifier
from sklearn.model_selection import train_test_split
import pandas as pd


data = pd.read_csv("/Data/Data Set test.csv")
x = data.drop(['Jaundice'], axis=1)
y = data['Jaundice']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=123)
classifier = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None)
models, predictions = classifier.fit(x_train, x_test, y_train, y_test)
print(models)