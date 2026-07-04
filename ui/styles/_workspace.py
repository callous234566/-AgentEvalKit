WORKSPACE_CSS = """
    .app-hero {
        position: relative;
        overflow: hidden;
        border: 1px solid var(--rag-blue-100);
        border-radius: 28px;
        padding: 1.55rem 1.65rem;
        margin: 0 0 1rem;
        background:
            radial-gradient(circle at 8% 12%, rgba(56, 189, 248, 0.20), transparent 30%),
            radial-gradient(circle at 92% 8%, rgba(34, 197, 94, 0.16), transparent 28%),
            linear-gradient(135deg, var(--rag-bg-card) 0%, var(--rag-bg-card-alt) 58%, var(--rag-blue-50) 100%);
        box-shadow: var(--rag-shadow-lg);
    }
    .app-hero::before {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        opacity: 0.42;
        background-image:
            linear-gradient(90deg, rgba(148, 163, 184, 0.12) 1px, transparent 1px),
            linear-gradient(180deg, rgba(148, 163, 184, 0.12) 1px, transparent 1px);
        background-size: 42px 42px;
        mask-image: radial-gradient(circle at 22% 35%, black, transparent 68%);
    }
    .app-hero-orb {
        position: absolute;
        right: 1.35rem;
        top: 1.1rem;
        width: 58px;
        height: 58px;
        border-radius: 20px;
        display: grid;
        place-items: center;
        color: var(--rag-blue-primary);
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid var(--rag-blue-100);
        box-shadow: 0 18px 45px rgba(37, 99, 235, 0.16);
        transform: rotate(8deg);
    }
    .app-hero-orb .ui-icon {
        display: none;
    }
    .app-hero-orb::before {
        content: "";
        width: 26px;
        height: 26px;
        background: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='m12 3 1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5ZM19 14l.8 2.2L22 17l-2.2.8L19 20l-.8-2.2L16 17l2.2-.8ZM5 14l.8 2.2L8 17l-2.2.8L5 20l-.8-2.2L2 17l2.2-.8Z' fill='none' stroke='black' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='m12 3 1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5ZM19 14l.8 2.2L22 17l-2.2.8L19 20l-.8-2.2L16 17l2.2-.8ZM5 14l.8 2.2L8 17l-2.2.8L5 20l-.8-2.2L2 17l2.2-.8Z' fill='none' stroke='black' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    .app-hero-kicker {
        position: relative;
        z-index: 1;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        margin-bottom: 0.55rem;
        padding: 0.24rem 0.65rem;
        border-radius: 999px;
        background: var(--rag-blue-glow);
        color: var(--rag-blue-primary);
        font-size: 0.78rem;
        font-weight: 850;
        letter-spacing: 0.02em;
    }
    .app-hero-kicker .ui-icon {
        width: 0.92rem;
        height: 0.92rem;
    }
    .app-hero-title {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        gap: 0.55rem;
        font-size: clamp(1.45rem, 2vw, 2rem);
        font-weight: 900;
        color: var(--rag-text-primary);
        letter-spacing: -0.02em;
    }
    .app-hero-title .ui-icon {
        width: 1.35rem;
        height: 1.35rem;
        color: var(--rag-blue-primary);
    }
    .app-hero-copy {
        position: relative;
        z-index: 1;
        margin-top: 0.55rem;
        max-width: 760px;
        color: var(--rag-text-secondary);
        line-height: 1.75;
    }
    .app-hero-tags {
        position: relative;
        z-index: 1;
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 0.9rem;
    }
    .app-hero-tags span {
        display: inline-flex;
        align-items: center;
        gap: 0.32rem;
        border: 1px solid var(--rag-border);
        border-radius: 999px;
        padding: 0.28rem 0.7rem;
        background: rgba(255, 255, 255, 0.72);
        color: var(--rag-text-muted);
        font-size: 0.82rem;
        font-weight: 780;
        backdrop-filter: blur(10px);
    }
    .app-hero-tags .ui-icon {
        width: 0.9rem;
        height: 0.9rem;
        color: var(--rag-blue-primary);
    }

    .workspace-overview {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 1rem;
        margin: 1rem 0 1.1rem;
    }
    .workspace-card {
        position: relative;
        overflow: hidden;
        min-height: 138px;
        padding: 1.05rem 1.1rem;
        border: 1px solid var(--rag-border);
        border-radius: 22px;
        background:
            radial-gradient(circle at 88% 16%, rgba(96, 165, 250, 0.14), transparent 30%),
            var(--rag-blue-50-gradient);
        box-shadow: var(--rag-shadow-card);
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }
    .workspace-card:hover {
        transform: translateY(-2px);
        border-color: var(--rag-blue-200);
        box-shadow: var(--rag-shadow-card-hover);
    }
    .workspace-card::after {
        content: "";
        position: absolute;
        right: -28px;
        bottom: -34px;
        width: 104px;
        height: 104px;
        border-radius: 999px;
        background: var(--rag-blue-glow);
        pointer-events: none;
    }
    .workspace-card::before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: inherit;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.48), transparent 42%);
        pointer-events: none;
    }
    .workspace-card-top {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        gap: 0.55rem;
    }
    .workspace-icon-badge {
        position: relative;
        width: 34px;
        height: 34px;
        border-radius: 12px;
        display: inline-grid;
        place-items: center;
        flex: 0 0 auto;
        background: var(--rag-bg-card);
        border: 1px solid var(--rag-blue-100);
        color: var(--rag-blue-primary);
        box-shadow: var(--rag-shadow-sm);
    }
    .workspace-icon-badge::before {
        content: "";
        width: 18px;
        height: 18px;
        background: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cellipse cx='12' cy='5' rx='8' ry='3' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cellipse cx='12' cy='5' rx='8' ry='3' fill='none' stroke='black' stroke-width='2'/%3E%3Cpath d='M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    .workspace-icon-badge::after {
        content: "";
        position: absolute;
        right: -3px;
        top: -3px;
        width: 8px;
        height: 8px;
        border: 2px solid var(--rag-bg-card);
        border-radius: 999px;
        background: var(--rag-blue-primary);
    }
    .workspace-card-docs .workspace-icon-badge {
        color: var(--rag-green-text);
        border-color: var(--rag-green-border);
        background: var(--rag-green-bg);
    }
    .workspace-card-docs .workspace-icon-badge::before {
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='m12 2 9 5-9 5-9-5ZM3 12l9 5 9-5M3 17l9 5 9-5' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='m12 2 9 5-9 5-9-5ZM3 12l9 5 9-5M3 17l9 5 9-5' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    .workspace-card-docs .workspace-icon-badge::after {
        background: var(--rag-green-bright);
    }
    .workspace-card-session .workspace-icon-badge {
        color: var(--rag-amber-text);
        border-color: var(--rag-amber-border);
        background: var(--rag-amber-bg);
    }
    .workspace-card-session .workspace-icon-badge::before {
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    .workspace-card-session .workspace-icon-badge::after {
        background: #f59e0b;
    }
    .workspace-icon-badge .ui-icon {
        display: none;
    }
    .workspace-card-label {
        display: flex;
        align-items: center;
        color: var(--rag-text-placeholder);
        font-size: 0.82rem;
        font-weight: 800;
    }
    .workspace-card-value {
        position: relative;
        z-index: 1;
        margin-top: 0.65rem;
        color: var(--rag-text-primary);
        font-size: 1.12rem;
        font-weight: 900;
        line-height: 1.35;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .workspace-card-copy {
        position: relative;
        z-index: 1;
        margin-top: 0.5rem;
        color: var(--rag-text-muted);
        font-size: 0.86rem;
        line-height: 1.55;
    }
    .workspace-mini-stats {
        position: relative;
        z-index: 1;
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
        margin-top: 0.5rem;
    }
    .workspace-mini-stat {
        border: 1px solid var(--rag-border);
        border-radius: 999px;
        padding: 0.12rem 0.52rem;
        background: var(--rag-bg-card);
        color: var(--rag-text-muted);
        font-size: 0.74rem;
        font-weight: 750;
    }
    .workspace-mini-stat.active {
        background: var(--rag-green-bg);
        border-color: var(--rag-green-border);
        color: var(--rag-green-text);
    }
    .workspace-mini-stat.muted {
        color: var(--rag-text-placeholder);
    }

    .subsection-title {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        margin: 0 0 0.35rem;
        font-size: 0.95rem;
        font-weight: 780;
        color: var(--rag-text-secondary);
    }

    .metric-group {
        margin-top: 6px;
        margin-bottom: 6px;
    }
    .metric-group-title {
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 0.02em;
        color: var(--rag-text-placeholder);
        margin-bottom: 4px;
    }
    .metric-card {
        background: var(--rag-blue-50-gradient);
        border: 1px solid var(--rag-border);
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: var(--rag-shadow-sm);
        display: flex;
        flex-direction: column;
        gap: 10px;
        min-height: 130px;
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }
    .metric-card:hover {
        box-shadow: var(--rag-shadow-card-hover);
        transform: translateY(-2px);
    }
    .metric-title {
        font-size: 0.92rem;
        font-weight: 700;
        color: var(--rag-text-secondary);
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: var(--rag-text-primary);
        line-height: 1;
        margin-top: auto;
    }
    .metric-caption {
        font-size: 0.8rem;
        color: var(--rag-text-placeholder);
        margin-top: -6px;
    }
    .metric-caption.error {
        color: var(--rag-red-text);
    }
    .metric-actions {
        margin-top: auto;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
    }
    .status-badge.ok {
        background: var(--rag-green-bg);
        color: var(--rag-green-text);
    }
    .status-badge.ok::before {
        content: "";
        width: 7px;
        height: 7px;
        border-radius: 999px;
        background: var(--rag-green-bright);
        box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.15);
    }
    .status-badge.fail {
        background: var(--rag-red-bg);
        color: var(--rag-red-text);
    }
    .status-badge.fail::before {
        content: "";
        width: 7px;
        height: 7px;
        border-radius: 999px;
        background: var(--rag-red-strong);
        box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.15);
    }

    .settings-summary {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.48rem;
        margin: 0.25rem 0 1rem;
        padding: 0.72rem 0.8rem;
        border: 1px solid var(--rag-border);
        border-radius: 22px;
        background:
            radial-gradient(circle at 4% 0%, rgba(56, 189, 248, 0.12), transparent 28%),
            radial-gradient(circle at 100% 0%, var(--rag-blue-glow), transparent 28%),
            var(--rag-bg-card);
        box-shadow: var(--rag-shadow-card);
    }
    .settings-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.36rem;
        min-height: 30px;
        padding: 0.22rem 0.68rem;
        border: 1px solid var(--rag-border);
        border-radius: 999px;
        background: var(--rag-bg-elevated);
        color: var(--rag-text-muted);
        font-size: 0.8rem;
        font-weight: 780;
        white-space: nowrap;
    }
    .settings-chip .ui-icon {
        width: 0.86rem;
        height: 0.86rem;
        color: currentColor;
        opacity: 0.9;
    }
    .settings-chip strong {
        color: var(--rag-text-primary);
        font-weight: 900;
    }
    .settings-chip.on {
        background: var(--rag-green-bg);
        border-color: var(--rag-green-border);
        color: var(--rag-green-text);
    }
    .settings-chip.off {
        background: var(--rag-bg-elevated);
        border-color: var(--rag-border);
        color: var(--rag-text-placeholder);
    }

    .settings-group-card {
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        gap: 0.72rem;
        margin: 0.15rem 0 0.7rem;
        padding: 0.78rem 0.88rem;
        border: 1px solid var(--rag-border);
        border-radius: 18px;
        background:
            radial-gradient(circle at 100% 0%, var(--rag-blue-glow), transparent 34%),
            var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
    }
    .settings-group-card::after {
        content: "";
        position: absolute;
        right: -18px;
        bottom: -24px;
        width: 72px;
        height: 72px;
        border-radius: 999px;
        background: var(--rag-blue-glow);
        pointer-events: none;
    }
    .settings-group-card > .ui-icon {
        position: relative;
        z-index: 1;
        width: 2.05rem;
        height: 2.05rem;
        padding: 0.48rem;
        border-radius: 14px;
        border: 1px solid var(--rag-blue-100);
        background: var(--rag-blue-50);
        color: var(--rag-blue-primary);
        box-sizing: border-box;
        flex: 0 0 auto;
    }
    .settings-group-card.generation > .ui-icon {
        border-color: var(--rag-green-border);
        background: var(--rag-green-bg);
        color: var(--rag-green-text);
    }
    .settings-group-card.agent > .ui-icon {
        border-color: var(--rag-amber-border);
        background: var(--rag-amber-bg);
        color: var(--rag-amber-text);
    }
    .settings-group-title {
        position: relative;
        z-index: 1;
        color: var(--rag-text-primary);
        font-size: 0.96rem;
        font-weight: 900;
        line-height: 1.3;
    }
    .settings-group-copy {
        position: relative;
        z-index: 1;
        margin-top: 0.12rem;
        color: var(--rag-text-placeholder);
        font-size: 0.78rem;
        line-height: 1.5;
    }

    .marketing-copilot-hero {
        position: relative;
        overflow: hidden;
        margin: 0.25rem 0 1rem;
        padding: 1.25rem 1.35rem;
        border: 1px solid var(--rag-border);
        border-radius: 24px;
        background:
            radial-gradient(circle at 92% 8%, var(--rag-blue-glow), transparent 26%),
            linear-gradient(135deg, var(--rag-bg-card), var(--rag-bg-elevated));
        box-shadow: var(--rag-shadow-card);
    }
    .marketing-copilot-kicker,
    .marketing-copilot-tags span,
    .marketing-flow-heading,
    .marketing-section-title {
        display: flex;
        align-items: center;
    }
    .marketing-copilot-kicker {
        gap: 0.4rem;
        color: var(--rag-blue-primary);
        font-size: 0.78rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0;
    }
    .marketing-copilot-kicker .ui-icon,
    .marketing-copilot-tags .ui-icon {
        width: 0.95rem;
        height: 0.95rem;
        color: currentColor;
    }
    .marketing-copilot-title {
        margin-top: 0.4rem;
        color: var(--rag-text-primary);
        font-size: clamp(1.55rem, 3vw, 2.35rem);
        font-weight: 950;
        line-height: 1.12;
    }
    .marketing-copilot-copy {
        max-width: 860px;
        margin-top: 0.58rem;
        color: var(--rag-text-secondary);
        font-size: 0.94rem;
        line-height: 1.65;
    }
    .marketing-copilot-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.48rem;
        margin-top: 0.88rem;
    }
    .marketing-copilot-tags span {
        gap: 0.35rem;
        min-height: 30px;
        padding: 0.18rem 0.62rem;
        border: 1px solid var(--rag-border);
        border-radius: 999px;
        background: var(--rag-bg-elevated);
        color: var(--rag-text-muted);
        font-size: 0.78rem;
        font-weight: 780;
    }
    .marketing-section-title {
        justify-content: space-between;
        gap: 0.7rem;
        margin: 0.1rem 0 0.65rem;
        color: var(--rag-text-primary);
    }
    .marketing-section-title strong {
        font-size: 1rem;
        font-weight: 930;
    }
    .marketing-section-title span {
        color: var(--rag-text-placeholder);
        font-size: 0.78rem;
    }
    .marketing-flow-card,
    .marketing-checklist {
        min-height: 178px;
        margin-bottom: 0.7rem;
        padding: 1rem;
        border: 1px solid var(--rag-border);
        border-radius: 18px;
        background: var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
    }
    .marketing-flow-heading {
        gap: 0.7rem;
    }
    .marketing-flow-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 2.15rem;
        height: 2.15rem;
        border: 1px solid var(--rag-blue-100);
        border-radius: 13px;
        background: var(--rag-blue-50);
        color: var(--rag-blue-primary);
        flex: 0 0 auto;
    }
    .marketing-flow-icon .ui-icon {
        width: 1.05rem;
        height: 1.05rem;
        color: currentColor;
    }
    .marketing-flow-title {
        color: var(--rag-text-primary);
        font-size: 0.98rem;
        font-weight: 930;
        line-height: 1.28;
    }
    .marketing-flow-subtitle,
    .marketing-flow-output,
    .marketing-checklist li,
    .marketing-checklist-note {
        color: var(--rag-text-secondary);
        font-size: 0.8rem;
        line-height: 1.55;
    }
    .marketing-flow-output {
        margin-top: 0.75rem;
        color: var(--rag-text-placeholder);
    }
    .marketing-checklist-title {
        color: var(--rag-text-primary);
        font-weight: 930;
        margin-bottom: 0.5rem;
    }
    .marketing-checklist ol {
        margin: 0.25rem 0 0.8rem 1.1rem;
        padding: 0;
    }
    .marketing-checklist code {
        color: var(--rag-blue-primary);
        background: var(--rag-blue-50);
        border-radius: 6px;
        padding: 0.08rem 0.28rem;
    }
    .marketing-checklist-note {
        padding-top: 0.7rem;
        border-top: 1px solid var(--rag-border-subtle);
        color: var(--rag-text-placeholder);
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: background 0.18s, border-color 0.18s, color 0.18s;
    }

    @media (max-width: 900px) {
        .metric-card {
            min-height: 100px;
            padding: 14px 16px;
        }
        .metric-value {
            font-size: 1.5rem;
        }
    }
"""
