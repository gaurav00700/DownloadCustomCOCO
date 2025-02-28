import os
from pycocotools.coco import COCO
from tqdm import tqdm
import requests
from collections import defaultdict
import json

# Paths and settings
coco_root = 'annotations_trainval2017'
annotations_file = os.path.join(coco_root, 'annotations/instances_train2017.json')
image_dir = os.path.join(coco_root, 'annotated_images', 'images')

# Initialize COCO API
coco_api = COCO(annotations_file)

# Define the classes and number of images per class
classes = ["person", "car", "truck", "motorcycle", "bicycle"]
images_per_class = 5

def download_images_and_annotations(coco_api, image_dir, images_per_class, classes):
    
    # Create a common directory for storing images with annotations from all classes
    os.makedirs(image_dir, exist_ok=True)

    # Prepare a dictionary to hold the data
    annotated_data = defaultdict(dict)

    for cls in tqdm(classes, desc="Downloading images and annotations for each classes..."):
        
        cat_ids = coco_api.getCatIds(catNms=[cls])
        
        # Get image IDs that contain annotations of the current class
        img_ids = coco_api.getImgIds(catIds=cat_ids)
        print(f"Class: {cls}, Total images: {len(img_ids)}")
        
        for i, img_id in tqdm(enumerate(img_ids), total= images_per_class, desc=f"Downloading images for class {cls}..."):
            
            if i >= images_per_class: break
            
            ann_ids = coco_api.getAnnIds(imgIds=img_id, catIds=cat_ids)
            annotations = coco_api.loadAnns(ann_ids)
            
            # Load image info
            img_info = coco_api.loadImgs(img_id)[0]
            
            try:
                # Download the image
                response = requests.get(img_info['coco_url'])
                if response.status_code == 200:
                    with open(os.path.join(image_dir, f'{img_info["file_name"]}'), 'wb') as f:
                        f.write(response.content)
                else:
                    print(f"Failed to download {img_info['file_name']} due to: HTTP status code {response.status_code}")
                
                # Save annotations in JSON format
                annotated_data[img_info['file_name']]['id'] = img_info['id']
                annotated_data[img_info['file_name']]['annotations'] = annotations
                annotated_data[img_info['file_name']]['coco_url'] = img_info['coco_url']
                annotated_data[img_info['file_name']]['width'] = img_info['width']
                annotated_data[img_info['file_name']]['height'] = img_info['height']

            except Exception as e:
                print(f"Failed to download {img_info['file_name']} due to: {str(e)}")

    # Save the annotated data in JSON format
    with open(os.path.join(os.path.dirname(image_dir), 'annotated_data.json'), 'w') as f:
        json.dump(annotated_data, f, indent=4)

# Run the function
download_images_and_annotations(coco_api, image_dir, images_per_class, classes)
print("Process is complete............")