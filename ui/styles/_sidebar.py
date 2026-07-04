SIDEBAR_CSS = """
    [data-testid="stSidebar"] div[class*="st-key-collection_select_"],
    [data-testid="stSidebar"] div[class*="st-key-collection_pin_"],
    [data-testid="stSidebar"] div[class*="st-key-collection_rename_"],
    [data-testid="stSidebar"] div[class*="st-key-collection_delete_"],
    [data-testid="stSidebar"] div[class*="st-key-session_select_"],
    [data-testid="stSidebar"] div[class*="st-key-session_pin_"],
    [data-testid="stSidebar"] div[class*="st-key-session_rename_"],
    [data-testid="stSidebar"] div[class*="st-key-session_delete_"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    .stSidebar .stMarkdown h3:first-child {
        margin-top: 0;
        padding-top: 0;
    }

    .sidebar-main-header {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        margin: 0 0 0.75rem;
        padding: 0.72rem 0.78rem;
        border: 1px solid var(--rag-border);
        border-radius: 18px;
        background:
            radial-gradient(circle at 12% 20%, var(--rag-blue-glow), transparent 42%),
            var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
        font-size: 1.05rem;
        font-weight: 800;
        letter-spacing: -0.01em;
        color: var(--rag-text-primary);
    }
    .sidebar-main-header::before {
        content: "";
        width: 8px;
        height: 8px;
        border-radius: 999px;
        background: var(--rag-blue-primary);
        box-shadow: 0 0 0 4px var(--rag-blue-glow);
        flex: 0 0 auto;
    }

    .sidebar-api-ok {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        max-width: 100%;
        box-sizing: border-box;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        padding: 3px 10px;
        border-radius: 999px;
        background: var(--rag-green-bg);
        color: var(--rag-green-text);
        font-size: 12px;
        font-weight: 700;
    }
    .sidebar-api-ok::before {
        content: "";
        width: 7px;
        height: 7px;
        border-radius: 999px;
        background: var(--rag-green-bright);
        box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.15);
    }

    .sidebar-api-fail {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        max-width: 100%;
        box-sizing: border-box;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        padding: 3px 10px;
        border-radius: 999px;
        background: var(--rag-red-bg);
        color: var(--rag-red-text);
        font-size: 12px;
        font-weight: 700;
    }
    .sidebar-api-fail::before {
        content: "";
        width: 7px;
        height: 7px;
        border-radius: 999px;
        background: var(--rag-red-strong);
        box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.15);
    }

    .sidebar-section {
        margin: 0 0 0.45rem;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 0.02em;
        color: var(--rag-text-placeholder);
    }
    .sidebar-section span {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }

    .sidebar-stats {
        display: flex;
        gap: 8px;
        margin: 0 0 0.35rem;
    }
    .sidebar-stat-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 10px;
        border-radius: 999px;
        background: var(--rag-blue-glow);
        color: var(--rag-blue-primary);
        font-size: 12px;
        font-weight: 700;
        white-space: nowrap;
        min-width: 0;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .sidebar-divider {
        margin: 0.25rem 0 0.6rem;
        border: none;
        border-top: 1px solid var(--rag-border);
    }

    .collection-label,
    .session-label {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        min-width: 0;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        font-size: 0.92rem;
        font-weight: 760;
    }
    .collection-label .ui-icon,
    .session-label .ui-icon {
        flex: 0 0 auto;
        width: 1rem;
        height: 1rem;
        color: var(--rag-text-muted);
    }
    .collection-actions,
    .session-actions {
        display: inline-flex;
        align-items: center;
        flex: 0 0 auto;
    }
    .collection-action-btn,
    .session-action-btn {
        width: 28px;
        height: 28px;
        border: 0;
        border-radius: 10px;
        background: var(--rag-bg-card);
        color: var(--rag-text-placeholder);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        opacity: 1;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
    }
    .collection-action-btn::before,
    .session-action-btn::before {
        content: "";
        width: 16px;
        height: 16px;
        display: block;
        background: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='5' cy='12' r='2'/%3E%3Ccircle cx='12' cy='12' r='2'/%3E%3Ccircle cx='19' cy='12' r='2'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='5' cy='12' r='2'/%3E%3Ccircle cx='12' cy='12' r='2'/%3E%3Ccircle cx='19' cy='12' r='2'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    .collection-action-btn:hover,
    .session-action-btn:hover {
        background: var(--rag-bg-surface);
        color: var(--rag-text-primary);
        opacity: 1;
    }
    .collection-action-btn .ui-icon,
    .session-action-btn .ui-icon {
        width: 1.1rem;
        height: 1.1rem;
    }

    [data-testid="stSidebar"] div[class*="st-key-collection_row_select_"] button,
    [data-testid="stSidebar"] div[class*="st-key-session_row_select_"] button {
        min-height: 42px !important;
        padding: 0.54rem 0.72rem 0.54rem 0.82rem !important;
        border: 0 !important;
        border-radius: 16px 0 0 16px !important;
        background: transparent !important;
        color: var(--rag-text-primary) !important;
        justify-content: flex-start !important;
        text-align: left !important;
        font-size: 0.9rem !important;
        font-weight: 680 !important;
        box-shadow: none !important;
        overflow: hidden !important;
        white-space: nowrap !important;
        text-overflow: ellipsis !important;
        transition: background 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_row_select_"] button:hover,
    [data-testid="stSidebar"] div[class*="st-key-session_row_select_"] button:hover {
        background: transparent !important;
        border-color: transparent !important;
        box-shadow: none !important;
        transform: none;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_row_more_"] button:hover,
    [data-testid="stSidebar"] div[class*="st-key-session_row_more_"] button:hover {
        background: transparent !important;
        border-color: transparent !important;
        box-shadow: none !important;
        color: var(--rag-blue-primary) !important;
        transform: none !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_row_select_"] button:focus-visible,
    [data-testid="stSidebar"] div[class*="st-key-session_row_select_"] button:focus-visible,
    [data-testid="stSidebar"] div[class*="st-key-collection_row_more_"] button:focus-visible,
    [data-testid="stSidebar"] div[class*="st-key-session_row_more_"] button:focus-visible {
        border-color: var(--rag-border-focus) !important;
        box-shadow: 0 0 0 3px var(--rag-blue-glow), var(--rag-shadow-sm) !important;
        outline: none !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_row_select_"] button p,
    [data-testid="stSidebar"] div[class*="st-key-session_row_select_"] button p {
        overflow: hidden !important;
        white-space: nowrap !important;
        text-overflow: ellipsis !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_row_more_"] button,
    [data-testid="stSidebar"] div[class*="st-key-session_row_more_"] button {
        min-height: 42px !important;
        height: 42px !important;
        padding: 0 !important;
        border: 0 !important;
        border-radius: 0 16px 16px 0 !important;
        background: transparent !important;
        color: var(--rag-text-placeholder) !important;
        box-shadow: none !important;
        font-size: 1rem !important;
        font-weight: 900 !important;
        line-height: 1 !important;
        letter-spacing: 0 !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_row_more_"] button:hover,
    [data-testid="stSidebar"] div[class*="st-key-session_row_more_"] button:hover {
        background: transparent !important;
        color: var(--rag-text-primary) !important;
        border-color: transparent !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"],
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"] {
        position: relative !important;
        overflow: visible !important;
        z-index: 1;
        margin: 0.38rem 0 !important;
        border: 1px solid var(--rag-border-light);
        border-radius: 13px;
        background: var(--rag-bg-elevated);
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
        transition: background 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
    }
    .sidebar-row-meta {
        display: inline-flex;
        align-items: center;
        max-width: calc(100% - 0.9rem);
        margin: 0.46rem 0.64rem -0.12rem;
        padding: 0.08rem 0.42rem;
        border: 1px solid var(--rag-border-light);
        border-radius: 999px;
        background: var(--rag-bg-card-alt);
        color: var(--rag-text-placeholder);
        font-size: 0.68rem;
        font-weight: 690;
        line-height: 1.3;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .sidebar-section-copy {
        margin: -0.18rem 0 0.5rem;
        color: var(--rag-text-placeholder);
        font-size: 0.74rem;
        line-height: 1.45;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"] div[data-testid="stHorizontalBlock"],
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"] div[data-testid="stHorizontalBlock"] {
        gap: 0 !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"]:hover button,
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"]:hover button,
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"]:has(div[class*="st-key-collection_action_panel_"]) button,
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"]:has(div[class*="st-key-session_action_panel_"]) button {
        background: transparent !important;
        border-color: transparent !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"]:hover,
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"]:hover,
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"]:has(div[class*="st-key-collection_action_panel_"]),
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"]:has(div[class*="st-key-session_action_panel_"]) {
        background: var(--rag-blue-50);
        border-color: var(--rag-blue-100);
        box-shadow: 0 14px 30px rgba(37, 99, 235, 0.10);
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"]:has(div[class*="st-key-collection_action_panel_"]),
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"]:has(div[class*="st-key-session_action_panel_"]) {
        z-index: 30;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_action_panel_"],
    [data-testid="stSidebar"] div[class*="st-key-session_action_panel_"] {
        position: absolute !important;
        right: 0;
        top: 2.85rem;
        width: 138px;
        margin: 0 !important;
        padding: 0.38rem;
        border: 1px solid var(--rag-border);
        border-radius: 16px;
        background: var(--rag-bg-card);
        box-shadow: var(--rag-shadow-lg);
        z-index: 40;
        backdrop-filter: blur(14px);
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_action_panel_"] button,
    [data-testid="stSidebar"] div[class*="st-key-session_action_panel_"] button {
        position: relative !important;
        min-height: 34px !important;
        border: 0 !important;
        border-radius: 10px !important;
        background: transparent !important;
        color: var(--rag-text-primary) !important;
        justify-content: flex-start !important;
        font-size: 0.86rem !important;
        font-weight: 760 !important;
        box-shadow: none !important;
        padding: 0 0.58rem 0 2rem !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_action_panel_"] button::before,
    [data-testid="stSidebar"] div[class*="st-key-session_action_panel_"] button::before {
        content: "";
        position: absolute;
        left: 0.58rem;
        top: 50%;
        width: 14px;
        height: 14px;
        transform: translateY(-50%);
        background: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 17V5M7 10l5-5 5 5M5 19h14' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 17V5M7 10l5-5 5 5M5 19h14' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    [data-testid="stSidebar"] div[class*="st-key-session_action_share_"] button::before {
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='18' cy='5' r='3' fill='none' stroke='black' stroke-width='2'/%3E%3Ccircle cx='6' cy='12' r='3' fill='none' stroke='black' stroke-width='2'/%3E%3Ccircle cx='18' cy='19' r='3' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='M8.6 10.7 15.4 6.3M8.6 13.3l6.8 4.4' fill='none' stroke='black' stroke-width='2'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='18' cy='5' r='3' fill='none' stroke='black' stroke-width='2'/%3E%3Ccircle cx='6' cy='12' r='3' fill='none' stroke='black' stroke-width='2'/%3E%3Ccircle cx='18' cy='19' r='3' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='M8.6 10.7 15.4 6.3M8.6 13.3l6.8 4.4' fill='none' stroke='black' stroke-width='2'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_action_rename_"] button::before,
    [data-testid="stSidebar"] div[class*="st-key-session_action_rename_"] button::before {
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_action_delete_"] button::before,
    [data-testid="stSidebar"] div[class*="st-key-session_action_delete_"] button::before {
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6M10 11v6M14 11v6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6M10 11v6M14 11v6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_action_panel_"] button:hover,
    [data-testid="stSidebar"] div[class*="st-key-session_action_panel_"] button:hover {
        background: var(--rag-bg-surface) !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_action_panel_"] button:focus-visible,
    [data-testid="stSidebar"] div[class*="st-key-session_action_panel_"] button:focus-visible {
        background: var(--rag-blue-50) !important;
        outline: 2px solid var(--rag-blue-glow) !important;
        outline-offset: 1px !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_action_delete_"] button,
    [data-testid="stSidebar"] div[class*="st-key-session_action_delete_"] button {
        color: var(--rag-red-strong) !important;
    }

    .current-collection-badge {
        display: flex;
        align-items: flex-start;
        gap: 0.65rem;
        margin: 0.75rem 0 0.85rem;
        padding: 0.82rem 0.9rem;
        border: 1px solid var(--rag-blue-100);
        border-radius: 16px;
        background: var(--rag-blue-50-gradient);
        color: var(--rag-text-primary);
        box-shadow: var(--rag-shadow-sm);
    }
    .current-collection-badge .ui-icon {
        width: 1.05rem;
        height: 1.05rem;
        flex: 0 0 auto;
        margin-top: 0.1rem;
        color: var(--rag-blue-primary);
    }
    .current-collection-badge span {
        display: block;
        margin-bottom: 0.2rem;
        color: var(--rag-text-placeholder);
        font-size: 0.78rem;
        font-weight: 800;
    }
    .current-collection-badge strong {
        display: block;
        color: var(--rag-text-primary);
        font-size: 0.98rem;
        font-weight: 850;
        line-height: 1.45;
        word-break: break-word;
    }
"""
