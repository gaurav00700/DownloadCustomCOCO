# Download COCO custom image class and its annotations.

## Steps:

1. Clone the repository 
   ```
   git clone https://github.com/samueljamesc/coco_custom_image_class.git
   ```

2. Download JSON file from COCO website

   - For 2017 version,
    ```
    wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip or open the link and save the zip file
    ```
   - For 2014 version,
    ```
    wget http://images.cocodataset.org/annotations/annotations_trainval2014.zip or open the link and save the zip file
    ```
    
   - Unzip the file

3. Create python environment and install the required packages using 
   ```
   pip install -r requirements.txt
   ```

4. Enter the path for root directory and image directory as required in download_coco.py file

5. Run the following command
   ```
    python download_coco.py
    ```

6. Images and annotations will be downloaded and saved in the image directory

