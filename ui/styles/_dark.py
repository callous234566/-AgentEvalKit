DARK_MODE_CSS = """
/* ============================================
   暗黑模式 (body.rag-dark)

   Most color changes are handled by CSS custom
   properties in _variables.py.  This file only
   contains overrides that cannot be expressed as
   simple variable swaps: Streamlit widget chrome,
   scrollbar styling, code blocks, inputs, etc.
   ============================================ */

/* Streamlit widgets that don't respect custom properties */
body.rag-dark .stAlert,
body.rag-dark .stWarning,
body.rag-dark .stSuccess,
body.rag-dark .stError,
body.rag-dark .stInfo {
    background: var(--rag-bg-card) !important;
    color: var(--rag-text-primary) !important;
    border: 1px solid var(--rag-border) !important;
}

body.rag-dark .stMarkdown,
body.rag-dark .stMarkdown p,
body.rag-dark .stMarkdown li,
body.rag-dark .stMarkdown span {
    color: var(--rag-text-primary) !important;
}

body.rag-dark .stTabs [data-baseweb="tab"] {
    color: var(--rag-text-primary) !important;
    background: transparent !important;
}

body.rag-dark .stTabs [data-baseweb="tab-highlight"] {
    background-color: var(--rag-blue-accent) !important;
}

body.rag-dark .stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

body.rag-dark .stDownloadButton > button {
    background: var(--rag-bg-elevated) !important;
    color: var(--rag-text-primary) !important;
    border: 1px solid var(--rag-border) !important;
}

body.rag-dark div[data-testid="stExpander"] details,
body.rag-dark div[data-testid="stDataFrame"],
body.rag-dark div[data-testid="stTable"],
body.rag-dark [data-testid="stMarkdownContainer"] table,
body.rag-dark .dir-table {
    background: var(--rag-bg-card) !important;
    border-color: var(--rag-border) !important;
}

body.rag-dark [data-testid="stMarkdownContainer"] th,
body.rag-dark .dir-table thead th {
    background: var(--rag-bg-elevated) !important;
    color: var(--rag-text-primary) !important;
}

body.rag-dark [data-testid="stMarkdownContainer"] blockquote {
    background: var(--rag-bg-elevated);
    border-left-color: var(--rag-blue-300);
}

body.rag-dark .stButton > button {
    background: var(--rag-bg-elevated) !important;
    color: var(--rag-text-primary) !important;
    border: 1px solid var(--rag-border) !important;
}

body.rag-dark .stButton > button:hover {
    background: var(--rag-border) !important;
    border-color: var(--rag-border-strong) !important;
}

body.rag-dark .stButton > button[kind="primary"],
body.rag-dark button[data-testid="stBaseButton-primary"] {
    background: var(--rag-blue-accent) !important;
    color: #ffffff !important;
}

body.rag-dark .stButton > button[kind="primary"]:hover,
body.rag-dark button[data-testid="stBaseButton-primary"]:hover {
    background: var(--rag-blue-primary) !important;
}

body.rag-dark textarea,
body.rag-dark input[type="text"],
body.rag-dark [data-baseweb="input"] input,
body.rag-dark [data-baseweb="textarea"] textarea,
body.rag-dark .stTextArea textarea {
    background: var(--rag-bg-card) !important;
    color: var(--rag-text-primary) !important;
    border: 1px solid var(--rag-border) !important;
}

body.rag-dark textarea:focus,
body.rag-dark input[type="text"]:focus {
    border-color: var(--rag-border-focus) !important;
    box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.3) !important;
}

body.rag-dark :focus-visible,
body.rag-dark button:focus-visible,
body.rag-dark [role="button"]:focus-visible,
body.rag-dark summary:focus-visible,
body.rag-dark input:focus-visible,
body.rag-dark textarea:focus-visible,
body.rag-dark select:focus-visible {
    outline-color: rgba(96, 165, 250, 0.42) !important;
}

body.rag-dark [data-baseweb="input"] input::placeholder,
body.rag-dark textarea::placeholder {
    color: var(--rag-text-placeholder) !important;
}

body.rag-dark code,
body.rag-dark pre,
body.rag-dark pre code {
    background: var(--rag-bg-code) !important;
    color: var(--rag-text-primary) !important;
}

body.rag-dark hr,
body.rag-dark [data-testid="stMarkdownContainer"] hr {
    border-color: var(--rag-border) !important;
}

body.rag-dark h1,
body.rag-dark h2,
body.rag-dark h3,
body.rag-dark h4,
body.rag-dark h5,
body.rag-dark h6 {
    color: var(--rag-text-primary) !important;
}

body.rag-dark input[type="number"] {
    background: var(--rag-bg-card) !important;
    color: var(--rag-text-primary) !important;
}

body.rag-dark [data-baseweb="select"] > div {
    background: var(--rag-bg-card) !important;
    color: var(--rag-text-primary) !important;
    border-color: var(--rag-border) !important;
}

body.rag-dark [data-baseweb="tag"] {
    background: var(--rag-blue-100) !important;
    color: var(--rag-blue-300) !important;
}

body.rag-dark .stProgress > div > div {
    background-color: var(--rag-blue-accent) !important;
}

body.rag-dark .app-hero-tags span,
body.rag-dark .app-hero-orb {
    background: rgba(17, 24, 39, 0.82);
    border-color: var(--rag-border);
}

body.rag-dark .chat-topbar {
    border-color: var(--rag-border);
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.96) 0%, rgba(15, 23, 42, 0.82) 100%);
}

body.rag-dark .user-avatar {
    background:
        radial-gradient(circle at 28% 20%, rgba(255, 255, 255, 0.16), transparent 28%),
        linear-gradient(145deg, rgba(37, 99, 235, 0.20) 0%, rgba(15, 23, 42, 0.96) 100%);
    border-color: rgba(96, 165, 250, 0.38);
    color: var(--rag-blue-primary);
}

body.rag-dark .ai-avatar {
    background:
        radial-gradient(circle at 28% 20%, rgba(255, 255, 255, 0.15), transparent 28%),
        linear-gradient(145deg, rgba(34, 197, 94, 0.16) 0%, rgba(15, 23, 42, 0.96) 100%);
    border-color: rgba(134, 239, 172, 0.34);
    color: var(--rag-green-text);
}

body.rag-dark .workspace-card::before {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), transparent 44%);
}

body.rag-dark .upload-task-panel,
body.rag-dark .document-card,
body.rag-dark .doc-toolbar,
body.rag-dark .settings-summary,
body.rag-dark .settings-group-card,
body.rag-dark .chat-context-bar,
body.rag-dark .section-intro,
body.rag-dark .doc-confirm-panel,
body.rag-dark .inline-confirm-panel,
body.rag-dark .share-panel {
    border-color: var(--rag-border);
    box-shadow: var(--rag-shadow-sm);
}

body.rag-dark .source-box,
body.rag-dark .doc-confirm-panel,
body.rag-dark .inline-confirm-panel,
body.rag-dark .share-panel {
    background: var(--rag-bg-elevated);
    border-color: var(--rag-border);
}

body.rag-dark .settings-group-card::after {
    background: rgba(96, 165, 250, 0.10);
}

body.rag-dark .doc-confirm-icon {
    background: rgba(239, 68, 68, 0.14);
    border-color: rgba(248, 113, 113, 0.34);
    color: #fca5a5;
}

body.rag-dark .doc-confirm-hint {
    background: rgba(245, 158, 11, 0.13);
    border-color: rgba(245, 158, 11, 0.32);
    color: #fbbf24;
}

body.rag-dark .share-panel-title,
body.rag-dark .share-panel-title .ui-icon {
    color: var(--rag-blue-300);
}

body.rag-dark .ai-message.typing-cursor::before,
body.rag-dark .upload-task-row.processing::after {
    background: linear-gradient(110deg, transparent 0%, rgba(96, 165, 250, 0.13) 45%, transparent 62%);
}

/* Scrollbar */
body.rag-dark ::-webkit-scrollbar-track {
    background: var(--rag-bg-card);
}

body.rag-dark ::-webkit-scrollbar-thumb {
    background: var(--rag-border);
}

body.rag-dark ::-webkit-scrollbar-thumb:hover {
    background: var(--rag-border-strong);
}

"""
