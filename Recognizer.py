import cv2
import torch
import numpy as np
from model import Net

class Recognizer:
    """
    The Recognizer class handles image recognition tasks using a pre-trained model.

    This class provides methods to initialize the object, perform image recognition, and determine if the recognized
    letter matches the expected letter.
    """
    def __init__(self):
        """
        Initializes the Recognizer object.

        This method initializes the Recognizer object by loading the pre-trained model and setting it to evaluation mode.
        The model is moved to the CPU device. Additionally, a dictionary of sign labels and corresponding letters is
        created.

        Attributes:
        - model (torch.jit.ScriptModule): The pre-trained model for image recognition.
        - signs (dict): A dictionary mapping label indices to corresponding letters.
        """

        self.model = torch.jit.load('model_scripted.pt')
        self.model.eval()
        self.model.to('cpu')
        self.signs = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F', '6': 'G', '7': 'H', '8': 'I',
                      '10': 'K', '11': 'L', '12': 'M', '13': 'N', '14': 'O', '15': 'P', '16': 'Q', '17': 'R',
                      '18': 'S', '19': 'T', '20': 'U', '21': 'V', '22': 'W', '23': 'X', '24': 'Y' }

    def is_correct(self, path_img: str, letter: str):
        """
        Performs image recognition and checks if the recognized letter matches the expected letter.

        This method takes the path to an image file and an expected letter as input. It processes the image, performs
        recognition using the pre-trained model, and compares the recognized letter with the expected letter.

        Args:
        - path_img (str): The path to the image file.
        - letter (str): The expected letter.

        Returns:
        - bool: True if the recognized letter matches the expected letter, False otherwise.
        """
        if letter == self._process_frame(path_img):
            return True
        return False

    def _process_frame(self, img: None):
        """
        Processes the image for recognition.

        This method takes an image and prepares it for recognition by resizing it to 28x28 pixels, converting it to
        grayscale, normalizing the pixel values, and passing it through the pre-trained model for inference.

        Args:
        - img (None): The image to process.

        Returns:
        - str: The recognized letter.

        Note:
        This is a method and should not be called directly from outside the class.

        """
        img = cv2.imread(img)

        res = cv2.resize(img, dsize=(28, 28), interpolation=cv2.INTER_CUBIC)
        res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

        res1 = np.reshape(res, (1, 1, 28, 28)) / 255
        res1 = torch.from_numpy(res1)
        res1 = res1.type(torch.FloatTensor)

        out = self.model(res1)
        probs, label = torch.topk(out, 25)
        probs = torch.nn.functional.softmax(probs, 1)

        pred = out.max(1, keepdim=True)[1]
        # if float(probs[0, 0]) < 0.4:
        #     return 'Sign not detected'
        # else:
        return self.signs[str(int(pred))]