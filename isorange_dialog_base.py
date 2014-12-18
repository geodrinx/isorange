# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'isorange_dialog_base.ui'
#
# Created: Thu Dec 11 22:27:48 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ecofocusareaDialogBase(object):
    def setupUi(self, ecofocusareaDialogBase):
        ecofocusareaDialogBase.setObjectName(_fromUtf8("ecofocusareaDialogBase"))
        ecofocusareaDialogBase.resize(287, 121)
        self.button_box = QtGui.QDialogButtonBox(ecofocusareaDialogBase)
        self.button_box.setGeometry(QtCore.QRect(100, 80, 171, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.edit_distanza = QtGui.QLineEdit(ecofocusareaDialogBase)
        self.edit_distanza.setGeometry(QtCore.QRect(150, 20, 121, 20))
        self.edit_distanza.setObjectName(_fromUtf8("edit_distanza"))
        self.label = QtGui.QLabel(ecofocusareaDialogBase)
        self.label.setGeometry(QtCore.QRect(10, 20, 131, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.checkBox_MostraTriangoliEsterni = QtGui.QCheckBox(ecofocusareaDialogBase)
        self.checkBox_MostraTriangoliEsterni.setGeometry(QtCore.QRect(150, 50, 141, 18))
        self.checkBox_MostraTriangoliEsterni.setObjectName(_fromUtf8("checkBox_MostraTriangoliEsterni"))

        self.retranslateUi(ecofocusareaDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), ecofocusareaDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), ecofocusareaDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(ecofocusareaDialogBase)

    def retranslateUi(self, ecofocusareaDialogBase):
        ecofocusareaDialogBase.setWindowTitle(_translate("ecofocusareaDialogBase", "IsoRange", None))
        self.edit_distanza.setText(_translate("ecofocusareaDialogBase", "15.00", None))
        self.label.setText(_translate("ecofocusareaDialogBase", "Distanza dei punti in metri :", None))
        self.checkBox_MostraTriangoliEsterni.setText(_translate("ecofocusareaDialogBase", "Mostra Triangoli Esterni", None))

