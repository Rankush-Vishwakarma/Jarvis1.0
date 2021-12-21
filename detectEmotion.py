from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
from time import sleep
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
def load_model():
    json_file = open('facial_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights("facial_model_h5.h5")
    return model
#global faces, face
#dictionary = {'Angry':0, 'Disgust':0,'Fear':0,'Happy':0,'Neutral':0, 'Sad':0, 'surprise':0}
global cap
def Emotion(dictionary=None):
    loaded_model = load_model()
    #print("model loaded")

    face_classfier = cv2.CascadeClassifier(r'FrontalFace_harscascade.xml')

    Emotion = ['Angry', 'Disgust','Fear','Happy','Neutral', 'Sad', 'surprise']
    dictionary = {'Angry':0, 'Disgust':0,'Fear':0,'Happy':0,'Neutral':0, 'Sad':0, 'surprise':0}

    cap = cv2.VideoCapture(0)

    while True:
        success , frame = cap.read()
        labels = []
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_classfier.detectMultiScale(gray)
        #print(faces)
        # getting single face only with the help of Region of Interest (ROI), and grab the largest area.
        if type(faces) is not tuple:
            max_  = max(faces, key=lambda faces: sum(faces.tolist())).tolist()
            if sum(max_) > 700:
                face_index = faces.tolist().index(max_)
                face = np.take(faces,face_index,axis=0)
                face = face.reshape((1,4))
                #print(type(face),'-',face,':faces-:',faces)
                faces = face.copy()
        else:
            continue
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            roi_gray = gray[y:y+h, x:x+h]
            roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray])!=0:
                #roi = roi_gray.astype('float')/255.0
                roi = img_to_array(roi_gray)
                roi = np.expand_dims(roi,axis = 0)

                prediction = loaded_model.predict(roi)
            
                label = Emotion[prediction.argmax()]
                for key,value in dictionary.items():
                    if key==label:
                        dictionary[key]+=1
                print(dictionary)
                label_position = (x,y-10)
                cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),2)
            else:
                cv2.putText(frame, 'No face', (30,80),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),2)
        #cv2.imshow('Emotion Detect ', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return dictionary

if __name__ == '__main__':
    dictionary = Emotion()
