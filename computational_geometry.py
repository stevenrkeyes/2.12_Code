import numpy as np

class Segment:
    # a line consists of two points as np arrays
    def __init__(self, x1, x2):
        # TODO: check that the points are the same dimensions
        # TODO: check that the point arrays are row vectors
        self.x1 = x1
        self.x2 = x2

    # check if the line segment intersects another line segment
    # see http://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    def intersects(self, other):
        # first, check if their bounding boxes could possibly intersect (this is a fast check)
        if not self.bounding_box_translation_intersects(other):
            return False
        
        # rewrite the segments in relative vector notation: 
        # p = self.x1; p + r = self.x2; q = other.x1; q + s = other.x2
        p = self.x1
        r = self.x2 - p
        q = other.x1
        s = other.x2 - q
        bottom_cross_product = np.linalg.norm(np.cross(r, s))
        difference = q - p        
        top_cross_product1 = np.linalg.norm(np.cross(difference, r))

        # check if the properties of this notation suggest an intersection
        if bottom_cross_product == 0:
            # if the cross product of the lengths is 0,
            # then the lines are parallel
            if top_cross_product1 == 0:
                # if (q - p) x r == 0, then the lines are colinear
                if (0 <= np.dot(difference, r) <= np.dot(r, r)) or \
                   (0 <= np.dot(difference, s) <= np.dot(s, s)):
                    # then segments are overlapping
                    return True
                else:
                    # the lines are collinear but disjoint
                    return False
            else:
                # the lines are parallel but non-intersecting
                return False
        else: # bottom_cross_product != 0
            t = np.linalg.norm(np.cross(difference, s)) / bottom_cross_product
            u = top_cross_product1 / bottom_cross_product
            
            if 0 <= t <= 1 and 0 <= u <= 1:
                # the two line segments meet at a point somewhere along them
                # specifically (p + t*r) which is the same as (q + u*s)
                return True
            else:
                # the two line segments are not parallel but do not intersect
                return False

    # check if two lines' bounding boxes intersect
    # TODO: make this work for general geometric objects, not just lines
    # TODO: make this work in greater than 2 dimensions
    # NOTE: currently checking if any vertical or horizontal translation of the bounding box intersects
    def bounding_box_translation_intersects(self, other):
        (oleft, oright) = sorted2(other.x1[0], other.x2[0])
        (sleft, sright) = sorted2(self.x1[0], self.x2[0])
        (obottom, otop) = sorted2(other.x1[0], other.x2[0])
        (sbottom, stop) = sorted2(self.x1[0], self.x2[0])
        
        #if (sleft > oright) or \
        #   (sright < oleft) or \
        #   (stop < obottom) or \
        #   (sbottom > otop):
        #    return False
        #return True
        return (sleft <= oright) and \
               (sright >= oleft) and \
               (stop >= obottom) and \
               (sbottom <= otop)
        
def sorted2(a, b):
    if a > b:
        return (b, a)
    else:
        return (a, b)

# TODO: substantiate this and other shapes (and their intersection
# conditions) if we want to be able to input more varied workspaces
class Circle:
    def __init__(self, center, radius):
        pass
