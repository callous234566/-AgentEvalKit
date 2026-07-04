DOCUMENTS_CSS = """
    .section-intro {
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: flex-start;
        gap: 0.78rem;
        margin: 0 0 1rem;
        padding: 0.9rem 1rem;
        border: 1px solid var(--rag-border);
        border-radius: 20px;
        background:
            radial-gradient(circle at 92% 0%, var(--rag-blue-glow), transparent 30%),
            var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
    }
    .section-intro > .ui-icon {
        width: 2.15rem;
        height: 2.15rem;
        padding: 0.48rem;
        border-radius: 14px;
        border: 1px solid var(--rag-blue-100);
        background: var(--rag-blue-50);
        color: var(--rag-blue-primary);
        flex: 0 0 auto;
        box-sizing: border-box;
    }
    .section-intro-title {
        color: var(--rag-text-primary);
        font-size: 0.98rem;
        font-weight: 880;
        line-height: 1.35;
    }
    .section-intro-copy {
        margin-top: 0.16rem;
        color: var(--rag-text-muted);
        font-size: 0.88rem;
        line-height: 1.65;
    }

    .doc-toolbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.65rem;
        margin: 0.65rem 0 0.48rem;
        padding: 0.68rem 0.75rem;
        border: 1px solid var(--rag-border);
        border-radius: 17px;
        background: var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
        transition: border-color 0.18s ease, box-shadow 0.18s ease, background-color 0.18s ease;
    }
    .doc-toolbar-left {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.45rem;
        min-width: 0;
    }
    .doc-status-pill,
    .doc-status-note {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        min-height: 28px;
        border-radius: 999px;
        padding: 0.24rem 0.68rem;
        font-size: 0.8rem;
        font-weight: 780;
        white-space: nowrap;
    }
    .doc-status-pill .ui-icon,
    .doc-status-note .ui-icon {
        width: 0.9rem;
        height: 0.9rem;
    }
    .doc-status-pill.active {
        background: var(--rag-green-bg);
        border: 1px solid var(--rag-green-border);
        color: var(--rag-green-text);
    }
    .doc-status-pill.disabled {
        background: var(--rag-amber-bg);
        border: 1px solid var(--rag-amber-border);
        color: var(--rag-amber-text);
    }
    .doc-status-note {
        background: var(--rag-bg-elevated);
        border: 1px solid var(--rag-border);
        color: var(--rag-text-muted);
    }
    .doc-toolbar-info {
        display: inline-flex;
        align-items: baseline;
        gap: 0.18rem;
        padding: 0.24rem 0.58rem;
        border: 1px solid var(--rag-border);
        border-radius: 12px;
        background: var(--rag-bg-elevated);
        color: var(--rag-text-muted);
        white-space: nowrap;
        font-weight: 800;
    }
    .doc-toolbar.has-selection {
        border-color: var(--rag-blue-200);
        background:
            radial-gradient(circle at 100% 0%, var(--rag-blue-glow), transparent 24%),
            var(--rag-bg-card);
        box-shadow: 0 8px 18px rgba(37, 99, 235, 0.08);
    }
    .doc-toolbar.has-selection .doc-toolbar-info {
        border-color: var(--rag-blue-200);
        background: var(--rag-blue-50);
        color: var(--rag-blue-primary);
    }
    .doc-toolbar-count {
        font-size: 1rem;
        font-weight: 900;
    }
    .doc-toolbar-total,
    .doc-toolbar-sep,
    .doc-toolbar-label {
        font-size: 0.78rem;
    }
    .doc-toolbar-hint {
        display: flex;
        align-items: center;
        gap: 0.36rem;
        margin: 0 0 0.52rem;
        color: var(--rag-text-placeholder);
        font-size: 0.76rem;
        line-height: 1.45;
    }
    .doc-toolbar-hint .ui-icon {
        width: 0.82rem;
        height: 0.82rem;
        color: var(--rag-blue-primary);
        flex: 0 0 auto;
    }

    .document-card {
        margin: 0.18rem 0 0.72rem;
        padding: 0.85rem 0.95rem;
        border: 1px solid var(--rag-border);
        border-radius: 18px;
        background: var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
        transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
        position: relative;
        overflow: hidden;
    }
    .document-card::before {
        content: "";
        position: absolute;
        left: 0;
        top: 14px;
        bottom: 14px;
        width: 3px;
        border-radius: 999px;
        background: var(--rag-blue-300);
        opacity: 0.7;
    }
    .document-card:hover {
        transform: translateY(-1px);
        border-color: var(--rag-blue-200);
        box-shadow: var(--rag-shadow-card-hover);
    }
    .document-card-disabled {
        opacity: 0.72;
        background: var(--rag-bg-elevated);
    }
    .document-card-disabled::before {
        background: var(--rag-amber-border);
    }
    .document-card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        position: relative;
        z-index: 1;
    }
    .document-card-icon {
        position: relative;
        display: inline-grid;
        place-items: center;
        width: 38px;
        height: 38px;
        border-radius: 14px;
        background: var(--rag-blue-50);
        border: 1px solid var(--rag-blue-100);
        color: var(--rag-blue-primary);
        flex: 0 0 auto;
    }
    .document-card-icon::before {
        content: "";
        width: 19px;
        height: 19px;
        background: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z' fill='none' stroke='black' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M14 2v6h6M8 12h8M8 16h8M8 20h5' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z' fill='none' stroke='black' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M14 2v6h6M8 12h8M8 16h8M8 20h5' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    .document-card-icon .ui-icon {
        display: none;
    }
    .document-card-main {
        min-width: 0;
        flex: 1;
    }
    .document-card-title-row {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        min-width: 0;
    }
    .document-card-name {
        min-width: 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        color: var(--rag-text-primary);
        font-size: 0.96rem;
        font-weight: 850;
    }
    .document-card-meta {
        margin-top: 0.18rem;
        color: var(--rag-text-placeholder);
        font-size: 0.8rem;
        line-height: 1.55;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.28rem;
    }
    .document-card-meta::before {
        content: "";
        width: 7px;
        height: 7px;
        border-radius: 999px;
        background: var(--rag-blue-300);
        box-shadow: 0 0 0 4px var(--rag-blue-glow);
    }
    .document-enabled-badge,
    .document-disabled-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.28rem;
        border-radius: 999px;
        padding: 0.18rem 0.5rem;
        font-size: 0.74rem;
        font-weight: 780;
        white-space: nowrap;
    }
    .document-enabled-badge {
        background: var(--rag-green-bg);
        color: var(--rag-green-text);
        border: 1px solid var(--rag-green-border);
    }
    .document-disabled-badge {
        margin-top: 0.32rem;
        background: var(--rag-amber-bg);
        color: var(--rag-amber-text);
        border: 1px solid var(--rag-amber-border);
    }
    .document-enabled-badge .ui-icon,
    .document-disabled-badge .ui-icon {
        width: 0.82rem;
        height: 0.82rem;
    }

    .dir-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        table-layout: fixed;
        margin-top: 4px;
        overflow: hidden;
        border: 1px solid var(--rag-border);
        border-radius: 16px;
        background: var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
    }

    .dir-table thead th {
        padding: 9px 10px;
        font-size: 12px;
        font-weight: 850;
        color: var(--rag-text-placeholder);
        text-align: left;
        white-space: nowrap;
        border-bottom: 1px solid var(--rag-border);
        background: var(--rag-bg-elevated);
    }

    .dir-table tbody td {
        padding: 9px 10px;
        font-size: 14px;
        vertical-align: middle;
        color: var(--rag-text-primary);
        border-bottom: 1px solid var(--rag-border-light);
    }

    .dir-table tbody tr {
        transition: background-color 0.16s ease;
    }

    .dir-table tbody tr:hover {
        background: var(--rag-blue-50);
    }

    .dir-table tbody tr:last-child td {
        border-bottom: none;
    }

    .dir-table .dir-col-name {
        width: 320px;
        min-width: 120px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .dir-table .dir-col-count {
        width: 72px;
        min-width: 56px;
        text-align: right;
    }

    .dir-table .dir-col-time {
        width: 110px;
        min-width: 100px;
        color: var(--rag-text-muted);
        font-size: 12px;
    }

    .dir-table .dir-col-check {
        width: 40px;
        text-align: center;
    }

    .dir-table thead th.dir-col-check {
        text-align: center;
    }

    .dir-source-disabled {
        color: var(--rag-text-disabled);
        font-size: 13px;
        font-weight: 400;
    }

    @media (max-width: 900px) {
        .doc-toolbar {
            align-items: flex-start;
            flex-direction: column;
        }
        .document-card-title-row {
            align-items: flex-start;
            flex-direction: column;
            gap: 0.35rem;
        }
    }
"""
