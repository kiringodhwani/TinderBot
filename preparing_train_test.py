import cv2

import numpy as np
from numpy import savez_compressed
from numpy import asarray
from numpy import load
from numpy import expand_dims
from numpy import asarray
from numpy import savez_compressed
from numpy.lib.polynomial import poly

import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import dlib 
import mtcnn
from mtcnn.mtcnn import MTCNN

from os import listdir
from os.path import isdir
from keras_facenet import FaceNet
import tensorflow as tf

def count_faces(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 
    pixels = np.asarray(img)

    detector = MTCNN()
    results = detector.detect_faces(pixels)
    
    for i, face in enumerate(results): 
        x1, y1, width, height = face['box']
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height

#         cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2) 

#         # Display the box and faces 
#         cv2.putText(img, 'face num'+str(i), (x1-10, y1-10), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) 
    
#     output = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
#     plt.figure(figsize=(10, 10))
#     plt.axis("off")
#     plt.imshow(output)
#     plt.show()

    if len(results) != 1:
        print('Multiple People or No People')
        return len(results), 0, 0, 0, 0
    else:  
        print('One Person in Photo')
        return len(results), x1, x2, y1, y2
    
    
def extract_face(filename, x1, x2, y1, y2):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 
    pixels = np.asarray(img)
    
    face = pixels[y1:y2, x1:x2]
    face_array = cv2.resize(face, (224, 224))
    
#     fig, ax = plt.subplots(figsize=(2, 2))
#     plt.imshow(face_array)
#     plt.show()
    return face_array

def load_faces(directory):
    faces = list()
    for filename in listdir(directory):
        path = directory + filename
        if filename.startswith('.'):
            continue
        print(path)
        count, x1, x2, y1, y2 = count_faces(path)
        if count == 1:
            face = extract_face(path, x1, x2, y1, y2)
            faces.append(face)
        else:
            print('bad face')

    return faces
    
def load_dataset(directory):
    X, y = list(), list()
    for subdir in listdir(directory):
        path = directory + subdir + '/'
        if not isdir(path):
            continue
        
        print(path)
        faces = load_faces(path)
        labels = [subdir for _ in range(len(faces))]
        print('>loaded %d examples for class: %s' % (len(faces), subdir))
        X.extend(faces)
        y.extend(labels)
        
    return asarray(X), asarray(y)

def get_embedding(model, face_pixels):
    face_pixels = face_pixels.astype('float32')
    
    # standardize pixel values across channels (global)
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    
    # transform face into one sample
    samples = expand_dims(face_pixels, axis=0)
    
    # make prediction to get embedding
    yhat = model.predict(samples)
    return yhat[0]

trainX, trainy = load_dataset('celebrity_faces/train/')
print(trainX.shape, trainy.shape)
savez_compressed('mindy-or-no-dataset-train.npz', trainX, trainy)

testX, testy = load_dataset('celebrity_faces/val/')
print(testX.shape, testy.shape)
savez_compressed('mindy-or-no-dataset-test.npz', testX, testy)

embedder = FaceNet()
model = tf.keras.applications.ResNet50(weights='imagenet')
 
# load the face dataset
train_data = load('mindy-or-no-dataset-train.npz')
test_data = load('mindy-or-no-dataset-test.npz')
trainX, trainy = train_data['arr_0'], train_data['arr_1']
testX, testy = test_data['arr_0'], test_data['arr_1']
print('Loaded: ', trainX.shape, trainy.shape, testX.shape, testy.shape)

# convert each face in the train set to an embedding
newTrainX = list()
for face_pixels in trainX:
    embedding = get_embedding(model, face_pixels)
    newTrainX.append(embedding)
newTrainX = asarray(newTrainX)
print(newTrainX.shape)

# convert each face in the test set to an embedding
newTestX = list()
for face_pixels in testX:
    embedding = get_embedding(model, face_pixels)
    newTestX.append(embedding)
    
newTestX = asarray(newTestX)
print(newTestX.shape)

# save arrays to one file in compressed format
savez_compressed('mindy-or-no-embeddings.npz', newTrainX, trainy, newTestX, testy)