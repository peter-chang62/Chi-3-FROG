import sys
import numpy as np
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg

# Create sample data
x = np.linspace(0, 10, 100)  # 100 points along X
y = np.linspace(0, 5, 50)    # 50 points along Y
X, Y = np.meshgrid(x, y)

# Original Z data
Z = np.sin(X) * np.cos(Y)

app = QApplication(sys.argv)

# Create a PlotItem to hold the image and display axis ticks
plot_item = pg.PlotItem()
plot_item.setLabel("left", "Y-axis")
plot_item.setLabel("bottom", "X-axis")
# plot_item.showGrid(x=True, y=True)

# Create an ImageView and set the PlotItem
win = pg.ImageView(view=plot_item)

# Add ImageItem directly to PlotItem
img_item = pg.ImageItem(Z.T)  # Transpose Z to match PyQtGraph's orientation
plot_item.addItem(img_item)

# ✅ Auto-range to fit the image perfectly
plot_item.autoRange(padding=0)

# Hide the color bar
win.ui.histogram.hide()

# ✅ Hide only the Menu button
win.ui.menuBtn.hide()  # Hide Menu button
win.ui.roiBtn.hide()  # Hide Menu button
# ROI button remains visible

# Show the window
win.show()
sys.exit(app.exec_())
