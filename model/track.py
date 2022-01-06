import pygame

# ------------------------------
import utils
# -----------------------------

class Track:
    _circuit = None
    _cback = (128,128,128)
    _cfore = (10,10,10)
    _width = 30
    _screen = None
    _cachedLength = []
    _cachedNormals = []

    def __init__(self, screen):
        self._circuit = utils.__circuit__
        self._screen = screen
        for i in range(0,len(self._circuit)):
            self._cachedNormals.append(utils.vecDiff(self._circuit[i], self._circuit[len(self._circuit)-1 if i-1 < 0 else i-1]))
            self._cachedLength.append(utils.approximateLength(self._cachedNormals[i]))
            self._cachedNormals[i] = (self._cachedNormals[i][0]/self._cachedLength[i], self._cachedNormals[i][1]/self._cachedLength[i] )


    def _segmentPointAddLength(self, segment, point, length):
        ''' get the segment and point (on it) after adding length to the segment and point (on it), by following the
        path'''
        nextStep = utils.approximateDistance(point, self._circuit[segment])
        if nextStep > length: # We stay on the same segment
            nextPoint = utils.vecAdd(point, utils.vecScalarMult(self._cachedNormals[segment], length))
            return (segment, (int(nextPoint[0]), int(nextPoint[1])))
        length -= nextStep
        segment = segment+1 if segment+1<len(self._circuit) else 0
        while length > self._cachedLength[segment]:
            length -= self._cachedLength[segment]
            segment = segment+1 if segment+1<len(self._circuit) else 0
        nextPoint = utils.vecAdd(self._circuit[segment-1 if segment > 0 else len(self._circuit)-1],
                utils.vecScalarMult(self._cachedNormals[segment], length))
        return (segment, (int(nextPoint[0]), int(nextPoint[1])))

    def _closestSegmentPointToPoint(self,point):
        bestLength = None
        bestPoint = None
        bestSegment = None
        for i in range(0, len(self._circuit)):
            p = self._closestPointToSegment(i,point)
            l = utils.approximateDistance(p,point)
            if bestLength is None or l < bestLength:
                bestLength = l
                bestPoint = p
                bestSegment = i
        return (bestSegment, bestPoint, bestLength)

    def _closestPointToSegment(self, numSegment, point):
        ''' Returns the closest point on the circuit segment from point'''
        p0 = self._circuit[len(self._circuit)-1 if numSegment-1 < 0 else numSegment-1]
        p1 = self._circuit[numSegment]
        local = utils.vecDiff(point, p0)
        projection = utils.vecDot(local, self._cachedNormals[numSegment])
        if projection < 0:
            return p0
        if projection > self._cachedLength[numSegment]:
            return p1
        return utils.vecAdd(p0,utils.vecScalarMult(self._cachedNormals[numSegment], projection))

    def drawMe(self, scene = None):

        for p in self._circuit: # Draw simple inner joins
            pygame.draw.circle(self._screen,self._cback,p,int(self._width/2),0)
        pygame.draw.lines(self._screen, self._cback, True, self._circuit, self._width)
        pygame.draw.lines(self._screen, self._cfore, True, self._circuit, 1)

        for i,p in enumerate(self._circuit):
            pygame.draw.line(self._screen, (0,0,250), p, utils.vecAdd(p,utils.vecScalarMult(self._cachedNormals[i], 50)))

        # if scene is not None:
        #     for i,p in enumerate(self._circuit):
        #         scene.drawText(str(int(self._cachedLength[i])), p)
