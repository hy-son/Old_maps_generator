from tqdm import tqdm
import cv2
from pathlib import Path
import argparse
import numpy as np
from queue import Queue
import multiprocessing as mp

counter = None

def init(args):
    ''' store the counter for later use '''
    global counter
    counter = args

def preprocess(image_size, in_folder, out_folder):
    """
    Crop images and save then in out_folder. Empty images will be removed.
    :param image_size: int. Size of the output image (image are square)
    :param in_folder: str. Were are the raw data (JPG)
    :param out_folder: srt. Were to save the images
    :return: None
    """
    Path(out_folder).mkdir(parents=True, exist_ok=True)
    raw_images_list = [(p, out_folder, image_size) for p in Path(in_folder).glob("*.jpg")]
    counter = mp.Value('i', 0)
    pool = mp.Pool(processes=3, initializer = init, initargs = (counter, ))
    pool.map(crop_image_of_interest, raw_images_list)

    pool.close()
    pool.join()
    pool.terminate()


def crop_image_of_interest(arg):
    #print(arg)
    global counter
    img_name, out_folder, image_size = arg
    kernel = np.ones((5, 5), np.uint8)
    img = cv2.imread(str(img_name))
    width, height, _ = img.shape

    # Crop the image
    for w in range(0, width, image_size):
        for h in range(0, width, image_size):
            croped = img[h:h + image_size, w:w + image_size]
            # If the image is not empty
            test_empty = cv2.cvtColor(croped, cv2.COLOR_BGR2GRAY)
            test_empty = cv2.Canny(test_empty, 80, 150)
            test_empty = cv2.dilate(test_empty, kernel, iterations=1)
            test_empty = cv2.erode(test_empty, kernel, iterations=3)

            # If the image is not empty we save it
            if test_empty.max() != 0:
                with counter.get_lock():
                    counter.value += 1
                    cv2.imwrite(str(Path(out_folder) / Path(f"{counter.value}.jpg")), croped)
                    print(f"Will save {counter.value}.jpg")

if __name__ == "__main__":
    # Read the arguments given
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--image_size', help="Image crop size, it must be an int. default: 500", dest='image_size', type=int, default=500) # Image will be square
    parser.add_argument('-i','--in_folder', help="Input image folder, where the raw images are, default: raw_data, IMAGE MUST BE JPG", dest='in_folder',type=str, default="raw_data/0")
    parser.add_argument('-o','--out_folder', help="Output image folder, where the pre processed images are saved, default: data", dest='out_folder', type=str, default="data/0")
    args = parser.parse_args()

    preprocess(args.image_size, args.in_folder, args.out_folder)




