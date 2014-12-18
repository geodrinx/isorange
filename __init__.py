# -*- coding: utf-8 -*-
"""
/***************************************************************************
 isorange
                                 A QGIS plugin
  isorange
                             -------------------
        begin                : 2014-12-11
        copyright            : (C) 2014 by geodrinx
        email                : geodrinx@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load isorange class from file isorange.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .isorange import isorange
    return isorange(iface)
