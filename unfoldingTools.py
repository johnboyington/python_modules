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
    
    def responseFunctions(self, rfErgEdges, responses, rfErgUnits='MeV'):
        self.rfErgEdges = rfErgEdges
        self.responses = responses
        self.rfErgUnits = rfErgUnits
        
        
        
        if self.rfErgUnits == 'eV' : self.rfIEU = 0
        if self.rfErgUnits == 'MeV' : self.rfIEU = 1
        if self.rfErgUnits == 'KeV' : self.rfIEU = 2
        
        
        
        fmtString  = 'Response Function file for Bonner Spheres\n'
        fmtString += 'Contains {} spheres and {} energy groups using units of {}\n'.format(len(self.sphereIDs), len(self.rfErgEdges), self.ergUnits)
        fmtString += '  {}  {}\n'.format(len(self.rfErgEdges), self.rfIEU)
        
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
    
    def defaultSpectrum(self, dsErgEdges, defaultSpectrum, defaultSpectrumError, mode=1, dsErgUnits='MeV'):
        self.mode = mode
        self.dsErgUnits = dsErgUnits
        self.dS = defaultSpectrum
        self.dsErr = defaultSpectrumError
        self.dsErgEdges = dsErgEdges
        
        
        
        if self.dsErgUnits == 'eV' : self.dsIEU = 0
        if self.dsErgUnits == 'MeV' : self.dsIEU = 1
        if self.dsErgUnits == 'KeV' : self.dsIEU = 2
        
        
        fluString  = 'Default Spectrum for Bonner Sphere Unfolding\n'
        fluString += '   {}   {}\n'.format(self.mode, self.dsIEU)
        fluString += '       2         {}        {}       {:4.3e}\n'.format(len(self.dS), len(self.dS), max(self.dsErgEdges))
        for i, value in enumerate(self.dS):
            fluString += '{:4.3e}  {:4.3e}  {:4.3e}\n'.format(self.dsErgEdges[i], value, self.dsErr[i])
        return fluString
    
    def controlFile(self, ibuName, fmtName, fluName, outName, finalChiSqr, temp=[1.0, 0.85], solnStructure=2, solnRepresentation=1, scaling):
        self.ibuName = ibuName
        self.fmtName = fmtName
        self.fluName = fluName
        self.outName = outName
        self.finalChiSqr = finalChiSqr
        self.temp = temp
        self.solnStructure = solnStructure
        self.solnRepresentation = solnRepresentation
        self.scaling = scaling
        
        
        inpString  = '{}   \n'.format(self.ibuName)
        inpString += '{}   \n'.format(self.fmtName)
        inpString += '{}   \n'.format(self.outName)
        inpString += '{}   \n'.format(self.fluName)
        inpString += '{}   \n'.format(max(self.rfErgEdges))
        inpString += '{}   \n'.format(self.finalChiSqr)
        inpString += '{}, {}   \n'.format(self.temp[0], self.temp[1])
        inpString += '{}, {}   \n'.format(self.solnStructure, self.solnRepresentation)
        inpString += '{}   \n{}   \n{}\n'.format(self.scaling[0], self.scaling[1], self.scaling[2])
        return inpString

















