import numpy as np
from PIL import Image


class Plane:
    
    def __init__():
        self.point_x = 0
        self.point_y = 0
        self.point_z = 0

        self.normal_x = 0
        self.normal_y = 0
        self.normal_z = 0


def pixel_weights(image, window_size, gamma):
    weights = [[{} for _ in range(image.shape[1])] for _ in range(image.shape[0])]

    for row in range(image.shape[0]):
        for col in range(image.shape[1]):

            for y in range(row - window_size // 2, row + window_size // 2 + 1):
                for x in range(col - window_size // 2, col + window_size // 2 + 1):
                    if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
                        weights[row][col][y, x] = np.exp(np.abs(image[row, col] - image[y, x]) / gamma)

    return weights


def greyscale_gradient(image):
    pass


def initialize_random_planes(shape, max_disparity):
    
    planes = [[Plane() for _ in range(shape[1])] for _ in range(shape[0])]

    for row in range(shape[0]):
        for col in range(shape[1]):
            planes[row][col].point_x = col
            planes[row][col].point_y = row
            planes[row][col].point_z = np.random.uniform(0, max_disparity)

            planes[row][col].normal_x = np.random.uniform(np.iinfo(np.int32).min, np.iinfo(np.int32).max)
            planes[row][col].normal_y = np.random.uniform(np.iinfo(np.int32).min, np.iinfo(np.int32).max)
            planes[row][col].normal_z = np.random.uniform(np.iinfo(np.int32).min, np.iinfo(np.int32).max)

    return planes


def patch_match_process():
    pass


def patch_match_postprocess(disparity_left, disparity_right):
    pass


def patch_match_stereo(image_left, image_rightm, hyperparameters):
    # Compute interpixel weights
    pixel_weights_left = pixel_weights(
        image_left,
        hyperparameters["window_size"],
        hyperparameters["gamma"]
    )
    pixel_weights_right = pixel_weights(
        image_right,
        hyperparameters["window_size"],
        hyperparameters["gamma"]
    )

    # Compute grayscale gradients
    gradient_left = greyscale_gradient(image_left)
    gradient_right = greyscale_gradient(image_right)

    # Intialize random planes
    planes_left = initialize_random_planes(image_left.shape, hyperparameters["max_disparity"])
    planes_right = initialize_random_planes(image_right.shape, hyperparameters["max_disparity"])

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
    hyperparameters = {
        "alpha": 0.9,
        "gamma": 10.0,
        "tau_c": 10.0,
        "tau_g": 2.0,
        "max_disparity": 60,
        "window_size": 35
    }

    # Input image filepaths
    image_left_filepath = "images\\aloe_left.png"
    image_right_filepath = "images\\aloe_right.png"

    # Output disparity images filepaths
    disparity_left_filepath = "disparity\\aloe_left.png"
    disparity_right_filepath = "disparity\\aloe_right.png"

    # Load images
    try:
        image_left = np.array(Image.open(image_left_filepath).convert('LA'))
        image_right = np.array(Image.open(image_right_filepath).convert('LA'))
    except:
        assert False, "Invalid image filepaths."

    # Ensure images are of the same size
    if len(image_left.shape) != len(image_right.shape):
        assert False, "Invalid image sizes."
    for dim_left, dim_right in zip(image_left.shape, image_right.shape):
        assert dim_left == dim_right, "Invalid image sizes."

    # Find left and right disparities
    disparity_left, disparity_right = patch_match_stereo(image_left, image_right, hyperparameters)

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