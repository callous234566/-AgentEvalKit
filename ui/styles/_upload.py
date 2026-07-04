"""Styles for upload."""

UPLOAD_CSS = """
    div[class*="st-key-upload_preview_prev"],
    div[class*="st-key-upload_preview_next"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }

    div[class*="st-key-upload_task_native_"] {
        position: relative !important;
        margin: 0.28rem 0 !important;
    }
    div[class*="st-key-upload_task_native_"] div[class*="st-key-upload_remove_visible_"] {
        position: absolute !important;
        top: 50% !important;
        right: 0.85rem !important;
        z-index: 5 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 34px !important;
        height: 34px !important;
        min-height: 34px !important;
        padding: 0 !important;
        margin: 0 !important;
        transform: translateY(-50%) !important;
    }
    div[class*="st-key-upload_remove_visible_"] button {
        position: relative !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 34px !important;
        min-width: 34px !important;
        height: 34px !important;
        min-height: 34px !important;
        padding: 0 !important;
        margin: 0 !important;
        border-radius: 12px !important;
        border: 1px solid var(--rag-blue-100) !important;
        background:
            radial-gradient(circle at 35% 15%, rgba(59, 130, 246, 0.10), transparent 42%),
            var(--rag-bg-card) !important;
        color: var(--rag-text-secondary) !important;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.06) !important;
        font-size: 0 !important;
        line-height: 0 !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease, background 0.18s ease, color 0.18s ease !important;
    }
    div[class*="st-key-upload_remove_visible_"] button p {
        display: none !important;
    }
    div[class*="st-key-upload_remove_visible_"] button::before {
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0.96rem;
        height: 0.96rem;
        display: block;
        margin: 0;
        transform: translate(-50%, -50%);
        background: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6M10 11v6M14 11v6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6M10 11v6M14 11v6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    div[class*="st-key-upload_remove_visible_"] button:hover {
        transform: translateY(-1px) !important;
        border-color: var(--rag-red-border) !important;
        background: var(--rag-red-bg) !important;
        color: var(--rag-red-text) !important;
        box-shadow: 0 10px 22px rgba(239, 68, 68, 0.12) !important;
    }

    .upload-empty-inline {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 0.9rem 0 0.35rem;
        padding: 0.9rem 1rem;
        border: 1px solid var(--rag-blue-100);
        border-radius: 18px;
        background:
            radial-gradient(circle at 0% 0%, var(--rag-blue-glow), transparent 38%),
            var(--rag-bg-card);
        color: var(--rag-text-secondary);
        box-shadow: var(--rag-shadow-sm);
    }
    .upload-empty-inline > span {
        width: 34px;
        height: 34px;
        border-radius: 13px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        color: var(--rag-green-text);
        background: var(--rag-green-bg);
        border: 1px solid var(--rag-green-border);
        flex: 0 0 auto;
    }
    .upload-empty-inline .ui-icon {
        width: 1rem;
        height: 1rem;
    }
    .upload-empty-inline strong {
        display: block;
        color: var(--rag-text-primary);
        font-size: 0.92rem;
        font-weight: 850;
        line-height: 1.45;
    }
    .upload-empty-inline small {
        display: block;
        margin-top: 0.08rem;
        color: var(--rag-text-placeholder);
        font-size: 0.78rem;
        line-height: 1.5;
    }

    .upload-flow-steps {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.55rem;
        margin: 0.85rem 0 0.2rem;
        padding: 0.42rem;
        border: 1px solid var(--rag-border-light);
        border-radius: 18px;
        background: var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
    }
    .upload-step {
        display: flex;
        align-items: center;
        gap: 0.58rem;
        min-width: 0;
        padding: 0.58rem 0.68rem;
        border: 1px solid transparent;
        border-radius: 14px;
        color: var(--rag-text-placeholder);
        transition: border-color 0.18s ease, background-color 0.18s ease, color 0.18s ease;
    }
    .upload-step-index {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        flex: 0 0 24px;
        border-radius: 9px;
        border: 1px solid var(--rag-border);
        background: var(--rag-bg-elevated);
        color: var(--rag-text-muted);
        font-size: 0.72rem;
        font-weight: 900;
    }
    .upload-step strong,
    .upload-step small {
        display: block;
    }
    .upload-step strong {
        color: var(--rag-text-secondary);
        font-size: 0.82rem;
        line-height: 1.35;
        font-weight: 850;
    }
    .upload-step small {
        margin-top: 0.06rem;
        color: var(--rag-text-placeholder);
        font-size: 0.72rem;
        line-height: 1.35;
    }
    .upload-step.active {
        border-color: var(--rag-blue-200);
        background: var(--rag-blue-50);
        color: var(--rag-blue-primary);
    }
    .upload-step.active .upload-step-index {
        border-color: var(--rag-blue-200);
        background: var(--rag-blue-primary);
        color: #ffffff;
        box-shadow: 0 0 0 4px var(--rag-blue-glow);
    }
    .upload-step.active strong {
        color: var(--rag-blue-primary);
    }
    .upload-step.done {
        border-color: var(--rag-green-border);
        background: var(--rag-green-bg);
    }
    .upload-step.done .upload-step-index {
        border-color: var(--rag-green-border);
        background: var(--rag-green-bright);
        color: #ffffff;
    }
    .upload-step.done strong {
        color: var(--rag-green-text);
    }

    div[class*="st-key-upload_process_button"] button {
        position: relative !important;
        min-height: 46px !important;
        height: 46px !important;
        margin: 0.9rem 0 0.55rem !important;
        border-radius: 16px !important;
        border: 1px solid var(--rag-blue-200) !important;
        background:
            radial-gradient(circle at 8% 0%, var(--rag-blue-glow), transparent 36%),
            linear-gradient(180deg, #ffffff 0%, var(--rag-blue-50) 100%) !important;
        color: var(--rag-blue-primary) !important;
        box-shadow: 0 8px 18px rgba(37, 99, 235, 0.08) !important;
        font-size: 0.9rem !important;
        font-weight: 860 !important;
        letter-spacing: 0.01em !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease, filter 0.18s ease !important;
    }
    div[class*="st-key-upload_process_button"] button::before {
        display: none !important;
    }
    div[class*="st-key-upload_process_button"] button:hover {
        transform: translateY(-1px);
        border-color: var(--rag-blue-300) !important;
        background:
            radial-gradient(circle at 8% 0%, rgba(37, 99, 235, 0.14), transparent 38%),
            linear-gradient(180deg, #ffffff 0%, var(--rag-blue-50) 100%) !important;
        box-shadow: 0 10px 22px rgba(37, 99, 235, 0.12) !important;
        filter: saturate(1.04);
    }
    div[class*="st-key-upload_process_button"] button:active {
        transform: translateY(0);
        box-shadow: var(--rag-shadow-sm) !important;
    }
    div[class*="st-key-upload_process_button"] button:disabled,
    div[class*="st-key-upload_process_button"] button:disabled:hover {
        transform: none !important;
        border-color: var(--rag-border) !important;
        background: var(--rag-bg-elevated) !important;
        color: var(--rag-text-placeholder) !important;
        box-shadow: none !important;
        cursor: not-allowed !important;
        filter: none !important;
    }
    div[data-testid="stProgress"] {
        display: none !important;
    }

    .upload-task-panel {
        position: relative;
        margin-top: 0.95rem;
        border: 1px solid var(--rag-blue-100);
        border-radius: 22px;
        background:
            radial-gradient(circle at 92% 8%, var(--rag-blue-glow), transparent 28%),
            var(--rag-bg-card);
        box-shadow: var(--rag-shadow-lg);
        overflow: hidden;
    }
    .upload-task-panel::before {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        opacity: 0.35;
        background-image:
            linear-gradient(90deg, rgba(148, 163, 184, 0.10) 1px, transparent 1px),
            linear-gradient(180deg, rgba(148, 163, 184, 0.10) 1px, transparent 1px);
        background-size: 34px 34px;
        mask-image: linear-gradient(180deg, black, transparent 62%);
    }
    .upload-task-header {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        padding: 0.88rem 1rem;
        border-bottom: 1px solid var(--rag-border);
        background: var(--rag-blue-50-gradient);
    }
    .upload-task-title {
        display: inline-flex;
        align-items: center;
        gap: 0.42rem;
        color: var(--rag-text-primary);
        font-size: 0.96rem;
        font-weight: 850;
    }
    .upload-task-title .ui-icon {
        width: 1rem;
        height: 1rem;
        padding: 0.25rem;
        border-radius: 11px;
        background: var(--rag-blue-50);
        border: 1px solid var(--rag-blue-100);
        color: var(--rag-blue-primary);
        box-sizing: content-box;
    }
    .upload-task-summary {
        display: inline-flex;
        align-items: center;
        flex-wrap: wrap;
        justify-content: flex-end;
        gap: 0.38rem;
        color: var(--rag-text-placeholder);
        font-size: 0.82rem;
    }
    .upload-task-summary span {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        min-height: 26px;
        padding: 0.16rem 0.52rem;
        border: 1px solid var(--rag-border);
        border-radius: 999px;
        background: var(--rag-bg-card);
        white-space: nowrap;
        font-weight: 760;
    }
    .upload-task-summary .ui-icon {
        width: 0.78rem;
        height: 0.78rem;
    }
    .upload-task-summary span.success {
        color: var(--rag-green-text);
        background: var(--rag-green-bg);
        border-color: var(--rag-green-border);
    }
    .upload-task-summary span.failed {
        color: var(--rag-red-text);
        background: var(--rag-red-bg);
        border-color: var(--rag-red-border);
    }
    .upload-task-summary span.processing {
        color: var(--rag-blue-primary);
        background: var(--rag-blue-50);
        border-color: var(--rag-blue-200);
    }
    .upload-task-panel-streamlit {
        margin-bottom: 0.45rem;
    }
    .upload-task-row {
        display: grid;
        grid-template-columns: auto minmax(0, 1fr) auto;
        gap: 0.75rem;
        align-items: center;
        padding: 0.72rem 0.55rem;
        border-bottom: 1px solid var(--rag-border-light);
        border-radius: 15px;
        transition: background-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
    }
    .upload-task-row-native {
        min-height: 64px;
        margin: 0.28rem 0;
        padding: 0.72rem 4.25rem 0.72rem 0.9rem;
        border: 1px solid var(--rag-border-light);
        border-radius: 18px;
        background:
            radial-gradient(circle at 100% 0%, var(--rag-blue-glow), transparent 28%),
            var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
    }
    .upload-task-row:hover {
        background: var(--rag-bg-card-alt);
        box-shadow: var(--rag-shadow-sm);
    }
    .upload-task-row.processing {
        position: relative;
        overflow: hidden;
        background:
            linear-gradient(90deg, var(--rag-blue-glow) 0%, rgba(37, 99, 235, 0.02) 68%, transparent 100%);
        box-shadow: inset 3px 0 0 var(--rag-blue-accent);
        transform: translateX(2px);
    }
    .upload-task-row.processing::after {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(110deg, transparent 0%, rgba(255,255,255,0.42) 45%, transparent 62%);
        transform: translateX(-120%);
        animation: upload-row-shimmer 1.65s ease-in-out infinite;
        pointer-events: none;
    }
    .upload-task-row:last-child {
        border-bottom: 0;
    }
    .upload-task-icon {
        position: relative;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        border-radius: 14px;
        background: var(--rag-blue-50);
        color: var(--rag-blue-primary);
        flex: 0 0 38px;
        display: inline-flex;
        border: 1px solid var(--rag-blue-100);
        box-shadow: var(--rag-shadow-sm);
    }
    .upload-task-icon::before {
        content: "";
        width: 19px;
        height: 19px;
        background: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z' fill='none' stroke='black' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M14 2v6h6M8 12h8M8 16h8M8 20h5' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z' fill='none' stroke='black' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M14 2v6h6M8 12h8M8 16h8M8 20h5' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    .upload-task-icon .ui-icon {
        display: none !important;
    }
    .upload-task-name {
        color: var(--rag-text-primary);
        font-size: 0.92rem;
        font-weight: 650;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .upload-task-message {
        color: var(--rag-text-placeholder);
        font-size: 0.8rem;
        line-height: 1.45;
        margin-top: 0.12rem;
    }
    .upload-task-guidance {
        margin-top: 0.22rem;
        color: var(--rag-amber-text);
        font-size: 0.76rem;
        font-weight: 680;
        line-height: 1.45;
    }
    .upload-task-actions {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
    }
    .upload-task-badge {
        border-radius: 999px;
        padding: 0.2rem 0.62rem;
        border: 1px solid var(--rag-border);
        background: var(--rag-bg-elevated);
        color: var(--rag-text-muted);
        font-size: 0.78rem;
        font-weight: 800;
        white-space: nowrap;
    }
    .upload-task-badge.waiting {
        color: var(--rag-text-muted);
        background: var(--rag-bg-elevated);
    }
    .upload-task-badge.processing {
        color: var(--rag-blue-primary);
        background: var(--rag-blue-50);
        border-color: var(--rag-blue-200);
        animation: upload-pulse 1.35s ease-in-out infinite;
    }
    .upload-task-row.processing .upload-task-icon {
        color: #ffffff;
        background: linear-gradient(135deg, var(--rag-blue-accent) 0%, #38bdf8 100%);
        box-shadow: 0 0 0 5px var(--rag-blue-glow);
        animation: upload-icon-pulse 1.35s ease-in-out infinite;
    }
    .upload-task-badge.success {
        color: var(--rag-green-text);
        background: var(--rag-green-bg);
        border-color: var(--rag-green-border);
        box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.08);
    }
    .upload-task-badge.failed {
        color: var(--rag-red-text);
        background: var(--rag-red-bg);
        border-color: var(--rag-red-border);
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.08);
    }
    .upload-task-row.success {
        box-shadow: inset 3px 0 0 var(--rag-green-bright);
    }
    .upload-task-row.failed {
        box-shadow: inset 3px 0 0 var(--rag-red-text);
    }
    .upload-task-footer {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.7rem 0.95rem 0.82rem;
        border-top: 1px solid var(--rag-border-light);
        color: var(--rag-text-placeholder);
        font-size: 0.84rem;
    }
    .upload-task-footer-native {
        margin-top: 0.35rem;
        border: 1px solid var(--rag-border-light);
        border-radius: 15px;
        background: var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
    }
    .upload-result-inline {
        margin: 0.45rem 0 0.2rem;
        padding: 0.72rem 0.9rem;
        border-radius: 16px;
        border: 1px solid var(--rag-border);
        background: var(--rag-bg-card);
        color: var(--rag-text-secondary);
        box-shadow: var(--rag-shadow-sm);
        font-size: 0.86rem;
        font-weight: 760;
        text-align: center;
    }
    .upload-result-inline.success {
        border-color: var(--rag-green-border);
        background: var(--rag-green-bg);
        color: var(--rag-green-text);
    }
    .upload-result-inline.failed {
        border-color: var(--rag-amber-border);
        background: var(--rag-amber-bg);
        color: var(--rag-amber-text);
    }
    @keyframes upload-pulse {
        0%, 100% { box-shadow: 0 0 0 0 var(--rag-blue-glow); }
        50% { box-shadow: 0 0 0 5px rgba(37, 99, 235, 0.05); }
    }
    @keyframes upload-icon-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.06); }
    }
    @keyframes upload-row-shimmer {
        0% { transform: translateX(-120%); opacity: 0; }
        20% { opacity: 1; }
        100% { transform: translateX(120%); opacity: 0; }
    }
    @media (max-width: 900px) {
        .upload-flow-steps {
            grid-template-columns: 1fr;
        }
        .upload-task-header,
        .upload-task-footer {
            align-items: flex-start;
            flex-direction: column;
        }
    }
"""
