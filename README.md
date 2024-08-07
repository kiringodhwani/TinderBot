# TinderBot with Race-based Swiping

A Tinder bot that opens and logs into Tinder, swipes right on ('likes') only East Asian women, scrapes Tinder matches for their profile information, and messages Tinder matches with real Boston locations related to their passions. 

## Description
A fully autonomous bot that…
1. Opens and logs into Tinder using a connected Facebook account.
2. Swipes through potential matches, only ‘liking’ the profiles of East Asian women (i.e., swipes right on East Asian woman and swipes left on all other woman).
3. Scrapes the profiles of Tinder matches and messages them based on their name, age, and passions. Includes real Boston locations in the messages.
4. Handles all Tinder pop-ups that may appear during 1-3.

For an in-depth explanation of TinderBot's capabilities along with video examples of TinderBot in action, please see the attached Youtube video.

## Steps of Race-based Auto Swiping
1. Use Selenium to extract the current image from the person’s profile.
2. Apply a Multi-Task Cascaded Convolutional Neural Network (MTCNN) for face detection. The MTCNN identifies all faces in the image and draws bounding boxes around them. This is a deep learning model presented in "Joint Face Detection and Alignment Using Multitask Cascaded Convolutional Networks" from 2016.
3. Extract the person’s face according to the bounding box drawn by the MTCNN. 
4. Apply a ResNet50 neural network pretrained on ImageNet to create a face embedding for the extracted face. This maps the face to a vector representation that captures its important characteristics. The distance between two face embeddings directly corresponds to a measure of face similarity. The model can be found here: https://www.tensorflow.org/api_docs/python/tf/keras/applications/ResNet50. 
5. Apply a KNeighborsClassifier (trained on 500+ face embeddings) to the face embedding to determine if the person is East Asian or not. If the classifier has more than 75% confidence that the current person is East Asian, then we swipe right (i.e., ‘like’ the current profile). Else, we flip to the next image in the user’s profile and repeat. 
If the model cannot confidently identify the person as East Asian after reviewing all profile images, then we swipe left (i.e., ‘dislike’ the current profile).

**For video of this process, please see the attached Youtube video!**

Tech Tools Used: **Tensorflow**, **Keras**, **scikit-learn**, **OpenCV**, **NumPy**, **Selenium**, **Matplotlib**

## Steps of Tinder messaging with real Boston locations related to the Tinder match's passions
1. Scrape matches for their chat id, name, age, work, place of study, home location, gender, bio, relationship preference, distance from you, and passions.
2. Use the Google Gemini API to message matches based on their name, age, and passions. Use a prompt that requires Gemini to include real Boston locations in the messages it generates.

**For video of this process, please see the attached Youtube video!**

<ins>Google Gemini prompt:</ins>

*Task: Write an introductory message to a girl named {match name} that I met on a dating app.*

*Context: {match name} is a {match age}-year-old girl that lives in Boston. She is passionate about {match passions}.*

*Examples:*

*- For a 21-year-old girl from Boston named Maria that is passionate about Tennis -> "Hey Maria. Tennis this weekend at Dean park? I can pick you up."*

*- For a 19-year-old girl from Boston named Jenna that is passionate about painting and sushi -> "Hey Jenna. How about we show each other our favorite paintings at the Museum of Fine Arts and then I buy you some sushi down the street at Douzo Sushi?*

*- For a 22-year-old girl from Boston named Maya that is passionate about ramen -> "Hey Maya. Ramen date at Ganko Ittetsu on me?"*

*Format: A concise 1-2 sentence text message with no exclamation points and no return characters. Do not include bracketed text like "[sushi restaurant near you]" or “[Rock climbing gym in Boston]”; instead, provide real locations in Boston in your message. If your message includes bracketed text instead of real locations than everything will explode.*

Tech Tools Used:  **Google Gemini API**, **Selenium**

## Description

## Getting Started

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
