import os
import numpy as np
import json
import random
from PIL import Image

def match_filter(patch, filter, threshold):
    '''
    This fonction convolves a patch with a filter, anc compares the result to a
    threshold. If result > threshold, returns 1. Otherwise, returns 0.
    '''
    # flatten to vector
    patch_vector = patch.flatten()
    filter_vector = filter.flatten()

    # normalize vectors
    patch_norm = np.linalg.norm(patch_vector)
    filter_norm = np.linalg.norm(filter_vector)
    patch = patch_vector / patch_norm if patch_norm else patch_vector
    filter = filter_vector / filter_norm if filter_norm else filter_vector

    convo = np.inner(patch, filter)

    if convo > threshold:
        return 1
    else:
        return 0

def random_bbox():
    # generates between 1 and 5 random boxes of fixed size and returns the results in the proper format.
    box_height = 8
    box_width = 6
    
    num_boxes = np.random.randint(1,5) 
    
    for i in range(num_boxes):
        (n_rows,n_cols,n_channels) = np.shape(I)
        
        tl_row = np.random.randint(n_rows - box_height)
        tl_col = np.random.randint(n_cols - box_width)
        br_row = tl_row + box_height
        br_col = tl_col + box_width
        
        bounding_boxes.append([tl_row,tl_col,br_row,br_col]) 


def detect_red_light(I, filters, threshold, noise=False):
    '''
    This function takes a numpy array <I> and returns a list <bounding_boxes>.
    The list <bounding_boxes> should have one element for each red light in the 
    image. Each element of <bounding_boxes> should itself be a list, containing 
    four integers that specify a bounding box: the row and column index of the 
    top left corner and the row and column index of the bottom right corner (in
    that order). See the code below for an example.
    
    Note that PIL loads images in RGB order, so:
    I[:,:,0] is the red channel
    I[:,:,1] is the green channel
    I[:,:,2] is the blue channel
    '''

    bounding_boxes = [] # This should be a list of lists, each of length 4. See format example below. 
    threshold = threshold
    w, h, c = I.shape

    if noise:
        # generate some 2D noise
        noise_2d = np.zeros(I.shape, np.uint8)
        for x in range(w):
            for y in range(h):
                for z in range(c):
                    # generate noise
                    pixel_noise = random.randrange(-15, 15, 1)
                    pixel_value = I[x,y,z]
                    noisy_pixel = pixel_value + pixel_noise

                    # clip noise
                    if 0 <= noisy_pixel <= 255:
                        I[x,y,z] = noisy_pixel
                    elif noisy_pixel < 0:
                        I[x,y,z] = 0
                    else:
                        I[x,y,z] = 255


    
    ##########################################################################
    #
    #       Match Filtering
    #
    ##########################################################################

    # for each filter
    for filter in filters:
        # get size of filter to help with sweeping -- padding not implemented
        fw, fh, _ = filter.shape

        # sweeping
        for x in range(0, w-fw, 2):
            for y in range(0, h-fh, 2):
                patch = I[x:x+fw, y:y+fh, :]

                # convolve
                match = match_filter(patch, filter, threshold)

                # produce bbox if match
                if match:
                    bounding_boxes.append([x, y, fw, fh])
    
    # check bbox are well formed
    for i in range(len(bounding_boxes)):
        assert len(bounding_boxes[i]) == 4
    
    return bounding_boxes


#############################################
#
#   Setup
#
#############################################

# project path
dir_path = os.getcwd()

# set the path to the downloaded data: 
data_path = os.path.join(dir_path, '../data/RedLights2011_Medium')

# set a path for saving predictions: 
preds_path = os.path.join(dir_path, '../data/hw01_preds' )
os.makedirs(preds_path,exist_ok=True) # create directory if needed 

# get sorted list of files:
file_names = sorted(os.listdir(data_path)) 

# remove any non-JPEG files: 
file_names = [f for f in file_names if '.jpg' in f]


#############################################
#
#   Prediction for various techniques
#
#############################################
techniques = {'match_filtering_red': 'reds',
              'match_filtering_lights': 'lights',
              #'match_filtering_lights_noise': 'lights'
              }

for technique, filter_folder in techniques.items():
    print('detecting with', technique)
    preds = {}
    noise = 'noise' in technique
    if 'red' in technique: threshold = 0.7
    if 'lights' in technique: threshold = 0.91

    # load filters
    filters_path = os.path.join(dir_path, 'filters', filter_folder)
    filters_files = os.listdir(filters_path)
    filters = [Image.open(os.path.join(filters_path, f)) for f in filters_files]
    filters = [np.asarray(f) for f in filters]

    print("iterate over images...")

    for i in range(10):
        if i % 10 == 0: print(i)
        
        # read image using PIL:
        I = Image.open(os.path.join(data_path,file_names[i]))
        
        # convert to numpy array:
        I = np.asarray(I)
        
        preds[file_names[i]] = detect_red_light(I, filters, threshold, noise)

    # save preds (overwrites any previous predictions!)
    with open(os.path.join(preds_path,'new_preds_{}.json'.format(technique)),'w') as f:
        json.dump(preds,f)
