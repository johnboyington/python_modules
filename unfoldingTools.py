'''
Used to create functions and classes useful for the spectral unfolding.

'''

import numpy as np
import matplotlib.pyplot as plt



class BonnerSphereTools(object):
    def __init__(self):
        self.sphereIDs = None
        self.sphereSizes = None
        self.responseData = None
        self.responseError = None
        self.extraError = None
        self.correctionFactor = 0
        self.rfErgEdges = None
        self.responses = None
        self.rfErgUnits = 'MeV'
        self.mode = 1
        self.dsErgUnits = 'MeV'
        self.dS = None
        self.dsErr = None
        self.dsErgEdges = None
        self.ibuName = None
        self.fmtName = None
        self.fluName = None
        self.outName = None
        self.inpName = None
        self.finalChiSqr = 1.1
        self.temp = [1.0, 0.85]
        self.solnStructure = 2
        self.solnRepresentation = 1
        self.scaling = [0, 1, 1]
    
    
    def writeMeasuredData(self):
        
        ibuString  = 'Measured Responses for Bonner Spheres\n'
        ibuString += '   {}   {}\n'.format(len(self.sphereSizes), self.correctionFactor)
        for i, names in enumerate(self.sphereIDs):
            ibuString += '{}   {:4.1f}   {:4.3E}   {:4.3E}   {:5.4f}   {:5.4f}   {:2d}\n'.format(self.sphereIDs[i][0], self.sphereSizes[i], self.responseData[i], self.responseData[i] * self.responseError[i], self.responseError[i], self.extraError[i], i + 1)
        ibuString += '\n'
        with open('{}.ibu'.format(self.ibuName), 'w+') as F:
            F.write(ibuString)
        return
    
    def writeResponseFunctions(self):
        if self.rfErgUnits == 'eV' : self.rfIEU = 0
        if self.rfErgUnits == 'MeV' : self.rfIEU = 1
        if self.rfErgUnits == 'keV' : self.rfIEU = 2
        fmtString  = 'Response Function file for Bonner Spheres\n'
        fmtString += 'Contains {} spheres and {} energy groups using units of {}\n'.format(len(self.sphereIDs), len(self.rfErgEdges), self.rfErgUnits)
        fmtString += '  {}  {}\n'.format(len(self.rfErgEdges), self.rfIEU)
        
        for i, erg in enumerate(self.rfErgEdges):
            fmtString += '{:4.3E} '.format(erg)
            if (i + 1) % 8 == 0:
                fmtString += '\n'
                eolFlag = 1
            else:
                eolFlag = 0
        if eolFlag == 0:
            fmtString += '\n'
        
        fmtString += '   0   \n'
        fmtString += '   {}   \n'.format(len(self.sphereSizes))
        
        for i, names in enumerate(self.sphereIDs):
            fmtString += '{}  {}\n'.format(names[0], names[1])
            fmtString += '1.000E+00      cm^2         0         0    3    1    1    0\n'
            
            for j, resp in enumerate(self.responses[i]):
                fmtString += '{:4.3E} '.format(resp)
                if (j + 1) % 8 == 0:
                    fmtString += '\n'
                    eolFlag = 1
                else:
                    eolFlag = 0
            if eolFlag == 0:
                fmtString += '\n'
        with open('{}.fmt'.format(self.fmtName), 'w+') as F:
            F.write(fmtString)
        return
    
    def writeDefaultSpectrum(self):
        if self.dsErgUnits == 'eV' : self.dsIEU = 0
        if self.dsErgUnits == 'MeV' : self.dsIEU = 1
        if self.dsErgUnits == 'keV' : self.dsIEU = 2
        fluString  = 'Default Spectrum for Bonner Sphere Unfolding\n'
        fluString += '   {}   {}\n'.format(self.mode, self.dsIEU)
        fluString += '       2         {}        {}       {:4.3E}\n'.format(len(self.dS), len(self.dS), max(self.dsErgEdges))
        for i, value in enumerate(self.dS):
            fluString += '{:4.3E}  {:4.3E}  {:4.3E}\n'.format(self.dsErgEdges[i], value, self.dsErr[i])
        with open('{}.flu'.format(self.fluName), 'w+') as F:
            F.write(fluString)
        return

    
    def writeControlFile(self):
        inpString  = '{}.ibu   \n'.format(self.ibuName)
        inpString += '{}.fmt   \n'.format(self.fmtName)
        inpString += '{}   \n'.format(self.outName)
        inpString += '{}.flu   \n'.format(self.fluName)
        inpString += '{}   \n'.format(max(self.rfErgEdges))
        inpString += '{}   \n'.format(self.finalChiSqr)
        inpString += '{}, {}   \n'.format(self.temp[0], self.temp[1])
        inpString += '{}, {}   \n'.format(self.solnStructure, self.solnRepresentation)
        inpString += '{}   \n{}   \n{}\n'.format(self.scaling[0], self.scaling[1], self.scaling[2])
        with open('{}.inp'.format(self.inpName), 'w+') as F:
            F.write(inpString)
        return
    
    def writeMaxedFiles(self):
        self.writeMeasuredData()
        self.writeResponseFunctions()
        self.writeDefaultSpectrum()
        self.writeControlFile()
