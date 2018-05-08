import os.path

from qgis.core import QgsRasterLayer, QgsMapLayerRegistry, QgsVectorLayer
from PyQt4 import QtGui, uic

from wmf import wmf

class controlHS:
    
    def __init__(self):
        self.DEM = 0
        self.DIR = 0
        self.xll = 0
        self.yll = 0
        self.nodata = 0

    def cargar_mapa_raster (self,pathMapaRaster):
    
        retornoCargaLayerMapaRaster = False
    
        pathMapaRaster = pathMapaRaster.strip ()
    
        if (os.path.exists (pathMapaRaster)):
    
            baseNameMapaRaster   = os.path.basename (pathMapaRaster)
            baseNameMapaRaster = os.path.splitext(baseNameMapaRaster)[0]
            layerMapaRaster = QgsRasterLayer (pathMapaRaster, baseNameMapaRaster)
            QgsMapLayerRegistry.instance ().addMapLayer (layerMapaRaster)
    
            retornoCargaLayerMapaRaster = layerMapaRaster.isValid ()
    
        return retornoCargaLayerMapaRaster
    
    def cargar_mapa_vector(self, pathMapaVector, color = (50,50,250), width = 0.5):
        #Inicia vandera de cargado y ruta del vector
        retornoCargarMapaVector = False
        pathMapaVector = pathMapaVector.strip()
        #verifica existencia y dado el caso carga
        if os.path.exists(pathMapaVector):
            baseNameMapaVector = os.path.basename(pathMapaVector)
            baseNameMapaVector = os.path.splitext(baseNameMapaVector)[0]
            layerMapaVector = QgsVectorLayer(pathMapaVector, baseNameMapaVector, 'ogr')
            QgsMapLayerRegistry.instance().addMapLayer(layerMapaVector)
            
            symbols = layerMapaVector.rendererV2().symbols()
            symbol = symbols[0]
            symbol.setColor(QtGui.QColor.fromRgb(color[0],color[1],color[2]))
            symbol.setWidth(width)
            
            retornoCargarMapaVector = layerMapaVector.isValid()
        return retornoCargarMapaVector, layerMapaVector
    
    def cargar_mapa_dem_wmf (self,pathMapaDEM, dxp):
    
        retornoCargaLayerMapaRaster = False
    
        pathMapaDEM = pathMapaDEM.strip ()
    
        try:
    
            self.DEM = wmf.read_map_raster (pathMapaDEM, isDEMorDIR = True, dxp = dxp, noDataP = -9999)
            retornoCargaLayerMapaRaster = True
    
        except:
    
            retornoCargaLayerMapaRaster = False
    
        return retornoCargaLayerMapaRaster
    
    
    def cargar_mapa_dir_wmf (self,pathMapaDIR, dxp):
        retornoCargaLayerMapaRaster = False
        pathMapaDIR = pathMapaDIR.strip ()
        try:
            self.DIR = wmf.read_map_raster (pathMapaDIR, isDEMorDIR = True, isDIR = True, dxp = dxp, noDataP = -9999)
            retornoCargaLayerMapaRaster = True    
        except:
            self.DIR = 1
        return retornoCargaLayerMapaRaster
    
    def trazador_corriente(self,x,y, path = None):
        #Traza la corriente en las coordenadas especificadas
        self.stream = wmf.Stream(x, y, self.DEM, self.DIR)
        #Guarda la corriente.
        if path is not None:
            self.stream.Save_Stream2Map(path)
        
    def trazador_cuenca(self,x,y, dxp,umbral,PathDiv, PathRed, PathNC,TopoNodes = False, LastStream = True):
        # Traza la cuenca con y sin la ultima corriente.
        if LastStream:
            self.cuenca = wmf.SimuBasin(x, y, self.DEM, self.DIR, stream=self.stream)
        else:
            self.cuenca = wmf.SimuBasin(x, y, self.DEM, self.DIR)
        # Guarda los shapes de divisoria y de red hidrica.
        if len(PathDiv)>2:
            self.cuenca.Save_Basin2Map(PathDiv, dxp)
        if len(PathRed)>2:
            self.cuenca.Save_Net2Map(PathRed, dxp, umbral)
        
            
