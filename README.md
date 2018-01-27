# MoodHymns
# ABSTRACT
Our project basically deals with the the creation of an automatically generated playlist based on the mood of the user as music plays a very important role in human daily life and in the modern advanced technologies. The difficulties in the creation of large playlists and time required to search a song based on the current mood can be overcome here. This Music Website itself selects songs according to the current mood of the user.
Since existing methods for automating the playlist generation process are computationally slow, less accurate and additional hardware like EEG and sensors are required to achieve the task,this proposed approach will use machine learning algorithms to get the information about current facial expressions and hence generate a playlist based on the result.
# INTRODUCTION
Since facial expressions are best way to express ones feelings,mood and emotions and its computational algorithms have leser complexity,it can be one of the best way to decide one current flavour of music.
The introduction of spotify API in the traditional music players provided automatically parsing the playlist based on various classes of emotions and moods which was parsed through 'face_classification'.
'face_classification' API basically categorises a user's mood in one of the five categories 'Happy','Sad','Angry','Neutral' and 'Surprise' and based on that result a playlist of the songs is generated.  
# TECHNICAL APPROACH
To analyse the current mood of the user we used an API 'face_classification' which have implemented deep learning(Tensor Flow) in its methodology and this result was fed as input to an another API 'Spotify'.
An input to our project is given by feeding an image clicked through webcam.

