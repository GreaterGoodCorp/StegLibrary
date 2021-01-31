from StegLibrary.errors import HeaderError, ImageFileValidationError
from StegLibrary.gui import Ui_MainWindow
from StegLibrary import Header
import StegLibrary.steglib as steg
import sys
import webbrowser
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.register_logic()

    def register_logic(self):
        # Add function for Close button
        self.action_close.triggered.connect(self.close)

        # Add function for Help button
        self.action_help.triggered.connect(lambda: webbrowser.open(
            "https://github.com/MunchDev/StegLibrary"
        ))

        # Add function for Select (Input) button
        self.button_input.clicked.connect(self.select_input)

        # Add function for Select (Image) button
        self.button_image.clicked.connect(self.select_image)
        pass

    def select_input(self):
        # Ask user to choose a file
        file_name = QtWidgets.QFileDialog.getOpenFileName()[0]

        # If the user does not select any file
        # exit the routine
        if file_name is None or len(file_name) == 0:
            return

        # Display text output
        self.write_output("File selected at: " + file_name)

        # Show the path to file
        self.field_input.setText(file_name)

        # Set correspongding status and text colours depending
        # on if it is a steganograph
        try:
            header = steg.extract_steg(file_name, "", "", False, True)
            self.write_output("File selected is a valid steganograph. Creation disabled!")
            # Set text on label
            self.label_input_status.setText("Valid steganograph")
            # Set colour label
            self.label_input_status.setStyleSheet("QLabel { color : green; }")
            # Disable field_image, button_image and check_showim
            self.field_image.setDisabled(1)
            self.button_image.setDisabled(1)
            self.check_showim.setDisabled(1)
            # Display compression and density
            self.spin_compress.setValue(header["compression"])
            self.spin_compress.setDisabled(1)
            self.spin_density.setValue(header["density"])
            self.spin_density.setDisabled(1)
            self.write_output("Steganograph is ready for extraction!")
        except:
            # If it is a normal file
            self.write_output("File selected is not a steganograph. Extraction disabled!")
            # Set text on label
            self.label_input_status.setText("Valid file")
            # Set colour label
            self.label_input_status.setStyleSheet("QLabel { color : green; }")
            # Set status
            # Disable params check
            self.check_nowrite.setDisabled(1)
            self.check_stdout.setDisabled(1)
            self.write_output("File is ready for creation!")


    def select_image(self):
        # Ask user to choose a file
        file_name = QtWidgets.QFileDialog.getOpenFileName()[0]

        # If the user does not select any file
        # exit the routine
        if file_name is None or len(file_name) == 0:
            return

        # Display text output
        self.write_output("Image selected at: " + file_name)

        # Show the path to file
        self.field_image.setText(file_name)

        # Validate image
        try:
            steg.validate_image_file(file_name)
        except ImageFileValidationError as e:
            self.label_image_status.setText("Invalid image")
            self.label_image_status.setStyleSheet("QLabel { color: red; }")
            self.write_output(str(e))
        else:
            self.write_output("")


    def write_output(self, msg: str):
        self.text_output.appendPlainText(msg)



def execute_gui():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
