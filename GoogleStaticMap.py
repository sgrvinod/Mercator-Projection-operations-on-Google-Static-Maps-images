import numpy
from PIL import Image, ImageDraw
from MercatorProjection import G_LatLng, G_Point, MercatorProjection


# Create a class for operations on a Google Static Map image
class GoogleStaticMap():
    # Initialize class object with
    def __init__(self, mapWidth=640, mapHeight=640):
        # Set the dimensions of Google Static Map image
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight

    # Create a method for finding optimal zoom of Google Static Map image image for a given property bound-box
    def getOptimalZoom(self, bbox):
        center = G_LatLng((bbox[0].lat + bbox[1].lat) / 2, (bbox[0].lng + bbox[1].lng) / 2)
        gMap = GoogleStaticMap()
        maxZoom = 21
        zooms = list(reversed(range(maxZoom + 1)))
        for z in zooms:
            corners = gMap.getCorners(center, z)
            if ((corners['Sgeo'] <= bbox[0].lat <= corners['Ngeo']) &
                    (corners['Sgeo'] <= bbox[1].lat <= corners['Ngeo']) &
                    (corners['Wgeo'] <= bbox[0].lng <= corners['Egeo']) &
                    (corners['Wgeo'] <= bbox[1].lng <= corners['Egeo'])):
                optimalZoom = z
                break
        return optimalZoom

    # Create a method to get z=0 pixel/geo edges of returned Google Static Map image of specified zoom and center and width, height
    def getCorners(self, center, zoom):
        scale = 2 ** zoom
        proj = MercatorProjection()
        # Find z=0 pixel coordinates of the center
        centerPx = proj.fromLatLngToPoint(center)
        # Find z=0 pixel coordinates of the corners of the Google Static Map image
        SWPoint = G_Point(centerPx.x - (self.mapWidth / 2) / scale, centerPx.y + (self.mapHeight / 2) / scale)
        NEPoint = G_Point(centerPx.x + (self.mapWidth / 2) / scale, centerPx.y - (self.mapHeight / 2) / scale)
        # Find geographical coordinates of the corners of the Google Static Map image
        SWLatLon = proj.fromPointToLatLng(SWPoint)
        NELatLon = proj.fromPointToLatLng(NEPoint)
        # Return both z=0 pixel bounds and geographical bounds of the corners of the Google Static Map image
        return {
            'Ngeo': NELatLon.lat,
            'Egeo': NELatLon.lng,
            'Sgeo': SWLatLon.lat,
            'Wgeo': SWLatLon.lng,
            'Npix': NEPoint.y,
            'Epix': NEPoint.x,
            'Spix': SWPoint.y,
            'Wpix': SWPoint.x
        }

    # Create a method to calculate normalized pixel coordinates (in range of 0-width/height) at a custom zoom level
    # for cropping
    # The upper left corner of the image will be the origin (0, 0), since this is the standard in the PIL module
    def getPixelsToCropAt(self, shapeFile, corners, bleed=None):
        proj = MercatorProjection()
        z0Pixels = []
        zCustomPixels = []
        # For the geographical coordinates of the crop-points, get z0 pixel coordinates
        for geo in shapeFile:
            z0Pixels.append(proj.fromLatLngToPoint(G_LatLng(geo[1], geo[0])))
        # For the z0 pixel coordinates, get normalized zCustom coordinates
        # If no bleed, find normalized pixels corresponding to the z0 pixels of the shapefile
        if bleed is None:
            for pix in z0Pixels:
                normY = (pix.y - corners['Npix']) * self.mapHeight / (corners['Spix'] - corners['Npix'])
                normX = (pix.x - corners['Wpix']) * self.mapWidth / (corners['Epix'] - corners['Wpix'])
                zCustomPixels.append((normX, normY))
        # If bleed is required, find normalized pixels slightly outside the z0 pixels of the shapefile
        # Do this by making a pretense of slightly shrinking the Google Static Map image, and then normalizing
        # This way, they are normalized to slightly outside the shapefile
        if bleed is not None:
            shrinkNW = (corners['Spix'] - corners['Npix']) * (bleed / 100)
            shrinkSE = -1 * (corners['Spix'] - corners['Npix']) * (bleed / 100)
            for pix in z0Pixels:
                normY = (pix.y - (shrinkNW + corners['Npix'])) * self.mapHeight / (
                    (shrinkSE + corners['Spix']) - (shrinkNW + corners['Npix']))
                normX = (pix.x - (shrinkNW + corners['Wpix'])) * self.mapWidth / (
                    (shrinkSE + corners['Epix']) - (shrinkNW + corners['Wpix']))
                zCustomPixels.append((normX, normY))
        return zCustomPixels

    # Create method for cropping a Google Static Map image to the shape file of the property
    def cropImage(self, cropAtPixels, readFrom, writeTo):
        # Read image as RGB, and add alpha (transparency)
        im = Image.open(readFrom).convert("RGBA")
        # Convert to numpy array (for convenience)
        imArray = numpy.asarray(im)
        # Create mask
        polygon = cropAtPixels
        maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
        ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
        mask = numpy.array(maskIm)
        # Assemble new image (uint8: 0-255)
        croppedImArray = numpy.empty(imArray.shape, dtype='uint8')
        # Colors (three columns, RGB)
        croppedImArray[:, :, :3] = imArray[:, :, :3]
        # Transparency (fourth column, A)
        croppedImArray[:, :, 3] = mask * 255
        # Reconvert numpy array to image
        croppedIm = Image.fromarray(croppedImArray, "RGBA")
        # Save to file
        croppedIm.save(writeTo)
