from ImageProcessing import imageProcessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import pickle
import cv2


data = pd.read_csv("/media/mina/Mina M. Atalla/Projects/Web_App/WEB_APP/MODEL/Data Set test.csv")
im = cv2.imread("/home/mina/Desktop/14.1.jpeg")
x = data.drop(['Jaundice'], axis=1)
y = data['Jaundice']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=123)
classifier = GaussianNB()
classifier.fit(x_train, y_train)
eye , face = imageProcessing.__init__(im)

cases = [eye, face]
classi = classifier.predict([cases])
if classi == 1:
    cla = 'Has Jaundice'
    TcB = 1
else:
    cla = 'Does not Have Jaundice'
    TcB = 0
    
    
    
print(cla)    