# ScribbleScan - Application for detecting spelling mistakes from a photo of handwritten text
The project was done as part of my Engineering Thesis for the Military University of Technology

# Description
The application works on the basis of an HTR model I created, which uses neural networks. 
The whole model accepts as training data a set of IAMs and its own created set of images in Polish. 
Upon start-up, the application asks the user to upload an image for text analysis and to select the language in 
which the text is located (the application currently supports Polish and English). The application then reads 
out the text in the photo using a previously created and trained HTR model. The user can correct the text if 
it has been misread by the application, and then, after the text has been sent, the application displays the 
sent photo with the spelling mistake highlighted and provides suggestions for the correct word. In addition, 
the app corrects the text according to the suggestions and shows the mistakes the user has made. The application 
will only work properly if images of a scan of handwritten text with a thick black marker are uploaded to it.

# Screen demo
* Home Screen
![image](https://github.com/Pixel535/ScribbleScan---Engineering-thesis/assets/72218516/089abcdc-66c9-45cb-8c28-3598d0f284f3)
* Image Selection Screen
![image](https://github.com/Pixel535/ScribbleScan---Engineering-thesis/assets/72218516/15f8ac80-381a-4986-a5bd-f8012759d899)
* Choosing language Screen
![image](https://github.com/Pixel535/ScribbleScan---Engineering-thesis/assets/72218516/14595151-e49d-4480-bd29-08e35bcb2037)
* Text Reading Screen
![image](https://github.com/Pixel535/ScribbleScan---Engineering-thesis/assets/72218516/c6525752-a7d2-4908-a66a-3c2531d12b73)
* Text Updating Screen
![image](https://github.com/Pixel535/ScribbleScan---Engineering-thesis/assets/72218516/af0cbd8b-4b8e-4d58-9947-40f259784cd0)
* Marking Spelling Mistakes Screen
![image](https://github.com/Pixel535/ScribbleScan---Engineering-thesis/assets/72218516/5de3fbf0-b2bc-43e4-a087-b041aed7a984)


# Getting started
To add all modules and packages required for this project you need to open terminal and type following commands:
```
$ pip install mltu==0.1.7
$ pip install tensorflow==2.10.0
$ pip install pyenchant
$ pip install tkinter
$ pip install opencv-python
$ pip install pillow
```

# Used Technologies
* Python 3.10
* Matplotlib
* Tkinter
* OpenCV
* PyEnchant
* NumPy
* Mltu (Machine Learning Training Utilities)
* Keras
* TensorFlow
* Typing
* Pillow


# Special thanks go to Pylessons (https://pylessons.com/handwritten-sentence-recognition) for the clear tutorial, help and the library that helped in creating and training the HTR model.
