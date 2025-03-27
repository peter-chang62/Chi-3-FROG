import sys
import numpy as np
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg

# Create sample data
x = np.linspace(0, 10, 100)
y = np.linspace(0, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

app = QApplication(sys.argv)

# Create a PlotItem to hold the image and display axis ticks
plot_item = pg.PlotItem()
plot_item.setLabel('left', 'Y-axis')
plot_item.setLabel('bottom', 'X-axis')
plot_item.showGrid(x=True, y=True)

# Create an ImageView and set the PlotItem
win = pg.ImageView(view=plot_item)
win.setImage(Z.T, pos=[x[0], y[0]], scale=[(x[-1] - x[0]) / (len(x) - 1), (y[-1] - y[0]) / (len(y) - 1)])

# Show the window
win.show()
sys.exit(app.exec_())
