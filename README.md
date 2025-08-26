🎨 Image Colorization with GAN

This project implements a system that receives a black-and-white image and automatically returns a colorized version of it using a Generative Adversarial Network (GAN).

🏗️ Project Structure

The project is divided into several main components, with different languages and libraries used in each part:

1. Model (Python – PyTorch)

Implemented in Python using PyTorch.

GAN architecture: includes the Generator and Discriminator built with torch.nn.

Training scripts for model training and saving weights.

Key libraries used:

torch.utils.data.Dataset – custom dataset handling

PIL.Image – image loading

numpy – numerical operations

skimage.color.rgb2lab – color space conversion

torchvision.transforms – preprocessing & data augmentation

constants.py – project constants (e.g., image size SIZE)

2. Dataset

Collection of grayscale and color images for training and testing.

Preprocessing pipeline converts RGB images to Lab color space for model training.

3. Server (Python – Flask)

Built in Python using Flask.

Loads the trained model and returns a colorized image when a grayscale image is sent.

4. Client (React)

Graphical user interface built with React.

Allows uploading a grayscale image and displays the colorized output.

5. Results

Sample images showing before and after colorization.
