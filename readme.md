# Map generator

## Goal:

This project is to create a map generator. Those map will be used for DnD games, so the main objectif is the graphical look.

## Data description
The Carte d'etat major dataset is a massive dataset of 85 Gb of jp2 images divided in 2 class, the 10k (0) and 40k (1). The 10k class represent maps with a 1: 10 000 resolution, each pixels represent 1 meters square.
The 40k dataset have mutch more maps and each pixels represent a square of 4 by 4 meters.
Each images are a square of 5 000 by 5 000 pixels in jp2 format and can contain old maps data with or without border. This border can be detected as those are areas with no color variation.

## Dataset creation
To create those dataset, zip files have to bee downoloaded form the IGPN FTP server, unziped and here, I transforme the jp2 images in jpg images for ease of use.
This raw dataset was then splitted in images of 500 by 500 pixels without image containing only the border. To detect the border, the standart deviation of one image channel was computed and if this deviation is equal to 0 (or bellow 1 in practice) then the croped images is a broder.
The preprocessing steps are extremely slow as these steps are done at night on my computer so I haven't optimised them.

## Dificulty:
Detection of empty area (border), border and area with sparce road are similar. To detect them a naive approch used is to compute the mean of the images.
For the 10k dataset, empty image have empty caract
If an images has those mean and std, that mean that the images is empty.

## Data_preprocessing
Raw images have a resolution of 5 000 by 5 000 pixels making them to big to be usefull for a D&D maps usage. So a script was made to:
- Load images from `in_folder` (`raw_data` by default)
- Crop the images to an `image_size` dimension (px)
- Detect border/empty crop by detecting the edges on the images (cv2.Canny), dilate the edges (cv2.dilate) with a kernel of 5 by 5 and erode the image. This allow to to fill area with lot of features and remove area with low features. ![image_detection](https://raw.githubusercontent.com/hy-son/Old_maps_generator/master/images/Datapreprocessing_demo.png) 
- This preprocessing code can be configured using the images_size, in and out folder:
```bash 
python3 data_proprocessing.py --image_size 500 --in_folder "raw_data/0" --out_folder "data/1" 
```

