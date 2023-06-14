from ImageProcessing import imageProcessing
import os
import cv2
from tqdm import tqdm
from csv import writer


FILEPATH0 = 'Data/Image/J2'
FILEPATH = 'Data/Image/train/No Jaundice'
for img in tqdm(os.listdir(FILEPATH)):
    path = os.path.join(FILEPATH, img)
    image = cv2.imread(path)
    eye , face = imageProcessing.__init__(image)
    print(img)
    inter = [eye, face, 0]
    with open('Data/DataSet.csv','a')as f_object:
        write = writer(f_object)
        write.writerow(inter)
    pass