"""Final mobile layout refinements for compact screens."""

MOBILE_REFINEMENT_CSS = """
    @media (max-width: 900px) {
        /* Sidebar stays usable on phones without covering the full viewport. */
        section[data-testid="stSidebar"] {
            width: min(86vw, 310px) !important;
            min-width: min(86vw, 310px) !important;
            max-width: min(86vw, 310px) !important;
        }
        section[data-testid="stSidebar"] > div:first-child {
            width: min(86vw, 310px) !important;
            min-width: min(86vw, 310px) !important;
            max-width: min(86vw, 310px) !important;
        }
        /*
         * The global shell hides Streamlit's header chrome. On compact screens
         * the sidebar is an overlay, so keep only its native collapse controls
         * interactive; otherwise an opened sidebar can trap the main content.
         */
        header[data-testid="stHeader"] {
            visibility: visible !important;
            background: transparent !important;
            pointer-events: none !important;
        }
        header[data-testid="stHeader"] > div {
            pointer-events: none !important;
        }
        header[data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarCollapsedControl"] {
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        header[data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stSidebarCollapsedControl"] button {
            width: 38px !important;
            min-width: 38px !important;
            height: 38px !important;
            min-height: 38px !important;
            border: 1px solid var(--rag-border) !important;
            border-radius: 13px !important;
            background: var(--rag-bg-card) !important;
            box-shadow: var(--rag-shadow-sm) !important;
        }

        /* Fixed composer: input on top, compact controls and prompt strip below. */
        div[class*="st-key-chat_input_area"] {
            left: var(--rag-chat-composer-left, 0.55rem) !important;
            bottom: max(0.55rem, env(safe-area-inset-bottom)) !important;
            width: var(--rag-chat-composer-width, calc(100vw - 1.1rem)) !important;
            padding: 7px 8px 6px !important;
            border-radius: 15px !important;
        }
        div[class*="st-key-chat_input_area"] div[data-testid="stHorizontalBlock"] {
            gap: 0.36rem !important;
        }
        div[class*="st-key-chat_input_area"] div[data-testid="stTextArea"] > div,
        div[class*="st-key-chat_input_area"] div[data-testid="stTextArea"] textarea {
            min-height: 38px !important;
            height: 38px !important;
        }
        div[class*="st-key-chat_input_area"] div[data-testid="stTextArea"] textarea {
            padding: 8px 10px !important;
            font-size: 0.82rem !important;
        }
        div[class*="st-key-send_button"] button,
        div[class*="st-key-clear_button"] button,
        div[class*="st-key-stop_generation_button"] button {
            min-width: 48px !important;
            height: 38px !important;
            min-height: 38px !important;
            padding: 0 0.3rem 0 1.18rem !important;
            border-radius: 11px !important;
            font-size: 0.68rem !important;
        }
        div[class*="st-key-send_button"] button::before,
        div[class*="st-key-clear_button"] button::before,
        div[class*="st-key-stop_generation_button"] button::before {
            left: 0.36rem !important;
            width: 11px !important;
            height: 11px !important;
        }
        div[class*="st-key-chat_prompt_tools"] {
            overflow-x: auto;
            overflow-y: hidden;
            padding-bottom: 0.1rem;
            scrollbar-width: none;
        }
        div[class*="st-key-chat_prompt_tools"]::-webkit-scrollbar {
            display: none;
        }
        div[class*="st-key-chat_prompt_tools"] > div {
            min-width: 630px;
        }
        .chat-prompt-strip,
        .chat-input-hint {
            white-space: nowrap;
        }
        .chat-input-hint kbd {
            padding: 0.04rem 0.28rem;
            font-size: 0.66rem;
        }
        .status-notice {
            gap: 0.52rem;
            padding: 0.62rem 0.68rem;
            border-radius: 14px;
        }
        .status-notice-icon {
            width: 28px;
            height: 28px;
            flex-basis: 28px;
            border-radius: 10px;
        }
        .status-notice-copy strong {
            font-size: 0.8rem;
        }
        .status-notice-copy small {
            font-size: 0.72rem;
        }

        /* Upload queue prioritizes readable file state over decoration. */
        .upload-task-header {
            gap: 0.48rem;
            padding: 0.72rem 0.76rem;
        }
        .upload-task-summary {
            justify-content: flex-start;
            gap: 0.28rem;
        }
        .upload-task-summary span {
            min-height: 23px;
            padding: 0.12rem 0.42rem;
            font-size: 0.72rem;
        }
        .upload-task-row-native {
            grid-template-columns: auto minmax(0, 1fr);
            gap: 0.56rem;
            min-height: 60px;
            padding: 0.66rem 3.55rem 0.66rem 0.72rem;
            border-radius: 15px;
        }
        .upload-task-row-native > div {
            min-width: 0;
        }
        .upload-task-icon {
            width: 34px;
            height: 34px;
            flex-basis: 34px;
            border-radius: 12px;
        }
        .upload-task-icon::before {
            width: 17px;
            height: 17px;
        }
        .upload-task-actions {
            grid-column: 2;
            justify-content: flex-start;
        }
        .upload-task-name {
            font-size: 0.84rem;
        }
        .upload-task-message,
        .upload-task-guidance {
            font-size: 0.72rem;
        }
        div[class*="st-key-upload_task_native_"] div[class*="st-key-upload_remove_visible_"] {
            right: 0.64rem !important;
        }
        /* Document management: preserve tap targets and prevent toolbar overflow. */
        .doc-toolbar {
            gap: 0.48rem;
            padding: 0.58rem 0.62rem;
        }
        .doc-toolbar-left {
            width: 100%;
            gap: 0.32rem;
        }
        .doc-status-pill,
        .doc-status-note {
            min-height: 25px;
            padding: 0.16rem 0.48rem;
            font-size: 0.72rem;
        }
        .doc-toolbar-info {
            padding: 0.2rem 0.48rem;
            font-size: 0.76rem;
        }
        div[class*="st-key-toolbar_"] button {
            min-height: 34px !important;
            padding: 0 0.42rem 0 1.58rem !important;
            font-size: 0.7rem !important;
        }
        div[class*="st-key-toolbar_"] button::before {
            left: 0.44rem !important;
            width: 12px !important;
            height: 12px !important;
        }
        .document-card {
            margin-bottom: 0.58rem;
            padding: 0.7rem 0.72rem;
            border-radius: 15px;
        }
        .document-card-header {
            gap: 0.58rem;
        }
        .document-card-icon {
            width: 34px;
            height: 34px;
            border-radius: 12px;
        }
        .document-card-icon::before {
            width: 17px;
            height: 17px;
        }
        .document-card-name {
            font-size: 0.86rem;
        }
        .document-card-meta {
            font-size: 0.72rem;
            overflow-wrap: anywhere;
        }
        div[class*="st-key-doc_sel_"] {
            min-height: 66px !important;
        }

        /* Tabs remain reachable instead of wrapping into an uneven stack. */
        div[data-testid="stTabs"] [role="tablist"] {
            overflow-x: auto !important;
            overflow-y: hidden !important;
            flex-wrap: nowrap !important;
            scrollbar-width: none;
        }
        div[data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar {
            display: none;
        }
        div[data-testid="stTabs"] button[role="tab"] {
            flex: 0 0 auto !important;
            padding: 0.56rem 0.68rem !important;
            font-size: 0.78rem !important;
            white-space: nowrap !important;
        }
    }

    @media (max-width: 560px) {
        /* Composer keeps the input readable while controls retain tap targets. */
        div[class*="st-key-chat_input_area"] form div[data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: minmax(0, 1fr) 56px 56px !important;
            gap: 0.3rem !important;
        }
        div[class*="st-key-chat_input_area"] form div[data-testid="stHorizontalBlock"] > div {
            width: auto !important;
            min-width: 0 !important;
        }
        .message-row {
            gap: 0.34rem;
            margin: 18px 0;
        }
        .avatar {
            width: 30px;
            height: 30px;
            border-radius: 12px;
            margin-inline: 1px;
        }
        .avatar::before {
            width: 15px;
            height: 15px;
        }
        .user-message,
        .ai-message,
        .source-evidence,
        .agent-debug-panel {
            max-width: calc(100% - 38px);
        }
        .user-message,
        .ai-message {
            padding: 11px 12px;
            border-radius: 17px;
            font-size: 0.88rem;
        }
        .rag-latest-answer-button {
            min-height: 31px;
            padding: 0.3rem 0.62rem 0.3rem 0.48rem;
            font-size: 0.7rem;
        }
        .rag-latest-answer-button i {
            width: 13px;
            height: 13px;
            flex-basis: 13px;
        }
        div[class*="st-key-chat_prompt_tools"] > div {
            min-width: 430px;
        }
        div[class*="st-key-chat_prompt_tools"] div[data-testid="stHtml"]:has(.chat-input-hint) {
            display: none !important;
        }

        /* Stack document controls on very narrow screens. */
        .doc-toolbar-hint {
            display: none;
        }
        div[class*="st-key-doc_filters"] div[data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: 1fr !important;
            gap: 0.42rem !important;
        }
        div[class*="st-key-doc_filters"] div[data-testid="stHorizontalBlock"] > div {
            width: 100% !important;
        }
        div[class*="st-key-doc_batch_actions"] div[data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
            gap: 0.42rem !important;
        }
        div[class*="st-key-doc_batch_actions"] div[data-testid="stHorizontalBlock"] > div {
            width: auto !important;
            min-width: 0 !important;
        }
        div[class*="st-key-doc_batch_actions"] div[data-testid="stHorizontalBlock"] > div:last-child {
            display: none !important;
        }

        /* Sidebar action panels stay inside the phone drawer. */
        [data-testid="stSidebar"] div[class*="st-key-collection_action_panel_"],
        [data-testid="stSidebar"] div[class*="st-key-session_action_panel_"] {
            right: 0.28rem !important;
            width: 126px !important;
            max-height: min(62vh, 280px);
            overflow-y: auto;
        }
        .app-hero-copy {
            font-size: 0.86rem;
        }
        .app-hero-tags {
            gap: 0.34rem;
        }
        .app-hero-tags span {
            padding: 0.24rem 0.48rem;
            font-size: 0.72rem;
        }
        .workspace-empty-heading {
            align-items: flex-start;
        }
        .workspace-empty-icon {
            width: 36px;
            height: 36px;
            flex-basis: 36px;
            border-radius: 13px;
        }
        .workspace-empty-title {
            font-size: 0.92rem;
        }
        .workspace-empty-copy {
            font-size: 0.8rem;
        }
        .source-evidence {
            max-width: calc(100% - 44px);
            margin-left: 44px;
        }
    }
"""
