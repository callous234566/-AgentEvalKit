"""Final sidebar rhythm overrides.

This layer loads after the shared button system so the sidebar keeps one
predictable visual language without changing any Streamlit widget behavior.
"""

SIDEBAR_REFINEMENT_CSS = """
    [data-testid="stSidebar"] {
        --rag-sidebar-control-height: 44px;
        --rag-sidebar-radius: 15px;
    }

    /* Header and semantic status */
    [data-testid="stSidebar"] .sidebar-main-header {
        min-height: var(--rag-sidebar-control-height);
        margin-bottom: 0.62rem;
        padding: 0.62rem 0.72rem;
        border-radius: var(--rag-sidebar-radius);
        gap: 0.52rem;
        font-size: 1rem;
        box-shadow: 0 5px 16px rgba(15, 23, 42, 0.05);
    }
    [data-testid="stSidebar"] .sidebar-main-header::before {
        display: none;
    }
    [data-testid="stSidebar"] .sidebar-main-header .ui-icon {
        width: 1.05rem;
        height: 1.05rem;
        color: var(--rag-blue-primary);
    }
    [data-testid="stSidebar"] .sidebar-api-ok,
    [data-testid="stSidebar"] .sidebar-api-fail {
        margin-bottom: 0.18rem;
        padding: 3px 9px;
        font-size: 11px;
    }
    [data-testid="stSidebar"] hr {
        margin: 0.76rem 0 !important;
    }

    /* Create, new conversation and help controls share one compact rhythm. */
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"],
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"],
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        margin: 0.4rem 0 !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"] button,
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"] button,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        min-height: var(--rag-sidebar-control-height) !important;
        height: var(--rag-sidebar-control-height) !important;
        border-radius: var(--rag-sidebar-radius) !important;
        justify-content: flex-start !important;
        padding: 0 0.82rem 0 2.55rem !important;
        font-size: 0.9rem !important;
        font-weight: 780 !important;
        box-shadow: 0 5px 16px rgba(15, 23, 42, 0.045) !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"] button::before,
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"] button::before,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary::before {
        left: 0.88rem;
        width: 15px;
        height: 15px;
    }
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"] button p,
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"] button p {
        left: 2.55rem !important;
        font-size: 0.9rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] details {
        border-radius: var(--rag-sidebar-radius) !important;
        box-shadow: 0 5px 16px rgba(15, 23, 42, 0.045) !important;
    }

    /* Collection and session rows remain one bubble with an embedded menu trigger. */
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"],
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"] {
        margin: 0.34rem 0 !important;
        border-radius: var(--rag-sidebar-radius) !important;
        box-shadow: 0 5px 15px rgba(15, 23, 42, 0.045) !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_row_select_"] button,
    [data-testid="stSidebar"] div[class*="st-key-session_row_select_"] button {
        height: var(--rag-sidebar-control-height) !important;
        min-height: var(--rag-sidebar-control-height) !important;
        padding-left: 2.28rem !important;
        padding-right: 2.55rem !important;
        border-radius: var(--rag-sidebar-radius) !important;
        font-size: 0.89rem !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"]::before,
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"]::before {
        left: 0.74rem;
        width: 15px;
        height: 15px;
    }
    [data-testid="stSidebar"] .sidebar-pinned-marker {
        display: none;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"]:has(.sidebar-pinned-marker)::after,
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"]:has(.sidebar-pinned-marker)::after {
        content: "";
        position: absolute;
        top: 50%;
        right: 2.52rem;
        z-index: 3;
        width: 13px;
        height: 13px;
        transform: translateY(-50%);
        background: var(--rag-blue-primary);
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M14 4l6 6-3 1-4 4-1 5-2-2-4-4-2-2 5-1 4-4zM9 15l-5 5' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M14 4l6 6-3 1-4 4-1 5-2-2-4-4-2-2 5-1 4-4zM9 15l-5 5' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        pointer-events: none;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_row_more_"],
    [data-testid="stSidebar"] div[class*="st-key-session_row_more_"] {
        right: 0.5rem !important;
        width: 28px !important;
        height: var(--rag-sidebar-control-height) !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_row_more_"] button,
    [data-testid="stSidebar"] div[class*="st-key-session_row_more_"] button,
    [data-testid="stSidebar"] div[class*="st-key-collection_row_more_"] button p,
    [data-testid="stSidebar"] div[class*="st-key-session_row_more_"] button p {
        width: 28px !important;
        height: var(--rag-sidebar-control-height) !important;
        min-height: var(--rag-sidebar-control-height) !important;
        border-radius: 9px !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_row_more_"] button:hover,
    [data-testid="stSidebar"] div[class*="st-key-session_row_more_"] button:hover {
        background: transparent !important;
        border-color: transparent !important;
        box-shadow: none !important;
        color: var(--rag-blue-primary) !important;
        transform: none !important;
    }

    /* Action menus inherit the same compact language without changing keys. */
    [data-testid="stSidebar"] div[class*="st-key-collection_action_panel_"],
    [data-testid="stSidebar"] div[class*="st-key-session_action_panel_"] {
        top: 2.68rem;
        width: 136px;
        padding: 0.34rem;
        border-radius: 14px;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_action_panel_"] button,
    [data-testid="stSidebar"] div[class*="st-key-session_action_panel_"] button {
        min-height: 33px !important;
        border-radius: 9px !important;
        font-size: 0.84rem !important;
        transform: none !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_action_panel_"] button:hover,
    [data-testid="stSidebar"] div[class*="st-key-session_action_panel_"] button:hover {
        transform: none !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_action_pin_"] button:disabled,
    [data-testid="stSidebar"] div[class*="st-key-session_action_pin_"] button:disabled {
        border: 1px solid var(--rag-blue-100) !important;
        background: var(--rag-blue-50) !important;
        color: var(--rag-blue-primary) !important;
        opacity: 1 !important;
        cursor: default !important;
    }

    /* Current collection stays visible but no longer dominates the sidebar. */
    [data-testid="stSidebar"] .current-collection-badge {
        gap: 0.58rem;
        margin: 0.62rem 0 0.72rem;
        padding: 0.7rem 0.78rem;
        border-radius: var(--rag-sidebar-radius);
        box-shadow: 0 5px 16px rgba(15, 23, 42, 0.045);
    }
    [data-testid="stSidebar"] .current-collection-badge .ui-icon {
        width: 1rem;
        height: 1rem;
    }
    [data-testid="stSidebar"] .current-collection-badge span {
        margin-bottom: 0.12rem;
        font-size: 0.72rem;
    }
    [data-testid="stSidebar"] .current-collection-badge strong {
        font-size: 0.92rem;
        line-height: 1.35;
    }
"""
