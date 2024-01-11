import rasterio
import os
import glob

import numpy as np
import matplotlib.pyplot as plt


# Image patches path
image_path = glob.glob("/home/tlcrs/Downloads/babak_data/CSKS_milano/create_patch/image/building_norm_128_70_Raw/*.tif") # Directory of image patches 
image_path.sort()

# Footprint pathces path
footprint_path = glob.glob("/home/tlcrs/Downloads/babak_data/CSKS_milano/create_patch/footprint/footprint_128_70_Tonia_Raw/*.tif") # Directory of footprint patches
footprint_path.sort()

if len(image_path) != len(footprint_path):
    print("The number of images and footprints are not equal. Check the directories.")
    exit()

for i in range(len(image_path)):
    image_data = rasterio.open(image_path[i]).read(1)
    image_meta = rasterio.open(image_path[i]).meta.copy()

    mask_data = rasterio.open(footprint_path[i]).read(1)
    mask_meta = rasterio.open(footprint_path[i]).meta.copy()

    print("Image and mask # {} is in process.".format(i))

    # Find suitable data, find the footprints that cover at least 30% of area and its corresponding image patch
    if np.mean(mask_data) > 0.3:
        # Save the image
        output_dir = "/home/tlcrs/Downloads/babak_data/CSKS_milano/create_patch/image/building_norm_128_70_Tonia/"
        output_path = os.path.join(output_dir, f"tile_{i}.tif")
        # print(output_path)
        with rasterio.open(output_path, 'w', **image_meta) as dst:
            dst.write(image_data, 1)

        # Save the mask
        output_dir = "/home/tlcrs/Downloads/babak_data/CSKS_milano/create_patch/footprint/footprint_128_70_Tonia/"
        output_path = os.path.join(output_dir, f"tile_{i}.tif")
        # print(output_path)
        with rasterio.open(output_path, 'w', **mask_meta) as dst:
            dst.write(mask_data, 1)
