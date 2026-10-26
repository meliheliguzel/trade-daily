# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'accounts_set.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import rc_icons

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(255, 290)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.lineEdit_name = QLineEdit(Form)
        self.lineEdit_name.setObjectName(u"lineEdit_name")
        self.lineEdit_name.setFont(font)
        self.lineEdit_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.lineEdit_name)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.pushButton_create = QPushButton(Form)
        self.pushButton_create.setObjectName(u"pushButton_create")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_create.sizePolicy().hasHeightForWidth())
        self.pushButton_create.setSizePolicy(sizePolicy)
        self.pushButton_create.setFont(font)
        icon = QIcon()
        icon.addFile(u":/icons/add-user.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_create.setIcon(icon)

        self.verticalLayout.addWidget(self.pushButton_create)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"New account create", None))
        self.label.setText(QCoreApplication.translate("Form", u"Accounts name", None))
        self.lineEdit_name.setInputMask("")
        self.lineEdit_name.setPlaceholderText(QCoreApplication.translate("Form", u"name...", None))
        self.pushButton_create.setText(QCoreApplication.translate("Form", u"Create", None))
    # retranslateUi

