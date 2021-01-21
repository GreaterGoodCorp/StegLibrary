from StegLibrary import write_steg, extract_steg, Header
import click
from click import echo

@click.group()
def steg():
    pass

@steg.command("create", help="Create stegnograph")
@click.option("-i", "--image", help="Path to custom image file", type=click.Path(True, True, False))
@click.option("-k", "--key", help="The authentication key", type=str, default=Header.default_key)
@click.option("-c", "--compress", help="Compression level of the stegnograph", type=int, default=9)
@click.option("-p", "--pack", help="Density of the stegnograph", type=click.Choice(["1", "2", "3"]), default="1")
@click.option("-o", "--output", help="Path to output file", type=click.Path(False))
@click.argument("data", type=click.Path(True, True, False))
def create(image, key, compress, pack, output, data):
    pack = int(pack)
    if image == None:
        image = "images/sample.png"
    if output == None:
        output = data + ".steg.png"
    write_steg(data, image, key, compress, pack, output)

@steg.command("extract", help="Extract stegnograph")
@click.option("-k", "--key", help="The authentication key", type=str, default=Header.default_key)
@click.option("-o", "--output", help="Path to output file", type=click.Path(False), required=True)
@click.argument("stegnograph", required=True, type=click.Path(True, True, False))
def extract(key, output, stegnograph):
    extract_steg(stegnograph, output, key)

if __name__ == "__main__":
    steg()