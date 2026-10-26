# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'text_edit.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTextEdit,
    QVBoxLayout, QWidget)
import rc_icons

class Ui_text_edit(object):
    def setupUi(self, text_edit):
        if not text_edit.objectName():
            text_edit.setObjectName(u"text_edit")
        text_edit.resize(575, 451)
        icon = QIcon()
        icon.addFile(u":/icons/icons/edit.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        text_edit.setWindowIcon(icon)
        text_edit.setLocale(QLocale(QLocale.Swedish, QLocale.Sweden))
        self.verticalLayout = QVBoxLayout(text_edit)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_info = QLabel(text_edit)
        self.label_info.setObjectName(u"label_info")
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_info)

        self.frame_2 = QFrame(text_edit)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_link = QPushButton(self.frame_2)
        self.pushButton_link.setObjectName(u"pushButton_link")
        self.pushButton_link.setMaximumSize(QSize(128, 32))
        icon1 = QIcon()
        icon1.addFile(u":/icons/link.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_link.setIcon(icon1)
        self.pushButton_link.setIconSize(QSize(32, 32))
        self.pushButton_link.setCheckable(False)
        self.pushButton_link.setChecked(False)
        self.pushButton_link.setAutoRepeat(False)
        self.pushButton_link.setAutoExclusive(False)
        self.pushButton_link.setFlat(False)

        self.horizontalLayout_2.addWidget(self.pushButton_link)


        self.verticalLayout.addWidget(self.frame_2)

        self.textEdit = QTextEdit(text_edit)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setFrameShape(QFrame.Shape.NoFrame)
        self.textEdit.setTabChangesFocus(False)
        self.textEdit.setReadOnly(False)
        self.textEdit.setOverwriteMode(True)
        self.textEdit.setAcceptRichText(True)
        self.textEdit.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextEditable|Qt.TextInteractionFlag.TextEditorInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.textEdit)

        self.frame = QFrame(text_edit)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_ok = QPushButton(self.frame)
        self.pushButton_ok.setObjectName(u"pushButton_ok")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_ok.sizePolicy().hasHeightForWidth())
        self.pushButton_ok.setSizePolicy(sizePolicy)
        icon2 = QIcon()
        icon2.addFile(u":/icons/check.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_ok.setIcon(icon2)

        self.horizontalLayout.addWidget(self.pushButton_ok)

        self.pushButton_cancel = QPushButton(self.frame)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        sizePolicy.setHeightForWidth(self.pushButton_cancel.sizePolicy().hasHeightForWidth())
        self.pushButton_cancel.setSizePolicy(sizePolicy)
        icon3 = QIcon()
        icon3.addFile(u":/icons/left.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_cancel.setIcon(icon3)

        self.horizontalLayout.addWidget(self.pushButton_cancel)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(text_edit)

        self.pushButton_link.setDefault(False)


        QMetaObject.connectSlotsByName(text_edit)
    # setupUi

    def retranslateUi(self, text_edit):
        text_edit.setWindowTitle(QCoreApplication.translate("text_edit", u"Form", None))
        self.label_info.setText("")
        self.pushButton_link.setText(QCoreApplication.translate("text_edit", u"add link", None))
        self.pushButton_ok.setText(QCoreApplication.translate("text_edit", u"ok", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("text_edit", u"cancel", None))
    # retranslateUi

