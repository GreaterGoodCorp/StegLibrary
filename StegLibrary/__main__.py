from StegLibrary import write_steg, extract_steg, Header
import click


@click.group()
def steg():
    pass


@steg.command("create", help="Create steganograph")
@click.option("-i", "--image", help="Path to custom image file", type=click.Path(True, True, False))
@click.option("-k", "--key", help="The authentication key", type=str, default=Header.default_key)
@click.option("-c", "--compress", help="Compression level of the steganograph", type=int, default=9)
@click.option("-p", "--pack", help="Density of the steganograph", type=click.Choice(["1", "2", "3"]), default="1")
@click.option("-o", "--output", help="Path to output file", type=click.Path(False))
@click.argument("data", type=click.Path(True, True, False), required=True)
def create(image: str, key: str, compress: str, pack: str, output: str, data: str):
    pack = int(pack)
    if image == None:
        image = "images/sample.png"
    if output == None:
        output = data.find(".", -5)
        output = data[:output+1] + ".png"
    write_steg(data, image, key, compress, pack, output)


@steg.command("extract", help="Extract steganograph")
@click.option("-k", "--key", help="The authentication key", type=str, default=Header.default_key)
@click.option("-o", "--output", help="Path to output file (default is stdout)", type=click.Path(False))
@click.argument("steganograph", required=True, type=click.Path(True, True, False))
def extract(key: str, output: str, steganograph: str):
    output = output if output else "stdout"
    extract_steg(steganograph, output, key)


if __name__ == "__main__":
    steg()
