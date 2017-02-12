import numpy as np

class functions():

    track_file = False


    @classmethod
    def getTrackData(self, colName = False):

        if functions.track_file is False:
            functions.track_file = np.loadtxt('ALLTrackData.csv', delimiter=',')
            
        #1 - 'Index' -  Index, for usefullness
        #2,3 - 'LongLat' - GPS Long and Lat
        #4,5,6 - 'CartCo' - X, Y and Z in meters, finish line as 0,0
        #7 - 'Dist' - Distance along track (cumulative)
        #8 - 'SectDist' - Distance between point and next
        #9 - 'RadCurve' - Radius of this point and neighbours (in X,Y)
        #10 - 'Grad' - Gradient (Z/Dist)
        #11 - 'AngleVert' - Angle to vertical
        #12 - 'Speed' - The recommended speed for that section of track
        
        if colName is False:
            return functions.track_file
        elif colName == "Index":
            return functions.track_file[:,0]
        elif colName == "LongLat":
            return functions.track_file[:,[1,2]]
        elif colName == "CartCo":
            return functions.track_file[:,[4,5,3]]
        elif colName == "Speed":
          return functions.track_file[:,[11]]
        elif colName == "Range":
          return functions.track_file[:,[12]]