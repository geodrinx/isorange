# -*- coding: utf-8 -*-
"""
/***************************************************************************
 isorange
                                 A QGIS plugin
  isorange
                              -------------------
        begin                : 2014-12-11
        git sha              : $Format:%H$
        copyright            : (C) 2014 by geodrinx
        email                : geodrinx@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from isorange_dialog import isorangeDialog
import os.path


import os.path

import qgis
from qgis.core import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.gui import QgsMessageBar

from shapely.wkb import loads
from shapely.wkt import dumps
from shapely.geometry import Polygon, Point

import shutil

import voronoi

import math


class isorange:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'isorange_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = isorangeDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&isorange')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'isorange')
        self.toolbar.setObjectName(u'isorange')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('isorange', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/isorange/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'isorange'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&isorange'),
                action)
            self.iface.removeToolBarIcon(action)

#--------------------------------------------------------------------
    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
#            pass


            edit_distanza = self.dlg.findChild(QLineEdit,"edit_distanza")
            distanza = float(edit_distanza.text())

#            checkBox_IncludiPuntiOriginali = self.dlg.findChild(QCheckBox,"checkBox_IncludiPuntiOriginali")            
#            if checkBox_IncludiPuntiOriginali.isChecked() == True:
#               IncludiPuntiOriginali = int(1)
#            else:
#               IncludiPuntiOriginali = int(0) 

            checkBox_MostraTriangoliEsterni = self.dlg.findChild(QCheckBox,"checkBox_MostraTriangoliEsterni")            
            if checkBox_MostraTriangoliEsterni.isChecked() == True:
               MostraTriangoliEsterni = int(1)
            else:
               MostraTriangoliEsterni = int(0) 

#            distanza = 15.00   #  <-----------  RISOLUZIONE (modificabile) 
#            misura = 9.00


            canvas = self.iface.mapCanvas()

            layer = canvas.currentLayer()


            if (layer == NULL):
               self.iface.messageBar().pushMessage("WARNING", "No active vector layer!!!", level=QgsMessageBar.WARNING, duration=3)            
               return  

            if layer.type() != layer.VectorLayer:
               self.iface.messageBar().pushMessage("WARNING", "You need to have a vector Point layer active !!!", level=QgsMessageBar.WARNING, duration=3)
               return

            
            crs = layer.crs()

            if (crs.authid() == "EPSG:4326"):
              dist = distanza / 100000  
            else:
              dist = distanza


            provider = layer.dataProvider()


#--------------------------------------------------------
            geomType = ("Point" + '?crs=%s') %(crs.authid())
            DronePlan = "ISR_Points_" + str(distanza) + "_m"             
            memLay_Point = QgsVectorLayer(geomType, DronePlan, 'memory') 
            memprovider_Point = memLay_Point.dataProvider()

            memLay_Point.updateExtents()
            memLay_Point.commitChanges()
            QgsMapLayerRegistry.instance().addMapLayer(memLay_Point)
            res = memprovider_Point.addAttributes( [ QgsField("ID",  QVariant.String), QgsField("xo",  QVariant.String), QgsField("yo",  QVariant.String), QgsField("triangle",  QVariant.String), QgsField("triaord",  QVariant.String), QgsField("internal",  QVariant.String), QgsField("mediana",  QVariant.String), QgsField("misura", QVariant.String)] )             
#--------------------------------------------------------
#            geomType = ("Polygon" + '?crs=%s') %(crs.authid())
#            DronePlan = "ISR_Tin_" + str(distanza) + "_m"             
#            memLay_Tin = QgsVectorLayer(geomType, DronePlan, 'memory') 
#            memprovider_Tin = memLay_Tin.dataProvider()
#
#            memLay_Tin.updateExtents()
#            memLay_Tin.commitChanges()
#            QgsMapLayerRegistry.instance().addMapLayer(memLay_Tin)
#            res = memprovider_Tin.addAttributes( [ QgsField("nPoligono",  QVariant.String), QgsField("lato",  QVariant.String), QgsField("xo",  QVariant.String), QgsField("yo",  QVariant.String), QgsField("triangle",  QVariant.String), QgsField("triaord",  QVariant.String), QgsField("internal",  QVariant.String), QgsField("mediana",  QVariant.String), QgsField("misura", QVariant.String)] )                        
#--------------------------------------------------------
#            geomType = ("Point" + '?crs=%s') %(crs.authid())
#            DronePlan = "ISR_SpinePoints_" + str(distanza) + "_m"             
#            memLay_SpinePoints = QgsVectorLayer(geomType, DronePlan, 'memory') 
#            memprovider_SpinePoints = memLay_SpinePoints.dataProvider()
#
#            memLay_SpinePoints.updateExtents()
#            memLay_SpinePoints.commitChanges()
#            QgsMapLayerRegistry.instance().addMapLayer(memLay_SpinePoints)
#            res =  memprovider_SpinePoints.addAttributes( [ QgsField("nPoligono",  QVariant.String), QgsField("COD_VARIET", QVariant.String), QgsField("lato",  QVariant.String), QgsField("xo",  QVariant.String), QgsField("yo",  QVariant.String), QgsField("triangle",  QVariant.String), QgsField("triaord",  QVariant.String), QgsField("internal",  QVariant.String), QgsField("mediana",  QVariant.String), QgsField("misura", QVariant.String)] )   
#--------------------------------------------------------
#            geomType = ("LineString" + '?crs=%s') %(crs.authid())
#            DronePlan = "ISR_SpineLine_" + str(distanza) + "_m"             
#            memLay_SpineLine = QgsVectorLayer(geomType, DronePlan, 'memory') 
#            memprovider_SpineLine = memLay_SpineLine.dataProvider()
#
#            memLay_SpineLine.updateExtents()
#            memLay_SpineLine.commitChanges()
#            QgsMapLayerRegistry.instance().addMapLayer(memLay_SpineLine)
#            res =  memprovider_SpineLine.addAttributes( [ QgsField("nPoligono",  QVariant.String), QgsField("COD_VARIET", QVariant.String), QgsField("lato",  QVariant.String), QgsField("xo",  QVariant.String), QgsField("yo",  QVariant.String), QgsField("triangle",  QVariant.String), QgsField("triaord",  QVariant.String), QgsField("internal",  QVariant.String), QgsField("mediana",  QVariant.String), QgsField("misura", QVariant.String), QgsField("lunghezza", QVariant.String), QgsField("IdClass", QVariant.String)] )   
#--------------------------------------------------------

            styledir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "python/plugins/isorange/_QML_Styles"
            memLay_Point.loadNamedStyle(styledir + '/ISR_Points.qml')
#            memLay_Tin.loadNamedStyle(styledir + '/ISR_TIN.qml')
#            memLay_SpineLine.loadNamedStyle(styledir + '/ISR_SpineLine.qml')
#--------------------------------------------------------

# retreive every feature (or selected features) with its geometry and attributes


            nPoligono = 0
            nElement = 0


            count = layer.selectedFeatureCount()
            
            if (count != 0):
               iter = layer.selectedFeatures() 
            else:                          
               iter = layer.getFeatures()
            # EndIf 

            points = [] 
            poly   = [] 

            distance = float(distanza)
               
            for feat in iter:

              nPoligono = nPoligono +1

              # fetch geometry
              geom = feat.geometry()
              
              # show some information about the feature
              
              if geom.type() == QGis.Point:
                elem = geom.asPoint()
                point = elem                       

                points.append( point )
                poly.append( point )
                
                               
              elif geom.type() == QGis.Line:
                self.iface.messageBar().pushMessage("WARNING", "You need to have a vector Point layer active !!!", level=QgsMessageBar.WARNING, duration=3)
                return

              elif geom.type() == QGis.Polygon:
                self.iface.messageBar().pushMessage("WARNING", "You need to have a vector Point layer active !!!", level=QgsMessageBar.WARNING, duration=3)
                return

            # End For
                   
################


#  Delaunay Triangulation-----------------------------------------

#   Costruisco il poligono esterno
################
#                print ("DIST DIST*3 LENGTH %s %s %s") %(dist, dist*3, perimetro)
            if (nPoligono):
                
                   msg = ("Poligono %s") %(nPoligono)
                   self.iface.mainWindow().statusBar().showMessage(msg)
                   
                   polEsterno = Polygon(poly)

# Calcola il TIN
#                   print points
                   
                   triangles = voronoi.computeDelaunayTriangulation( points )

                   msg = ("Delaunay %s") %(nPoligono)
                   self.iface.mainWindow().statusBar().showMessage(msg)
    
                   feat =           QgsFeature()
                   featSpinePoint = QgsFeature()
                   featSpineLine  = QgsFeature()                   
                   nFeat =          len( triangles )
    
                   nElement = 0


# Disegna i triangoli (solo se contenuti nel poligono)
###################!
                   for triangle in triangles:

                      indicies = list( triangle )


                      # Metto gli indici in ordine crescente
                      
                      ind0 = indicies[0]
                      ind1 = indicies[1]
                      ind2 = indicies[2]
      
      
                      x0 = points[ind0].x()
                      y0 = points[ind0].y()
      
                      x1 = points[ind1].x()
                      y1 = points[ind1].y()
      
                      x2 = points[ind2].x()
                      y2 = points[ind2].y()            


                      lato = 0
                      xa = x0
                      ya = y0
                      xb = x2
                      yb = y2
                      xc = x1
                      yc = y1                         
         
                      dxAB = (xb-xa)
                      dyAB = (yb-ya)

                      dxBC = (xc-xb)
                      dyBC = (yc-yb)

                      dxCA = (xa-xc)
                      dyCA = (ya-yc)
    
                      distAB = math.sqrt(dxAB*dxAB + dyAB*dyAB)
                      distBC = math.sqrt(dxBC*dxBC + dyBC*dyBC)
                      distCA = math.sqrt(dxCA*dxCA + dyCA*dyCA)    


                      tria = ("%s %s %s %s") %(nPoligono, ind0, ind1, ind2)
                      triaord = ("%05d %05d %05d %05d") %(nPoligono, ind0, ind1, ind2)

                      xCenAC = (xa+xc)/2.  # questo è il punto centrale del lato
                      yCenAC = (ya+yc)/2.    

                      xo = (xCenAC + xb)/2.  # questo è il punto centrale della mediana                      
                      yo = (yCenAC + yb)/2.

                      pun = Point(xo, yo)
      
                      dentro = polEsterno.contains(pun)

                      mediana = 0

                      internal = '0'
                      if ( (dentro == True) ):
                         internal = '1'                      
                      
                      if (distAB < distance):
                         Point1 = QgsGeometry.fromPoint( QgsPoint(xa, ya) )
                         Point2 = QgsGeometry.fromPoint( QgsPoint(xb, yb) )

                         dista = distAB

                         feat.setGeometry( Point1 ) 
                         feat.initAttributes(8)

                         values = [(ind0),  (xa), (ya), (tria), (triaord), (internal), (mediana), (dista)]                  
                         feat.setAttributes(values) 
                         memprovider_Point.addFeatures([feat])

                         feat.setGeometry( Point2 ) 
                         feat.initAttributes(8)
                         
                         values = [(ind1),  (xb), (yb), (tria), (triaord), (internal), (mediana), (dista)]                  
                         feat.setAttributes(values) 
                         memprovider_Point.addFeatures([feat])                         

                      if (distBC < distance):
                         Point1 = QgsGeometry.fromPoint( QgsPoint(xc, yc) )
                         Point2 = QgsGeometry.fromPoint( QgsPoint(xb, yb) )

                         dista = distBC

                         feat.setGeometry( Point1 ) 
                         feat.initAttributes(8)

                         values = [(ind2),  (xc), (yc), (tria), (triaord), (internal), (mediana), (dista)]                  
                         feat.setAttributes(values) 
                         memprovider_Point.addFeatures([feat])

                         feat.setGeometry( Point2 ) 
                         feat.initAttributes(8)
                         
                         values = [(ind1),  (xb), (yb), (tria), (triaord), (internal), (mediana), (dista)]                  
                         feat.setAttributes(values) 
                         memprovider_Point.addFeatures([feat])  
                            
                      if (distCA < distance):
                         Point1 = QgsGeometry.fromPoint( QgsPoint(xa, ya) )
                         Point2 = QgsGeometry.fromPoint( QgsPoint(xc, yc) )                                                        

                         dista = distCA

                         feat.setGeometry( Point1 ) 
                         feat.initAttributes(8)

                         values = [(ind0),  (xa), (ya), (tria), (triaord), (internal), (mediana), (dista)]                  
                         feat.setAttributes(values) 
                         memprovider_Point.addFeatures([feat])

                         feat.setGeometry( Point2 ) 
                         feat.initAttributes(8)
                         
                         values = [(ind2),  (xc), (yc), (tria), (triaord), (internal), (mediana), (dista)]                  
                         feat.setAttributes(values) 
                         memprovider_Point.addFeatures([feat])  

#  ----------------------!
     

###################!


################
            msg = ("SpineLine %s") %(nPoligono)
            self.iface.mainWindow().statusBar().showMessage(msg)

            nElement += 1

            memLay_Point.updateFields()

            
#            memLay_Tin.updateFields()


#            memLay_SpinePoints.updateFields()
#            memLay_SpineLine.updateFields()                      
################
            #if dista*3 <= length:
                        
#            memLay_Tin.updateExtents()                                                                                                                         

            msg = ("Terminati Poligoni %s") %(nPoligono)
            self.iface.messageBar().pushMessage("IsoRange:   ",
                                                msg,
                                                QgsMessageBar.INFO, 3)

            canvas.refresh() 
