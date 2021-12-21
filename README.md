# P5-Baxter (AAU robotics, 5. semester)
This is the 5. semester project "Knowledge driven spoken language interface for industrial robotics manipulation based on Baxter Robot".
The project aims to create a language-interface based solution for assembly of the dummmy phone using the Baxter Robot. The language interface will be built using the Google Cloud speech API for capturing and recognizing audio stream. This input will be processed and used as commands in knowledge-driven decision making for the Baxter robot to assemble a dummy phone. For object detection of the dummy phone parts, a pre-trained YOLOv3 network were to be used, but it performed poor in our case, so instead an OpenCV script has been used. Integration of these different methods for an overall solution can be found in this repository. Custom grippers and fixtures has also been made for this project.

To run this repo, two computers must be used. One running Ubuntu 14 and a valid version of ROS. The other one just needs to work and have python 3 installed.
The Ubuntu 14 computer will need to be connected to Baxter, and a regular WiFi network which allows the use of our TCP server-client.
The other computer, lets call it python3 computer, will have to be connected to the same WiFi. 

PYTHON3 computer start:
*****************************************************************************************************
*A good start is to make sure you have a working google voice recognition API token.                *
*Please make sure, that all libraries is installed. Most should be standard libraries, except       *
*the ones from the Google script.                                                                   *
*Maybe try following a Google tutorial.                                                             *
*When the speechrecogaudiostream.py script is working all that is needed, is to run this script.    *
*It will open TCP client itself and send whatever data is needed. However please make sure the IP   *
*in the Client script is working                                                                    *
*****************************************************************************************************

Ubuntu 14 computer start:

First step is to use the baxter.sh script in the terminal to setup the environment for communicating with baxter (make sure baxter ip and your ip are correct in the script)
The first script needs to be launched in a terminal where the baxter.sh script has been used. The script is started using rosrun baxter_tools actionserver.py

In a second terminal again run the baxter.sh script. Then go to the SpeechRecognitionGoogle folder and use rosrun baxter_tools TCP_server.py

Make sure the action folder is located in baxter_tools folder