# TinderBot with Race-based Auto Swiping

TinderBot opens and logs into Tinder, uses a trained face recognition system to swipe right on ('like') only East Asian women, scrapes Tinder matches for their profile information, and messages Tinder matches with real Boston locations related to their passions. 

[**Youtube Video:**](https://www.youtube.com/watch?v=Vy4h-TA6Ylo)

[<img width="725" alt="Screenshot 2024-08-09 at 5 42 26 PM" src="https://github.com/user-attachments/assets/211b6fec-585a-4d7c-a4ec-86d5c1189ff1">](https://www.youtube.com/watch?v=Vy4h-TA6Ylo)

## Description
A fully autonomous bot that…
1. Opens and logs into Tinder using a connected Facebook account.
2. Uses a trained face recognition system to swipe through potential matches, only ‘liking’ the profiles of East Asian women (i.e., swipes right on East Asian woman and swipes left on all other woman). See **Steps of Race-based Auto Swiping** for further explanation. 
3. Scrapes the profiles of Tinder matches and sends tailored messages to them, utilizing their name, age, and passions. Includes real Boston locations related to their passions in the messages.
4. Handles all Tinder pop-ups that may appear during 1-3.

**For an in-depth explanation of TinderBot's capabilities along with video examples of TinderBot in action, please see the attached [Youtube video](https://www.youtube.com/watch?v=Vy4h-TA6Ylo)!**

### Steps of Race-based Auto Swiping

Tech Tools Used: **Tensorflow**, **Keras**, **scikit-learn**, **OpenCV**, **NumPy**, **Selenium**, **Matplotlib**
1. Use Selenium to extract the current image from the person’s profile.
2. Apply a Multi-Task Cascaded Convolutional Neural Network (MTCNN) for face detection. The MTCNN identifies all faces in the image and draws bounding boxes around them. This is a deep learning model presented in "Joint Face Detection and Alignment Using Multitask Cascaded Convolutional Networks" from 2016.
3. Extract the person’s face according to the bounding box drawn by the MTCNN. 
4. Apply a ResNet50 neural network pretrained on ImageNet to create a face embedding for the extracted face. This maps the face to a vector representation that captures its important characteristics. The distance between two face embeddings directly corresponds to a measure of face similarity. The model can be found here: https://www.tensorflow.org/api_docs/python/tf/keras/applications/ResNet50. 
5. Apply a KNeighborsClassifier (trained on 500+ face embeddings) to the face embedding to determine if the person is East Asian or not. If the classifier has more than 75% confidence that the current person is East Asian, then TinderBot swipes right (i.e., ‘likes’ the current profile). Else, TinderBot flips to the next image in the user’s profile and repeats.
6. If TinderBot cannot confidently identify the person as East Asian after reviewing all profile images, then TinderBot swipes left (i.e., ‘dislikes’ the current profile).

**For video of the auto swiping process, please see the attached Youtube video!**

### Steps of Tinder Messaging

Tech Tools Used:  **Google Gemini API**, **Selenium**
1. Scrape matches for their chat id, name, age, work, place of study, home location, gender, bio, relationship preference, distance from you, and passions.
2. Use the Google Gemini API to message matches based on their name, age, and passions. Use a prompt that requires Gemini to include real Boston locations related to the match's passions in the message it generates.

<ins>Google Gemini prompt:</ins>

*Task: Write an introductory message to a girl named {match name} that I met on a dating app.*

*Context: {match name} is a {match age}-year-old girl that lives in Boston. She is passionate about {match passions}.*

*Examples:*

*- For a 21-year-old girl from Boston named Maria that is passionate about Tennis -> "Hey Maria. Tennis this weekend at Dean park? I can pick you up."*

*- For a 19-year-old girl from Boston named Jenna that is passionate about painting and sushi -> "Hey Jenna. How about we show each other our favorite paintings at the Museum of Fine Arts and then I buy you some sushi down the street at Douzo Sushi?*

*- For a 22-year-old girl from Boston named Maya that is passionate about ramen -> "Hey Maya. Ramen date at Ganko Ittetsu on me?"*

*Format: A concise 1-2 sentence text message with no exclamation points and no return characters. Do not include bracketed text like "[sushi restaurant near you]" or “[Rock climbing gym in Boston]”; instead, provide real locations in Boston in your message. If your message includes bracketed text instead of real locations than everything will explode.*

**For video of the messaging process, please see the attached [Youtube video](https://www.youtube.com/watch?v=Vy4h-TA6Ylo)!**

## Getting Started 

### Dependencies
* Python Platform: macOS-14.4.1-arm64-arm-64bit
* Python 3.10.14
* selenium==4.22.0
* tensorflow==2.16.2
* keras==3.4.1
* opencv-python==4.10.0.84
* numpy==1.26.4
* scikit-learn==1.5.1

### Configuration
In your **config.py** file, you have to set the following fields:
1. The email and password for the Facebook account that you use to sign into Tinder.
2. Your Google Gemini API Key.

### Executing program
```
python run.py
```

## Authors
[Kirin Godhwani](https://www.linkedin.com/in/kiringodhwani/) (kiringodhwani@gmail.com)

## Acknowledgments
* [TinderBotz](https://github.com/frederikme/TinderBotz)
* [Automate Tinder using Python & ChatGPT 🔥 | Code with me](https://www.youtube.com/watch?v=VM55efbOkCM)
* [How to Develop a Face Recognition System Using FaceNet in Keras](https://machinelearningmastery.com/how-to-develop-a-face-recognition-system-using-facenet-in-keras-and-an-svm-classifier/)
