import numpy


def raycast(location, polygon):
    r = [
        polygon[0][0] - location[0],
        polygon[0][1] - location[1]
    ]
    #check if this ray hits any other edge 
    intersections = 0 
    for i in range(len(polygon) - 1):
        # check if vertex hits this particular edge
        checkIntersection(r, polygon[i], polygon[i+1])

        

def checkIntersection(r, v1, v2):
    print(r, v1, v2)
    intersectionCount = 0 
