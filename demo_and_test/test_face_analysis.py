"""
    test - face analysis by azure cognitive

    dependency:     python, azure cognitive
    reference:      face_analysis_azure
    notes:          as a sample for face analysis 
"""

import unittest
import os
import sys

'''
    add path to package

    Note: optional (depending on the environment)
'''
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from face_analysis_azure.face_analysis import FaceAnalysis
import face_analysis_azure.secrets as commvar


class TestFaceAnalysisAzure(unittest.TestCase):
    """
        test functions - face_analysis
        note: serve as demo and showcase
    """

    def __init__(self, *args, **kwargs):
        """
            init: create an instance of face_analysis
        """
        super().__init__(*args, **kwargs)
        self.face_analysis = FaceAnalysis(commvar.COG_FACEAPI_ENDPOINT, commvar.COG_FACEAPI_KEY)
        self.imageuri = commvar.IMAGE_URL_1

    def test_face_attributes(self):
        """
            call module to analysis faces in an image
        """
        try:
            exception = None
            self.face_analysis.analyze_faces(self.imageuri)
        except Exception as context:
            exception = context
            print(f"failed: {context}")

        # with self.assertRaises(Exception) as context:
        #     self.face_analysis.analyze_faces(self.imageuri)

        # demo purpose, make it pass
        # with self.assertRaises(Exception):
        #     print("failed!")
        self.assertIsNone(exception, f"Face analysis failed: {exception}")
        # self.assertIn("Invalid request", str(context.exception), "")

    
if __name__ == "__main__":
    unittest.main()
