#!/usr/bin/python3



import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
import spotipy.util as util
import pprint
from statistics import mode
import cgitb;
import cv2,cgi
from keras.models import load_model
import numpy as np

from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input

# parameters for loading data and images
detection_model_path = '/home/akshay/face_classification/trained_models/detection_models/haarcascade_frontalface_default.xml'
emotion_model_path = '/home/akshay/face_classification/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
gender_model_path = '/home/akshay/face_classification/trained_models/gender_models/simple_CNN.81-0.96.hdf5'
emotion_labels = get_labels('fer2013')
gender_labels = get_labels('imdb')
font = cv2.FONT_HERSHEY_SIMPLEX

# hyper-parameters for bounding boxes shape
frame_window = 10
gender_offsets = (30, 60)
emotion_offsets = (20, 40)

# loading models
face_detection = load_detection_model(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
gender_classifier = load_model(gender_model_path, compile=False)

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]
gender_target_size = gender_classifier.input_shape[1:3]

# starting lists for calculating modes
gender_window = []
emotion_window = []

# starting video streaming
cv2.namedWindow('window_frame')
video_capture = cv2.VideoCapture(0)
while True:

    bgr_image = video_capture.read()[1]
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    faces = detect_faces(face_detection, gray_image)

    for face_coordinates in faces:

        x1, x2, y1, y2 = apply_offsets(face_coordinates, gender_offsets)
        rgb_face = rgb_image[y1:y2, x1:x2]

        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
        gray_face = gray_image[y1:y2, x1:x2]
        try:
            rgb_face = cv2.resize(rgb_face, (gender_target_size))
            gray_face = cv2.resize(gray_face, (emotion_target_size))
        except:
            continue
        gray_face = preprocess_input(gray_face, False)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        emotion_label_arg = np.argmax(emotion_classifier.predict(gray_face))
        emotion_text = emotion_labels[emotion_label_arg]
        emotion_window.append(emotion_text)

        rgb_face = np.expand_dims(rgb_face, 0)
        rgb_face = preprocess_input(rgb_face, False)
        gender_prediction = gender_classifier.predict(rgb_face)
        gender_label_arg = np.argmax(gender_prediction)
        gender_text = gender_labels[gender_label_arg]
        gender_window.append(gender_text)

        if len(gender_window) > frame_window:
            emotion_window.pop(0)
            gender_window.pop(0)
        try:
            emotion_mode = mode(emotion_window)
            gender_mode = mode(gender_window)
        except:
            continue

        if gender_text == gender_labels[0]:
            color = (0, 0, 255)
        else:
            color = (255, 0, 0)

  
    print ("Content-type:text/html\r\n\r\n")
    print("<html>")
    print("<head>")
    print("<meta charset='utf-8'>")
    print("<title>MoodHymn</title>")
    #print("<script src='includefiles/jquery-3.1.1.min.js'></script>")
    #print('<link rel="stylesheet" href="includefiles/bootstrap-3.3.7/dist/css/bootstrap.min.css">')
    #print("<script type='text/javascript' src='includefiles/bootstrap-3.3.7/dist/js/bootstrap.min.js'></script>")
    #print('<link rel = "stylesheet" type = "text/css" href = "x.css">')

    print("</head>")
    if emotion_text=='happy':
        print('<body style= "background-color:powderblue;">') 
    elif emotion_text=='neutral':
        print('<body style= "background-color:gray;">')
    elif emotion_text=='angry':
        print('<body style= "background-color:red;">')
    elif emotion_text=='sad':
        print('<body style= "background-color:cyan;">')
    else :
        print('<body style= "background-color:magenta;">') 




    print("<h2 style='text-align: center;'>Hello %s %s</h2>" % (emotion_text,gender_text))
    break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client_id='d8f7a47d2e124cfaa89a631d1b37a586'
client_secret='23b9f3608a654d3f99f2197f376ddd7d'
redirect_uri='http://localhost:8080/callback/'
scope = 'playlist-modify-public'
username='nsb42mgqzd11gj0th9tim29dd'

client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
creds = oauth2.SpotifyClientCredentials(client_id, client_secret)
token = creds.get_access_token()
#emotion_text='happy'
#print(' <iframe src="https://www.google.com" height="200" width="300" name="iframe_a"></iframe>  ')
results = sp.search(q=emotion_text, limit=25)
print("<div id='sent-mail'>")
print('<div>')
print('<div>')
print('<div>')
print('<ul ">')
for i, t in enumerate(results['tracks']['items']):
    print('<li>')
    print('<h3><i>%s</i> &nbsp &nbsp <a target="_blank" href="%s"> Play </a> </h3>' %(t['name'],t['external_urls']['spotify']))
    print('<hr>');
    print(" </li>")
print("</ul></div></div></div></div>")
print("</body>")
print("</html>")

























