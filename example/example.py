from MercatorProjection import G_LatLng, MercatorProjection
from GoogleStaticMap import GoogleStaticMap

# Create class object for mercator projection and google map image operations
mp = MercatorProjection()
gm = GoogleStaticMap()

# Start with a shapefile (from Stephane's function)
shapeFile = [[-122.12383758245336, 37.75571233182055], [-122.12417229112891, 37.755581544780114],
             [-122.12417786881252, 37.755594075381474], [-122.12424662138503, 37.75574856188482],
             [-122.12388534031416, 37.75586057852918], [-122.1238793355483, 37.75583734460038],
             [-122.12387281699273, 37.75581420454203], [-122.12386579509725, 37.75579115437591],
             [-122.12385826751844, 37.7557682073795], [-122.12385023293253, 37.755745363222445],
             [-122.12384169955205, 37.755722636082446], [-122.12383758245336, 37.75571233182055]]

# Get bound-box (from Stephane's function)
bbox = [G_LatLng(37.75586057852918, -122.12424662138503), G_LatLng(37.755581544780114, -122.12383758245336)]

# Get center of bound-box (from Stephane's function)
centerLat = 37.75572106165465
centerLon = -122.1240421019192
center = G_LatLng(centerLat, centerLon)

# Get optimal zoom
zoom = gm.getOptimalZoom(bbox)

# Get corners of map
corners = gm.getCorners(center, zoom)

# Get pixels to crop at
cropAtPixels = gm.getPixelsToCropAt(shapeFile, corners, bleed=None)

# Crop map to these pixels
gm.cropImage(cropAtPixels, 'C:/image/example.png', 'C:/image/out.png')
