"""Predict with pre-trained SSD models
===================================

This article goes through how to play with pre-trained SSD models with several
lines of code.

"""

from gluonvision import model_zoo, data, utils
from matplotlib import pyplot as plt

######################################################################
# Obtain a pretrained model
# -------------------------
#
# Let's get a SSD model that is trained with 512x512 images on the Pascal VOC
# dataset with ResNet-50 V1 as the base model. By specifying
# ``pretrained=True``, it will automatically download the model from the model
# zoo if necessary. For more pretrained models, refer to
# :doc:`../../model_zoo/index`.

net = model_zoo.get_model('ssd_512_resnet50_v1_voc', pretrained=True)

######################################################################
# Pre-process an image
# --------------------
#
# Next we download an image, and pre-process with preset data transforms. Here we
# specify that we resize the short edge of the image into 512 px. But you can
# feed an arbitrary size image.
#
# You can provide a list of image filenames, such as ``[im_fname1, im_fname2,
# ...]`` to :py:func:`gluonvision.data.transforms.presets.ssd.load_test` if you
# want to load multiple image together.
#
# This function returns two results, the first is a NDArray with shape
# `(batch_size, RGB_channels, height, width)` that can be feed into the
# model directly. While the second one contains the images in numpy format to
# easy to be plotted. Since we only loaded a single image, the first dimension
# of `x` is 1.

im_fname = utils.download('https://github.com/dmlc/web-data/blob/master/' +
                          'gluonvision/detection/street_small.jpg?raw=true')
x, img = data.transforms.presets.ssd.load_test(im_fname, short=512)
print('Shape of pre-processed image:', x.shape)

######################################################################
# Inference and display
# ---------------------
#
# The forward function will return all possible bounding boxes, and the
# corresponding predicted class IDs and confidence score. Their shapes are
# `(batch_size, num_bboxes, 1)`, `(batch_size, num_bboxes, 1)`, and
# `(batch_size, num_bboxes, 4)`, respectively.
#
# We can use :py:func:`gluonvision.utils.viz.plot_bbox` to visualize the
# results. We slice the results for the first image, then feed into `plot_bbox`.

class_IDs, scores, bounding_boxs = net(x)

ax = utils.viz.plot_bbox(img, bounding_boxs[0], scores[0],
                         class_IDs[0], class_names=net.classes)
plt.show()