import math


# Create class for pixel coordinates (cartesian)
class G_Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


# Create class for geographical coordinates
class G_LatLng:
    def __init__(self, lt, ln):
        self.lat = lt
        self.lng = ln


# Create class for Mercator projection operations
class MercatorProjection:
    # NOTE:
    # The base world map (zoom=0) is 256x256 pixels
    # Every additional zoom increases both width and height by a factor of 2
    # There are two types of coordinates - geographical (latlong) and pixel coordinates (for a given zoom)
    # For each pixel coordinate reference, I've specified it as "z=# pixel coordinates"
    # For example, "z=0 pixel coordinates" are pixel coordinates at z=0
    # The z=0 pixel coordinates refer to the pixel coordinates (0-256, 0-256) of a point on the z=0 world map,
    # with the upper left corner as the origin (0,0)
    # At any zoom level #, (z=# pixel coordinates) = (z=0 pixel coordinates) * (2^#)

    # Initialize class object with
    def __init__(self):
        # Set the width of the base Google world map @ zoom=0
        z0WorldMapWidth = 256  # This will not change unless Google changes their entire system
        # Set the center of the z=0 base world map (128, 128)
        self.worldZ0Center_ = G_Point(z0WorldMapWidth / 2, z0WorldMapWidth / 2)
        # Set the number of z=0 pixels per degree longitude
        self.pixelsPerLonDegree_ = z0WorldMapWidth / 360
        # Set the number of z=0 pixels per radian longitude
        self.pixelsPerLonRadian_ = z0WorldMapWidth / (2 * math.pi)

    # Create a method for bound for the sine function
    # so that it doesn't hit -1 or 1
    # so that we don't divide by 0, or try log(0), in a later function
    def bound(self, value, minBound, maxBound):
        value = max(value, minBound)
        value = min(value, maxBound)
        return value

    # Create a method for converting degrees to radians
    def degreesToRadians(self, deg):
        return deg * (math.pi / 180)

    # Create a method for converting radians to degrees
    def radiansToDegrees(self, rad):
        return rad / (math.pi / 180)

    # Create a method for converting geographical coordinates to z=0 pixel coordinates
    # NOTE: The z=0 pixel coordinates are such that the the origin is at the upper left of the base world map
    def fromLatLngToPoint(self, latLng):
        proj = MercatorProjection()
        point = G_Point(0, 0)
        origin = self.worldZ0Center_
        point.x = origin.x + latLng.lng * self.pixelsPerLonDegree_
        siny = proj.bound(math.sin(proj.degreesToRadians(latLng.lat)), -0.9999, 0.9999)
        # See wikipedia for mercator projection math
        # For R=width/2pi (usual case), y'(lat)=R*sec(lat), therefore, y=
        point.y = origin.y + 0.5 * math.log((1 + siny) / (1 - siny)) * (-self.pixelsPerLonRadian_)
        return point

    # Create a method for converting z=0 pixel coordinates to geographical coordinates
    def fromPointToLatLng(self, point):
        proj = MercatorProjection()
        origin = self.worldZ0Center_
        lng = (point.x - origin.x) / self.pixelsPerLonDegree_
        latRadians = (point.y - origin.y) / -self.pixelsPerLonRadian_
        lat = proj.radiansToDegrees(2 * math.atan(math.exp(latRadians)) - math.pi / 2)
        return G_LatLng(lat, lng)
