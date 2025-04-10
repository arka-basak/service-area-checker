import json

#main driver to generate safety status of clinician
def generateSafetyStatus(res):
    location, polygons = parseClinicianStatus(res)
    polygons = prunePolygonSet(polygons)


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

    # prunedPolygons = []
    # for polygon in polygons: 
    #     if polygon[0] == polygon[-1]:
    #         prunedPolygons.append(polygon)

    #todo: check for self-intersections (maybe)
    print(json.dumps(prunedPolygons, indent = 2))
    return prunedPolygons


with open('testdata/invalid.json') as f:
    res = json.load(f)   
    generateSafetyStatus(res)