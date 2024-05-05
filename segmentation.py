import rasterio
import os
import numpy as np

from PIL import Image
from matplotlib import pyplot as plt
from keras.utils import normalize
from sklearn.model_selection import train_test_split
from unet_model import unet_model

SIZE = 128

# Load data paths
image_directory = "/Your_Path/"
mask_directory = "/Your_Path/"

image_dataset = []  # Many ways to handle data, you can use pandas. Here, we are using a list format.
mask_dataset = []  # Place holders to define add labels. We will add 0 to all parasitized images and 1 to uninfected.

images = os.listdir(image_directory)
images.sort()
for i, image_name in enumerate(images):    # Enumerate method adds a counter and returns the enumerate object
    if (image_name.split('.')[1] == 'tif'):
        image = rasterio.open(image_directory+image_name).read(1)
        image = Image.fromarray(image)
        image = image.resize((SIZE, SIZE))
        image_dataset.append(np.array(image))

masks = os.listdir(mask_directory)
masks.sort()
for i, image_name in enumerate(masks):
    if (image_name.split('.')[1] == 'tif'):
        image = rasterio.open(mask_directory+image_name).read(1)
        image = Image.fromarray(image)
        image = image.resize((SIZE, SIZE))
        mask_dataset.append(np.array(image))

# Change datatype to float32
for i in range(len(image_dataset)):
    image_dataset[i] = image_dataset[i].astype("float32")

for i in range(len(mask_dataset)):
    mask_dataset[i] = mask_dataset[i].astype("float32")

# Add a dimension to the images and masks
image_dataset = np.expand_dims(image_dataset,3)
mask_dataset = np.expand_dims((np.array(mask_dataset)),3)

# split train and validation
X_rem, X_test, y_rem, y_test = train_test_split(image_dataset, mask_dataset, test_size = 0.1, random_state = 1)
X_train, X_valid, y_train, y_valid = train_test_split(X_rem, y_rem, test_size = 0.2, random_state = 1)

# In the model the shape of the image is (128, 128, 1)
IMG_HEIGHT = image_dataset.shape[1]
IMG_WIDTH  = image_dataset.shape[2]
IMG_CHANNELS = image_dataset.shape[3]

def get_model():
    return unet_model(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)

model = get_model()
history = model.fit(X_train, y_train,
                    batch_size = 16,
                    verbose=1,
                    epochs=30,
                    validation_data=(X_valid, y_valid),
                    shuffle=False)

model.save('/Your_Path/Model_Name.hdf5')
