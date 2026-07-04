"""Styles for chat."""

CHAT_CSS = """
    .chat-topbar {
        position: sticky;
        top: 0;
        z-index: 40;
        margin: -0.25rem 0 0.9rem;
        padding: 0.58rem 1rem 0.62rem;
        border-bottom: 1px solid var(--rag-border-light);
        background:
            linear-gradient(180deg, rgba(248, 250, 252, 0.96) 0%, rgba(248, 250, 252, 0.82) 100%);
        backdrop-filter: blur(14px);
        text-align: center;
    }
    .chat-topbar-title {
        max-width: 760px;
        margin: 0 auto;
        color: var(--rag-text-primary);
        font-size: 0.98rem;
        font-weight: 760;
        line-height: 1.38;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .chat-topbar-subtitle {
        margin-top: 0.18rem;
        color: var(--rag-text-disabled);
        font-size: 0.72rem;
        line-height: 1.35;
    }
    div[class*="st-key-chat_flow_area"] {
        max-width: 980px;
        margin: 0 auto !important;
    }
    div[class*="st-key-chat_input_shell"] {
        max-width: 980px;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    .user-message {
        background: linear-gradient(135deg, #1d7fff 0%, var(--rag-blue-accent) 100%);
        color: white;
        border-radius: 22px 22px 6px 22px;
        padding: 13px 16px;
        max-width: 75%;
        margin: 12px 10px 12px auto;
        word-wrap: break-word;
        box-shadow: 0 2px 8px var(--rag-blue-glow);
        transition: box-shadow 0.2s;
        font-size: 0.95rem;
        line-height: 1.5;
        white-space: pre-wrap;
        animation: message-enter 0.22s ease-out both;
    }
    .user-message:hover {
        box-shadow: 0 4px 12px rgba(22, 119, 255, 0.3);
    }
    .message-row.user .user-message {
        border: 1px solid rgba(255, 255, 255, 0.28);
    }

    /* AI消息气泡 */
    .ai-message {
        background:
            radial-gradient(circle at 0% 0%, var(--rag-blue-glow), transparent 30%),
            var(--rag-bg-card);
        color: var(--rag-text-secondary);
        border-radius: 22px 22px 22px 6px;
        border: 1px solid var(--rag-border);
        padding: 14px 17px;
        max-width: 75%;
        margin: 12px auto 12px 10px;
        word-wrap: break-word;
        white-space: normal;
        box-shadow: var(--rag-shadow-lg);
        transition: box-shadow 0.2s, transform 0.2s, border-color 0.2s;
        font-size: 0.95rem;
        line-height: 1.5;
        position: relative;
        animation: message-enter 0.24s ease-out both;
    }
    .ai-message.typing-cursor {
        overflow: hidden;
    }
    .ai-message.typing-cursor::before {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(110deg, transparent 0%, rgba(255,255,255,0.35) 42%, transparent 58%);
        transform: translateX(-120%);
        animation: answer-shimmer 1.8s ease-in-out infinite;
        pointer-events: none;
    }
    .ai-message:hover {
        border-color: var(--rag-blue-100);
        box-shadow: var(--rag-shadow-card-hover);
        transform: translateY(-1px);
    }
    .message-row.ai .ai-message {
        background: var(--rag-blue-50-gradient);
        border-color: var(--rag-border);
    }
    .ai-message.has-actions {
        padding-top: 40px;
        padding-bottom: 10px;
    }
    .message-content {
        white-space: pre-wrap;
        overflow-wrap: anywhere;
    }
    .answer-status-bar {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.38rem;
        margin: -0.08rem 0 0.58rem;
        padding-bottom: 0.52rem;
        border-bottom: 1px solid var(--rag-border-light);
    }
    .answer-status-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.32rem;
        min-height: 24px;
        padding: 0.16rem 0.48rem;
        border: 1px solid var(--rag-border);
        border-radius: 999px;
        background: var(--rag-bg-elevated);
        color: var(--rag-text-muted);
        font-size: 0.74rem;
        font-weight: 740;
        line-height: 1;
    }
    .answer-status-chip .ui-icon {
        width: 0.86rem;
        height: 0.86rem;
        color: var(--rag-blue-primary);
        stroke: currentColor;
    }
    .message-content p:first-child {
        margin-top: 0;
    }
    .message-content p:last-child {
        margin-bottom: 0;
    }
    .message-code {
        margin: 10px 0;
        padding: 12px;
        border-radius: 12px;
        background: var(--rag-bg-code);
        border: 1px solid var(--rag-border);
        color: var(--rag-text-primary);
        overflow-x: auto;
        white-space: pre;
        font-family: Consolas, "SFMono-Regular", Menlo, Monaco, monospace;
        font-size: 0.88rem;
        line-height: 1.45;
    }
    .message-code code {
        font-family: inherit;
        font-size: inherit;
    }
    .answer-copy-btn {
        position: absolute;
        top: 8px;
        right: 12px;
        height: 28px;
        min-width: 68px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        border: 1px solid var(--rag-blue-200);
        border-radius: 999px;
        background: var(--rag-bg-card-alt);
        color: var(--rag-blue-light);
        font-size: 0.78rem;
        line-height: 1;
        cursor: pointer;
        transition: all 0.2s;
    }
    .answer-copy-btn:hover {
        background: var(--rag-blue-100);
        border-color: var(--rag-blue-300);
    }
    .answer-copy-btn:focus-visible,
    .answer-regenerate-btn:focus-visible,
    .source-copy-btn:focus-visible,
    .source-evidence summary:focus-visible {
        outline: 3px solid var(--rag-blue-glow) !important;
        outline-offset: 3px !important;
        border-color: var(--rag-border-focus) !important;
    }
    .answer-copy-btn.copied {
        color: var(--rag-green-text);
        border-color: var(--rag-green-bright);
        background: var(--rag-green-bg);
    }
    .answer-copy-btn .ui-icon {
        width: 13px;
        height: 13px;
        color: currentColor;
        stroke: currentColor;
        stroke-width: 2.1;
        flex: 0 0 auto;
    }
    .answer-actions {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        min-height: 28px;
        margin-top: 8px;
    }
    .answer-regenerate-btn {
        width: 32px;
        height: 28px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        border: 1px solid var(--rag-border);
        background: var(--rag-bg-card);
        color: var(--rag-text-muted);
        cursor: pointer;
        font-size: 0.95rem;
        line-height: 1;
        transition: all 0.2s;
    }
    .answer-regenerate-btn .ui-icon {
        width: 16px;
        height: 16px;
        color: currentColor;
        stroke: currentColor;
        stroke-width: 2.2;
        display: block;
    }
    .answer-regenerate-btn::before {
        content: "";
        width: 16px;
        height: 16px;
        display: block;
        background-color: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 12a9 9 0 0 1-15.5 6.3L3 16'/%3E%3Cpath d='M3 21v-5h5'/%3E%3Cpath d='M3 12A9 9 0 0 1 18.5 5.7L21 8'/%3E%3Cpath d='M21 3v5h-5'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 12a9 9 0 0 1-15.5 6.3L3 16'/%3E%3Cpath d='M3 21v-5h5'/%3E%3Cpath d='M3 12A9 9 0 0 1 18.5 5.7L21 8'/%3E%3Cpath d='M21 3v5h-5'/%3E%3C/svg%3E") center / contain no-repeat;
    }
    .answer-regenerate-btn > .ui-icon {
        display: none;
    }
    .answer-regenerate-btn:hover {
        background: var(--rag-bg-surface);
        border-color: var(--rag-border-strong);
        color: var(--rag-blue-light);
    }
    .answer-copy-btn:disabled,
    .answer-regenerate-btn:disabled {
        opacity: 0.45;
        cursor: not-allowed;
    }
    div[class*="st-key-regen_trigger_"] {
        position: absolute !important;
        width: 1px !important;
        height: 1px !important;
        overflow: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* 消息行布局 */
    .message-row {
        display: flex;
        align-items: flex-start;
        gap: 0.52rem;
        margin: 26px 0;
    }
    .message-row.user {
        flex-direction: row-reverse;
    }

    /* 头像样式 */
    .avatar {
        position: relative;
        width: 34px;
        height: 34px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        margin: 2px 4px 0;
        overflow: hidden;
        box-shadow: 0 10px 22px rgba(15, 23, 42, 0.10);
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }
    .avatar::before {
        content: "";
        position: absolute;
        left: 50%;
        top: 50%;
        z-index: 1;
        width: 17px;
        height: 17px;
        transform: translate(-50%, -50%);
        background: currentColor;
        -webkit-mask: center / contain no-repeat;
        mask: center / contain no-repeat;
        pointer-events: none;
    }
    .avatar::after {
        content: "";
        position: absolute;
        right: 4px;
        bottom: 4px;
        width: 6px;
        height: 6px;
        border-radius: 999px;
        background: currentColor;
        box-shadow: 0 0 0 2px var(--rag-bg-card);
        opacity: 0.86;
    }
    .message-row:hover .avatar {
        transform: translateY(-1px);
        box-shadow: 0 14px 28px rgba(15, 23, 42, 0.14);
    }
    .ui-icon {
        width: 1.1em;
        height: 1.1em;
        display: inline-block;
        vertical-align: -0.18em;
        stroke: currentColor;
        stroke-width: 2;
        stroke-linecap: round;
        stroke-linejoin: round;
        fill: none;
    }
    .sidebar-main-header .ui-icon,
    .subsection-title .ui-icon {
        width: 1.05em;
        height: 1.05em;
    }
    .avatar .ui-icon {
        display: none !important;
    }
    .user-avatar {
        border: 1px solid var(--rag-blue-200);
        background:
            radial-gradient(circle at 28% 20%, rgba(255, 255, 255, 0.92), transparent 26%),
            linear-gradient(145deg, var(--rag-blue-50) 0%, var(--rag-blue-100) 100%);
        color: var(--rag-blue-primary);
    }
    .user-avatar::before {
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z'/%3E%3C/svg%3E");
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z'/%3E%3C/svg%3E");
    }
    .ai-avatar {
        border: 1px solid var(--rag-green-border);
        background:
            radial-gradient(circle at 28% 20%, rgba(255, 255, 255, 0.94), transparent 28%),
            linear-gradient(145deg, var(--rag-green-bg) 0%, var(--rag-bg-card) 100%);
        color: var(--rag-green-text);
    }
    .ai-avatar::before {
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='m12 2l1.75 6.25L20 10l-6.25 1.75L12 18l-1.75-6.25L4 10l6.25-1.75Zm7 14l.75 2.25L22 19l-2.25.75L19 22l-.75-2.25L16 19l2.25-.75Z'/%3E%3C/svg%3E");
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='m12 2l1.75 6.25L20 10l-6.25 1.75L12 18l-1.75-6.25L4 10l6.25-1.75Zm7 14l.75 2.25L22 19l-2.25.75L19 22l-.75-2.25L16 19l2.25-.75Z'/%3E%3C/svg%3E");
    }

    /* 引用来源样式 */
    .source-evidence {
        max-width: 72%;
        margin: -2px auto 11px 54px;
        border: 1px solid var(--rag-blue-100);
        border-radius: 14px;
        background:
            radial-gradient(circle at 100% 0%, var(--rag-blue-glow), transparent 30%),
            var(--rag-blue-50-gradient);
        box-shadow: var(--rag-shadow-sm);
        overflow: hidden;
    }
    .source-evidence summary {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.62rem;
        padding: 0.58rem 0.75rem;
        cursor: pointer;
        color: var(--rag-blue-accent);
        font-size: 0.82rem;
        font-weight: 820;
        list-style: none;
    }
    .source-evidence summary::-webkit-details-marker {
        display: none;
    }
    .source-evidence summary::after {
        content: "";
        width: 14px;
        height: 14px;
        flex: 0 0 14px;
        background: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='m7 10 5 5 5-5' fill='none' stroke='black' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='m7 10 5 5 5-5' fill='none' stroke='black' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        transition: transform 0.18s ease;
    }
    .source-evidence[open] summary::after {
        transform: rotate(180deg);
    }
    .source-evidence-body {
        padding: 0 0.72rem 0.7rem;
    }
    .source-evidence-meta {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        color: var(--rag-text-placeholder);
        font-size: 0.8rem;
        font-weight: 600;
        white-space: nowrap;
    }
    .source-evidence-title,
    .source-evidence-actions {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        min-width: 0;
    }
    .source-evidence-actions {
        margin-left: auto;
    }
    .source-box {
        background: var(--rag-bg-card);
        border: 1px solid var(--rag-border);
        border-radius: 12px;
        padding: 12px 13px;
        margin: 8px 0;
        box-shadow: var(--rag-shadow-sm);
    }
    .source-box:hover {
        border-color: var(--rag-blue-200);
        box-shadow: var(--rag-shadow-md);
    }
    .source-title {
        display: flex;
        align-items: center;
        gap: 0.42rem;
        font-weight: 650;
        color: var(--rag-blue-primary);
        margin-bottom: 8px;
        font-size: 0.9rem;
        min-width: 0;
    }
    .source-file {
        display: inline-flex;
        align-items: center;
        gap: 0.38rem;
        min-width: 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .source-index {
        display: inline-flex;
        align-items: center;
        flex: 0 0 auto;
        color: var(--rag-text-muted);
        background: var(--rag-bg-card-alt);
        border: 1px solid var(--rag-border);
        border-radius: 999px;
        padding: 0.08rem 0.42rem;
        font-size: 0.72rem;
        font-weight: 720;
        line-height: 1.25;
    }
    .source-score {
        margin-left: auto;
        color: var(--rag-blue-primary);
        background: var(--rag-blue-50);
        border: 1px solid var(--rag-blue-200);
        border-radius: 999px;
        padding: 0.08rem 0.45rem;
        font-size: 0.78rem;
        font-weight: 600;
        flex: 0 0 auto;
    }
    .source-label {
        display: inline-flex;
        align-items: center;
        margin-bottom: 5px;
        color: var(--rag-text-placeholder);
        font-size: 0.72rem;
        font-weight: 760;
        letter-spacing: 0;
    }
    .source-trace-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.32rem;
        margin: -2px 0 0.52rem;
    }
    .source-trace-chip {
        display: inline-flex;
        align-items: center;
        min-height: 22px;
        padding: 0.08rem 0.42rem;
        border: 1px solid var(--rag-border);
        border-radius: 999px;
        background: var(--rag-bg-elevated);
        color: var(--rag-text-placeholder);
        font-size: 0.72rem;
        font-weight: 680;
        line-height: 1;
    }
    .source-content {
        color: var(--rag-text-muted);
        font-size: 0.85rem;
        line-height: 1.55;
    }
    .source-copy-btn {
        margin-left: 0.45rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.28rem;
        min-height: 26px;
        border: 1px solid var(--rag-blue-200);
        border-radius: 999px;
        background: var(--rag-bg-card);
        color: var(--rag-blue-primary);
        padding: 0.12rem 0.56rem;
        font-size: 0.76rem;
        font-weight: 650;
        line-height: 1;
        cursor: pointer;
        box-shadow: 0 5px 12px rgba(37, 99, 235, 0.04);
        transition:
            transform 0.16s ease,
            box-shadow 0.16s ease,
            border-color 0.16s ease,
            background 0.16s ease,
            color 0.16s ease;
    }
    .source-copy-btn:hover,
    .source-copy-btn.copied {
        background: var(--rag-blue-50);
    }
    .source-copy-btn:hover {
        transform: translateY(-1px);
        border-color: var(--rag-blue-300);
        box-shadow: 0 8px 18px var(--rag-blue-glow);
    }
    .source-copy-btn.copied {
        border-color: var(--rag-green-border);
        color: var(--rag-green-text);
        background: var(--rag-green-bg);
    }
    .source-copy-btn .ui-icon {
        width: 0.86rem;
        height: 0.86rem;
        flex: 0 0 auto;
        color: currentColor;
        stroke: currentColor;
        stroke-width: 2.2;
    }
    .source-copy-all {
        padding: 0.16rem 0.62rem;
        background: var(--rag-bg-card-alt);
    }

    /* 思考过程行内样式：外层复用 AI 气泡 */
    .process-step {
        display: flex;
        align-items: center;
        gap: 8px;
        min-height: 24px;
        color: var(--rag-text-secondary);
        font-size: 0.9rem;
        line-height: 1.5;
        transition: color 0.18s ease, transform 0.18s ease;
    }
    .process-step.done {
        color: var(--rag-green-text);
    }
    .process-step.active {
        color: var(--rag-blue-primary);
        font-weight: 600;
        transform: translateX(2px);
    }
    .process-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--rag-border-strong);
        flex: 0 0 auto;
    }
    .process-step.done .process-dot {
        background: var(--rag-green-bright);
    }
    .process-step.active .process-dot {
        background: var(--rag-blue-light);
        box-shadow: 0 0 0 4px var(--rag-blue-glow);
        animation: process-breath 1.15s ease-in-out infinite;
    }

    /* Immediate browser-side feedback shown before the Streamlit rerun completes. */
    .rag-immediate-loading {
        position: fixed;
        z-index: 1001;
        display: flex;
        align-items: center;
        gap: 0.72rem;
        box-sizing: border-box;
        min-height: 58px;
        padding: 0.7rem 0.9rem;
        border: 1px solid var(--rag-blue-100);
        border-radius: 16px;
        background:
            radial-gradient(circle at 7% 0%, var(--rag-blue-glow), transparent 42%),
            var(--rag-bg-card);
        box-shadow: 0 14px 34px rgba(15, 23, 42, 0.12);
        color: var(--rag-text-secondary);
        pointer-events: none;
        animation: rag-loading-enter 0.18s ease-out both;
    }
    .rag-loading-icon {
        width: 30px;
        height: 30px;
        flex: 0 0 30px;
        border-radius: 11px;
        background:
            radial-gradient(circle at 50% 50%, var(--rag-blue-light) 0 3px, transparent 4px),
            var(--rag-blue-50);
        border: 1px solid var(--rag-blue-100);
        box-shadow: 0 0 0 4px var(--rag-blue-glow);
        animation: process-breath 1.15s ease-in-out infinite;
    }
    .rag-loading-copy {
        display: grid;
        gap: 0.08rem;
        min-width: 0;
    }
    .rag-loading-copy strong {
        color: var(--rag-blue-primary);
        font-size: 0.86rem;
        line-height: 1.35;
    }
    .rag-loading-copy small {
        color: var(--rag-text-placeholder);
        font-size: 0.76rem;
        line-height: 1.35;
    }
    .rag-loading-skeleton {
        display: inline-flex;
        align-items: center;
        gap: 0.26rem;
        margin-left: auto;
    }
    .rag-loading-skeleton i {
        width: 6px;
        height: 6px;
        border-radius: 999px;
        background: var(--rag-blue-light);
        opacity: 0.35;
        animation: rag-loading-dot 1s ease-in-out infinite;
    }
    .rag-loading-skeleton i:nth-child(2) {
        animation-delay: 0.14s;
    }
    .rag-loading-skeleton i:nth-child(3) {
        animation-delay: 0.28s;
    }
    @keyframes rag-loading-enter {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes rag-loading-dot {
        0%, 100% { opacity: 0.32; transform: translateY(0); }
        50% { opacity: 1; transform: translateY(-2px); }
    }

    .rag-latest-answer-button {
        position: fixed;
        z-index: 1002;
        display: inline-flex;
        align-items: center;
        gap: 0.38rem;
        min-height: 34px;
        padding: 0.36rem 0.72rem 0.36rem 0.56rem;
        border: 1px solid var(--rag-blue-200);
        border-radius: 999px;
        background: var(--rag-bg-card);
        color: var(--rag-blue-primary);
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.12);
        font-family: inherit;
        font-size: 0.76rem;
        font-weight: 820;
        line-height: 1;
        white-space: nowrap;
        cursor: pointer;
        opacity: 0;
        pointer-events: none;
        transform: translate(-50%, 8px);
        transition: opacity 0.18s ease, transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
    }
    .rag-latest-answer-button.visible {
        opacity: 1;
        pointer-events: auto;
        transform: translate(-50%, 0);
    }
    .rag-latest-answer-button:hover {
        border-color: var(--rag-blue-300);
        box-shadow: 0 12px 28px rgba(37, 99, 235, 0.16);
    }
    .rag-latest-answer-button:focus-visible {
        outline: 3px solid var(--rag-blue-glow);
        outline-offset: 3px;
    }
    .rag-latest-answer-button i {
        width: 15px;
        height: 15px;
        flex: 0 0 15px;
        background: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='m6 9l6 6l6-6' fill='none' stroke='black' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='m6 9l6 6l6-6' fill='none' stroke='black' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat;
    }

    /* 输入区域 - 固定悬浮输入框 */
    div[class*="st-key-chat_input_area"] {
        position: fixed !important;
        left: var(--rag-chat-composer-left, 23rem) !important;
        right: auto !important;
        bottom: 0.82rem !important;
        width: var(--rag-chat-composer-width, calc(100vw - 25rem)) !important;
        max-width: none !important;
        box-sizing: border-box;
        background:
            radial-gradient(circle at 8% 0%, var(--rag-blue-glow), transparent 32%),
            linear-gradient(180deg, rgba(255, 255, 255, 0.90) 0%, var(--rag-bg-card) 45%);
        padding: 8px 10px 7px;
        border: 1px solid var(--rag-border);
        border-radius: 18px;
        z-index: 1000;
        margin: 0 !important;
        box-shadow: 0 -12px 30px rgba(15, 23, 42, 0.08);
        backdrop-filter: blur(16px);
    }
    .block-container:has(div[class*="st-key-chat_input_area"]) {
        padding-bottom: var(--rag-chat-composer-space, 15rem) !important;
    }
    .chat-scroll-sentinel {
        height: 1px;
        scroll-margin-bottom: var(--rag-chat-composer-space, 15rem);
    }
    .chat-tools-row,
    div[class*="st-key-chat_prompt_tools"] {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.55rem;
        margin: 0.18rem 0 0;
        min-height: 18px;
    }
    div[class*="st-key-chat_prompt_tools"] > div {
        width: 100%;
    }
    .chat-prompt-strip {
        display: inline-flex;
        align-items: center;
        gap: 0.34rem;
        color: var(--rag-text-placeholder);
        font-size: 0.72rem;
        font-weight: 760;
    }
    .chat-prompt-strip::before {
        content: "";
        width: 7px;
        height: 7px;
        border-radius: 999px;
        background: #38bdf8;
        box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.12);
    }
    div[class*="st-key-quick_prompt_"] button {
        position: relative;
        min-width: 0 !important;
        min-height: 21px !important;
        height: 21px !important;
        padding: 0 0.44rem 0 1.12rem !important;
        border-radius: 999px !important;
        border: 1px solid var(--rag-border) !important;
        background: rgba(255, 255, 255, 0.56) !important;
        color: var(--rag-text-secondary) !important;
        font-size: 0.66rem !important;
        font-weight: 730 !important;
        white-space: nowrap !important;
        box-shadow: none !important;
        opacity: 0.9;
    }
    div[class*="st-key-quick_prompt_"] button::before {
        content: "";
        position: absolute;
        left: 0.42rem;
        top: 50%;
        width: 9px;
        height: 9px;
        transform: translateY(-50%);
        background: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='m12 2l1.75 6.25L20 10l-6.25 1.75L12 18l-1.75-6.25L4 10l6.25-1.75Zm7 14l.75 2.25L22 19l-2.25.75L19 22l-.75-2.25L16 19l2.25-.75Z'/%3E%3C/svg%3E") center / contain no-repeat;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='m12 2l1.75 6.25L20 10l-6.25 1.75L12 18l-1.75-6.25L4 10l6.25-1.75Zm7 14l.75 2.25L22 19l-2.25.75L19 22l-.75-2.25L16 19l2.25-.75Z'/%3E%3C/svg%3E") center / contain no-repeat;
        opacity: 0.72;
    }
    div[class*="st-key-quick_prompt_"] button:hover {
        background: var(--rag-bg-card) !important;
        border-color: var(--rag-blue-200) !important;
        color: var(--rag-blue-primary) !important;
        box-shadow: 0 5px 12px var(--rag-blue-glow) !important;
    }
    div[class*="st-key-quick_prompt_"] button:disabled {
        background: var(--rag-bg-elevated) !important;
        color: var(--rag-text-disabled) !important;
        border-color: var(--rag-border) !important;
        box-shadow: none !important;
    }
    div[class*="st-key-chat_prompt_tools"] details,
    div[class*="st-key-chat_flow_area"] details {
        border-radius: 16px;
    }
    div[class*="st-key-chat_prompt_tools"] details summary,
    div[class*="st-key-chat_flow_area"] details summary {
        color: var(--rag-text-muted);
        font-size: 0.82rem;
        font-weight: 780;
    }
    div[class*="st-key-chat_prompt_tools"] div[class*="st-key-quick_prompt_"] button,
    div[class*="st-key-chat_flow_area"] div[class*="st-key-sample_question_"] button {
        justify-content: flex-start !important;
        min-height: 38px !important;
        height: auto !important;
        padding: 0.52rem 0.72rem 0.52rem 1.82rem !important;
        border-radius: 14px !important;
        font-size: 0.84rem !important;
        white-space: normal !important;
        text-align: left !important;
    }
    div[class*="st-key-send_button"] button,
    div[class*="st-key-clear_button"] button,
    div[class*="st-key-stop_generation_button"] button {
        position: relative;
        min-width: 62px !important;
        height: 40px !important;
        padding: 0 0.48rem 0 1.42rem !important;
        border-radius: 12px !important;
        font-size: 0.74rem !important;
        font-weight: 820 !important;
        white-space: nowrap !important;
        box-shadow: none !important;
    }
    div[class*="st-key-send_button"] button::before,
    div[class*="st-key-clear_button"] button::before,
    div[class*="st-key-stop_generation_button"] button::before {
        content: "";
        position: absolute;
        left: 0.48rem;
        top: 50%;
        width: 12px;
        height: 12px;
        transform: translateY(-50%);
        background: currentColor;
        -webkit-mask: center / contain no-repeat;
        mask: center / contain no-repeat;
    }
    div[class*="st-key-send_button"] button {
        border: 1px solid var(--rag-blue-200) !important;
        background: var(--rag-blue-50) !important;
        color: var(--rag-blue-primary) !important;
    }
    div[class*="st-key-send_button"] button::before {
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m22 2l-7 20l-4-9l-9-4Zm0 0L11 13'/%3E%3C/svg%3E");
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m22 2l-7 20l-4-9l-9-4Zm0 0L11 13'/%3E%3C/svg%3E");
    }
    div[class*="st-key-clear_button"] button {
        border: 1px solid var(--rag-border) !important;
        background: var(--rag-bg-elevated) !important;
        color: var(--rag-text-muted) !important;
    }
    div[class*="st-key-clear_button"] button::before {
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M3 6h18M8 6V4h8v2m3 0l-1 14H6L5 6m4 4v6m6-6v6'/%3E%3C/svg%3E");
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M3 6h18M8 6V4h8v2m3 0l-1 14H6L5 6m4 4v6m6-6v6'/%3E%3C/svg%3E");
    }
    div[class*="st-key-stop_generation_button"] button {
        border: 1px solid var(--rag-red-border) !important;
        background: var(--rag-red-bg) !important;
        color: var(--rag-red-text) !important;
    }
    div[class*="st-key-stop_generation_button"] button::before {
        border-radius: 3px;
        background: currentColor;
    }
    div[class*="st-key-stop_generation_button"] button:hover {
        border-color: var(--rag-red-text) !important;
        background: #fee2e2 !important;
        box-shadow: 0 8px 18px rgba(239, 68, 68, 0.10) !important;
    }
    div[class*="st-key-send_button"] button:hover {
        border-color: var(--rag-blue-300) !important;
        background: var(--rag-blue-100) !important;
        box-shadow: 0 8px 18px var(--rag-blue-glow) !important;
    }
    div[class*="st-key-clear_button"] button:hover {
        border-color: var(--rag-red-border) !important;
        background: var(--rag-red-bg) !important;
        color: var(--rag-red-text) !important;
        box-shadow: 0 8px 18px rgba(239, 68, 68, 0.10) !important;
    }
    .chat-input-hint {
        display: inline-flex;
        align-items: center;
        justify-content: flex-start;
        gap: 0.28rem;
        width: max-content;
        max-width: 100%;
        margin-top: 0;
        color: var(--rag-text-placeholder);
        font-size: 0.72rem;
        line-height: 1.45;
        white-space: nowrap;
    }
    div[class*="st-key-chat_prompt_tools"] div[data-testid="stHtml"]:has(.chat-input-hint) {
        display: flex;
        justify-content: flex-end;
    }
    div[class*="st-key-chat_input_area"] div[data-testid="stTextArea"] > div {
        min-height: 40px !important;
        border-radius: 12px !important;
    }
    div[class*="st-key-chat_input_area"] div[data-testid="stTextArea"] textarea {
        min-height: 40px !important;
        height: 40px !important;
        padding: 9px 13px !important;
        font-size: 0.86rem !important;
    }
    .chat-input-hint span {
        display: inline-flex;
        align-items: center;
        gap: 0.32rem;
    }
    .chat-tools-row .chat-input-hint {
        display: inline-flex;
        flex: 0 0 auto;
        justify-content: flex-end;
        white-space: nowrap;
    }
    .chat-input-hint kbd {
        border: 1px solid var(--rag-border-strong);
        border-bottom-width: 2px;
        border-radius: 7px;
        padding: 0.08rem 0.38rem;
        background: var(--rag-bg-elevated);
        color: var(--rag-text-secondary);
        font-size: 0.74rem;
        font-family: inherit;
    }

    .chat-context-bar {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin: 0.35rem 0 0.85rem;
        padding: 0.7rem 0.78rem;
        border: 1px solid var(--rag-border);
        border-radius: 18px;
        background: var(--rag-bg-card);
        box-shadow: var(--rag-shadow-sm);
    }
    .chat-context-item {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        min-height: 28px;
        padding: 0.2rem 0.5rem;
        border-radius: 999px;
        background: var(--rag-bg-elevated);
        color: var(--rag-text-muted);
        font-size: 0.8rem;
        font-weight: 760;
    }
    .chat-context-item strong {
        color: var(--rag-text-primary);
        max-width: 180px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .chat-context-dot {
        width: 4px;
        height: 4px;
        border-radius: 999px;
        background: var(--rag-border-strong);
    }

    .agent-debug-panel {
        max-width: 78%;
        border-style: dashed;
        background:
            radial-gradient(circle at 0% 0%, var(--rag-amber-bg), transparent 35%),
            var(--rag-bg-card) !important;
    }
    .agent-debug-title {
        display: inline-flex;
        align-items: center;
        margin-bottom: 0.5rem;
        padding: 0.12rem 0.5rem;
        border: 1px solid var(--rag-border);
        border-radius: 999px;
        background: var(--rag-bg-elevated);
        color: var(--rag-text-primary);
        font-size: 0.78rem;
        font-weight: 820;
    }

    @keyframes message-enter {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes answer-shimmer {
        0% { transform: translateX(-120%); opacity: 0; }
        20% { opacity: 1; }
        70% { opacity: 1; }
        100% { transform: translateX(120%); opacity: 0; }
    }
    @keyframes process-breath {
        0%, 100% { box-shadow: 0 0 0 4px var(--rag-blue-glow); transform: scale(1); }
        50% { box-shadow: 0 0 0 7px rgba(37, 99, 235, 0.08); transform: scale(1.12); }
    }

    @media (max-width: 900px) {
        .user-message,
        .ai-message,
        .source-evidence,
        .agent-debug-panel {
            max-width: calc(100% - 46px);
        }
        .answer-status-bar,
        .source-title,
        .source-evidence summary {
            align-items: flex-start;
        }
        .source-evidence-actions {
            flex-wrap: wrap;
            justify-content: flex-end;
        }
        .chat-context-bar {
            gap: 0.35rem;
        }
        .chat-context-dot {
            display: none;
        }
        .chat-input-hint {
            flex-direction: row;
        }
    }

    /* 输入框样式 - 简洁无滚动条 */
"""
