RESPONSIVE_CSS = """
    @media (max-width: 768px) {
        .user-message, .ai-message {
            max-width: 90%;
        }
        .answer-copy-btn {
            min-width: 74px;
            height: 32px;
        }
        .answer-regenerate-btn,
        .source-copy-btn {
            min-width: 36px;
            min-height: 36px;
        }
        .source-evidence summary {
            align-items: flex-start;
            flex-direction: column;
        }
        .source-evidence-actions {
            width: 100%;
            margin-left: 0;
            justify-content: space-between;
        }
        .source-title {
            align-items: flex-start;
            flex-wrap: wrap;
        }
        .source-file {
            flex: 1 1 100%;
            width: 100%;
        }
        .source-score {
            margin-left: 0;
        }
    }
    @media (max-width: 900px) {
        .app-hero {
            padding: 1.15rem;
            border-radius: 22px;
        }
        .app-hero-orb {
            display: none;
        }
        .workspace-overview {
            grid-template-columns: 1fr;
        }
        .settings-summary {
            align-items: stretch;
            flex-direction: column;
        }
        .settings-chip {
            justify-content: space-between;
            width: 100%;
        }
        .section-intro {
            border-radius: 18px;
            padding: 0.82rem;
        }
        [data-testid="stMarkdownContainer"] table {
            display: block;
            overflow-x: auto;
            white-space: nowrap;
        }
        div[data-testid="stExpander"] summary {
            min-height: 42px;
            padding: 0.68rem 0.78rem !important;
        }
        .doc-toolbar-left,
        .chat-context-bar {
            gap: 0.4rem;
        }
        .doc-status-pill,
        .doc-status-note,
        .chat-context-item {
            white-space: normal;
        }
    }
    @media (max-width: 1024px) {
        .stButton > button {
            width: 100%;
        }
    }
"""
