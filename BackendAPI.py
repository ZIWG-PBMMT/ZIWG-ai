from flask import Flask, request
import requests
import base64
import json                    

image_file = 'TestImg.jpg'

app = Flask(__name__)
url = 'http://127.0.0.1:5053/validate'

@app.route("/",methods = ['POST', 'GET'])
def main():
    """
    The main route of the Flask application.

    This route returns the string "Hello world!" when accessed.

    Returns:
    - str: The response message "Hello world!".

    """

    return "Hello world!"

@app.route("/send",methods = ['POST', 'GET'])
def send():
    """
    Sends the image data to the validation endpoint.

    This route reads the image file, encodes it as base64, and sends it along with a letter as JSON data to the
    validation endpoint at the specified URL.

    Returns:
    - str: A confirmation message indicating that the data has been sent.
    """

    with open(image_file, "rb") as img:
        string = base64.b64encode(img.read()).decode('utf-8')

    requests.post(url, json={'user_photo':string, 'letter':'k'})   

    return "Data sent"

@app.route("/receive",methods = ['POST', 'GET'])
def receive():
    """
    Receives the response from the validation endpoint.

    This route receives the JSON response from the validation endpoint and prints the value of the 'recognition' field.

    Returns:
    - dict: The received JSON data.
    """
    response = request.get_json()
    print(f"Twoja odpowiedz jest: {response['recognition']}")

    return response

app.run(debug=True, port=5050)