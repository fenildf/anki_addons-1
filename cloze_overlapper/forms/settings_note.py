# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/settings_note.ui'
#
# Created: Tue Mar  7 19:13:45 2017
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(390, 210)
        Dialog.setMinimumSize(QtCore.QSize(390, 210))
        Dialog.setMaximumSize(QtCore.QSize(390, 210))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 176, 371, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 371, 158))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout_1 = QtGui.QGridLayout()
        self.gridLayout_1.setContentsMargins(0, -1, 0, -1)
        self.gridLayout_1.setObjectName(_fromUtf8("gridLayout_1"))
        self.label_4 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_1.addWidget(self.label_4, 1, 2, 1, 1)
        self.sb_before = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.sb_before.setMinimum(-1)
        self.sb_before.setObjectName(_fromUtf8("sb_before"))
        self.gridLayout_1.addWidget(self.sb_before, 2, 0, 1, 1)
        self.sb_cloze = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.sb_cloze.setMinimum(1)
        self.sb_cloze.setObjectName(_fromUtf8("sb_cloze"))
        self.gridLayout_1.addWidget(self.sb_cloze, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_1.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_1.addWidget(self.label_3, 1, 1, 1, 1)
        self.sb_after = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.sb_after.setMinimum(-1)
        self.sb_after.setObjectName(_fromUtf8("sb_after"))
        self.gridLayout_1.addWidget(self.sb_after, 2, 2, 1, 1)
        self.label_1 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.gridLayout_1.addWidget(self.label_1, 0, 0, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout_1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setContentsMargins(0, -1, 0, -1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.cb_ncf = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.cb_ncf.setObjectName(_fromUtf8("cb_ncf"))
        self.gridLayout_2.addWidget(self.cb_ncf, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 2)
        self.cb_ncl = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.cb_ncl.setObjectName(_fromUtf8("cb_ncl"))
        self.gridLayout_2.addWidget(self.cb_ncl, 2, 0, 1, 1)
        self.cb_incr = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.cb_incr.setObjectName(_fromUtf8("cb_incr"))
        self.gridLayout_2.addWidget(self.cb_incr, 1, 1, 1, 1)
        self.cb_gfc = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.cb_gfc.setObjectName(_fromUtf8("cb_gfc"))
        self.gridLayout_2.addWidget(self.cb_gfc, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.sb_before, self.sb_cloze)
        Dialog.setTabOrder(self.sb_cloze, self.sb_after)
        Dialog.setTabOrder(self.sb_after, self.cb_ncf)
        Dialog.setTabOrder(self.cb_ncf, self.cb_ncl)
        Dialog.setTabOrder(self.cb_ncl, self.cb_incr)
        Dialog.setTabOrder(self.cb_incr, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Overlapping Cloze Note Settings", None))
        self.label_4.setText(_translate("Dialog", "Context After", None))
        self.sb_before.setToolTip(_translate("Dialog", "Number of context cues before the prompt.<br>Set to -1/\'all\' to show all previous items as context", None))
        self.sb_before.setSpecialValueText(_translate("Dialog", "all", None))
        self.sb_cloze.setToolTip(_translate("Dialog", "Number of items to prompt for per card", None))
        self.label_2.setText(_translate("Dialog", "Context Before", None))
        self.label_3.setText(_translate("Dialog", "Cloze Prompts", None))
        self.sb_after.setToolTip(_translate("Dialog", "Number of context cues after the prompt.<br>Set to -1/\'all\' to show all following items as context", None))
        self.sb_after.setSpecialValueText(_translate("Dialog", "all", None))
        self.label_1.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Context Cues and Prompts</span></p></body></html>", None))
        self.cb_ncf.setToolTip(_translate("Dialog", "Don\'t provide any context cues for first cloze item", None))
        self.cb_ncf.setText(_translate("Dialog", "No cues for first item", None))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Other Cloze Generation Options</span></p></body></html>", None))
        self.cb_ncl.setToolTip(_translate("Dialog", "Don\'t provide any context cues for last cloze item", None))
        self.cb_ncl.setText(_translate("Dialog", "No cues for last item", None))
        self.cb_incr.setToolTip(_translate("Dialog", "For notes that have multiple clozes revealed per card,<br>gradually build up to full reveal count at the start,<br>and vice-versa in the end", None))
        self.cb_incr.setText(_translate("Dialog", "Gradual build-up/-down", None))
        self.cb_gfc.setToolTip(_translate("Dialog", "Don\'t provide any context cues for first cloze item", None))
        self.cb_gfc.setText(_translate("Dialog", "Don\'t generate full cloze", None))

