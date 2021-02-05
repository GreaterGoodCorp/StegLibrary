
# Builtin modules
from os import path, getcwd

# Internal modules
from StegLibrary import write_steg, extract_steg
from StegLibrary.header import Header
from StegLibrary.helper import err_imp
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


@steg.command("create", help="Create steganograph")
@click.option("-i", "--image", help="Path to custom image file", type=click.Path(True, True, False), required=True)
@click.option("-k", "--key", help="The authentication key", type=str, default=Header.default_key)
@click.option("-c", "--compress", help="Compression level of the steganograph", type=int, default=9)
@click.option("-p", "--pack", help="Density of the steganograph (from 1 to 3)", type=int, default=1)
@click.option("-o", "--output", help="Path to output file", type=click.Path(False))
@click.argument("data", type=click.Path(True, True, False), required=True)
def create(image: str, key: str, compress: int, pack: int, output: str, data: str):
    if pack not in Header.available_density:
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

    write_steg(data, image, key, compress, pack, output)


@steg.command("extract", help="Extract steganograph")
@click.option("-k", "--key", help="The authentication key", type=str, default=Header.default_key)
@click.option("-o", "--output", help="Path to output file", type=click.Path(False))
@click.option("-s", "--stdout", help="Additionally output to stdout", type=bool, default=False)
@click.argument("steganograph", required=True, type=click.Path(True, True, False))
def extract(key: str, output: str, stdout: bool, steganograph: str):
    if not path.isabs(steganograph):
        # Get the absolute path for the steganograph
        steganograph = path.join(getcwd(), *path.split(steganograph))

    if output is None:
        # Get the absolute path of the default output file
        # Default is the name of the steganograph, extension-stripped
        output = path.splitext(steganograph)[0]

    extract_steg(steganograph, output, key, stdout)


@steg.command("gui", help="Run the Graphical User Interface")
def gui():
    execute_gui()


if __name__ == "__main__":
    import sys
    sys.argv[0] = "StegLibrary"
    steg()
