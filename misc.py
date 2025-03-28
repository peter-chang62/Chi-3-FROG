import pyqtgraph as pg


class ImageView(pg.ImageView):
    """
    it's hard to change the viewbox after the fact so i just want to have an
    imageview item that's initialized with imageview(plot_item)
    """

    def __init__(self, *args, **kwargs):
        self.plot_item = pg.PlotItem()
        # plot_item.setLabel("left", "Y-axis")
        # plot_item.setLabel("bottom", "X-axis")

        super().__init__(view=self.plot_item)

        self.ui.histogram.hide()
        self.ui.menuBtn.hide()
