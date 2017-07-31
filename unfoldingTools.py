'''
Used to create functions and classes useful for the spectral unfolding.

'''

import numpy as np
import matplotlib.pyplot as plt



class BonnerSphereTools(object):
    def __init__(self):
        pass
    
    
    def measuredData(self, sphereIDs, sphereSizes, responseData, responseError, extraError, correctFactor=0):
        self.sphereIDs = sphereIDs
        self.sphereSizes = sphereSizes
        self.responseData = responseData
        self.responseError = responseError
        self.extraError = extraError
        self.numOfSpheres = len(sphereSizes)
        self.correctionFactor = correctFactor
        
        ibuString  = 'Input file for Bonner Spheres\n'
        ibuString += '   {}   {}\n'.format(self.numOfSpheres, self.correctionFactor)
        for i, names in enumerate(self.sphereIDs):
            ibuString += '{}   {}   {}   {}   {}   {}   {}\n'.format(self.sphereIDs[i][0], self.sphereSizes[i], self.responseData[i], self.responseData[i] * self.responseError[i], self.responseError[i], self.extraError[i], i)
        ibuString += '\n'
        
        return ibuString
    
    def responseFunctions(self, rfErgEdges, responses, ergUnits='MeV'):
        self.rfErgEdges = rfErgEdges
        self.responses = responses
        self.ergUnits = ergUnits
        
        
        
        if self.ergUnits == 'eV' : self.ieu = 0
        if self.ergUnits == 'MeV' : self.ieu = 1
        if self.ergUnits == 'KeV' : self.ieu = 2
        
        
        
        fmtString  = 'Response Function file for Bonner Spheres\n'
        fmtString += 'Contains {} spheres and {} energy groups using units of {}\n'.format(len(self.sphereIDs), len(self.rfErgEdges), self.ergUnits)
        fmtString += '  {}  {}\n'.format(len(self.rfErgEdges), self.ieu)
        
        for i, erg in enumerate(self.rfErgEdges):
            fmtString += '{:4.3e} '.format(erg)
            if (i + 1) % 8 == 0:
                fmtString += '\n'
                eolFlag = 1
            else:
                eolFlag = 0
        if eolFlag == 0:
            fmtString += '\n'
        
        fmtString += '   0   \n'
        fmtString += '   {}   \n'.format(len(self.numOfSpheres))
        
        for i, names in enumerate(self.sphereIDs):
            fmtString += '{}  {}\n'.format(names[0], names[1])
            fmtString += '1.000E+00      cm^2         0         0    3    1    1    0\n'
            
            LHS = i * len(self.rfErgEdges)
            RHS = (i + 1) * len(self.rfErgEdges) 
            for i, resp in enumerate(self.responses[LHS:RHS]):
                fmtString += '{:4.3e} '.format(resp)
                if (i + 1) % 8 == 0:
                    fmtString += '\n'
                    eolFlag = 1
                else:
                    eolFlag = 0
                if eolFlag == 0:
                    fmtString += '\n'
        
        return fmtString
    
    def defaultSpectrum(self, ):
        pass
    
    def controlFile(self, ):
        pass