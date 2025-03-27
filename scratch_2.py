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
win = pg.GraphicsLayoutWidget(show=True, title="pcolormesh with PyQtGraph")
plot = win.addPlot(title="pcolormesh-like Plot")

# Create an ImageItem and set data
img_item = pg.ImageItem(Z.T)
plot.addItem(img_item)

# Define the transformation to map pixel coordinates to data coordinates
x_scale = (x[-1] - x[0]) / (Z.shape[1] - 1)
y_scale = (y[-1] - y[0]) / (Z.shape[0] - 1)
img_item.setRect(x[0], y[0], x_scale * Z.shape[1], y_scale * Z.shape[0])

# ✅ Add grid and labels
plot.showGrid(x=True, y=True, alpha=0.5)  # alpha controls grid transparency
plot.setLabel("left", "Y-axis")
plot.setLabel("bottom", "X-axis")

# Add colorbar
# hist = pg.HistogramLUTItem(image=img_item)
# win.addItem(hist)

sys.exit(app.exec_())
