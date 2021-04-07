# CS 148 - Homework 1
**Data evaluation**

There are 334 images, each of them is of dimensions 480x640 with 3 channels (RGB).

**Summary**

Red light detection is performed by match filtering. Manually created square filters with a red dot on a black background generate many False Positives and several False Negatives. Real life rectangular patches from daylight and night used as filters perform better but are very sensitive to threshold tuning.

**Deliverables**

- algorithm code: https://github.com/laure-delisle/cs148-hw1/blob/master/run_predictions.py
- example plotting code: https://github.com/laure-delisle/cs148-hw1/blob/master/plot_predictions.ipynb
- predictions: https://github.com/laure-delisle/cs148-hw1/blob/master/predictions.json

## Used techniques
**Algorithms**

I used match filtering, with predefined filters. We sweep a filter on an image, and at each location we compute the inner product of a given filter and a patch of the image cut to the filter's dimensions.

<img src="./resources/sweep.png?raw=true" width="60%" alt="Sweeping over the image"> <img src="./resources/inner_product.png?raw=true" width="30%" alt="Inner Product of patch and filter">

More precisely, we flatten both the patch and the filter to vectors, normalize them to obtain unit vectors, and compute their inner product.

**Filters**

I initially used manually drawn red disks on a square black background as filters, that I created with GIMP. To increase the chances of a match at different scales, I created 5 versions of this filter and swept images with each of the filters.

<img src="./resources/filters_square.png?raw=true" width="30%" alt="Red dot on square black background">

This generated many False Positives as it detected any red light, including car rear lights, red light reflections in cars, and lights on buildings. It also missed many red lights (False Negatives). To improve on this, I captured two real life rectangular examples from daylight and night images in the dataset, at various scales.

<img src="./resources/filters_rect.png?raw=true" width="30%" alt="Real life filters">

Currently, no padding is implemented: a red light partially visible at the edge of the image might not be detected.

## Performance Evaluation
**Evaluation method**

I evaluated my algorithms' performance via visual inspection, using my own observation skills as the "ground truth". This helped guide my intuition as to which examples were difficult for a given technique (false negatives), and which elements were wrongly triggering the algorithm (false positives).

This evaluation method is risky: it is prone to confirmation bias (I pay more attention to the successes than the failures) and requires a good domain knowledge. Furthermore, it is time-consuming (not appropriate for large datasets) and empirical. This calls for a better evaluation, where ground truth labels are created by domain experts or trained workers, and performance metrics are used (FPR, FNR, IOU).

**Best performing algorithm**

The second algorithm using fewer but realistic rectangular filters performed best, with a threshold of 0.91. This can be explained by the new filters having more textural and local context. Indeed, the rectangular vertical shape is more characteristic of red lights in the US, where the dataset images are from. The daylight filters are rich in texture information, with the other two circles apparent and the red light having hues of orange and yellow. The night filter is rich is texture information as well, with the red light glare and the shades of white. As discussed above, these filters both generated less false positives and increased the detection capacity (less false negatives).

**Failures of other algorithms**

<img src="./results/reflection_example.png?raw=true" width="30%" alt="Success 1"> <img src="./results/fpr_bus_example.png?raw=true" width="30%" alt="Success 2"> <img src="./results/solved_bus_example.png?raw=true" width="30%" alt="Success 3">

(Left) The square filter detects the reflection of a red light on the surface of the car hood, (center) the red dot filter is too sensitive to hues of red, (right) the real-life rectangular filter is robust to hues of red and reflections.

## Successes and failures
**Successes**

<img src="./results/success_example.png?raw=true" width="30%" alt="Success 1"> <img src="./results/success_example_2.png?raw=true" width="30%" alt="Success 2"> <img src="./results/success_example_3.png?raw=true" width="30%" alt="Success 3">

The algorithm performs best on these examples where the red lights are very similar in texture and scale to the filters.

**Failures**

<img src="./results/hard_scale.png?raw=true" width="30%" alt="Success 1"> <img src="./results/hard_scale_2.png?raw=true" width="30%" alt="Success 2"> <img src="./results/hard_scale_night.png?raw=true" width="30%" alt="Success 3">

The algorithm struggles with smaller red lights. One easy fix would be to create new scaled-down filters, similarly to what was done for the square red dot filter. I am not sure how to mitigate the false positives here, there is a need for more context. Indeed, the red rear light from the car in front of the vehicle reflects on the surface of its hood: with some context, one understands that no light should be detected there, however seen in isolation the patch matches very closely a red light.

**Improvements**

I see two easy way to improve on the current algorithm's performance: creating filters of various scales, and implementing padding. Padding would help detect lights that are partially occulted because at the edge of the image (see center image in "Successes").

More involved improvements would include the creation of a validation set for tuning the detection threshold.
