# Form implementation generated from reading ui file 'services_page.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1030, 750)
        Widget.setMinimumSize(QtCore.QSize(1030, 750))
        self.gridLayout = QtWidgets.QGridLayout(Widget)
        self.gridLayout.setObjectName("gridLayout")
        self.services_list_label_and_actions_frame = QtWidgets.QFrame(parent=Widget)
        self.services_list_label_and_actions_frame.setMinimumSize(QtCore.QSize(0, 50))
        self.services_list_label_and_actions_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.services_list_label_and_actions_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.services_list_label_and_actions_frame.setObjectName("services_list_label_and_actions_frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.services_list_label_and_actions_frame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.sort_by_combobox = QtWidgets.QComboBox(parent=self.services_list_label_and_actions_frame)
        self.sort_by_combobox.setMinimumSize(QtCore.QSize(125, 30))
        self.sort_by_combobox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.sort_by_combobox.setObjectName("sort_by_combobox")
        self.sort_by_combobox.addItem("")
        self.sort_by_combobox.addItem("")
        self.gridLayout_4.addWidget(self.sort_by_combobox, 1, 1, 1, 1)
        self.services_list_label = QtWidgets.QLabel(parent=self.services_list_label_and_actions_frame)
        self.services_list_label.setMinimumSize(QtCore.QSize(250, 0))
        self.services_list_label.setObjectName("services_list_label")
        self.gridLayout_4.addWidget(self.services_list_label, 1, 0, 1, 1)
        self.sort_type_combobox = QtWidgets.QComboBox(parent=self.services_list_label_and_actions_frame)
        self.sort_type_combobox.setMinimumSize(QtCore.QSize(125, 30))
        self.sort_type_combobox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.sort_type_combobox.setObjectName("sort_type_combobox")
        self.sort_type_combobox.addItem("")
        self.sort_type_combobox.addItem("")
        self.gridLayout_4.addWidget(self.sort_type_combobox, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 1, 3, 1, 1)
        self.add_service_button = QtWidgets.QPushButton(parent=self.services_list_label_and_actions_frame)
        self.add_service_button.setMinimumSize(QtCore.QSize(125, 30))
        self.add_service_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.add_service_button.setObjectName("add_service_button")
        self.gridLayout_4.addWidget(self.add_service_button, 1, 4, 1, 1)
        self.gridLayout.addWidget(self.services_list_label_and_actions_frame, 1, 0, 1, 1)
        self.search_bar_frame = QtWidgets.QFrame(parent=Widget)
        self.search_bar_frame.setMinimumSize(QtCore.QSize(0, 50))
        self.search_bar_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.search_bar_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.search_bar_frame.setObjectName("search_bar_frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.search_bar_frame)
        self.gridLayout_3.setContentsMargins(0, -1, 0, -1)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 0, 1, 1)
        self.search_lineedit = QtWidgets.QLineEdit(parent=self.search_bar_frame)
        self.search_lineedit.setMinimumSize(QtCore.QSize(425, 50))
        self.search_lineedit.setReadOnly(False)
        self.search_lineedit.setObjectName("search_lineedit")
        self.gridLayout_3.addWidget(self.search_lineedit, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.search_bar_frame, 0, 0, 1, 1)
        self.service_table_view_frame = QtWidgets.QFrame(parent=Widget)
        self.service_table_view_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.service_table_view_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.service_table_view_frame.setObjectName("service_table_view_frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.service_table_view_frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.services_table_view = QtWidgets.QTableView(parent=self.service_table_view_frame)
        self.services_table_view.setShowGrid(False)
        self.services_table_view.setObjectName("services_table_view")
        self.services_table_view.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.services_table_view, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.service_table_view_frame, 2, 0, 1, 1)
        self.page_buttons_frame = QtWidgets.QFrame(parent=Widget)
        self.page_buttons_frame.setMinimumSize(QtCore.QSize(0, 50))
        self.page_buttons_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.page_buttons_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.page_buttons_frame.setObjectName("page_buttons_frame")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.page_buttons_frame)
        self.gridLayout_5.setObjectName("gridLayout_5")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_5.addItem(spacerItem3, 0, 0, 1, 1)
        self.next_page_button = QtWidgets.QPushButton(parent=self.page_buttons_frame)
        self.next_page_button.setMinimumSize(QtCore.QSize(120, 30))
        self.next_page_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.next_page_button.setObjectName("next_page_button")
        self.gridLayout_5.addWidget(self.next_page_button, 0, 2, 1, 1)
        self.previous_page_button = QtWidgets.QPushButton(parent=self.page_buttons_frame)
        self.previous_page_button.setMinimumSize(QtCore.QSize(120, 30))
        self.previous_page_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.previous_page_button.setObjectName("previous_page_button")
        self.gridLayout_5.addWidget(self.previous_page_button, 0, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_5.addItem(spacerItem4, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.page_buttons_frame, 3, 0, 1, 1)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Form"))
        self.sort_by_combobox.setItemText(0, _translate("Widget", "Sort by Service Name"))
        self.sort_by_combobox.setItemText(1, _translate("Widget", "Sort by Rate"))
        self.services_list_label.setText(_translate("Widget", "Services List"))
        self.sort_type_combobox.setItemText(0, _translate("Widget", "Ascending"))
        self.sort_type_combobox.setItemText(1, _translate("Widget", "Descending"))
        self.add_service_button.setText(_translate("Widget", "Add Service"))
        self.search_lineedit.setPlaceholderText(_translate("Widget", "Search"))
        self.next_page_button.setText(_translate("Widget", "Next Page"))
        self.previous_page_button.setText(_translate("Widget", "Previous Page"))
