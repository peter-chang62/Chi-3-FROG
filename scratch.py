import sys
from PyQt5.QtCore import QObject, QThread, QTimer, pyqtSignal
from PyQt5.QtWidgets import QApplication


class Worker(QObject):
    number_signal = pyqtSignal(int)  # Signal to emit numbers
    finished = pyqtSignal()  # Signal to indicate work is done

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.max_count = 100  # Stop after 100 iterations

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.print_number)
        self.timer.start(100)  # 100 ms interval

    def print_number(self):
        self.counter += 1
        print(f"Number: {self.counter}")
        self.number_signal.emit(self.counter)

        # Stop the timer after 100 iterations
        if self.counter >= self.max_count:
            self.stop_timer()

    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            print("Stopping the timer after 100 iterations.")
            self.finished.emit()


class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # Create the thread and worker
        self.thread = QThread()
        self.worker = Worker()

        # Move the worker to the thread
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.worker.start_timer)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.app.quit)

        # Start the thread
        self.thread.start()

    def run(self):
        # Start the event loop
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
