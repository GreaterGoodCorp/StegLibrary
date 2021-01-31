from StegLibrary.header import Header
from os import path

from StegLibrary.errors import SteganographyError, ImageFileValidationError
from StegLibrary.gui import Ui_MainWindow
import StegLibrary.steglib as steg
import sys
import webbrowser
from PIL import Image
from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.reset()
        self.register_logic()

    def reset(self):
        self.has_steg = False
        self.has_data = False
        self.has_image = False
        self.has_output = False

        self.input_file = ""
        self.output_file = ""
        self.image_file = ""

        self.field_input.setText("")
        self.label_input_status.setText("Select input file")
        self.label_input_status.setStyleSheet("")
        self.field_image.setText("")
        self.label_image_status.setText("Not available")
        self.label_image_status.setStyleSheet("")
        self.field_output.setText("")
        self.label_output_status.setText("Not available")
        self.label_output_status.setStyleSheet("")
        self.field_authkey.setText("")
        self.spin_compress.setValue(9)
        self.spin_density.setValue(1)

        self.check_nowrite.setChecked(0)
        self.check_showim.setChecked(0)
        self.check_stdout.setChecked(0)

        self.text_output.clear()

    def register_logic(self):
        # Add function for Close button
        self.action_close.triggered.connect(self.close)

        # Add function for Help button
        self.action_help.triggered.connect(
            lambda: webbrowser.open("https://github.com/MunchDev/StegLibrary"))

        # Add function for Select (Input) button
        self.button_input.clicked.connect(self.select_input)

        # Add function for Select (Image) button
        self.button_image.clicked.connect(self.select_image)

        # Add function for Select (Output) button
        self.button_output.clicked.connect(self.select_output)

        # Add function for Create button
        self.button_create.clicked.connect(self.create)

        # Add function for Extract button
        self.button_extract.clicked.connect(self.extract)

        # Add function for Clear all button
        self.button_clear.clicked.connect(self.reset)
        pass

    def select_input(self):
        # Empty all other arguments
        self.reset()

        # Ask user to choose a file
        self.input_file = QtWidgets.QFileDialog.getOpenFileName()[0]

        # If the user does not select any file
        # exit the routine
        if self.input_file is None or len(self.input_file) == 0:
            return

        # Display text output
        self.write_output("[User] File selected at: " + self.input_file)

        # Show the path to file
        self.field_input.setText(self.input_file)

        # Set correspongding status and text colours depending
        # on if it is a steganograph
        try:
            header = steg.extract_steg(self.input_file, "", "", False, True)
            self.write_output(
                "[System] File selected is a valid steganograph. Creation disabled!"
            )
            # Set text on label
            self.label_input_status.setText("Valid steganograph")
            # Set colour label
            self.label_input_status.setStyleSheet("QLabel { color : green; }")
            # Display compression and density
            self.spin_compress.setValue(header["compression"])
            self.spin_density.setValue(header["density"])
            # Enable widgets
            self.button_output.setEnabled(1)
            self.write_output("[System] Steganograph is ready for extraction!")

            self.has_steg = True
        except:
            # If it is a normal file
            self.write_output(
                "[System] File selected is not a steganograph. Extraction disabled!"
            )
            # Set text on label
            self.label_input_status.setText("Valid file")
            self.label_image_status.setText("Please select image")
            self.label_output_status.setText("Please select output fil")
            # Set colour label
            self.label_input_status.setStyleSheet("QLabel { color : green; }")
            # Enable widgets
            self.button_image.setEnabled(1)
            self.button_output.setEnabled(1)
            self.write_output("[System] File is ready for creation!")

            self.has_data = True
        self.enable_parametres()

    def select_image(self):
        # Ask user to choose a file
        self.image_file = QtWidgets.QFileDialog.getOpenFileName()[0]

        # If the user does not select any file
        # exit the routine
        if self.image_file is None or len(self.image_file) == 0:
            return

        # Display text output
        self.write_output("[User] Image selected at: " + self.image_file)

        # Show the path to file
        self.field_image.setText(self.image_file)

        # Validate image
        try:
            steg.validate_image_file(self.image_file)
        except ImageFileValidationError as e:
            self.label_image_status.setText("Invalid image")
            self.label_image_status.setStyleSheet("QLabel { color: red; }")
            self.write_output("[System] " + str(e))
            self.disable_parametres()
        else:
            self.label_image_status.setText("Valid image")
            self.label_image_status.setStyleSheet("QLabel { color: green; }")
            self.write_output("[System] The image file is valid!")

            self.has_image = True
            self.enable_parametres()

    def select_output(self):
        # Ask user to choose a directory
        self.output_file = QtWidgets.QFileDialog.getExistingDirectory()

        # If the user does not select any file
        # exit the routine
        if self.output_file is None or len(self.output_file) == 0:
            return

        # Display text output
        self.write_output("[User] Output folder selected at: " +
                          self.output_file)

        # Create default output file
        self.output_file = path.join(
            self.output_file,
            path.splitext(path.split(self.input_file)[-1])[0])

        # Add numbering in case file already exists
        ext = "" if self.has_steg else ".png"
        if not steg.check_file_availability(self.output_file + ext):
            i = 1
            while not steg.check_file_availability(self.output_file + f"_{i}" +
                                                   ext):
                i += 1
            self.output_file += f"_{i}" + ext
        else:
            self.output_file += ext

        self.write_output("[System] Default output filename is: " +
                          self.output_file)

        # Show the path to file
        self.field_output.setText(self.output_file)

        self.label_output_status.setText("Valid file")
        self.label_output_status.setStyleSheet("QLabel { color: green; }")
        self.has_output = True
        self.enable_parametres()

    def create(self):
        self.write_output("[User] Start creating steganograph...")

        pass

    def extract(self):
        self.write_output("[User] Start extracting steganograph...")
        pass

    def print_system_status(self):
        self.write_output(f"[System] Status report:")
        self.write_output(f"[System] Input file: {self.input_file}")
        if self.has_steg:
            self.write_output(f"[System] Image file: Not applicable")
        else:
            self.write_output(f"[System] Image file: {self.image_file}")
        self.write_output(f"[System] Output file: {self.input_file}")
        pass

    def enable_parametres(self):
        if self.has_steg and not self.has_output:
            return
        if not (self.has_steg or (self.has_image and self.has_output)):
            return

        self.write_output("[System] All files are valid!")

        if self.has_steg:
            self.field_authkey.setEnabled(1)
            self.check_stdout.setEnabled(1)
            self.check_nowrite.setEnabled(1)
            self.button_extract.setEnabled(1)

            self.write_output(
                "[System] Please enter the authentication key used during creation."
            )
            self.write_output(
                "[System] Please check the appropriate options and click 'Extract' to start."
            )
        else:
            self.field_authkey.setEnabled(1)
            self.spin_compress.setEnabled(1)
            self.spin_density.setEnabled(1)
            self.check_showim.setEnabled(1)
            self.button_create.setEnabled(1)

            self.write_output(
                "[System] Please enter the authentication key for creation.")
            self.write_output(
                "[System] The key is required to extract data from the steganograph later."
            )
            self.write_output(
                "[Systen] Please choose a compression level and density for creation."
            )
            self.write_output(
                "[System] Please check the appropriate options and click 'Create' to start."
            )

    def disable_parametres(self):
        self.field_authkey.setDisabled(1)
        self.spin_compress.setDisabled(1)
        self.spin_density.setDisabled(1)
        self.check_showim.setDisabled(1)
        self.check_stdout.setDisabled(1)
        self.check_nowrite.setDisabled(1)
        self.button_create.setDisabled(1)
        self.button_extract.setDisabled(1)

    def write_output(self, msg: str):
        self.text_output.appendPlainText(msg)


def execute_gui():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
