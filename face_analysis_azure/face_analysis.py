"""
    face services

    dependency: azure, azure Ai/cognitive, face Api, python
    reference: Azure AI services doc

    features:
    - 

    notes:
    
"""


# from azure.cognitiveservices.vision


class FaceAnalysis:

    def __init__(self, faceapi_endpoint, faceapi_key):
        """
        create azure ai face api instance
        """
        # self.faceapiclient = ComputerVisionClient(vision_endpoint, CognitiveServicesCredentials(vision_key))