import rasterio
import os
import glob


# Image patches path
image_path = glob.glob("/Your_Path/*.tif") # Insert the directory path of image patches 
image_path.sort()

# Footprint pathces path
footprint_path = glob.glob("/Your_Path/*.tif") # Insert the directory path of footprint patches
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

    # Find suitable data, find the footprints that cover at least 10% of area and its corresponding image patch
    if np.mean(mask_data) > 0.1:
        # Save the image
        output_dir = "Output_Path" # Insert the directory path of output
        output_path = os.path.join(output_dir, f"tile_{i}.tif") 
        # print(output_path)
        with rasterio.open(output_path, 'w', **image_meta) as dst:
            dst.write(image_data, 1)

        # Save the mask
        output_dir = "Output_Path" # Insert the directory path of output
        output_path = os.path.join(output_dir, f"tile_{i}.tif")
        # print(output_path)
        with rasterio.open(output_path, 'w', **mask_meta) as dst:
            dst.write(mask_data, 1)
