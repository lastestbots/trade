from core.utils.colour import ColourTxtUtil


def operation_help_info() -> str:
    return "{} {}: Busy {}: Sell  {}:Account {}: Next".format(
        ColourTxtUtil.cyan('Command'),
        ColourTxtUtil.red("B"),
        ColourTxtUtil.red("S"),
        ColourTxtUtil.red("A"),
        ColourTxtUtil.red("N"),

    )
