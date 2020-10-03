import numpy as np
from PIL import Image


def pixel_weights(image_left, image_right):
    pass


def greyscale_gradient(image):
    pass


def initialize_random_planes(image_left, image_right):
    pass


def patch_match_process():
    pass


def patch_match_postprocess(disparity_left, disparity_right):
    pass


def patch_match_stereo(image_left, image_right):
    # Compute interpixel weights
    pixel_weights_left, pixel_weights_right = pixel_weights(image_left, image_right)

    # Compute grayscale gradients
    gradient_left = greyscale_gradient(image_left)
    gradient_right = greyscale_gradient(image_right)

    # Intialize random planes
    planes_left, planes_right = initialize_random_planes(image_left, image_right)

    # Evalute initial plane cost
    
    # PatchMatch processing
    patch_match_process()

    # Post processing
    disparity_left = disparity_from_planes(planes_left)
    disparity_right = disparity_from_planes(planes_right)
    patch_match_postprocess(disparity_left, disparity_right)

    # Compute final disparity and return it
    disparity_left = disparity_from_planes(planes_left)
    disparity_right = disparity_from_planes(planes_right)

    return disparity_left, disparity_right


if __name__ == "__main__":
    # Hyperparameters
    alpha = 0.9
    gamma = 10.0
    tau_c = 10.0
    tau_g = 2.0

    # Input image filepaths
    image_left_filepath = "images\\aloe_left.png"
    image_right_filepath = "images\\aloe_right.png"

    # Output disparity images filepaths
    disparity_left_filepath = "disparity\\aloe_left.png"
    disparity_right_filepath = "disparity\\aloe_right.png"

    # Load images
    try:
        image_left = np.array(Image.open(image_left_filepath))
        image_right = np.array(Image.open(image_right_filepath))
    except:
        assert False, "Invalid image filepaths."

    # Ensure images are of the same size
    if len(image_left.shape) != len(image_right.shape):
        assert False, "Invalid image sizes."
    for dim_left, dim_right in zip(image_left.shape, image_right.shape):
        assert dim_left == dim_right, "Invalid image sizes."

    # Find left and right disparities
    disparity_left, disparity_right = patch_match_stereo(image_left, image_right)

    # Scale left disparity image
    if disparity_left.max() - disparity_left.min() != 0:
        disparity_left = (disparity_left - disparity_left.min()) / \
            (disparity_left.max() - disparity_left.min())
        disparity_left *= 255

    # Scale right disparity image
    if disparity_right.max() - disparity_right.min() != 0:
        disparity_right = (disparity_right - disparity_right.min()) / \
            (disparity_right.max() - disparity_right.min())
        disparity_right *= 255

    # Save disparities as images
    try:
        disparity_left_image = Image.fromarray(disparity_left.astype(np.uint8))
        disparity_left_image.save(disparity_left_filepath)

        disparity_right_image = Image.fromarray(disparity_right.astype(np.uint8))
        disparity_right_image.save(disparity_right_filepath)
    except:
        print("Failed to save images.")