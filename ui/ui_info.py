
################################################################################
## Form generated from reading UI file 'info.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QLocale, QMetaObject, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem, QTextBrowser, QVBoxLayout


class Ui_info:
    def setupUi(self, info):
        if not info.objectName():
            info.setObjectName("info")
        info.resize(658, 858)
        icon = QIcon()
        icon.addFile(":/icons/icons/icons8-info-64.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        info.setWindowIcon(icon)
        info.setLocale(QLocale(QLocale.Swedish, QLocale.Sweden))
        self.verticalLayout = QVBoxLayout(info)
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.textBrowser = QTextBrowser(info)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setFrameShape(QFrame.Shape.NoFrame)
        self.textBrowser.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.textBrowser)

        self.frame = QFrame(info)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        icon1 = QIcon()
        icon1.addFile(":/icons/left.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(info)

        QMetaObject.connectSlotsByName(info)
    # setupUi

    def retranslateUi(self, info):
        info.setWindowTitle(QCoreApplication.translate("info", "Info", None))
        self.textBrowser.setHtml(QCoreApplication.translate("", None))
        self.pushButton.setText(QCoreApplication.translate("info", "Back", None))
    # retranslateUi
