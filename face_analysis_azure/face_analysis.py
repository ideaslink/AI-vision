"""
    face services

    dependency: azure, azure Ai/cognitive, face Api, python
    reference: Azure AI services doc

    features:
    - 

    notes:
    
"""


from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import FaceAttributeType
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
import requests
from io import BytesIO

class FaceAnalysis:

    def __init__(self, faceapi_endpoint, faceapi_key):
        """
        create azure ai face api instance
        """
        self.faceapiclient = FaceClient(faceapi_endpoint, CognitiveServicesCredentials(faceapi_key))

    def analyze_faces(self, image_url, features=None):
        """
        analyze faces
        """
        print("\nanalyzing faces---\n")
        
        # analyze image and get face attributes

        # get face attributes
        if features is None:
            features = [FaceAttributeType.age, FaceAttributeType.gender, FaceAttributeType.smile, FaceAttributeType.glasses, FaceAttributeType.emotion]
              
        # features = [FaceAttributeType.age, FaceAttributeType.gender, FaceAttributeType.smile, FaceAttributeType.facialHair, FaceAttributeType.glasses, FaceAttributeType.emotion, ]
        # resp = requests.get(image_url)
        # image = BytesIO(resp.content)
        # image.show()

        # with open("trump_td.jpg", "rb") as f:
            # detected_faces = self.faceapiclient.face.detect_with_stream(image=f, return_face_attributes=features, return_face_id=True)
       
        detected_faces = self.faceapiclient.face.detect_with_url(url=image_url, return_face_attributes=features)

        if not detected_faces:
            print("No face detected in the image.")
            return

        for face in detected_faces:
            # print(f"\nFace ID: {face.face_id}\n")
            print("\nFace attributes:\n")
            attrs = face.face_attributes.as_dict()
            for attr, value in attrs.items():
                print(f"\n  {attr}: {value}")

            