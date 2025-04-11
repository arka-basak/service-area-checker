TOLERANCE = 1e-15


def raycast(location, polygon):
    """
    Loops through polygon vertices to check if rays from "location" intersect this edge
    Counts intersections, if count(intersection) is odd, must be outside polygon
    ** Ray-Casting Algorithm **

    Parameters:
    location ([float, float]): lat-long location of clinician
    polygons ([[lat,long],[lat,long]]): array of polygons (polygons-> list of vertices)

    Notes:
    Calls checkIntersection for intersection computations

    """
    intersections = 0
    for i in range(len(polygon) - 1):
        if (checkIntersection(location, polygon[i], polygon[i+1])):
            intersections += 1
    return (intersections % 2 == 1)

        

def checkIntersection(p, v1, v2):
    """
    Given a point p, shoot a horizontal ray (right) to check for intersection.
    Checks for intersection using the 2-point formula.

    Parameters:
    p ([float, float]): lat-long location of clinician
    v1, v2 ([lat,long],[lat,long]): lat-long location of 2 vertices

    Notes:
    establishes a tolerance to account for float error 

    """
    xp,yp = p[0], p[1]
    xv1, yv1 = v1[0],v1[1]
    xv2, yv2 = v2[0],v2[1]

    if (yp < yv1 and yp < yv2) or (yp > yv1 and yp > yv2):
        #outside y range 
        return False
    
    if xp > xv1 and xp > xv1 : 
        #point is to the right of x_range 
        return False

    if xp < xv1 and xp < xv1 : 
        #inside y_range and point is left of the edge
        return True
    
    if abs(yv2 - yv1) <= TOLERANCE:
        #inside, and segment is almost vertical (avoid div0)
        return True
    
    x_int = xv1 + (((yp-yv1)/(yv2-yv1)) * (xv2-xv1))
    return x_int >= xp 