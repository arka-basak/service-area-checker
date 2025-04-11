from clinicianStatus import updateSafetyStatus
from mathtools.raycast import raycast

def generateSafetyStatus(res):
    """
    main driver-entry to generate safety status of clinician

    Parameters:
    res (response object): From Clinician Status API, should contain list of features
    """
    location, polygons = parseClinicianStatus(res)
    polygons = prunePolygonSet(polygons)
    if location and polygons:
        safetyStatus =  computeClinicianInServiceAreas(location, polygons)
        return safetyStatus



def parseClinicianStatus(res):
    """
    Processes api-response to serve clinician status geometry 

    Parameters:
    res (response object): From Clinician Status API, should contain list of features
    """
    locationCoordinates = []
    polygons = []
    for feature in res['features']:
        geom = feature['geometry']
        if geom['type'] == "Point":
            locationCoordinates = geom['coordinates']
        elif geom['type'] == "Polygon":
            for polygon in geom['coordinates']:
                polygons.append(polygon)
    return locationCoordinates , polygons



#
def prunePolygonSet(polygons):
    """
    Filters polygon-set to only contain valid polygons

    Parameters:
    polygons ([[lat,long],[lat,long]]): array of polygons (polygons-> list of vertices)
    """
    prunedPolygons = [p for p in polygons if p[0] == p[-1]]
    return prunedPolygons



def computeClinicianInServiceAreas(location, polygons):
    """
    Checks each pruned polygon and apply Raycast-algorithm

    Parameters:
    location ([float, float]): lat-long location of clinician
    polygons ([[lat,long],[lat,long]]): array of polygons (polygons-> list of vertices)
    Notes: 
    https://en.wikipedia.org/wiki/Ray_casting#:~:text=Ray%20casting%20is%20the%20most,scenes%20to%20two%2Ddimensional%20images.
    """
    intersections = [] 
    for polygon in polygons:
        intersections.append(raycast(location, polygon))
    return True in intersections


