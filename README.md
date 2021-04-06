# caltech-ee148-spring2020-hw01

# Data evaluation
There are 334 images, each of them is of dimensions 480x640 with 3 channels (RGB).

# Used techniques
I used match filtering, with predefined filters. As a first try, I manually created square filters of different sizes with a red dot on a black background. This tends to have a high False Positive Rate as it detects any red light, including car rear lights and lights on buildings. To improve on this, I captured two real life rectangular examples from daylight and night, at various scales.

The match filtering is performed by sweeping a filter on an image and convolving it with the patch it overlays each time. Currently, no padding is implemented: a red light partially visible at the edge of the image will not be detected.


- tweaking threshold >>> need val set
- square filters lead to high FPR
- new rectangular filters extracted from dataset help FPR a lot
- importance of threshold (see bus example)
