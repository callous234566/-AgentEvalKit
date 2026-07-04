"""Shared empty-state visual system."""

EMPTY_STATES_CSS = """
    .workspace-empty-state {
        position: relative;
        overflow: hidden;
        margin: 0.88rem 0 1rem;
        padding: 1rem 1.05rem;
        border: 1px solid var(--rag-blue-100);
        border-radius: 22px;
        background:
            radial-gradient(circle at 8% 0%, var(--rag-blue-glow), transparent 34%),
            radial-gradient(circle at 100% 16%, rgba(14, 165, 233, 0.08), transparent 26%),
            var(--rag-bg-card);
        box-shadow: var(--rag-shadow-card);
    }
    .workspace-empty-state::before {
        content: "";
        position: absolute;
        inset: 0;
        background-image:
            linear-gradient(var(--rag-border-light) 1px, transparent 1px),
            linear-gradient(90deg, var(--rag-border-light) 1px, transparent 1px);
        background-size: 30px 30px;
        opacity: 0.24;
        pointer-events: none;
    }
    .workspace-empty-state::after {
        content: "";
        position: absolute;
        right: -26px;
        top: -28px;
        width: 108px;
        height: 108px;
        border-radius: 999px;
        background: var(--rag-blue-glow);
        pointer-events: none;
    }
    .workspace-empty-heading,
    .workspace-empty-steps {
        position: relative;
        z-index: 1;
    }
    .workspace-empty-heading {
        display: flex;
        align-items: center;
        gap: 0.72rem;
    }
    .workspace-empty-icon {
        display: inline-grid;
        place-items: center;
        width: 42px;
        height: 42px;
        flex: 0 0 42px;
        border: 1px solid var(--rag-blue-100);
        border-radius: 15px;
        background: var(--rag-blue-50);
        color: var(--rag-blue-primary);
        box-shadow: var(--rag-shadow-sm);
    }
    .workspace-empty-icon::before {
        content: "";
        width: 1.12rem;
        height: 1.12rem;
        display: block;
        background: currentColor;
        -webkit-mask: var(--empty-icon-mask, var(--empty-icon-info)) center / contain no-repeat;
        mask: var(--empty-icon-mask, var(--empty-icon-info)) center / contain no-repeat;
    }
    .workspace-empty-title {
        color: var(--rag-text-primary);
        font-size: 1rem;
        font-weight: 900;
        line-height: 1.4;
    }
    .workspace-empty-copy {
        max-width: 880px;
        margin-top: 0.16rem;
        color: var(--rag-text-muted);
        font-size: 0.86rem;
        line-height: 1.65;
    }
    .workspace-empty-steps {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.58rem;
        margin-top: 0.82rem;
    }
    .workspace-empty-step {
        display: flex;
        align-items: flex-start;
        gap: 0.52rem;
        min-width: 0;
        padding: 0.66rem 0.7rem;
        border: 1px solid var(--rag-border);
        border-radius: 15px;
        background: var(--rag-bg-card);
        color: var(--rag-text-muted);
        box-shadow: var(--rag-shadow-sm);
        transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
    }
    .workspace-empty-step:hover {
        transform: translateY(-1px);
        border-color: var(--rag-blue-200);
        box-shadow: var(--rag-shadow-card-hover);
    }
    .workspace-empty-step-icon {
        content: "";
        width: 0.94rem;
        height: 0.94rem;
        flex: 0 0 auto;
        padding: 0.27rem;
        border: 1px solid var(--rag-blue-100);
        border-radius: 11px;
        background: var(--rag-blue-50);
        color: var(--rag-blue-primary);
        display: inline-grid;
        place-items: center;
        box-sizing: content-box;
    }
    .workspace-empty-step-icon::before {
        content: "";
        width: 0.94rem;
        height: 0.94rem;
        display: block;
        background: currentColor;
        -webkit-mask: var(--empty-icon-mask, var(--empty-icon-info)) center / contain no-repeat;
        mask: var(--empty-icon-mask, var(--empty-icon-info)) center / contain no-repeat;
    }
    .workspace-empty-state {
        --empty-icon-info: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='10' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='M12 16v-4M12 8h.01' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
        --empty-icon-upload: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 3v12m5-7-5-5-5 5m14 7v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
        --empty-icon-library: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M4 19.5A2.5 2.5 0 0 1 6.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2ZM8 7h8M8 11h6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
        --empty-icon-layers: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='m12 2 9 5-9 5-9-5Zm-9 10 9 5 9-5m-18 5 9 5 9-5' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
        --empty-icon-settings: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 15.5A3.5 3.5 0 1 0 12 8a3.5 3.5 0 0 0 0 7.5ZM19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06A1.7 1.7 0 0 0 15 19.4a1.7 1.7 0 0 0-1 .6 1.7 1.7 0 0 0-.4 1.1V21a2 2 0 1 1-4 0v-.09a1.7 1.7 0 0 0-.4-1.1 1.7 1.7 0 0 0-1-.6 1.7 1.7 0 0 0-1.88.34l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-.6-1 1.7 1.7 0 0 0-1.1-.4H3a2 2 0 1 1 0-4h.09a1.7 1.7 0 0 0 1.1-.4 1.7 1.7 0 0 0 .6-1 1.7 1.7 0 0 0-.34-1.88l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-.6 1.7 1.7 0 0 0 .4-1.1V3a2 2 0 1 1 4 0v.09a1.7 1.7 0 0 0 .4 1.1 1.7 1.7 0 0 0 1 .6 1.7 1.7 0 0 0 1.88-.34l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.7 1.7 0 0 0 19.4 9c.2.4.5.7.9.9.3.2.7.3 1.1.3h.1a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.1.4c-.4.2-.7.5-.9.9Z' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
        --empty-icon-bot: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 8V4H8' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3Crect width='16' height='12' x='4' y='8' rx='3' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='M2 14h2m16 0h2M9 13h.01M15 13h.01M10 18h4' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
        --empty-icon-database: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cellipse cx='12' cy='5' rx='8' ry='3' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
        --empty-icon-description: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z' fill='none' stroke='black' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M14 2v6h6M8 12h8M8 16h8M8 20h5' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
        --empty-icon-activity: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M3 12h4l3-8 4 16 3-8h4' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
        --empty-icon-message: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
        --empty-icon-search: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='11' cy='11' r='7' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='m20 20-3.6-3.6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
        --empty-icon-refresh: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M21 12a9 9 0 0 1-15.5 6.3L3 16m0 5v-5h5M3 12A9 9 0 0 1 18.5 5.7L21 8m0-5v5h-5' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
    }
    .empty-icon-upload { --empty-icon-mask: var(--empty-icon-upload); }
    .empty-icon-library { --empty-icon-mask: var(--empty-icon-library); }
    .empty-icon-layers { --empty-icon-mask: var(--empty-icon-layers); }
    .empty-icon-settings { --empty-icon-mask: var(--empty-icon-settings); }
    .empty-icon-bot { --empty-icon-mask: var(--empty-icon-bot); }
    .empty-icon-database { --empty-icon-mask: var(--empty-icon-database); }
    .empty-icon-description { --empty-icon-mask: var(--empty-icon-description); }
    .empty-icon-activity { --empty-icon-mask: var(--empty-icon-activity); }
    .empty-icon-message { --empty-icon-mask: var(--empty-icon-message); }
    .empty-icon-search { --empty-icon-mask: var(--empty-icon-search); }
    .empty-icon-refresh { --empty-icon-mask: var(--empty-icon-refresh); }
    .workspace-empty-step strong,
    .workspace-empty-step small {
        display: block;
    }
    .workspace-empty-step strong {
        color: var(--rag-text-primary);
        font-size: 0.86rem;
        font-weight: 860;
        line-height: 1.4;
    }
    .workspace-empty-step small {
        margin-top: 0.1rem;
        color: var(--rag-text-placeholder);
        font-size: 0.76rem;
        line-height: 1.48;
    }
    body.rag-dark .workspace-empty-state {
        border-color: var(--rag-border);
        background:
            radial-gradient(circle at 8% 0%, rgba(37, 99, 235, 0.12), transparent 34%),
            var(--rag-bg-elevated);
        box-shadow: var(--rag-shadow-sm);
    }
    body.rag-dark .workspace-empty-step {
        border-color: var(--rag-border);
        background: var(--rag-bg-card);
    }
    body.rag-dark .workspace-empty-step-icon {
        border-color: var(--rag-border);
        background: var(--rag-bg-elevated);
        color: var(--rag-blue-primary);
    }
    @media (max-width: 900px) {
        .workspace-empty-state {
            padding: 0.86rem;
            border-radius: 18px;
        }
        .workspace-empty-steps {
            grid-template-columns: 1fr;
        }
    }
"""
