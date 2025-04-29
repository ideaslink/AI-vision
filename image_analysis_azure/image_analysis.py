"""
    image analysis by azure cognitive

    dependency:     azure, azure Ai/cognitive, computer vision, python
    reference:      ms cognitive doc

    features:
    - describing image
    - analyzing image
    - tagging image
    - detecting objects
    - accessing domains

    notes:

"""

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
import sys
import time
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import requests


class ImageAnalysis:

    def __init__(self, vision_endpoint, vision_key):
        """
        create ComputerVisionClient instance
        """
        self.computervisionclient = ComputerVisionClient(vision_endpoint, CognitiveServicesCredentials(vision_key))

    def describe_image(self, image_url):
        """
        describe image
        """
        print('describing image...')
        # call cog vision api to get image description
        desc_results = self.computervisionclient.describe_image(image_url)

        # print('Image description:\n')

        if len(desc_results.captions) == 0:
            print('no description detected')
        else:
            for caption in desc_results.captions:
                print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))

    def analyze_image(self, image_url):
        """
        image category
        """

        print('\ndescribing image...\n')
        print('\ngetting image category...')

        # select features - category
        image_features = ['categories']
        cat_results = self.computervisionclient.analyze_image(image_url, image_features)

        print('image categories\n')

        if len(cat_results.categories) == 0:
            print('no categorie')
        else:
            for cat in cat_results.categories:
                print(f"'{cat.name}' with confidence {cat.score*100:.2f}%")

        '''
        image brands - detects common brands like logos and puts a bounding box around them.
        '''

        print("\ndetecting brands...\n")
        # select feature - brands
        image_feature_brand = ["brands"]
        brand_results = self.computervisionclient.analyze_image(image_url, image_feature_brand)

        if len(brand_results.brands) == 0:
            print("No brands detected.")
        else:
            for brand in brand_results.brands:
                print("'{}' brand detected with confidence {:.1f}% at location {}, {}, {}, {}".format( \
                brand.name, brand.confidence * 100, brand.rectangle.x, brand.rectangle.x + brand.rectangle.w, \
                brand.rectangle.y, brand.rectangle.y + brand.rectangle.h))

        '''
        Faces - detects faces in a image, gets their gender and age, and marks them with a bounding box.
        '''
        print("\ndetecting Faces\n")
        # select feature - face
        image_feature_face = ["faces"]
        face_results = self.computervisionclient.analyze_image(image_url, image_feature_face)

        print("Faces in the image: ")
        if len(face_results.faces) == 0:
            print("No faces detected.")
        else:
            cnt = 0
            for face in face_results.faces:
                cnt += 1
                print(f"\nFace: {cnt}\n")
                print("'{}' of age {} at location {}, {}, {}, {}".format(face.gender, face.age, \
                face.face_rectangle.left, face.face_rectangle.top, \
                face.face_rectangle.left + face.face_rectangle.width, \
                face.face_rectangle.top + face.face_rectangle.height))

                # attrs = face.face_attributes.as_dict()
                # # occlusion
                # if 'occlusion' in attrs:
                #     print(" - Occlusion:")
                #     for oc in attrs['occlusion']:
                #         print("   - {}: {}".format(oc, attrs['occlusion'][oc]))
                # # glasses
                # if 'glasses' in attrs:
                #     print(" - Glasses:")
                #     for gl in attrs['glasses']:
                #         print("   - {}: {}".format(gl, attrs['glasses'][gl]))
                # # head pose
                # if 'headPose' in attrs:
                #     print(" - Head Pose:")
                #     for hp in attrs['headPose']:
                #         print("   - {}: {}".format(hp, attrs['headPose'][hp]))
                # # hair
                # if 'hair' in attrs: 
                #     print(" - Hair:")
                #     for ha in attrs['hair']:
                #         print("   - {}: {}".format(ha, attrs['hair'][ha]))
                # # makeup
                # if 'makeup' in attrs:   
                #     print(" - Makeup:") 
                #     for mk in attrs['makeup']:
                #         print("   - {}: {}".format(mk, attrs['makeup'][mk]))
                # # emotions
                # if 'emotion' in attrs:      
                #     print(" - Emotions:")   
                #     for em in attrs['emotion']: 
                #         print("   - {}: {}".format(em, attrs['emotion'][em]))
                # # smile 
                # if 'smile' in attrs:            
                #     print(" - Smile:")      
                #     for sm in attrs['smile']:
                #         print("   - {}: {}".format(sm, attrs['smile'][sm]))
                # # facial hair
                # if 'facialHair' in attrs:           
                #     print(" - Facial Hair:")    
                #     for fh in attrs['facialHair']:
                #         print("   - {}: {}".format(fh, attrs['facialHair'][fh]))
                # # accessories
                # if 'accessories' in attrs:          
                #     print(" - Accessories:")    
                #     for ac in attrs['accessories']:
                #         print("   - {}: {}".format(ac, attrs['accessories'][ac]))
                # # clothes
                # if 'clothing' in attrs:            
                #     print(" - Clothing:")      
                #     for cl in attrs['clothing']:
                #         print("   - {}: {}".format(cl, attrs['clothing'][cl]))

                # # blur
                # if 'blur' in attrs:
                #     print(" - Blur:")           
                #     for bl in attrs['blur']:
                #         print("   - {}: {}".format(bl, attrs['blur'][bl]))

        '''
        Detect Adult or Racy Content - detects adult or racy content
        '''

        print("\ndetecting Adult or Racy Content\n")
        # Select features - adult
        image_feature_adult = ["adult"]
        adult_results = self.computervisionclient.analyze_image(image_url, image_feature_adult)

        # Print results with adult/racy score
        print("adult content: {} with confidence {:.2f}".format(adult_results.adult.is_adult_content, adult_results.adult.adult_score * 100))
        print("racy content: {} with confidence {:.2f}".format(adult_results.adult.is_racy_content, adult_results.adult.racy_score * 100))

        '''
        Color detects color info in a image
        '''

        print("\ndetecting Color\n")
        # Select feature - color
        image_feature_color = ["color"]
        color_results = self.computervisionclient.analyze_image(image_url, image_feature_color)

        # Print results of color scheme
        print("Getting color scheme of the remote image: ")
        print(f"Is black and white: {color_results.color.is_bw_img}")
        print(f"Accent color: {color_results.color.accent_color}")
        print(f"Dominant background color: {color_results.color.dominant_color_background}")
        print(f"Dominant foreground color: {color_results.color.dominant_color_foreground}")
        print(f"Dominant colors: {color_results.color.dominant_colors}")

        '''
        Image Types - detects an image's type (clip art/line drawing).
        '''

        print("\ndetecting Image Types\n")
        image_feature_type = [VisualFeatureTypes.image_type]
        type_results = self.computervisionclient.analyze_image(image_url, image_feature_type)

        # Prints type results with degree of accuracy
        print("Type of image:")
        if type_results.image_type.clip_art_type == 0:
            print("Image is not clip art.")
        elif type_results.image_type.line_drawing_type == 1:
            print("Image is ambiguously clip art.")
        elif type_results.image_type.line_drawing_type == 2:
            print("Image is normal clip art.")
        else:
            print("Image is good clip art.")

        if type_results.image_type.line_drawing_type == 0:
            print("Image is not a line drawing.")
        else:
            print("Image is a line drawing")

    def tag_image(self, image_url):
        """
        image tag
        """

        print("\ntagging image\n")
        tag_results = self.computervisionclient.tag_image(image_url )

        # Print results with confidence score
        print("image tags: \n")
        if len(tag_results.tags) == 0:
            print("No tag detected.")
        else:
            for tag in tag_results.tags:
                print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))

    def detect_object(self, image_url,result_image) -> None:
        """
            Detect Objects - detect objects with bounding boxes in an image

            :param image_url: image url
            :param result_image: image with detected objects
        """
        
        print("detecting Objects...\n")
        # Call API with URL
        obj_results = self.computervisionclient.detect_objects(image_url)

        if len(obj_results.objects) == 0:
            print("No objects detected.")
        else:
            fig = plt.figure(figsize=(6, 4))
            plt.axis('off')
            image = Image.open(requests.get(image_url, stream=True).raw)
            draw = ImageDraw.Draw(image)
            color = 'cyan'

            for obj in obj_results.objects:
                r = obj.rectangle
                draw.rectangle([r.x, r.y, r.x+r.w, r.y+r.h], outline=color, width=2)
                plt.annotate(obj.object_property, xy=(r.x, r.y), xycoords='data', color=color, weight='bold')
                print("object at location {}, {}, {}, {}".format(\
                obj.rectangle.x, obj.rectangle.x + obj.rectangle.w,\
                obj.rectangle.y, obj.rectangle.y + obj.rectangle.h))

            plt.imshow(image)
            # save result
            plt.savefig(result_image)
            plt.show()

    def access_domain(self, image_url):
        """
        Domain-specific Content - detects celebrites and landmarks in images
        """

        print("\ndetecting Domain-specific Content\n")
        domain_results = self.computervisionclient.analyze_image_by_domain("celebrities", image_url)

        if len(domain_results.result["celebrities"]) == 0:
            print("No celebrities detected.")
        else:
            for celeb in domain_results.result["celebrities"]:
                print(celeb["name"])

        # detected landmarks
        domain_results_landmarks = self.computervisionclient.analyze_image_by_domain("landmarks", image_url)
        print()

        print("Landmarks:")
        if len(domain_results_landmarks.result["landmarks"]) == 0:
            print("No landmarks detected.")
        else:
            for landmark in domain_results_landmarks.result["landmarks"]:
                print(landmark["name"])




