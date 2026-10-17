"""GenomeSpy color validation shared by plotting families."""

from typing import Any


# Scheme names shipped by the bundled GenomeSpy/Vega runtime.
_SCHEMES = frozenset(
    """
accent category10 category20 category20b category20c dark2 observable10 paired
pastel1 pastel2 set1 set2 set3 tableau10 tableau20 blues greens greys oranges
purples reds bluegreen bluepurple greenblue orangered purpleblue purplebluegreen
purplered redpurple yellowgreen yelloworangebrown yelloworangered blueorange
brownbluegreen purplegreen purpleorange redblue redgrey yellowgreenblue
redyellowblue redyellowgreen pinkyellowgreen spectral viridis magma inferno
plasma cividis rainbow sinebow turbo browns tealblues teals warmgreys goldgreen
goldorange goldred lightgreyred lightgreyteal lightmulti lightorange lighttealblue
darkblue darkgold darkgreen darkmulti darkred
""".split()
)


def native_scheme(value: Any, name: str, *, context: str = "gsc.pl.umap") -> str:
    if not isinstance(value, str) or value.lower() not in _SCHEMES:
        raise NotImplementedError(
            f"{context}: {name} requires a GenomeSpy scheme name, such as "
            "'viridis', 'redblue', or 'set1'; Matplotlib colormaps are unsupported."
        )
    return value.lower()


def native_color(value: Any, name: str, *, context: str = "gsc.pl.umap") -> str:
    # Keep parsing in GenomeSpy; exclude Matplotlib forms and entry alpha.
    if isinstance(value, str):
        named = (
            value.isalpha()
            and len(value) > 2
            and value.lower() not in ("transparent", "none")
        )
        hex_color = value.startswith("#") and len(value) in (4, 7)
        if named or hex_color:
            return value
    raise NotImplementedError(
        f"{context}: {name} requires an opaque CSS color name or #RGB/#RRGGBB. "
        "Matplotlib colors and per-color alpha are unsupported; use scalar alpha."
    )
