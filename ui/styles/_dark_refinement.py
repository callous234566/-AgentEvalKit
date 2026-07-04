"""Final dark-mode component overrides for high-frequency workspace surfaces."""

DARK_REFINEMENT_CSS = """
    /* Fixed composer and its compact controls */
    body.rag-dark div[class*="st-key-chat_input_area"] {
        border-color: var(--rag-border) !important;
        background:
            radial-gradient(circle at 8% 0%, var(--rag-blue-glow), transparent 32%),
            linear-gradient(180deg, rgba(15, 23, 42, 0.94) 0%, var(--rag-bg-card) 54%) !important;
        box-shadow: 0 -12px 30px rgba(0, 0, 0, 0.24) !important;
    }
    body.rag-dark .rag-immediate-loading {
        border-color: var(--rag-border) !important;
        background:
            radial-gradient(circle at 7% 0%, var(--rag-blue-glow), transparent 42%),
            var(--rag-bg-card) !important;
        box-shadow: 0 14px 34px rgba(0, 0, 0, 0.28) !important;
    }
    body.rag-dark .rag-latest-answer-button {
        border-color: var(--rag-blue-200);
        background: var(--rag-bg-elevated);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.26);
    }
    body.rag-dark .status-notice {
        border-color: var(--rag-border);
        background: var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
    }
    body.rag-dark .status-notice-icon {
        background: var(--rag-bg-elevated);
    }
    body.rag-dark div[data-testid="stTextInput"] > div,
    body.rag-dark div[data-testid="stTextInput"] [data-baseweb="input"] {
        border-color: var(--rag-border) !important;
        background: var(--rag-bg-input) !important;
        box-shadow: none !important;
        outline: none !important;
    }
    body.rag-dark div[data-testid="stTextInput"] > div:focus-within,
    body.rag-dark div[data-testid="stTextInput"] [data-baseweb="input"]:focus-within {
        border-color: var(--rag-blue-300) !important;
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.16) !important;
        outline: none !important;
    }
    body.rag-dark div[data-testid="stTextInput"] input {
        color: var(--rag-text-primary) !important;
        background: transparent !important;
        outline: none !important;
        box-shadow: none !important;
        -webkit-text-fill-color: var(--rag-text-primary) !important;
        caret-color: var(--rag-blue-primary) !important;
    }
    body.rag-dark div[data-testid="stTextInput"] input::placeholder {
        color: var(--rag-text-placeholder) !important;
        -webkit-text-fill-color: var(--rag-text-placeholder) !important;
    }
    body.rag-dark div[class*="st-key-quick_prompt_"] button {
        border-color: var(--rag-border) !important;
        background: rgba(30, 41, 59, 0.72) !important;
        color: var(--rag-text-secondary) !important;
    }
    body.rag-dark div[class*="st-key-quick_prompt_"] button:hover {
        border-color: var(--rag-blue-200) !important;
        background: var(--rag-bg-surface) !important;
        color: var(--rag-blue-primary) !important;
    }
    body.rag-dark div[class*="st-key-sample_question_"] button,
    body.rag-dark div[class*="st-key-quick_prompt_"] button:disabled {
        border-color: var(--rag-border) !important;
        background: rgba(15, 23, 42, 0.78) !important;
        color: var(--rag-text-secondary) !important;
        opacity: 0.92 !important;
        box-shadow: none !important;
    }
    body.rag-dark div[class*="st-key-sample_question_"] button:hover,
    body.rag-dark div[class*="st-key-quick_prompt_"] button:disabled:hover {
        border-color: var(--rag-blue-200) !important;
        background: var(--rag-bg-card) !important;
        color: var(--rag-blue-primary) !important;
    }
    body.rag-dark div[data-testid="stExpander"] details {
        border-color: var(--rag-border) !important;
        background: var(--rag-bg-card) !important;
        box-shadow: none !important;
    }
    body.rag-dark div[data-testid="stExpander"] summary,
    body.rag-dark div[data-testid="stExpander"] summary:hover,
    body.rag-dark div[data-testid="stExpander"] details > div[role="region"] {
        background: var(--rag-bg-card) !important;
        color: var(--rag-text-primary) !important;
        border-color: var(--rag-border) !important;
    }
    body.rag-dark div[data-testid="stExpander"] summary p,
    body.rag-dark div[data-testid="stExpander"] summary span,
    body.rag-dark div[data-testid="stExpander"] details > div[role="region"] p,
    body.rag-dark div[data-testid="stExpander"] details > div[role="region"] span {
        color: var(--rag-text-secondary) !important;
        opacity: 1 !important;
    }
    body.rag-dark div[data-testid="stExpander"] div[class*="st-key-sample_question_"] button,
    body.rag-dark div[data-testid="stExpander"] div[class*="st-key-quick_prompt_"] button {
        border-color: var(--rag-border) !important;
        background: var(--rag-bg-elevated) !important;
        color: var(--rag-text-secondary) !important;
        opacity: 1 !important;
    }
    body.rag-dark .answer-status-bar {
        border-color: var(--rag-border);
    }
    body.rag-dark .answer-status-chip,
    body.rag-dark .source-trace-chip,
    body.rag-dark .sidebar-row-meta {
        border-color: var(--rag-border) !important;
        background: var(--rag-bg-elevated) !important;
        color: var(--rag-text-secondary) !important;
    }
    body.rag-dark .answer-status-chip .ui-icon {
        color: var(--rag-blue-primary);
        stroke: currentColor;
    }
    body.rag-dark div[class*="st-key-clear_button"] button,
    body.rag-dark div[class*="st-key-stop_generation_button"] button {
        border-color: var(--rag-border) !important;
        background: var(--rag-bg-elevated) !important;
    }
    body.rag-dark div[class*="st-key-stop_generation_button"] button {
        border-color: var(--rag-red-border) !important;
        background: var(--rag-red-bg) !important;
        color: var(--rag-red-text) !important;
    }
    body.rag-dark div[class*="st-key-clear_button"] button:hover,
    body.rag-dark div[class*="st-key-stop_generation_button"] button:hover {
        border-color: var(--rag-red-border) !important;
        background: var(--rag-red-bg) !important;
        color: var(--rag-red-text) !important;
    }
    body.rag-dark div[class*="st-key-doc_delete_"] button:hover {
        border-color: var(--rag-red-border) !important;
        background: var(--rag-red-bg) !important;
        color: var(--rag-red-text) !important;
        box-shadow: 0 10px 22px rgba(239, 68, 68, 0.16) !important;
    }
    body.rag-dark .source-copy-btn {
        border-color: var(--rag-border);
        background: var(--rag-bg-elevated);
        color: var(--rag-blue-primary);
        box-shadow: var(--rag-shadow-sm);
    }
    body.rag-dark .source-index {
        border-color: var(--rag-border);
        background: var(--rag-bg-surface);
        color: var(--rag-text-secondary);
    }
    body.rag-dark .source-score {
        border-color: var(--rag-blue-200);
        background: rgba(96, 165, 250, 0.12);
        color: var(--rag-blue-primary);
    }
    body.rag-dark .source-label {
        color: var(--rag-text-placeholder);
    }
    body.rag-dark .source-copy-btn:hover {
        border-color: var(--rag-blue-200);
        background: var(--rag-bg-surface);
        box-shadow: 0 10px 22px rgba(0, 0, 0, 0.20);
    }
    body.rag-dark .source-copy-btn.copied {
        border-color: var(--rag-green-border);
        background: var(--rag-green-bg);
        color: var(--rag-green-text);
    }

    /* Upload queue and recovery controls */
    body.rag-dark .upload-flow-steps {
        background: transparent;
    }
    body.rag-dark .upload-step {
        border-color: var(--rag-border);
        background: var(--rag-bg-card);
        color: var(--rag-text-secondary);
        box-shadow: var(--rag-shadow-sm);
    }
    body.rag-dark .upload-step-index {
        border-color: var(--rag-border);
        background: var(--rag-bg-elevated);
        color: var(--rag-text-secondary);
    }
    body.rag-dark .upload-step.active {
        border-color: var(--rag-blue-200);
        background: var(--rag-bg-surface);
        color: var(--rag-blue-primary);
    }
    body.rag-dark .upload-step.active .upload-step-index {
        border-color: var(--rag-blue-200);
        background: var(--rag-blue-primary);
        color: #fff;
    }
    body.rag-dark .upload-step.done {
        border-color: var(--rag-green-border);
        background: var(--rag-green-bg);
    }
    body.rag-dark .upload-step.done .upload-step-index {
        border-color: var(--rag-green-border);
        background: var(--rag-green-bright);
        color: #fff;
    }
    body.rag-dark div[class*="st-key-upload_process_button"] button {
        border-color: var(--rag-blue-200) !important;
        background:
            radial-gradient(circle at 8% 0%, var(--rag-blue-glow), transparent 36%),
            linear-gradient(180deg, var(--rag-bg-card) 0%, var(--rag-bg-elevated) 100%) !important;
        color: var(--rag-blue-primary) !important;
        box-shadow: var(--rag-shadow-sm) !important;
    }
    body.rag-dark div[class*="st-key-upload_process_button"] button:hover {
        border-color: var(--rag-blue-300) !important;
        background:
            radial-gradient(circle at 8% 0%, var(--rag-blue-glow), transparent 38%),
            var(--rag-bg-surface) !important;
    }
    body.rag-dark [data-testid="stFileUploader"] section,
    body.rag-dark [data-testid="stFileUploaderDropzone"] {
        border-color: var(--rag-blue-300) !important;
        background:
            radial-gradient(circle at 8% 10%, rgba(37, 99, 235, 0.16), transparent 34%),
            var(--rag-bg-card) !important;
        color: var(--rag-text-secondary) !important;
    }
    body.rag-dark [data-testid="stFileUploader"] section p,
    body.rag-dark [data-testid="stFileUploader"] section small,
    body.rag-dark [data-testid="stFileUploader"] section span,
    body.rag-dark [data-testid="stFileUploaderDropzone"] p,
    body.rag-dark [data-testid="stFileUploaderDropzone"] small,
    body.rag-dark [data-testid="stFileUploaderDropzone"] span {
        color: var(--rag-text-secondary) !important;
        opacity: 1 !important;
    }
    body.rag-dark [data-testid="stFileUploader"] section svg,
    body.rag-dark [data-testid="stFileUploaderDropzone"] svg {
        color: var(--rag-text-secondary) !important;
        overflow: visible !important;
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
        fill: none !important;
        stroke: currentColor !important;
        opacity: 1 !important;
    }
    body.rag-dark [data-testid="stFileUploader"] section svg *,
    body.rag-dark [data-testid="stFileUploaderDropzone"] svg * {
        fill: none !important;
        stroke: currentColor !important;
    }
    body.rag-dark [data-testid="stFileUploader"] section svg rect,
    body.rag-dark [data-testid="stFileUploaderDropzone"] svg rect {
        stroke: none !important;
        fill: none !important;
    }
    body.rag-dark [data-testid="stFileUploader"] button,
    body.rag-dark [data-testid="stFileUploaderDropzone"] button {
        border-color: var(--rag-border) !important;
        background: var(--rag-bg-elevated) !important;
        color: var(--rag-text-primary) !important;
    }
    body.rag-dark .upload-task-row-native,
    body.rag-dark .upload-task-footer-native,
    body.rag-dark .upload-result-inline {
        border-color: var(--rag-border);
        background: var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
    }
    body.rag-dark .upload-task-row:hover {
        background: var(--rag-bg-surface);
    }
    body.rag-dark .upload-task-panel {
        border-color: var(--rag-border);
        background: var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
    }
    body.rag-dark .upload-task-summary span,
    body.rag-dark .upload-task-badge.waiting {
        border-color: var(--rag-border);
        background: var(--rag-bg-elevated);
        color: var(--rag-text-secondary);
    }
    body.rag-dark .upload-task-badge.processing,
    body.rag-dark .upload-task-summary span.processing {
        border-color: var(--rag-blue-200);
        background: var(--rag-blue-50);
        color: var(--rag-blue-primary);
    }
    /* Document cards, dialogs and sidebar menus */
    body.rag-dark .document-card,
    body.rag-dark .doc-toolbar,
    body.rag-dark .doc-confirm-panel,
    body.rag-dark .inline-confirm-panel,
    body.rag-dark .share-panel {
        border-color: var(--rag-border);
        background: var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
    }
    body.rag-dark .document-card-disabled {
        background: var(--rag-bg-elevated);
    }
    body.rag-dark [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"],
    body.rag-dark [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"],
    body.rag-dark [data-testid="stSidebar"] div[class*="st-key-collection_action_panel_"],
    body.rag-dark [data-testid="stSidebar"] div[class*="st-key-session_action_panel_"] {
        border-color: var(--rag-border);
        background: var(--rag-bg-card) !important;
        box-shadow: var(--rag-shadow-sm);
    }
    body.rag-dark [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"]:hover,
    body.rag-dark [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"]:hover,
    body.rag-dark [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"]:has(div[class*="st-key-collection_action_panel_"]),
    body.rag-dark [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"]:has(div[class*="st-key-session_action_panel_"]) {
        border-color: var(--rag-blue-200);
        background: var(--rag-bg-surface) !important;
    }
    body.rag-dark [data-testid="stSidebar"] div[class*="st-key-collection_row_more_"] button:hover,
    body.rag-dark [data-testid="stSidebar"] div[class*="st-key-session_row_more_"] button:hover {
        border-color: transparent !important;
        background: transparent !important;
        color: var(--rag-blue-light) !important;
        box-shadow: none !important;
    }
    body.rag-dark [data-testid="stSidebar"] div[class*="st-key-collection_action_panel_"] button:hover,
    body.rag-dark [data-testid="stSidebar"] div[class*="st-key-session_action_panel_"] button:hover {
        background: var(--rag-bg-surface) !important;
    }
    body.rag-dark .sidebar-section-copy {
        color: var(--rag-text-placeholder);
    }

    /* Dangerous confirmations must stay semantic without flashing light red. */
    body.rag-dark div[class*="st-key-confirm_delete_"] button:hover,
    body.rag-dark div[class*="st-key-batch_delete_confirm_yes"] button:hover,
    body.rag-dark div[class*="st-key-confirm_clear"] button:hover {
        border-color: var(--rag-red-border) !important;
        background: var(--rag-red-bg) !important;
        color: var(--rag-red-text) !important;
    }
"""
