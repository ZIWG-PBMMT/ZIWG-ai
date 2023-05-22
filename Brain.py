from flask import Flask, request
import base64
import requests
import os
from Recognizer import Recognizer


class Brain:
    """
    The Brain class handles the Flask server and image recognition tasks.

    This class represents the brain of the application, responsible for handling the Flask server and image recognition
    tasks. It provides methods to initialize the object, handle validation requests, and run the Flask server.
    """

    def __init__(self):
        """
        Initializes the Brain object.

        Attributes:
        - app (Flask): The Flask application object.
        - photo (str): String representation of the user's photo.
        - letter (str): String representation of the letter to validate.
        - path_img (str): Path to save the received image.
        - recognizer (Recognizer): The image recognition object.
        """
        self.app = Flask(__name__)
        self.photo = str
        self.letter = str
        self.path_img = 'compare.jpg'
        self.recognizer = Recognizer()
        
        @self.app.route("/validate", methods = ['POST', 'GET'])
        def validate_request():
            """
            Handles the request to validate the user's photo against a given letter.

            This method receives a request to validate the user's photo against a provided letter. It retrieves the user's
            photo and letter from the request's JSON payload. The received image is saved to the file system. Then it is
            passed to the `Recognizer` object to perform the validation. If it is correctly recognized as the provided
            letter, the response is set to True. Otherwise, the response is set to False.

            The validation response is sent as a JSON payload in a POST request to 'http://127.0.0.1:5050/receive'. The payload
            contains a single key-value pair with the response set as the value.

            After sending the response, image file is removed from the file system.

            Returns:
            - str: The validation response as a string. The response will be either 'True' or 'False'.
            """

            self.photo = request.get_json()['user_photo']
            self.letter = request.get_json()['letter']
            self._save_received_img(self.photo)
            if self.recognizer.is_correct(self.path_img, self.letter):
                response = True
            else:
                response = False
            # print(response)
            requests.post('http://127.0.0.1:5050/receive', json = {'recognition': response})
            try:
                os.remove('compare.jpg')
            except OSError:
                pass
            return str(response)


    def _save_received_img(self, photo):
        """
        Saves the received image to the file system.

        This method takes a string representation of the received image and decodes it from base64 format. The decoded
        photo data is then saved as an image file named "compare.jpg" in the file system.

        Args:
        - photo (str): String representation of the received image.
        """
        photo_data = base64.b64decode(photo)
        with open("compare.jpg", "wb") as file:
            file.write(photo_data)
    
    def run_server(self):
        """
        Runs the Flask server.

        Note:
        The server runs in debug mode and listens on port 5053.
        """
        self.app.run(debug=True, port=5053)

