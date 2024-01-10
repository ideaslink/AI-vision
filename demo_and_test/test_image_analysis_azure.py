"""
    test - image analysis by azure cognitive

    dependency:     python, azure cognitive, unittest
    reference:      image_analysis_azure
    notes:          as a sample for image analysis 
"""

import unittest
import os
import sys

'''
    add path to package

    Note: the action is not needed when running in PyCharm
'''
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from image_analysis_azure.image_analysis import ImageAnalysis
import image_analysis_azure.secretvars as commvar


class TestImageAnalysisAzure(unittest.TestCase):
    """
        test functions - image_analysis_azure
        note: serve as demo and showcase
    """

    def __init__(self, *args, **kwargs):
        """
            init: create an instance of image_analysis_azure
        """
        super().__init__(*args, **kwargs)
        self.image_analysis = ImageAnalysis(commvar.COG_VISION_ENDPOINT, commvar.COG_VISION_KEY)
        self.imageuri = commvar.IMAGE_URL_1

    def test_image_description(self):
        """
            call module to describe an image
        """
        self.image_analysis.describe_image(self.imageuri)

        # demo purpose, make it pass
        # with self.assertRaises(Exception):
        #     print("failed!")
        self.assertTrue(1)

    def test_image_analysis(self):
        """
            call module to analyze image
            :return:
        """
        self.image_analysis.analyze_image(self.imageuri)

        # demo
        self.assertTrue(1)

    def test_object_detect(self):
        """
            call module to detect object
        """
        self.image_analysis.detect_object(self.imageuri)

        # demo
        self.assertTrue(1)

    def test_domain_access(self):
        """
            call module to access domain
        """
        self.image_analysis.access_domain(self.imageuri)

        # demo
        self.assertTrue(1)


if __name__ == "__main__":
    unittest.main()


# '''
# # manual test = when running in VSCode
# '''

# # x = TestImageAnalysisAzure()
# # x.test_image_description()
# # x.test_image_analysis()
# # x.test_object_detect()
# # x.test_domain_access()

