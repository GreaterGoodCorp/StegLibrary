# Builtin modules
from re import match


class ANSIFormatter:
    """
    ANSIFormatter provides all ANSI formatting options
    for supported platforms.
    """
    # ANSI colour template
    ColourTemplate = "\u001b[{}m"

    # ANSI default reset
    Reset = ColourTemplate.format(0)

    # 8 basic foreground colours
    Black = ColourTemplate.format("30")
    Red = ColourTemplate.format("31")
    Green = ColourTemplate.format("32")
    Yellow = ColourTemplate.format("33")
    Blue = ColourTemplate.format("34")
    Magenta = ColourTemplate.format("35")
    Cyan = ColourTemplate.format("36")
    White = ColourTemplate.format("37")

    # 8 bright colours
    BrightBlack = ColourTemplate.format("30;1")
    BrightRed = ColourTemplate.format("31;1")
    BrightGreen = ColourTemplate.format("32;1")
    BrightYellow = ColourTemplate.format("33;1")
    BrightBlue = ColourTemplate.format("34;1")
    BrightMagenta = ColourTemplate.format("35;1")
    BrightCyan = ColourTemplate.format("36;1")
    BrightWhite = ColourTemplate.format("37;1")

    # 8 background colours
    BackgroundBlack = ColourTemplate.format("40")
    BackgroundRed = ColourTemplate.format("41")
    BackgroundGreen = ColourTemplate.format("42")
    BackgroundYellow = ColourTemplate.format("43")
    BackgroundBlue = ColourTemplate.format("44")
    BackgroundMagenta = ColourTemplate.format("45")
    BackgroundCyan = ColourTemplate.format("46")
    BackgroundWhite = ColourTemplate.format("47")

    # 8 background bright colours
    BackgroundBrightBlack = ColourTemplate.format("40;1")
    BackgroundBrightRed = ColourTemplate.format("41;1")
    BackgroundBrightGreen = ColourTemplate.format("42;1")
    BackgroundBrightYellow = ColourTemplate.format("43;1")
    BackgroundBrightBlue = ColourTemplate.format("44;1")
    BackgroundBrightMagenta = ColourTemplate.format("45;1")
    BackgroundBrightCyan = ColourTemplate.format("46;1")
    BackgroundBrightWhite = ColourTemplate.format("47;1")

    # Decoration
    Bold = ColourTemplate.format("1")
    Underline = ColourTemplate.format("4")
    Reversed = ColourTemplate.format("7")

    # Extended colour set
    @staticmethod
    def generate256bitColour(cls, code):
        """Generate the ANSI modifier for that colour code"""
        return ANSIFormatter.ColourTemplate.format(f"38;5;{code}")

    @staticmethod
    def generate256bitBackgroundColour(code):
        """Generate the ANSI modifier for that background colour code"""
        return ANSIFormatter.ColourTemplate.format(f"48;5;{code}")

    @staticmethod
    def is_ansi_code(code):
        """Check if the ANSI modifier is valid"""
        if type(code) != str:
            raise TypeError("ANSI code must be a string!")
        return True if match(r"^\u001b\[\d+;?\d*;?\d*m$", code) else False

    @staticmethod
    def extendedPrint(obj, *args, **kwargs):
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


def err_imp(pkg_name):
    s = f"[Package] This package is not installed: {pkg_name}"
    return ANSIFormatter.extendedPrint(s, ansi=ANSIFormatter.Red)
