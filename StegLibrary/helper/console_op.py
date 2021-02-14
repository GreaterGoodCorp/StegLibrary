# Builtin modules
from re import match
from typing import Any


class ANSIFormatter:
    """
    ANSIFormatter provides all ANSI formatting options
    for supported platforms.
    """
    # ANSI colour template
    ColourTemplate: str = "\u001b[{}m"

    # ANSI default reset
    Reset: str = ColourTemplate.format(0)

    # 8 basic foreground colours
    Black: str = ColourTemplate.format("30")
    Red: str = ColourTemplate.format("31")
    Green: str = ColourTemplate.format("32")
    Yellow: str = ColourTemplate.format("33")
    Blue: str = ColourTemplate.format("34")
    Magenta: str = ColourTemplate.format("35")
    Cyan: str = ColourTemplate.format("36")
    White: str = ColourTemplate.format("37")

    # 8 bright colours
    BrightBlack: str = ColourTemplate.format("30;1")
    BrightRed: str = ColourTemplate.format("31;1")
    BrightGreen: str = ColourTemplate.format("32;1")
    BrightYellow: str = ColourTemplate.format("33;1")
    BrightBlue: str = ColourTemplate.format("34;1")
    BrightMagenta: str = ColourTemplate.format("35;1")
    BrightCyan: str = ColourTemplate.format("36;1")
    BrightWhite: str = ColourTemplate.format("37;1")

    # 8 background colours
    BackgroundBlack: str = ColourTemplate.format("40")
    BackgroundRed: str = ColourTemplate.format("41")
    BackgroundGreen: str = ColourTemplate.format("42")
    BackgroundYellow: str = ColourTemplate.format("43")
    BackgroundBlue: str = ColourTemplate.format("44")
    BackgroundMagenta: str = ColourTemplate.format("45")
    BackgroundCyan: str = ColourTemplate.format("46")
    BackgroundWhite: str = ColourTemplate.format("47")

    # 8 background bright colours
    BackgroundBrightBlack: str = ColourTemplate.format("40;1")
    BackgroundBrightRed: str = ColourTemplate.format("41;1")
    BackgroundBrightGreen: str = ColourTemplate.format("42;1")
    BackgroundBrightYellow: str = ColourTemplate.format("43;1")
    BackgroundBrightBlue: str = ColourTemplate.format("44;1")
    BackgroundBrightMagenta: str = ColourTemplate.format("45;1")
    BackgroundBrightCyan: str = ColourTemplate.format("46;1")
    BackgroundBrightWhite: str = ColourTemplate.format("47;1")

    # Decoration
    Bold: str = ColourTemplate.format("1")
    Underline: str = ColourTemplate.format("4")
    Reversed: str = ColourTemplate.format("7")

    # Extended colour set
    @staticmethod
    def generate256bitColour(code: str) -> str:
        """Generate the ANSI modifier for that colour code"""
        return ANSIFormatter.ColourTemplate.format(f"38;5;{code}")

    @staticmethod
    def generate256bitBackgroundColour(code: str) -> str:
        """Generate the ANSI modifier for that background colour code"""
        return ANSIFormatter.ColourTemplate.format(f"48;5;{code}")

    @staticmethod
    def is_ansi_code(code: str) -> bool:
        """Check if the ANSI modifier is valid"""
        if type(code) != str:
            raise TypeError("ANSI code must be a string!")
        return True if match(r"^\u001b\[\d+;?\d*;?\d*m$", code) else False

    @staticmethod
    def extendedPrint(obj: Any, *args, **kwargs) -> None:
        """Extend the original print() to help print colour easier"""
        ansi_option = kwargs.pop("ansi", None)
        if ansi_option is None:
            return print(obj, *args, **kwargs)
        else:
            obj_str = str(obj)
            if type(ansi_option) == str:
                if ANSIFormatter.is_ansi_code(ansi_option):
                    obj_str = ansi_option + obj_str
                else:
                    _option = getattr(ANSIFormatter, ansi_option, None)
                    if _option is None:
                        raise ValueError(
                            f"Invalid ANSI code or colour name: {ansi_option}")
                    obj_str = _option + obj_str
            elif type(ansi_option) == list:
                for option in ansi_option:
                    if type(option) == str:
                        if ANSIFormatter.is_ansi_code(option):
                            obj_str = option + obj_str
                        else:
                            _option = getattr(ANSIFormatter, option, None)
                            if _option is None:
                                raise ValueError(
                                    "Invalid ANSI code or colour name: " +
                                    f"{option}"
                                )
                            obj_str = _option + obj_str
                    else:
                        raise ValueError(
                            "ANSI code or colour name must be a string!")
            return print(obj_str, *args, **kwargs)


def err_imp(pkg_name: str) -> None:
    s = f"[Package] This package is not installed: {pkg_name}"
    return ANSIFormatter.extendedPrint(s, ansi=ANSIFormatter.Red)
