# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/peterchang/Github/Chi-3-FROG/qt_designer/form.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1197, 992)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(912, 708))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_spectrometer = QtWidgets.QWidget()
        self.tab_spectrometer.setObjectName("tab_spectrometer")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_spectrometer)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.tab_spectrometer)
        self.groupBox.setMinimumSize(QtCore.QSize(377, 664))
        self.groupBox.setMaximumSize(QtCore.QSize(377, 664))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_6.addItem(spacerItem)
        self.pb_spectrometer = QtWidgets.QPushButton(self.groupBox)
        self.pb_spectrometer.setObjectName("pb_spectrometer")
        self.horizontalLayout_6.addWidget(self.pb_spectrometer)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.groupBox1 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pb_step_back = QtWidgets.QPushButton(self.groupBox1)
        self.pb_step_back.setObjectName("pb_step_back")
        self.gridLayout_2.addWidget(self.pb_step_back, 0, 0, 1, 1)
        self.pb_step_forward = QtWidgets.QPushButton(self.groupBox1)
        self.pb_step_forward.setObjectName("pb_step_forward")
        self.gridLayout_2.addWidget(self.pb_step_forward, 0, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.le_step_fs = QtWidgets.QLineEdit(self.groupBox1)
        self.le_step_fs.setMinimumSize(QtCore.QSize(139, 21))
        self.le_step_fs.setMaximumSize(QtCore.QSize(139, 21))
        self.le_step_fs.setObjectName("le_step_fs")
        self.horizontalLayout_4.addWidget(self.le_step_fs)
        self.label_5 = QtWidgets.QLabel(self.groupBox1)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 0, 1, 2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.le_step_um = QtWidgets.QLineEdit(self.groupBox1)
        self.le_step_um.setMinimumSize(QtCore.QSize(139, 21))
        self.le_step_um.setMaximumSize(QtCore.QSize(139, 21))
        self.le_step_um.setObjectName("le_step_um")
        self.horizontalLayout_5.addWidget(self.le_step_um)
        self.label_6 = QtWidgets.QLabel(self.groupBox1)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 2, 0, 1, 2)
        self.verticalLayout_4.addWidget(self.groupBox1)
        self.groupBox2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox2.setMinimumSize(QtCore.QSize(286, 155))
        self.groupBox2.setMaximumSize(QtCore.QSize(286, 155))
        self.groupBox2.setObjectName("groupBox2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 0, 0, 1, 1)
        self.pb_home = QtWidgets.QPushButton(self.groupBox2)
        self.pb_home.setObjectName("pb_home")
        self.gridLayout_3.addWidget(self.pb_home, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 0, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(28, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem4, 1, 0, 1, 1)
        self.pb_absolute_move = QtWidgets.QPushButton(self.groupBox2)
        self.pb_absolute_move.setObjectName("pb_absolute_move")
        self.gridLayout_3.addWidget(self.pb_absolute_move, 1, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem5, 1, 2, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.le_target_pos_fs = QtWidgets.QLineEdit(self.groupBox2)
        self.le_target_pos_fs.setMinimumSize(QtCore.QSize(125, 21))
        self.le_target_pos_fs.setMaximumSize(QtCore.QSize(125, 21))
        self.le_target_pos_fs.setObjectName("le_target_pos_fs")
        self.horizontalLayout_7.addWidget(self.le_target_pos_fs)
        self.label_7 = QtWidgets.QLabel(self.groupBox2)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_7.addWidget(self.label_7)
        self.gridLayout_3.addLayout(self.horizontalLayout_7, 2, 0, 1, 3)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.le_target_pos_um = QtWidgets.QLineEdit(self.groupBox2)
        self.le_target_pos_um.setMinimumSize(QtCore.QSize(125, 21))
        self.le_target_pos_um.setMaximumSize(QtCore.QSize(125, 21))
        self.le_target_pos_um.setObjectName("le_target_pos_um")
        self.horizontalLayout_8.addWidget(self.le_target_pos_um)
        self.label_8 = QtWidgets.QLabel(self.groupBox2)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_8.addWidget(self.label_8)
        self.gridLayout_3.addLayout(self.horizontalLayout_8, 3, 0, 1, 3)
        self.verticalLayout_4.addWidget(self.groupBox2)
        self.groupBox3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox3.setObjectName("groupBox3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.lcd_current_pos_um = QtWidgets.QLCDNumber(self.groupBox3)
        self.lcd_current_pos_um.setMinimumSize(QtCore.QSize(151, 31))
        self.lcd_current_pos_um.setSmallDecimalPoint(False)
        self.lcd_current_pos_um.setObjectName("lcd_current_pos_um")
        self.horizontalLayout_9.addWidget(self.lcd_current_pos_um)
        self.label_18 = QtWidgets.QLabel(self.groupBox3)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_9.addWidget(self.label_18)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.lcd_current_pos_fs = QtWidgets.QLCDNumber(self.groupBox3)
        self.lcd_current_pos_fs.setMinimumSize(QtCore.QSize(151, 31))
        self.lcd_current_pos_fs.setSmallDecimalPoint(False)
        self.lcd_current_pos_fs.setObjectName("lcd_current_pos_fs")
        self.horizontalLayout_10.addWidget(self.lcd_current_pos_fs)
        self.label_19 = QtWidgets.QLabel(self.groupBox3)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_10.addWidget(self.label_19)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_11.addItem(spacerItem6)
        self.pb_set_t0 = QtWidgets.QPushButton(self.groupBox3)
        self.pb_set_t0.setObjectName("pb_set_t0")
        self.horizontalLayout_11.addWidget(self.pb_set_t0)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_11.addItem(spacerItem7)
        self.verticalLayout_3.addLayout(self.horizontalLayout_11)
        self.verticalLayout_4.addWidget(self.groupBox3)
        self.frame = QtWidgets.QFrame(self.groupBox)
        self.frame.setMinimumSize(QtCore.QSize(347, 115))
        self.frame.setMaximumSize(QtCore.QSize(347, 115))
        self.frame.setObjectName("frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_23 = QtWidgets.QLabel(self.frame)
        self.label_23.setObjectName("label_23")
        self.gridLayout_4.addWidget(self.label_23, 0, 0, 1, 1)
        self.le_stage_com_port = QtWidgets.QLineEdit(self.frame)
        self.le_stage_com_port.setObjectName("le_stage_com_port")
        self.gridLayout_4.addWidget(self.le_stage_com_port, 0, 1, 2, 1)
        self.pb_initialize_hardware = QtWidgets.QPushButton(self.frame)
        self.pb_initialize_hardware.setObjectName("pb_initialize_hardware")
        self.gridLayout_4.addWidget(self.pb_initialize_hardware, 1, 0, 2, 1)
        self.tb_error = QtWidgets.QTextBrowser(self.frame)
        self.tb_error.setMaximumSize(QtCore.QSize(165, 51))
        self.tb_error.setObjectName("tb_error")
        self.gridLayout_4.addWidget(self.tb_error, 2, 1, 1, 1)
        self.verticalLayout_4.addWidget(self.frame)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox4 = QtWidgets.QGroupBox(self.tab_spectrometer)
        self.groupBox4.setMinimumSize(QtCore.QSize(501, 454))
        self.groupBox4.setObjectName("groupBox4")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox4)
        self.gridLayout.setObjectName("gridLayout")
        self.gv_spectrum = PlotWidget(self.groupBox4)
        self.gv_spectrum.setObjectName("gv_spectrum")
        self.gridLayout.addWidget(self.gv_spectrum, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox4)
        self.tabWidget.addTab(self.tab_spectrometer, "")
        self.tab_frog = QtWidgets.QWidget()
        self.tab_frog.setObjectName("tab_frog")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_frog)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.groupBox5 = QtWidgets.QGroupBox(self.tab_frog)
        self.groupBox5.setMinimumSize(QtCore.QSize(427, 253))
        self.groupBox5.setMaximumSize(QtCore.QSize(427, 253))
        self.groupBox5.setObjectName("groupBox5")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_10.addItem(spacerItem8, 0, 0, 1, 1)
        self.pb_save_frog = QtWidgets.QPushButton(self.groupBox5)
        self.pb_save_frog.setObjectName("pb_save_frog")
        self.gridLayout_10.addWidget(self.pb_save_frog, 0, 1, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_10.addItem(spacerItem9, 0, 2, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_10.addItem(spacerItem10, 1, 0, 1, 1)
        self.pb_frog = QtWidgets.QPushButton(self.groupBox5)
        self.pb_frog.setObjectName("pb_frog")
        self.gridLayout_10.addWidget(self.pb_frog, 1, 1, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_10.addItem(spacerItem11, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_10)
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.le_frog_start_fs = QtWidgets.QLineEdit(self.groupBox5)
        self.le_frog_start_fs.setObjectName("le_frog_start_fs")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.le_frog_start_fs)
        self.label_11 = QtWidgets.QLabel(self.groupBox5)
        self.label_11.setObjectName("label_11")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_11)
        self.le_frog_start_um = QtWidgets.QLineEdit(self.groupBox5)
        self.le_frog_start_um.setObjectName("le_frog_start_um")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.le_frog_start_um)
        self.label_10 = QtWidgets.QLabel(self.groupBox5)
        self.label_10.setObjectName("label_10")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_10)
        self.gridLayout_9.addLayout(self.formLayout_3, 0, 0, 1, 1)
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setObjectName("formLayout_4")
        self.le_frog_end_fs = QtWidgets.QLineEdit(self.groupBox5)
        self.le_frog_end_fs.setObjectName("le_frog_end_fs")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.le_frog_end_fs)
        self.label_12 = QtWidgets.QLabel(self.groupBox5)
        self.label_12.setObjectName("label_12")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_12)
        self.le_frog_end_um = QtWidgets.QLineEdit(self.groupBox5)
        self.le_frog_end_um.setObjectName("le_frog_end_um")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.le_frog_end_um)
        self.label_13 = QtWidgets.QLabel(self.groupBox5)
        self.label_13.setObjectName("label_13")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_13)
        self.gridLayout_9.addLayout(self.formLayout_4, 0, 1, 1, 1)
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setObjectName("formLayout_5")
        self.le_frog_step_fs = QtWidgets.QLineEdit(self.groupBox5)
        self.le_frog_step_fs.setObjectName("le_frog_step_fs")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.le_frog_step_fs)
        self.label_4 = QtWidgets.QLabel(self.groupBox5)
        self.label_4.setObjectName("label_4")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_4)
        self.le_frog_step_um = QtWidgets.QLineEdit(self.groupBox5)
        self.le_frog_step_um.setObjectName("le_frog_step_um")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.le_frog_step_um)
        self.label_9 = QtWidgets.QLabel(self.groupBox5)
        self.label_9.setObjectName("label_9")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_9)
        self.gridLayout_9.addLayout(self.formLayout_5, 1, 0, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_9.addItem(spacerItem12, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_9)
        self.progbar_frog = QtWidgets.QProgressBar(self.groupBox5)
        self.progbar_frog.setProperty("value", 24)
        self.progbar_frog.setObjectName("progbar_frog")
        self.verticalLayout.addWidget(self.progbar_frog)
        self.gridLayout_6.addWidget(self.groupBox5, 0, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_frog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gv_frog = GraphicsLayoutWidget(self.groupBox_3)
        self.gv_frog.setObjectName("gv_frog")
        self.verticalLayout_2.addWidget(self.gv_frog)
        self.gv_frog_autocorr = PlotWidget(self.groupBox_3)
        self.gv_frog_autocorr.setMaximumSize(QtCore.QSize(16777215, 200))
        self.gv_frog_autocorr.setObjectName("gv_frog_autocorr")
        self.verticalLayout_2.addWidget(self.gv_frog_autocorr)
        self.gridLayout_6.addWidget(self.groupBox_3, 0, 1, 3, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_frog)
        self.groupBox_5.setMaximumSize(QtCore.QSize(286, 132))
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.tb_frog_error = QtWidgets.QTextBrowser(self.groupBox_5)
        self.tb_frog_error.setObjectName("tb_frog_error")
        self.gridLayout_8.addWidget(self.tb_frog_error, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_5, 1, 0, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(20, 244, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem13, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab_frog, "")
        self.tab_settings = QtWidgets.QWidget()
        self.tab_settings.setObjectName("tab_settings")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.tab_settings)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_settings)
        self.groupBox_4.setMinimumSize(QtCore.QSize(342, 145))
        self.groupBox_4.setMaximumSize(QtCore.QSize(342, 145))
        self.groupBox_4.setObjectName("groupBox_4")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_4)
        self.formLayout.setObjectName("formLayout")
        self.le_integration_time = QtWidgets.QLineEdit(self.groupBox_4)
        self.le_integration_time.setObjectName("le_integration_time")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.le_integration_time)
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_3)
        self.le_n_avg = QtWidgets.QLineEdit(self.groupBox_4)
        self.le_n_avg.setObjectName("le_n_avg")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.le_n_avg)
        self.label_20 = QtWidgets.QLabel(self.groupBox_4)
        self.label_20.setObjectName("label_20")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_20)
        self.le_x_smooth = QtWidgets.QLineEdit(self.groupBox_4)
        self.le_x_smooth.setObjectName("le_x_smooth")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.le_x_smooth)
        self.label_21 = QtWidgets.QLabel(self.groupBox_4)
        self.label_21.setObjectName("label_21")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_21)
        self.le_x_timing = QtWidgets.QLineEdit(self.groupBox_4)
        self.le_x_timing.setObjectName("le_x_timing")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.le_x_timing)
        self.label_22 = QtWidgets.QLabel(self.groupBox_4)
        self.label_22.setObjectName("label_22")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_22)
        self.gridLayout_12.addWidget(self.groupBox_4, 0, 0, 2, 1)
        spacerItem14 = QtWidgets.QSpacerItem(769, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem14, 0, 1, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(20, 554, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem15, 1, 1, 3, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_settings)
        self.groupBox_2.setMinimumSize(QtCore.QSize(211, 131))
        self.groupBox_2.setMaximumSize(QtCore.QSize(211, 131))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.tb_settings_error = QtWidgets.QTextBrowser(self.groupBox_2)
        self.tb_settings_error.setObjectName("tb_settings_error")
        self.gridLayout_11.addWidget(self.tb_settings_error, 0, 0, 1, 1)
        self.gridLayout_12.addWidget(self.groupBox_2, 2, 0, 1, 1)
        spacerItem16 = QtWidgets.QSpacerItem(20, 554, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem16, 3, 0, 1, 1)
        self.tabWidget.addTab(self.tab_settings, "")
        self.gridLayout_13.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1197, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pb_spectrometer.setText(_translate("MainWindow", "spectrometer"))
        self.pb_step_back.setText(_translate("MainWindow", "step back"))
        self.pb_step_forward.setText(_translate("MainWindow", "step forward"))
        self.le_step_fs.setText(_translate("MainWindow", "5"))
        self.label_5.setText(_translate("MainWindow", "step (fs)"))
        self.label_6.setText(_translate("MainWindow", "step (um)"))
        self.pb_home.setText(_translate("MainWindow", "home stage"))
        self.pb_absolute_move.setText(_translate("MainWindow", "absolute move"))
        self.le_target_pos_fs.setText(_translate("MainWindow", "0"))
        self.label_7.setText(_translate("MainWindow", "target position (fs)"))
        self.label_8.setText(_translate("MainWindow", "target position (um)"))
        self.label_18.setText(_translate("MainWindow", "current position (um)"))
        self.label_19.setText(_translate("MainWindow", "current position (fs)"))
        self.pb_set_t0.setText(_translate("MainWindow", "set T0"))
        self.label_23.setText(_translate("MainWindow", "Zaber Stage Com Port"))
        self.le_stage_com_port.setText(_translate("MainWindow", "COM3"))
        self.pb_initialize_hardware.setText(_translate("MainWindow", "initialize hardware"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_spectrometer), _translate("MainWindow", "Spectrometer"))
        self.pb_save_frog.setText(_translate("MainWindow", "Save"))
        self.pb_frog.setText(_translate("MainWindow", "FROG"))
        self.le_frog_start_fs.setText(_translate("MainWindow", "-1000"))
        self.label_11.setText(_translate("MainWindow", "start (fs)"))
        self.label_10.setText(_translate("MainWindow", "start (um)"))
        self.le_frog_end_fs.setText(_translate("MainWindow", "1000"))
        self.label_12.setText(_translate("MainWindow", "end (fs)"))
        self.label_13.setText(_translate("MainWindow", "end (um)"))
        self.le_frog_step_fs.setText(_translate("MainWindow", "5"))
        self.label_4.setText(_translate("MainWindow", "step (fs)"))
        self.label_9.setText(_translate("MainWindow", "step (um)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_frog), _translate("MainWindow", "FROG"))
        self.label_3.setText(_translate("MainWindow", "integration time (5 - 1000 ms)"))
        self.label_20.setText(_translate("MainWindow", "scans to average (1 - 1000)"))
        self.label_21.setText(_translate("MainWindow", "x smooth (0 - 4)"))
        self.label_22.setText(_translate("MainWindow", "x timing (1 - 3)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_settings), _translate("MainWindow", "Settings"))
from pyqtgraph import GraphicsLayoutWidget, PlotWidget
