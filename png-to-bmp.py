import os
from PIL import Image

input_folder = "examples/c4l-image-dataset-master/c4l-image-dataset-master/2560x1920"
output_folder = "examples/large_images"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        img = Image.open(os.path.join(input_folder, filename)).convert("RGB")
        img.save(os.path.join(output_folder, filename.replace(".png", ".bmp")))