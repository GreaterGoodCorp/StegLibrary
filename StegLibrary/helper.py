from StegLibrary import ANSIFormatter

print = ANSIFormatter.extendedPrint


def err_imp(pkg_name):
    s = f"[Package] This package is not installed: {pkg_name}"
    return print(s, ansi=ANSIFormatter.Red)
