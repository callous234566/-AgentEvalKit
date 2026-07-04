"""Final shared button system overrides."""

BUTTONS_CSS = """
    :root {
        --rag-control-height-sm: 34px;
        --rag-control-height-md: 40px;
        --rag-control-height-lg: 44px;
        --rag-control-radius-sm: 11px;
        --rag-control-radius-md: 13px;
        --rag-control-radius-lg: 15px;
        --rag-control-icon-sm: 14px;
        --rag-control-icon-md: 16px;
    }

    /* Shared button chrome: calm by default, semantic color on purpose. */
    .stButton > button,
    div[data-testid="stFormSubmitButton"] > button,
    div[data-testid="stDownloadButton"] > button {
        min-height: var(--rag-control-height-md) !important;
        border-radius: var(--rag-control-radius-md) !important;
        font-weight: 760 !important;
        letter-spacing: 0.01em !important;
        transition:
            transform 0.16s ease,
            box-shadow 0.16s ease,
            border-color 0.16s ease,
            background-color 0.16s ease,
            color 0.16s ease !important;
    }
    .stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover,
    div[data-testid="stDownloadButton"] > button:hover {
        transform: translateY(-1px);
    }
    .stButton > button:active,
    div[data-testid="stFormSubmitButton"] > button:active,
    div[data-testid="stDownloadButton"] > button:active {
        transform: translateY(0);
    }
    .stButton > button:focus-visible,
    div[data-testid="stFormSubmitButton"] > button:focus-visible,
    div[data-testid="stDownloadButton"] > button:focus-visible {
        outline: 3px solid rgba(59, 130, 246, 0.22) !important;
        outline-offset: 2px !important;
        border-color: var(--rag-blue-300) !important;
        box-shadow:
            0 0 0 1px rgba(59, 130, 246, 0.16),
            var(--rag-shadow-sm) !important;
    }
    .stButton > button:disabled,
    div[data-testid="stFormSubmitButton"] > button:disabled,
    div[data-testid="stDownloadButton"] > button:disabled {
        transform: none !important;
        box-shadow: none !important;
        opacity: 0.55 !important;
    }

    /* Primary actions */
    div[class*="st-key-upload_process_button"] button,
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"] button,
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"] button,
    div[class*="st-key-send_button"] button {
        border: 1px solid var(--rag-blue-200) !important;
        background:
            radial-gradient(circle at 12% 0%, var(--rag-blue-glow), transparent 48%),
            var(--rag-blue-50) !important;
        color: var(--rag-blue-primary) !important;
        box-shadow: var(--rag-shadow-sm) !important;
    }
    div[class*="st-key-upload_process_button"] button:hover,
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"] button:hover,
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"] button:hover,
    div[class*="st-key-send_button"] button:hover {
        border-color: var(--rag-blue-300) !important;
        background: var(--rag-blue-100) !important;
        color: var(--rag-blue-primary) !important;
        box-shadow: 0 8px 18px var(--rag-blue-glow) !important;
    }

    /* Secondary actions */
    div[class*="st-key-clear_button"] button,
    div[class*="st-key-cancel_"] button {
        border: 1px solid var(--rag-border) !important;
        background: var(--rag-bg-card) !important;
        color: var(--rag-text-secondary) !important;
        box-shadow: var(--rag-shadow-sm) !important;
    }
    div[class*="st-key-clear_button"] button:hover,
    div[class*="st-key-cancel_"] button:hover {
        border-color: var(--rag-border-strong) !important;
        background: var(--rag-bg-elevated) !important;
        color: var(--rag-text-primary) !important;
    }

    /* Dangerous confirmations stay unmistakable. */
    div[class*="st-key-confirm_delete_"] button,
    div[class*="st-key-batch_delete_confirm_yes"] button,
    div[class*="st-key-confirm_clear"] button {
        border: 1px solid var(--rag-red-border) !important;
        background: var(--rag-red-bg) !important;
        color: var(--rag-red-text) !important;
        box-shadow: var(--rag-shadow-sm) !important;
    }
    div[class*="st-key-confirm_delete_"] button:hover,
    div[class*="st-key-batch_delete_confirm_yes"] button:hover,
    div[class*="st-key-confirm_clear"] button:hover {
        border-color: var(--rag-red-text) !important;
        background: #fee2e2 !important;
        color: #991b1b !important;
        box-shadow: 0 8px 18px rgba(239, 68, 68, 0.12) !important;
    }

    /* Compact icon-only controls */
    div[class*="st-key-upload_remove_visible_"] button {
        width: var(--rag-control-height-sm) !important;
        min-width: var(--rag-control-height-sm) !important;
        height: var(--rag-control-height-sm) !important;
        min-height: var(--rag-control-height-sm) !important;
        border-radius: var(--rag-control-radius-sm) !important;
    }
"""
