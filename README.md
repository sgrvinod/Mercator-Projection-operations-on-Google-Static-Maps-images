# Mercator-Projection-operations-on-Google-Static-Maps-images
Perform Mercator Projection operations on Google Static Maps images, usually as a data-preparation step for Image Classification tasks.

There are two classfiles for performing Mercator Projection and associated operations on Google Static Map images:

**MercatorProjection.py** contains functions to convert geographical coordinates to base Google world map pixel coordinates, and vice versa.

**GoogleStaticMap.py** contains functions to
**1.** Get optimal Google Maps zoom level for an address.
**2.** Get geographical and cartesian coordinates for corners of a returned Google Static Maps image.
**3.** Get pixel coordinates of the shapefile of an address, to crop the property from the Google Static Maps image.
**4.** Crop address/property from the Google Static Maps image, with a given bleed.

**Modeled in Python**

The example.py in the example folder contains an example for the operations listed above. Given the shapefile of a property in Alameda, CA, whose Google Static Maps image is available, it crops it to the boundaries of the property.

The image

![Cropped Google Static Maps Image](https://github.com/sgrvinod/Mercator-Projection-operations-on-Google-Static-Maps-images/blob/master/example/example.png?raw=true)

crops to

![Google Static Maps Image](https://github.com/sgrvinod/Mercator-Projection-operations-on-Google-Static-Maps-images/blob/master/example/out.png?raw=true)




