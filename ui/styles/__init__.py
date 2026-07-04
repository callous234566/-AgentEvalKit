"""Central style registry.

Imports all style modules and exposes them as constants.
CSS_CUSTOM_PROPERTIES are injected first so that component CSS can
reference var(--rag-*) from the start.
"""

from . import _variables as _variables_mod
from . import _global as _global_mod
from . import _chat as _chat_mod
from . import _dark as _dark_mod
from . import _responsive as _responsive_mod
from . import _sidebar as _sidebar_mod
from . import _workspace as _workspace_mod
from . import _documents as _documents_mod
from . import _upload as _upload_mod
from . import _widgets as _widgets_mod
from . import _buttons as _buttons_mod
from . import _sidebar_refinement as _sidebar_refinement_mod
from . import _empty_states as _empty_states_mod
from . import _dark_refinement as _dark_refinement_mod
from . import _mobile_refinement as _mobile_refinement_mod

# Ordered so that CSS variables are available before any component CSS.
CSS_PARTS = [
    _variables_mod.VARIABLES_CSS,
    _global_mod.GLOBAL_CSS,
    _chat_mod.CHAT_CSS,
    _dark_mod.DARK_MODE_CSS,
    _responsive_mod.RESPONSIVE_CSS,
    _sidebar_mod.SIDEBAR_CSS,
    _workspace_mod.WORKSPACE_CSS,
    _documents_mod.DOCUMENTS_CSS,
    _upload_mod.UPLOAD_CSS,
    _widgets_mod.WIDGETS_CSS,
    _buttons_mod.BUTTONS_CSS,
    _sidebar_refinement_mod.SIDEBAR_REFINEMENT_CSS,
    _empty_states_mod.EMPTY_STATES_CSS,
    _dark_refinement_mod.DARK_REFINEMENT_CSS,
    _mobile_refinement_mod.MOBILE_REFINEMENT_CSS,
]

CSS_STYLES = "".join(CSS_PARTS)

__all__ = ["CSS_PARTS", "CSS_STYLES"]
