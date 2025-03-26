from PyQt5.QtSerialPort import QSerialPort

ser = QSerialPort()
ser.setPortName('com3')
ser.isOpen()
