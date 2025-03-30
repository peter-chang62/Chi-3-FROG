# from PyQt5.QtWidgets import QLineEdit
# from PyQt5.QtGui import QIntValidator
# from PyQt5.QtCore import Qt


# class RangeLineEdit(QLineEdit):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#     def set_range(self, min_value, max_value):
#         self.min_value = min_value
#         self.max_value = max_value
#         self.validator = QIntValidator(min_value, max_value)
#         self.setValidator(self.validator)

#     def keyPressEvent(self, event):
#         # Handle backspace and delete keys, which should always work
#         if event.key() in [
#             Qt.Key_Backspace,
#             Qt.Key_Delete,
#             Qt.Key_Left,
#             Qt.Key_Right,
#             Qt.Key_Up,
#             Qt.Key_Down,
#         ]:
#             super().keyPressEvent(event)
#             return

#         # Get the current input text and the new character
#         current_text = self.text()
#         new_text = current_text + event.text()

#         # Check if the new input is valid and within range
#         try:
#             value = float(new_text)
#             if self.min_value <= value <= self.max_value:
#                 super().keyPressEvent(event)  # Allow the key press event if valid
#         except ValueError:
#             # Ignore the event if the input is not a valid number (e.g., letters)
#             pass
