import json
from mathtools.raycast import raycast

#main driver-entry to generate safety status of clinician
def generateSafetyStatus(res):
    location, polygons = parseClinicianStatus(res)
    polygons = prunePolygonSet(polygons)
    if location and polygons:
        return computeClinicianInServiceAreas(location, polygons)



#Processes api-response to serve clinician status geometry 
#todo: need to check individual coordinate if valid floats
def parseClinicianStatus(res):
    locationCoordinates = []
    polygons = []
    for feature in res['features']:
        geom = feature['geometry']
        if geom['type'] == "Point":
            #todo: check for invalid location (mult coords)
            locationCoordinates = geom['coordinates']
        elif geom['type'] == "Polygon":
            for polygon in geom['coordinates']:
                polygons.append(polygon)
    return locationCoordinates , polygons



#Filters polygon-set to only contain valid polygons
def prunePolygonSet(polygons):
    prunedPolygons = [p for p in polygons if p[0] == p[-1]]

    #todo: check for self-intersections (maybe)

    #print(json.dumps(prunedPolygons, indent = 2))
    return prunedPolygons



#computation driver 
def computeClinicianInServiceAreas(location, polygons):
    intersections = [] 
    for polygon in polygons:
        intersections.append(raycast(location, polygon))
    #decide on return 
    return True in intersections


# with open('testdata/invalid.json') as f:
#     res = json.load(f)   
#     print(generateSafetyStatus(res))