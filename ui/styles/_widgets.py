"""Styles for widgets."""

WIDGETS_CSS = """
    span[data-testid="stIconMaterial"] {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .status-notice {
        display: flex;
        align-items: center;
        gap: 0.66rem;
        margin: 0.55rem 0;
        padding: 0.72rem 0.82rem;
        border: 1px solid var(--rag-border);
        border-radius: 16px;
        background: var(--rag-bg-card);
        color: var(--rag-text-secondary);
        box-shadow: var(--rag-shadow-sm);
    }
    .status-notice-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        flex: 0 0 32px;
        border-radius: 12px;
        border: 1px solid var(--rag-border);
        background: var(--rag-bg-elevated);
    }
    .status-notice-icon::before {
        content: "";
        width: 1rem;
        height: 1rem;
        display: block;
        background: currentColor;
        -webkit-mask: var(--status-icon-mask, var(--status-icon-info)) center / contain no-repeat;
        mask: var(--status-icon-mask, var(--status-icon-info)) center / contain no-repeat;
    }
    .status-notice-icon .ui-icon {
        width: 1rem;
        height: 1rem;
    }
    .status-notice {
        --status-icon-info: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='10' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='M12 16v-4M12 8h.01' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
        --status-icon-check_circle: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M22 11.1V12a10 10 0 1 1-5.9-9.1M22 4 12 14.01l-3-3' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
        --status-icon-block: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='10' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='m4.9 4.9 14.2 14.2' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
        --status-icon-warning: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0ZM12 9v4m0 4h.01' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
    }
    .status-icon-info { --status-icon-mask: var(--status-icon-info); }
    .status-icon-check_circle { --status-icon-mask: var(--status-icon-check_circle); }
    .status-icon-block { --status-icon-mask: var(--status-icon-block); }
    .status-icon-warning { --status-icon-mask: var(--status-icon-warning); }
    .status-notice-copy {
        display: grid;
        gap: 0.08rem;
        min-width: 0;
    }
    .status-notice-copy strong {
        color: var(--rag-text-primary);
        font-size: 0.86rem;
        font-weight: 860;
        line-height: 1.35;
    }
    .status-notice-copy small {
        color: var(--rag-text-placeholder);
        font-size: 0.78rem;
        line-height: 1.45;
    }
    .status-notice.info,
    .status-notice.success,
    .status-notice.warning,
    .status-notice.error {
        background:
            radial-gradient(circle at 0% 0%, var(--rag-blue-glow), transparent 38%),
            var(--rag-bg-card);
    }
    .status-notice.info .status-notice-icon {
        color: var(--rag-blue-primary);
        background: var(--rag-blue-50);
        border-color: var(--rag-blue-100);
    }
    .status-notice.success {
        border-color: var(--rag-green-border);
        background: var(--rag-green-bg);
    }
    .status-notice.success .status-notice-icon {
        color: var(--rag-green-text);
        background: var(--rag-bg-card);
        border-color: var(--rag-green-border);
    }
    .status-notice.warning {
        border-color: var(--rag-amber-border);
        background: var(--rag-amber-bg);
    }
    .status-notice.warning .status-notice-icon {
        color: var(--rag-amber-text);
        background: var(--rag-bg-card);
        border-color: var(--rag-amber-border);
    }
    .status-notice.error {
        border-color: var(--rag-red-border);
        background: var(--rag-red-bg);
    }
    .status-notice.error .status-notice-icon {
        color: var(--rag-red-text);
        background: var(--rag-bg-card);
        border-color: var(--rag-red-border);
    }

div[data-testid="stTextInput"] > div {
        border-radius: 12px !important;
        border: 1.5px solid var(--rag-border-strong) !important;
        background-color: var(--rag-bg-input) !important;
        box-shadow: none !important;
        overflow: hidden !important;
        height: 52px !important;
    }
    div[data-testid="stTextInput"] > div:focus-within {
        border-color: var(--rag-border-focus) !important;
        box-shadow: 0 0 0 3px var(--rag-blue-glow) !important;
    }
    div[data-testid="stTextInput"] input {
        border: none !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
        height: 52px !important;
        background-color: transparent !important;
        box-shadow: none !important;
        outline: none !important;
    }
    div[data-testid="stTextArea"] > div {
        border-radius: 12px !important;
        border: 1.5px solid var(--rag-border-strong) !important;
        background-color: var(--rag-bg-input) !important;
        box-shadow: none !important;
        overflow: hidden !important;
        min-height: 52px !important;
    }
    div[data-testid="stTextArea"] > div:focus-within {
        border-color: var(--rag-border-focus) !important;
        box-shadow: 0 0 0 3px var(--rag-blue-glow) !important;
    }
    div[data-testid="stTextArea"] textarea {
        border: none !important;
        padding: 13px 16px !important;
        font-size: 0.95rem !important;
        line-height: 1.45 !important;
        min-height: 52px !important;
        max-height: 156px !important;
        resize: none !important;
        overflow-y: hidden;
        background-color: transparent !important;
        box-shadow: none !important;
        outline: none !important;
    }
    div[data-testid="stNumberInput"] > div,
    div[data-testid="stSelectbox"] > div > div,
    div[data-testid="stSlider"] [data-baseweb="slider"] {
        border-radius: 14px !important;
    }
    div[data-testid="stNumberInput"] input {
        min-height: 46px !important;
        border-radius: 14px !important;
        background: var(--rag-bg-input) !important;
        color: var(--rag-text-primary) !important;
    }
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
        min-height: 46px !important;
        border-radius: 14px !important;
        border-color: var(--rag-border-strong) !important;
        background: var(--rag-bg-input) !important;
        color: var(--rag-text-primary) !important;
        box-shadow: var(--rag-shadow-sm) !important;
    }
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div:hover,
    div[data-testid="stNumberInput"] > div:focus-within {
        border-color: var(--rag-border-focus) !important;
        box-shadow: 0 0 0 3px var(--rag-blue-glow) !important;
    }
    div[data-testid="stSlider"] [data-baseweb="slider"] > div {
        color: var(--rag-blue-primary) !important;
    }
    div[data-testid="stSlider"] [role="slider"] {
        border-color: var(--rag-blue-primary) !important;
        box-shadow: 0 0 0 5px var(--rag-blue-glow) !important;
    }
    div[data-testid="stToggle"] {
        position: relative;
        padding: 0.48rem 0.58rem 0.48rem 0.72rem;
        border: 1px solid var(--rag-border);
        border-radius: 16px;
        background:
            linear-gradient(90deg, rgba(37, 99, 235, 0.05), transparent 58%),
            var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
        transition: border-color 0.18s ease, background 0.18s ease, transform 0.18s ease;
    }
    div[data-testid="stToggle"]::before {
        content: "";
        position: absolute;
        left: 0;
        top: 12px;
        bottom: 12px;
        width: 3px;
        border-radius: 999px;
        background: var(--rag-blue-300);
        opacity: 0.7;
    }
    div[data-testid="stToggle"]:hover {
        transform: translateY(-1px);
        border-color: var(--rag-blue-200);
        background:
            linear-gradient(90deg, rgba(37, 99, 235, 0.08), transparent 60%),
            var(--rag-blue-50);
        box-shadow: var(--rag-shadow-card);
    }
    div[data-testid="stToggle"] label {
        gap: 0.55rem !important;
    }
    div[data-testid="stToggle"] p {
        font-weight: 820 !important;
        color: var(--rag-text-primary) !important;
    }
    div[data-testid="stCheckbox"] label,
    div[data-testid="stRadio"] label {
        color: var(--rag-text-secondary) !important;
        font-weight: 720 !important;
        min-height: 32px;
        align-items: center !important;
    }
    div[data-testid="stCheckbox"] [data-testid="stMarkdownContainer"],
    div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] {
        line-height: 1.35 !important;
    }
    div[data-testid="stCheckbox"] input,
    div[data-testid="stRadio"] input {
        accent-color: var(--rag-blue-primary);
    }
    div[data-testid="stCheckbox"] input:focus-visible,
    div[data-testid="stRadio"] input:focus-visible {
        outline: 3px solid var(--rag-blue-glow) !important;
        outline-offset: 2px !important;
    }
    div[data-testid="stCheckbox"]:hover label,
    div[data-testid="stRadio"] label:hover {
        color: var(--rag-blue-primary) !important;
    }
    div[data-testid="stExpander"] details {
        overflow: hidden;
        border: 1px solid var(--rag-border) !important;
        border-radius: 18px !important;
        background: var(--rag-bg-card) !important;
        box-shadow: var(--rag-shadow-sm) !important;
    }
    div[data-testid="stExpander"] summary {
        min-height: 46px;
        padding: 0.78rem 0.95rem !important;
        color: var(--rag-text-primary) !important;
        font-weight: 850 !important;
    }
    div[data-testid="stExpander"] summary:hover {
        background: var(--rag-bg-elevated) !important;
    }
    div[data-testid="stExpander"] details > div[role="region"] {
        padding: 0.2rem 0.95rem 0.95rem !important;
        color: var(--rag-text-secondary);
    }
    div[data-testid="stWidgetLabel"] p {
        color: var(--rag-text-secondary) !important;
        font-weight: 780 !important;
    }
    [data-testid="stFileUploader"],
    [data-testid="stFileUploaderDropzone"] {
        border-radius: 18px !important;
    }
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploaderDropzone"] {
        min-height: 94px !important;
        border: 1.5px dashed var(--rag-blue-200) !important;
        background:
            radial-gradient(circle at 8% 10%, var(--rag-blue-glow), transparent 32%),
            var(--rag-blue-50-gradient) !important;
        transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease !important;
    }
    [data-testid="stFileUploader"] section:hover,
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--rag-blue-400) !important;
        box-shadow: 0 14px 32px var(--rag-blue-glow) !important;
        transform: translateY(-1px);
    }
    [data-testid="stFileUploader"] section svg,
    [data-testid="stFileUploaderDropzone"] svg {
        overflow: visible !important;
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
    }
    [data-testid="stFileUploader"] section svg rect,
    [data-testid="stFileUploaderDropzone"] svg rect {
        stroke: none !important;
        fill: none !important;
    }

    /* 侧边栏输入框样式 */
    [data-testid="stSidebar"] div[data-testid="stTextInput"] > div {
        border-radius: 8px !important;
        border: 1px solid var(--rag-border-strong) !important;
        background-color: var(--rag-bg-input) !important;
        height: 40px !important;
    }
    [data-testid="stSidebar"] div[data-testid="stTextInput"] > div:focus-within {
        border-color: var(--rag-border-focus) !important;
        box-shadow: 0 0 0 2px var(--rag-blue-glow) !important;
    }
    [data-testid="stSidebar"] div[data-testid="stTextInput"] input {
        padding: 8px 12px !important;
        font-size: 0.9rem !important;
        height: 40px !important;
    }

    /* 隐藏 "Press Enter to apply" 提示 */
    div[data-testid="stTextInput"] div[data-testid="InputInstructions"],
    div[data-testid="stTextArea"] div[data-testid="InputInstructions"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* 按钮样式 - 现代风格 */
    .stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        border-radius: 14px !important;
        transition: all 0.2s !important;
        font-weight: 760 !important;
        height: 52px !important;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        min-width: 52px !important;
        border-color: var(--rag-border) !important;
        box-shadow: var(--rag-shadow-sm) !important;
    }
    .stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .stButton > button:disabled,
    div[data-testid="stFormSubmitButton"] > button:disabled {
        opacity: 0.54;
        cursor: not-allowed;
        transform: none;
        filter: grayscale(0.08);
        box-shadow: none !important;
    }
    .stButton > button:focus-visible,
    div[data-testid="stFormSubmitButton"] > button:focus-visible,
    div[data-testid="stDownloadButton"] > button:focus-visible {
        outline: 3px solid var(--rag-blue-glow) !important;
        outline-offset: 2px !important;
        border-color: var(--rag-border-focus) !important;
    }
    div[data-testid="stAlert"] {
        position: relative;
        overflow: hidden;
        border-radius: 16px !important;
        border: 1px solid var(--rag-blue-200) !important;
        background:
            radial-gradient(circle at 0% 0%, var(--rag-blue-glow), transparent 34%),
            var(--rag-bg-card) !important;
        box-shadow: var(--rag-shadow-sm) !important;
    }
    div[data-testid="stAlert"] p {
        line-height: 1.55 !important;
        color: var(--rag-text-primary) !important;
    }

    /* 问答输入表单：去掉默认边框并让三列底部对齐 */
    div[data-testid="stDownloadButton"] > button {
        min-height: 48px !important;
        white-space: nowrap !important;
        border-radius: 14px !important;
        border: 1px solid var(--rag-blue-200) !important;
        background:
            radial-gradient(circle at 10% 0%, var(--rag-blue-glow), transparent 45%),
            var(--rag-bg-card) !important;
        color: var(--rag-blue-primary) !important;
        box-shadow: var(--rag-shadow-sm) !important;
        font-weight: 780 !important;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background: var(--rag-blue-50) !important;
        border-color: var(--rag-blue-200) !important;
        box-shadow: 0 8px 20px var(--rag-blue-glow) !important;
    }
    div[data-testid="stDownloadButton"] > button p,
    div[data-testid="stDownloadButton"] > button span {
        white-space: nowrap !important;
    }
    div[class*="st-key-chat_export_"] button {
        position: relative !important;
        min-height: 46px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 0.58rem !important;
        padding: 0 0.9rem 0 3rem !important;
        border-color: var(--rag-blue-200) !important;
        background:
            radial-gradient(circle at 8% 0%, var(--rag-blue-glow), transparent 48%),
            var(--rag-bg-card) !important;
        color: var(--rag-text-primary) !important;
        box-shadow: var(--rag-shadow-sm) !important;
    }
    div[class*="st-key-chat_export_"] button:hover {
        border-color: var(--rag-blue-300) !important;
        background: var(--rag-blue-50) !important;
        color: var(--rag-blue-primary) !important;
        box-shadow: 0 10px 24px var(--rag-blue-glow) !important;
    }
    div[class*="st-key-chat_export_"] button::before {
        content: "";
        position: absolute;
        left: 1rem;
        top: 50%;
        width: 18px;
        height: 18px;
        flex: 0 0 18px;
        transform: translateY(-50%);
        background: var(--rag-blue-primary);
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z' fill='none' stroke='black' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M14 2v6h6M8 13h8M8 17h6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z' fill='none' stroke='black' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M14 2v6h6M8 13h8M8 17h6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    div[class*="st-key-chat_export_"] button p {
        position: absolute !important;
        left: 3rem !important;
        top: 50% !important;
        width: auto !important;
        margin: 0 !important;
        flex: 0 0 auto !important;
        transform: translateY(-50%) !important;
        text-align: left !important;
    }
    div[class*="st-key-chat_export_"] button > div {
        display: flex !important;
        width: auto !important;
        margin: 0 !important;
        align-items: center !important;
        justify-content: flex-start !important;
    }
    div[class*="st-key-chat_export_pdf"] button::before {
        background: var(--rag-red-text);
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z' fill='none' stroke='black' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M14 2v6h6' fill='none' stroke='black' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M8 16v-5h1.5a1.5 1.5 0 0 1 0 3H8m5 2v-5h1.2c1.4 0 2.3 1 2.3 2.5S15.6 16 14.2 16Zm6-5v5m0-5h2.8m-2.8 2h2.2' fill='none' stroke='black' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z' fill='none' stroke='black' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M14 2v6h6' fill='none' stroke='black' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M8 16v-5h1.5a1.5 1.5 0 0 1 0 3H8m5 2v-5h1.2c1.4 0 2.3 1 2.3 2.5S15.6 16 14.2 16Zm6-5v5m0-5h2.8m-2.8 2h2.2' fill='none' stroke='black' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }

    .doc-confirm-panel,
    .inline-confirm-panel,
    .share-panel {
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: flex-start;
        gap: 0.8rem;
        margin: 0.2rem 0 0.9rem;
        padding: 1rem;
        border: 1px solid var(--rag-border);
        border-radius: 20px;
        background:
            radial-gradient(circle at 94% 0%, var(--rag-blue-glow), transparent 32%),
            linear-gradient(180deg, var(--rag-bg-card), var(--rag-bg-elevated));
        box-shadow: var(--rag-shadow-card);
    }
    .doc-confirm-panel::after,
    .share-panel::after {
        content: "";
        position: absolute;
        right: -28px;
        top: -28px;
        width: 82px;
        height: 82px;
        border-radius: 999px;
        background: var(--rag-blue-50);
        opacity: 0.72;
        pointer-events: none;
    }
    .doc-confirm-icon {
        display: inline-grid;
        place-items: center;
        width: 42px;
        height: 42px;
        border-radius: 16px;
        border: 1px solid var(--rag-red-border);
        background: var(--rag-red-bg);
        color: var(--rag-red-text);
        flex: 0 0 auto;
    }
    .doc-confirm-icon .ui-icon,
    .share-panel-title .ui-icon,
    .inline-confirm-title .ui-icon {
        width: 1rem;
        height: 1rem;
    }
    .doc-confirm-title,
    .inline-confirm-title,
    .share-panel-title {
        color: var(--rag-text-primary);
        font-size: 1rem;
        font-weight: 900;
        line-height: 1.38;
    }
    .inline-confirm-title,
    .share-panel-title {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
    }
    .doc-confirm-copy,
    .inline-confirm-copy,
    .share-panel-copy {
        margin-top: 0.22rem;
        color: var(--rag-text-muted);
        font-size: 0.88rem;
        line-height: 1.65;
    }
    .doc-confirm-hint {
        display: inline-flex;
        margin-top: 0.54rem;
        padding: 0.32rem 0.62rem;
        border: 1px solid var(--rag-amber-border);
        border-radius: 999px;
        background: var(--rag-amber-bg);
        color: var(--rag-amber-text);
        font-size: 0.78rem;
        font-weight: 780;
    }
    .inline-confirm-panel {
        align-items: center;
        border-radius: 18px;
        background: var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
    }
    .inline-confirm-panel.danger {
        border-color: var(--rag-red-border);
        background:
            radial-gradient(circle at 100% 0%, rgba(239, 68, 68, 0.1), transparent 32%),
            var(--rag-bg-card);
    }
    .inline-confirm-panel.danger .inline-confirm-title,
    .inline-confirm-panel.danger .inline-confirm-title .ui-icon {
        color: var(--rag-red-text);
    }
    .share-panel {
        display: block;
        padding-right: 4.2rem;
        border-color: var(--rag-blue-200);
    }
    .share-panel-title {
        color: var(--rag-blue-primary);
    }
    .share-panel-copy {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        max-width: 100%;
    }
    .stProgress {
        margin: 0.6rem 0 0.9rem;
    }
    .stProgress > div {
        height: 8px !important;
        border-radius: 999px !important;
        background: var(--rag-bg-elevated) !important;
        overflow: hidden !important;
        box-shadow: inset 0 0 0 1px var(--rag-border);
    }
    .stProgress > div > div {
        border-radius: 999px !important;
        background:
            linear-gradient(90deg, var(--rag-blue-primary), var(--rag-blue-light)) !important;
        box-shadow: 0 0 18px var(--rag-blue-glow);
    }
    div[class*="st-key-confirm_delete_"] button,
    div[class*="st-key-batch_delete_confirm_yes"] button,
    div[class*="st-key-confirm_clear"] button {
        border-color: var(--rag-red-border) !important;
        background: var(--rag-red-text) !important;
        color: #ffffff !important;
        box-shadow: 0 10px 24px rgba(239, 68, 68, 0.2) !important;
    }
    div[class*="st-key-confirm_delete_"] button:hover,
    div[class*="st-key-batch_delete_confirm_yes"] button:hover,
    div[class*="st-key-confirm_clear"] button:hover {
        border-color: #ef4444 !important;
        background: #dc2626 !important;
        box-shadow: 0 14px 28px rgba(239, 68, 68, 0.28) !important;
    }
    div[class*="st-key-cancel_delete_"] button,
    div[class*="st-key-batch_delete_confirm_no"] button,
    div[class*="st-key-cancel_clear"] button,
    div[class*="st-key-share_close_"] button {
        border-color: var(--rag-border) !important;
        background: var(--rag-bg-card) !important;
        color: var(--rag-text-muted) !important;
        box-shadow: var(--rag-shadow-sm) !important;
    }
    div[class*="st-key-share_copy_"] button,
    div[class*="st-key-share_download_"] button {
        min-height: 42px !important;
        border-radius: 13px !important;
    }

    div[data-testid="stForm"] {
        border: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] {
        align-items: flex-end !important;
    }

    /* 流式输出光标 */
    .typing-cursor::after {
        content: "|";
        animation: blink 1s infinite;
        color: var(--rag-blue-light);
        font-weight: bold;
    }
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }

    /* 顶部主题切换 */
    div[class*="st-key-theme_toggle_btn"] button {
        position: relative;
        border-radius: 999px !important;
        height: 40px !important;
        min-width: 96px !important;
        padding-left: 2.2rem !important;
        border: 1px solid var(--rag-blue-200) !important;
        background:
            radial-gradient(circle at 15% 0%, var(--rag-blue-glow), transparent 45%),
            var(--rag-bg-card) !important;
        color: var(--rag-blue-light) !important;
        box-shadow: var(--rag-shadow-sm) !important;
    }
    div[class*="st-key-theme_toggle_btn"] button::before {
        content: "";
        position: absolute;
        left: 1rem;
        top: 50%;
        width: 15px;
        height: 15px;
        transform: translateY(-50%);
        background: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M21 12.8A8.5 8.5 0 1 1 11.2 3a6.7 6.7 0 0 0 9.8 9.8Z'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M21 12.8A8.5 8.5 0 1 1 11.2 3a6.7 6.7 0 0 0 9.8 9.8Z'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    body.rag-dark div[class*="st-key-theme_toggle_btn"] button::before {
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32 1.41 1.41M2 12h2m16 0h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41M12 8a4 4 0 1 0 0 8a4 4 0 0 0 0-8Z'/%3E%3C/svg%3E");
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32 1.41 1.41M2 12h2m16 0h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41M12 8a4 4 0 1 0 0 8a4 4 0 0 0 0-8Z'/%3E%3C/svg%3E");
    }
    div[data-testid="stTabs"] [role="tablist"] {
        gap: 0.36rem;
        padding: 0.28rem;
        border: 1px solid var(--rag-border);
        border-radius: 16px;
        background:
            radial-gradient(circle at 8% 0%, var(--rag-blue-glow), transparent 34%),
            var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
        margin-bottom: 0.95rem;
    }
    div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
    div[data-testid="stTabs"] [data-baseweb="tab-border"] {
        display: none !important;
    }
    div[data-testid="stTabs"] button[role="tab"] {
        position: relative;
        min-height: 38px !important;
        padding: 0.44rem 0.86rem 0.44rem 2rem !important;
        border-radius: 12px !important;
        color: var(--rag-text-placeholder) !important;
        font-weight: 780 !important;
        transition: color 0.18s ease, background-color 0.18s ease, box-shadow 0.18s ease !important;
    }
    div[data-testid="stTabs"] button[role="tab"]::before {
        content: "";
        position: absolute;
        left: 0.82rem;
        top: 50%;
        width: 14px;
        height: 14px;
        transform: translateY(-50%);
        background: currentColor;
        opacity: 0.9;
        -webkit-mask: center / contain no-repeat;
        mask: center / contain no-repeat;
    }
    div[data-testid="stTabs"] button[role="tab"]:nth-of-type(1)::before {
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 3v12m5-7-5-5-5 5m14 7v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4'/%3E%3C/svg%3E");
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 3v12m5-7-5-5-5 5m14 7v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4'/%3E%3C/svg%3E");
    }
    div[data-testid="stTabs"] button[role="tab"]:nth-of-type(2)::before {
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z'/%3E%3C/svg%3E");
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z'/%3E%3C/svg%3E");
    }
    div[data-testid="stTabs"] button[role="tab"]:nth-of-type(3)::before {
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m12 2 9 5-9 5-9-5Zm-9 10 9 5 9-5m-18 5 9 5 9-5'/%3E%3C/svg%3E");
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m12 2 9 5-9 5-9-5Zm-9 10 9 5 9-5m-18 5 9 5 9-5'/%3E%3C/svg%3E");
    }
    div[data-testid="stTabs"] button[role="tab"]:nth-of-type(4)::before {
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 15.5A3.5 3.5 0 1 0 12 8a3.5 3.5 0 0 0 0 7.5ZM19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06A1.7 1.7 0 0 0 15 19.4a1.7 1.7 0 0 0-1 .6a1.7 1.7 0 0 0-.4 1.1V21a2 2 0 1 1-4 0v-.09a1.7 1.7 0 0 0-.4-1.1a1.7 1.7 0 0 0-1-.6a1.7 1.7 0 0 0-1.88.34l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-.6-1a1.7 1.7 0 0 0-1.1-.4H3a2 2 0 1 1 0-4h.09a1.7 1.7 0 0 0 1.1-.4a1.7 1.7 0 0 0 .6-1a1.7 1.7 0 0 0-.34-1.88l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-.6a1.7 1.7 0 0 0 .4-1.1V3a2 2 0 1 1 4 0v.09a1.7 1.7 0 0 0 .4 1.1a1.7 1.7 0 0 0 1 .6a1.7 1.7 0 0 0 1.88-.34l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.7 1.7 0 0 0 19.4 9c.2.4.5.7.9.9c.3.2.7.3 1.1.3h.1a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.1.4c-.4.2-.7.5-.9.9Z'/%3E%3C/svg%3E");
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 15.5A3.5 3.5 0 1 0 12 8a3.5 3.5 0 0 0 0 7.5ZM19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06A1.7 1.7 0 0 0 15 19.4a1.7 1.7 0 0 0-1 .6a1.7 1.7 0 0 0-.4 1.1V21a2 2 0 1 1-4 0v-.09a1.7 1.7 0 0 0-.4-1.1a1.7 1.7 0 0 0-1-.6a1.7 1.7 0 0 0-1.88.34l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-.6-1a1.7 1.7 0 0 0-1.1-.4H3a2 2 0 1 1 0-4h.09a1.7 1.7 0 0 0 1.1-.4a1.7 1.7 0 0 0 .6-1a1.7 1.7 0 0 0-.34-1.88l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-.6a1.7 1.7 0 0 0 .4-1.1V3a2 2 0 1 1 4 0v.09a1.7 1.7 0 0 0 .4 1.1a1.7 1.7 0 0 0 1 .6a1.7 1.7 0 0 0 1.88-.34l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.7 1.7 0 0 0 19.4 9c.2.4.5.7.9.9c.3.2.7.3 1.1.3h.1a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.1.4c-.4.2-.7.5-.9.9Z'/%3E%3C/svg%3E");
    }
    div[data-testid="stTabs"] button[role="tab"]:hover {
        background: var(--rag-bg-elevated) !important;
        color: var(--rag-blue-primary) !important;
    }
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background: var(--rag-blue-50) !important;
        color: var(--rag-blue-primary) !important;
        box-shadow: inset 0 0 0 1px var(--rag-blue-100), var(--rag-shadow-sm) !important;
    }
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"]::after {
        content: "";
        position: absolute;
        left: 0.86rem;
        top: 50%;
        width: 4px;
        height: 4px;
        border-radius: 999px;
        background: var(--rag-blue-primary);
        transform: translateY(-50%);
        box-shadow: 0 0 0 4px var(--rag-blue-glow);
        opacity: 0.78;
    }
    div[class*="st-key-doc_delete_"] button {
        min-height: 38px !important;
        height: 38px !important;
        max-width: 168px !important;
        margin-left: auto !important;
        border-radius: 12px !important;
        border-color: var(--rag-red-border) !important;
        background: var(--rag-red-bg) !important;
        color: var(--rag-red-text) !important;
        box-shadow: none !important;
    }
    div[class*="st-key-doc_delete_"] button:hover {
        background: #fee2e2 !important;
        border-color: #fca5a5 !important;
        color: #991b1b !important;
    }
    div[class*="st-key-doc_delete_"] {
        margin-top: -0.35rem !important;
        margin-bottom: 0.35rem !important;
        display: flex !important;
        justify-content: flex-end !important;
    }
    div[class*="st-key-toolbar_select_all"] button,
    div[class*="st-key-toolbar_delete"] button,
    div[class*="st-key-toolbar_disable"] button,
    div[class*="st-key-toolbar_enable"] button {
        position: relative !important;
        width: 100% !important;
        min-height: 34px !important;
        height: 34px !important;
        padding: 0 0.5rem 0 1.82rem !important;
        border-radius: 11px !important;
        justify-content: flex-start !important;
        white-space: nowrap !important;
        font-size: 0.76rem !important;
        font-weight: 760 !important;
        box-shadow: none !important;
    }
    div[class*="st-key-toolbar_"] button p {
        margin: 0 !important;
        white-space: nowrap !important;
        line-height: 1 !important;
    }
    div[class*="st-key-toolbar_select_all"] button::before,
    div[class*="st-key-toolbar_delete"] button::before,
    div[class*="st-key-toolbar_disable"] button::before,
    div[class*="st-key-toolbar_enable"] button::before {
        content: "";
        position: absolute;
        left: 0.58rem;
        top: 50%;
        width: 13px;
        height: 13px;
        transform: translateY(-50%);
        background: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='4' y='4' width='6' height='6' rx='1' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='M14 7h6M4 17h6M14 17h6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='4' y='4' width='6' height='6' rx='1' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='M14 7h6M4 17h6M14 17h6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    div[class*="st-key-toolbar_delete"] button::before {
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6M10 11v6M14 11v6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6M10 11v6M14 11v6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    div[class*="st-key-toolbar_disable"] button::before {
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='9' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='m5.6 5.6 12.8 12.8' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='9' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='m5.6 5.6 12.8 12.8' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    div[class*="st-key-toolbar_enable"] button::before {
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='9' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='m8 12 2.6 2.6L16.5 9' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='9' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='m8 12 2.6 2.6L16.5 9' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    div[class*="st-key-toolbar_select_all"] button {
        border-color: var(--rag-blue-200) !important;
        background: var(--rag-blue-50) !important;
        color: var(--rag-blue-primary) !important;
    }
    div[class*="st-key-toolbar_delete"] button {
        border-color: var(--rag-red-border) !important;
        background: var(--rag-red-bg) !important;
        color: var(--rag-red-text) !important;
    }
    div[class*="st-key-toolbar_disable"] button {
        border-color: var(--rag-amber-border) !important;
        background: var(--rag-amber-bg) !important;
        color: var(--rag-amber-text) !important;
    }
    div[class*="st-key-toolbar_enable"] button {
        border-color: var(--rag-green-border) !important;
        background: var(--rag-green-bg) !important;
        color: var(--rag-green-text) !important;
    }
    div[class*="st-key-doc_sel_"] {
        min-height: 78px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-end !important;
        padding-right: 0 !important;
    }
    div[class*="st-key-doc_sel_"] div[data-testid="stCheckbox"] {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-end !important;
        margin: 0 !important;
    }
    div[class*="st-key-doc_sel_"] label {
        min-height: 20px !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    [data-testid="stSidebar"] .stTextInput label p,
    [data-testid="stSidebar"] .stTextArea label p,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    [data-testid="stSidebar"] .stCaption {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        color: var(--rag-text-placeholder) !important;
    }
    [data-testid="stSidebar"] div[data-testid="stTextInput"] input {
        min-height: 40px !important;
        border-radius: 12px !important;
        font-size: 0.95rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
    }
    [data-testid="stSidebar"] .stButton > button,
    [data-testid="stSidebar"] div[data-testid="stFormSubmitButton"] > button {
        min-height: 38px !important;
        padding: 0.42rem 0.8rem !important;
        border-radius: 12px !important;
        border: 1px solid var(--rag-blue-200) !important;
        background: var(--rag-bg-elevated) !important;
        color: var(--rag-text-primary) !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        box-shadow: var(--rag-shadow-sm) !important;
        transition: background-color 0.18s ease, border-color 0.18s ease, color 0.18s ease, box-shadow 0.18s ease !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover,
    [data-testid="stSidebar"] div[data-testid="stFormSubmitButton"] > button:hover {
        background: var(--rag-bg-card) !important;
        border-color: var(--rag-border-strong) !important;
        color: var(--rag-text-primary) !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08) !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"],
    [data-testid="stSidebar"] div[data-testid="stFormSubmitButton"] > button[kind="primary"],
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"] button,
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"] button {
        background: var(--rag-blue-50) !important;
        border-color: var(--rag-blue-200) !important;
        color: var(--rag-blue-primary) !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"] button:hover,
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"] button:hover {
        background: var(--rag-blue-100) !important;
        border-color: var(--rag-blue-300) !important;
        color: var(--rag-blue-primary) !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"] div,
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"] div {
        background: transparent !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"] .stButton > button,
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"] .stButton > button,
    [data-testid="stSidebar"] div[class*="st-key-collection_row_select_"] button,
    [data-testid="stSidebar"] div[class*="st-key-session_row_select_"] button,
    [data-testid="stSidebar"] div[class*="st-key-collection_row_more_"] button,
    [data-testid="stSidebar"] div[class*="st-key-session_row_more_"] button {
        border: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_row_select_"] button,
    [data-testid="stSidebar"] div[class*="st-key-session_row_select_"] button {
        width: 100% !important;
        height: 42px !important;
        min-height: 42px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        text-align: left !important;
        line-height: 1 !important;
        padding-left: 2.35rem !important;
        padding-right: 2.65rem !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_row_select_"] button p,
    [data-testid="stSidebar"] div[class*="st-key-session_row_select_"] button p {
        width: 100% !important;
        margin: 0 !important;
        overflow: hidden !important;
        line-height: 1.2 !important;
        text-align: left !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_row_more_"],
    [data-testid="stSidebar"] div[class*="st-key-session_row_more_"] {
        position: absolute !important;
        top: 0 !important;
        right: 0.58rem !important;
        z-index: 4 !important;
        display: flex !important;
        width: 30px !important;
        height: 42px !important;
        align-items: center !important;
        justify-content: flex-start !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_row_more_"] button,
    [data-testid="stSidebar"] div[class*="st-key-session_row_more_"] button {
        width: 30px !important;
        height: 42px !important;
        min-height: 42px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        line-height: 1 !important;
        margin: 0 !important;
        color: var(--rag-text-placeholder) !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_row_more_"] button p,
    [data-testid="stSidebar"] div[class*="st-key-session_row_more_"] button p {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        height: 42px !important;
        margin: 0 !important;
        line-height: 1 !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"],
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"] {
        background: var(--rag-bg-elevated) !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"]::before,
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"]::before {
        content: "";
        position: absolute;
        top: 50%;
        left: 0.78rem;
        width: 16px;
        height: 16px;
        z-index: 3;
        transform: translateY(-50%);
        background: var(--rag-text-placeholder);
        pointer-events: none;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='5' y='3' width='14' height='18' rx='2' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='M8 8h8M8 12h8M8 16h5' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='5' y='3' width='14' height='18' rx='2' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='M8 8h8M8 12h8M8 16h5' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"]::before {
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4z' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4z' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"]:hover,
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"]:hover,
    [data-testid="stSidebar"] div[class*="st-key-collection_item_wrap_"]:has(div[class*="st-key-collection_action_panel_"]),
    [data-testid="stSidebar"] div[class*="st-key-session_item_wrap_"]:has(div[class*="st-key-session_action_panel_"]) {
        background: var(--rag-blue-50) !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"] button,
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"] button,
    [data-testid="stSidebar"] div[class*="st-key-confirm_delete_"] button,
    [data-testid="stSidebar"] div[class*="st-key-cancel_delete_"] button,
    [data-testid="stSidebar"] div[data-testid="stFormSubmitButton"] > button {
        min-height: 40px !important;
    }
    [data-testid="stSidebar"] .stButton > button p,
    [data-testid="stSidebar"] div[data-testid="stFormSubmitButton"] > button p,
    [data-testid="stSidebar"] .stButton > button span,
    [data-testid="stSidebar"] div[data-testid="stFormSubmitButton"] > button span {
        font-size: 0.92rem !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"],
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"],
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        width: 100% !important;
        margin: 0.48rem 0 !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"] button,
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"] button,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        width: 100% !important;
        min-height: 44px !important;
        height: 44px !important;
        padding: 0 0.9rem !important;
        border-radius: 15px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.55rem !important;
        font-size: 0.92rem !important;
        font-weight: 780 !important;
        letter-spacing: 0.01em !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"] button p,
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"] button p {
        position: absolute !important;
        left: 2.7rem !important;
        top: 50% !important;
        width: auto !important;
        margin: 0 !important;
        flex: 0 0 auto !important;
        transform: translateY(-50%) !important;
        text-align: left !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"] button > div,
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"] button > div {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 0.55rem !important;
        width: auto !important;
        margin: 0 !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"] button {
        border-color: var(--rag-blue-200) !important;
        background:
            radial-gradient(circle at 12% 0%, var(--rag-blue-glow), transparent 48%),
            var(--rag-blue-50) !important;
        color: var(--rag-blue-primary) !important;
        box-shadow: var(--rag-shadow-sm) !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"] button:hover {
        border-color: var(--rag-blue-300) !important;
        background: var(--rag-blue-100) !important;
        color: var(--rag-blue-primary) !important;
        box-shadow: 0 10px 22px var(--rag-blue-glow) !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"] button {
        border-color: var(--rag-blue-200) !important;
        background:
            radial-gradient(circle at 10% 0%, var(--rag-blue-glow), transparent 46%),
            var(--rag-blue-50) !important;
        color: var(--rag-blue-primary) !important;
        box-shadow: var(--rag-shadow-sm) !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"] button:hover {
        border-color: var(--rag-blue-300) !important;
        background: var(--rag-blue-100) !important;
        color: var(--rag-blue-primary) !important;
        box-shadow: 0 10px 22px var(--rag-blue-glow) !important;
    }
    [data-testid="stSidebar"] div[class*="st-key-create_collection_btn"] button::before,
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"] button::before,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary::before {
        content: "";
        position: absolute;
        left: 1rem;
        top: 50%;
        width: 16px;
        height: 16px;
        flex: 0 0 16px;
        transform: translateY(-50%);
        background: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 5v14M5 12h14' fill='none' stroke='black' stroke-width='2.2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 5v14M5 12h14' fill='none' stroke='black' stroke-width='2.2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    [data-testid="stSidebar"] div[class*="st-key-new_session_btn"] button::before {
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3Cpath d='M18 2v6M15 5h6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3Cpath d='M18 2v6M15 5h6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] summary::before {
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='9' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='M9.8 9a2.4 2.4 0 1 1 4.2 1.6c-.9.8-2 1.3-2 2.9M12 17h.01' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='9' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='M9.8 9a2.4 2.4 0 1 1 4.2 1.6c-.9.8-2 1.3-2 2.9M12 17h.01' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        border: none !important;
        background: transparent !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] details {
        border: 1px solid var(--rag-border) !important;
        border-radius: 15px !important;
        background: var(--rag-bg-card) !important;
        overflow: hidden !important;
        box-shadow: var(--rag-shadow-sm) !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        min-height: 44px !important;
        height: 44px !important;
        padding: 0 0.9rem !important;
        font-size: 0.94rem !important;
        font-weight: 780 !important;
        color: var(--rag-text-primary) !important;
        display: flex !important;
        align-items: center !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
        background: var(--rag-bg-card) !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] details > div[role="region"] {
        padding: 0.1rem 0.95rem 0.85rem !important;
        color: var(--rag-text-muted) !important;
        font-size: 0.89rem !important;
        line-height: 1.6 !important;
    }
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"],
    [data-testid="stFileUploader"] [data-testid="stFileUploaderPagination"] {
        display: none !important;
    }
"""
