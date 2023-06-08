from PIL import Image
import numpy as np
from io import BytesIO


def jpeg_bytes_to_numpy_array(b: bytes) -> np.ndarray:
    # Create a readable buffer
    b = BytesIO(b)
    # Convert the bytes to an image
    image = Image.open(b, formats=["jpeg"])
    # Convert image to numpy array
    image = np.array(image)
    # Return the numpy array
    return image
