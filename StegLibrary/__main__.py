# Builtin modules
from os import path, getcwd
from sys import stdout as std

# Internal modules
from StegLibrary.helper import err_imp, raw_open, open_image
from StegLibrary.core import SteganographyConfig as Config
from StegLibrary.core.steg import write_steg, extract_steg
from StegLibrary.gui import execute_gui

# Non-builtin modules
try:
    import click
except ImportError:
    err_imp("click")
    exit(1)


@click.group()
def steg():
    pass


@steg.command(
    "create",
    help="Create steganograph"
)
@click.option(
    "-i",
    "--image",
    help="Path to custom image file",
    type=click.Path(True, True, False),
    required=True
)
@click.option(
    "-k",
    "--key",
    help="The authentication key",
    type=str,
    default=Config.default_auth_key
)
@click.option(
    "-c",
    "--compress",
    help="Compression level of the steganograph",
    type=int,
    default=Config.default_compression
)
@click.option(
    "-p",
    "--pack",
    help="Density of the steganograph (from 1 to 3)",
    type=int,
    default=Config.default_density
)
@click.option(
    "-o",
    "--output",
    help="Path to output file",
    type=click.Path(False)
)
@click.option(
    "--showim",
    help="Whether to show image on creation",
    type=bool,
    default=False,
)
@click.argument("data", type=click.Path(True, True, False), required=True)
def create(
    image: str,
    key: str,
    compress: int,
    pack: int,
    output: str,
    showim: bool,
    data: str
):
    if pack not in Config.available_density:
        raise click.exceptions.BadOptionUsage(
            "pack", "Density must be from 1 to 3!")

    if not path.isabs(image):
        # Get the absolute path for the user-specified image
        image = path.join(getcwd(), *path.split(image))

    if not path.isabs(data):
        # Get the absolute path for the user-specified data file
        data = path.join(getcwd(), *path.split(data))

    if output is None:
        # Get the absolute path for the default output file
        # Default is the name of data file, change extension to .png
        name_no_ext = path.splitext(data)[0]
        output = name_no_ext + ".png"
    elif not path.isabs(output):
        # Get the absolute path for the user-specified output file
        output = path.join(getcwd(), *path.split(output))

    # Attempt to read files
    try:
        image_fileobject = raw_open(image)
    except IOError:
        raise click.FileError(image)
    try:
        data_fileobject = raw_open(data)
    except IOError:
        raise click.FileError(data)
    try:
        output_fileobject = raw_open(output, "wb")
    except IOError:
        raise click.FileError(output)

    # Perform operation
    write_steg(
        data_fileobject,
        open_image(image_fileobject),
        output_fileobject,
        auth_key=key,
        compression=compress,
        density=pack,
        show_image_on_completion=showim,
    )


@steg.command(
    "extract",
    help="Extract steganograph",
)
@click.option(
    "-k",
    "--key",
    help="The authentication key",
    type=str,
    default=Config.default_auth_key,
)
@click.option(
    "-o",
    "--output",
    help="Path to output file",
    type=click.Path(False)
)
@click.option(
    "-s",
    "--stdout",
    help="Additionally output to stdout",
    type=bool,
    default=False
)
@click.argument(
    "steganograph",
    required=True,
    type=click.Path(True, True, False)
)
def extract(key: str, output: str, stdout: bool, steganograph: str):
    if not path.isabs(steganograph):
        # Get the absolute path for the steganograph
        steganograph = path.join(getcwd(), *path.split(steganograph))

    if output is None:
        # Get the absolute path of the default output file
        # Default is the name of the steganograph, extension-stripped
        output = path.splitext(steganograph)[0]

    # Attempt to read files
    try:
        steganograph_fileobject = raw_open(steganograph)
    except IOError:
        raise click.FileError(steganograph)
    try:
        output_fileobject = raw_open(output)
    except IOError:
        raise click.FileError(output)

    # Compile output files
    output_object = [output_fileobject]
    if stdout:
        output_object.append(std)

    extract_steg(
        steganograph_fileobject,
        output_object,
        auth_key=key,
    )


@steg.command(
    "gui",
    help="Run the Graphical User Interface"
)
def gui():
    execute_gui()


if __name__ == "__main__":
    import sys
    sys.argv[0] = "StegLibrary"
    steg()
