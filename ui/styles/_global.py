GLOBAL_CSS = """
/* ============================================
   全局基础样式
   ============================================ */

/* 隐藏 Streamlit 默认元素 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* 主内容区域：使用 CSS 变量，深色模式自动切换 */
.stApp,
.stApp > .main,
.stApp > .main > .block-container,
.stApp > .main > div[data-testid="stHeader"],
.stApp > div[data-testid="stDecoration"],
.stApp > div[data-testid="stHeader"],
section[data-testid="stSidebar"] > div:first-child {
    background: var(--rag-bg-page) !important;
}

.stApp > div[data-testid="stDecoration"]::before {
    display: none !important;
}

section[data-testid="stSidebar"] > div:first-child {
    padding-top: 10px;
}

section[data-testid="stSidebar"] > div:first-child > div {
    padding-top: 10px;
}

/* 重置 body 默认边距 */
body {
    margin: 0;
    padding: 0;
    background:
        radial-gradient(circle at 8% 0%, var(--rag-blue-glow), transparent 28%),
        radial-gradient(circle at 92% 10%, rgba(34, 197, 94, 0.08), transparent 24%),
        var(--rag-bg-page);
}

/* 全局字体设置 */
* {
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans SC", sans-serif !important;
}

::selection {
    background: var(--rag-blue-100);
    color: var(--rag-blue-primary);
}

:focus-visible {
    outline: 3px solid var(--rag-blue-glow);
    outline-offset: 3px;
}

button,
[role="button"],
input,
textarea,
select,
summary {
    -webkit-tap-highlight-color: transparent;
}

button:focus-visible,
[role="button"]:focus-visible,
summary:focus-visible,
input:focus-visible,
textarea:focus-visible,
select:focus-visible {
    outline: 3px solid var(--rag-blue-glow) !important;
    outline-offset: 3px !important;
}

::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    border: 2px solid transparent;
    border-radius: 999px;
    background: var(--rag-border-strong);
    background-clip: padding-box;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--rag-text-placeholder);
    background-clip: padding-box;
}

.block-container {
    padding-top: 1.25rem !important;
}

[data-testid="stMarkdownContainer"] {
    color: var(--rag-text-secondary);
    line-height: 1.72;
}

[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    color: var(--rag-text-primary);
    letter-spacing: -0.015em;
}

[data-testid="stMarkdownContainer"] a {
    color: var(--rag-blue-primary);
    text-decoration: none;
    border-bottom: 1px solid var(--rag-blue-200);
}

[data-testid="stMarkdownContainer"] a:hover {
    color: var(--rag-blue-accent);
    border-bottom-color: var(--rag-blue-accent);
}

[data-testid="stMarkdownContainer"] code:not(pre code) {
    padding: 0.12rem 0.34rem;
    border: 1px solid var(--rag-border);
    border-radius: 8px;
    background: var(--rag-bg-code);
    color: var(--rag-text-primary);
    font-size: 0.88em;
}

[data-testid="stMarkdownContainer"] pre,
[data-testid="stMarkdownContainer"] pre code {
    border-radius: 16px;
    background: var(--rag-bg-code) !important;
    color: var(--rag-text-primary) !important;
}

[data-testid="stMarkdownContainer"] pre {
    padding: 0.95rem 1rem;
    border: 1px solid var(--rag-border);
    box-shadow: var(--rag-shadow-sm);
    overflow-x: auto;
}

[data-testid="stMarkdownContainer"] blockquote {
    margin: 0.8rem 0;
    padding: 0.78rem 1rem;
    border-left: 4px solid var(--rag-blue-300);
    border-radius: 0 14px 14px 0;
    background: var(--rag-blue-50);
    color: var(--rag-text-secondary);
}

[data-testid="stMarkdownContainer"] table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    overflow: hidden;
    border: 1px solid var(--rag-border);
    border-radius: 16px;
    background: var(--rag-bg-card);
    box-shadow: var(--rag-shadow-sm);
}

[data-testid="stMarkdownContainer"] th,
[data-testid="stMarkdownContainer"] td {
    padding: 0.72rem 0.78rem;
    border-bottom: 1px solid var(--rag-border-light);
    color: var(--rag-text-secondary);
}

[data-testid="stMarkdownContainer"] th {
    background: var(--rag-bg-elevated);
    color: var(--rag-text-primary);
    font-weight: 850;
}

[data-testid="stMarkdownContainer"] tr:last-child td {
    border-bottom: 0;
}

[data-testid="stMarkdownContainer"] hr,
hr {
    margin: 1.15rem 0;
    border: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--rag-border-strong), transparent);
}

div[data-testid="stDataFrame"],
div[data-testid="stTable"] {
    overflow: hidden;
    border: 1px solid var(--rag-border);
    border-radius: 18px;
    background: var(--rag-bg-card);
    box-shadow: var(--rag-shadow-sm);
}

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
    }

    .ai-message.typing-cursor::before,
    .upload-task-row.processing::after {
        display: none !important;
    }
}
/* 隐藏 Streamlit 内置 checkbox 文本（仅限目录管理区） */
.dir-table .stCheckbox > label > span:last-child {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
    visibility: hidden !important;
}

/* 隐藏 checkbox 旁边的文本 */
.stCheckbox > label > span:last-child {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
    visibility: hidden !important;
}

"""
