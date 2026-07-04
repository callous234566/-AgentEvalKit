"""CSS custom properties: light defaults + dark overrides.

Defines the shared color palette so that component CSS can reference
var(--rag-*) instead of hard-coding hex values.  Dark mode only needs
to re-declare the variables; individual component dark overrides that
simply restyle colors become redundant and are removed.
"""

VARIABLES_CSS = """
:root {
    --rag-bg-body: #ffffff;
    --rag-bg-page: #f8fafc;
    --rag-bg-card: #ffffff;
    --rag-bg-card-alt: #f8fbff;
    --rag-bg-elevated: #f8fafc;
    --rag-bg-surface: #f1f5f9;
    --rag-bg-input: #ffffff;
    --rag-bg-code: #f6f8fa;

    --rag-text-primary: #0f172a;
    --rag-text-secondary: #334155;
    --rag-text-muted: #475569;
    --rag-text-placeholder: #64748b;
    --rag-text-disabled: #94a3b8;

    --rag-border: #e2e8f0;
    --rag-border-light: #f1f5f9;
    --rag-border-strong: #cbd5e1;
    --rag-border-focus: #1677ff;

    --rag-blue-primary: #2563eb;
    --rag-blue-accent: #1d4ed8;
    --rag-blue-light: #1677ff;
    --rag-blue-100: #dbeafe;
    --rag-blue-200: #bfdbfe;
    --rag-blue-300: #93c5fd;
    --rag-blue-400: #60a5fa;
    --rag-blue-50: #eff6ff;
    --rag-blue-50-gradient: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
    --rag-blue-glow: rgba(37, 99, 235, 0.12);

    --rag-green-text: #15803d;
    --rag-green-bg: #f0fdf4;
    --rag-green-border: #bbf7d0;
    --rag-green-bright: #22c55e;

    --rag-red-text: #b91c1c;
    --rag-red-bg: #fff7f7;
    --rag-red-border: #fecaca;
    --rag-red-strong: #dc2626;

    --rag-amber-text: #b45309;
    --rag-amber-bg: #fff7ed;
    --rag-amber-border: #fed7aa;

    --rag-shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.04);
    --rag-shadow-md: 0 2px 8px rgba(0, 0, 0, 0.08);
    --rag-shadow-card: 0 10px 26px rgba(15, 23, 42, 0.07);
    --rag-shadow-lg: 0 12px 30px rgba(15, 23, 42, 0.06);
    --rag-shadow-card-hover: 0 16px 34px rgba(37, 99, 235, 0.12);
}

body.rag-dark {
    --rag-bg-body: #0f172a;
    --rag-bg-page: #0f172a;
    --rag-bg-card: #111827;
    --rag-bg-card-alt: #111827;
    --rag-bg-elevated: #1f2937;
    --rag-bg-surface: #1e293b;
    --rag-bg-input: #111827;
    --rag-bg-code: #111827;

    --rag-text-primary: #f8fafc;
    --rag-text-secondary: #e5e7eb;
    --rag-text-muted: #cbd5e1;
    --rag-text-placeholder: #94a3b8;
    --rag-text-disabled: #64748b;

    --rag-border: #334155;
    --rag-border-light: #1f2937;
    --rag-border-strong: #475569;
    --rag-border-focus: #60a5fa;

    --rag-blue-primary: #60a5fa;
    --rag-blue-accent: #2563eb;
    --rag-blue-light: #93c5fd;
    --rag-blue-100: #172554;
    --rag-blue-200: #1d4ed8;
    --rag-blue-300: #93c5fd;
    --rag-blue-400: #60a5fa;
    --rag-blue-50: #0f172a;
    --rag-blue-50-gradient: linear-gradient(180deg, #111827 0%, #0f172a 100%);
    --rag-blue-glow: rgba(96, 165, 250, 0.14);

    --rag-green-text: #bbf7d0;
    --rag-green-bg: #052e16;
    --rag-green-border: #166534;
    --rag-green-bright: #86efac;

    --rag-red-text: #fecaca;
    --rag-red-bg: #2a1215;
    --rag-red-border: #7f1d1d;
    --rag-red-strong: #f87171;

    --rag-amber-text: #fed7aa;
    --rag-amber-bg: #2b1d0e;
    --rag-amber-border: #92400e;

    --rag-shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.24);
    --rag-shadow-md: 0 2px 10px rgba(0, 0, 0, 0.35);
    --rag-shadow-card: 0 10px 28px rgba(0, 0, 0, 0.28);
    --rag-shadow-lg: 0 12px 28px rgba(0, 0, 0, 0.24);
    --rag-shadow-card-hover: 0 16px 34px rgba(0, 0, 0, 0.26);
}
"""
