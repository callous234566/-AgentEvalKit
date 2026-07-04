"""UI static assets facade.

Re-exports CSS_STYLES, icon_svg, icon_label so existing imports
(`from ui.assets import ...`) continue to work unchanged.

Actual implementations live in:
  - ui/styles/   (CSS modules)
  - ui/icons.py  (SVG icon system)
"""

from ui.styles import CSS_PARTS
from ui.icons import ICON_PATHS, icon_svg, icon_label  # noqa: F401

CSS_STYLES = "<style>\n" + "\n".join(CSS_PARTS) + "\n</style>"
