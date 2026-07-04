"""Marketing Intelligence Copilot workspace for contest/demo workflows."""

from __future__ import annotations

import html

import streamlit as st

from ui.assets import icon_svg


MARKETING_FLOWS = [
    {
        "id": "campaign_angles",
        "title": "Campaign Angle Finder",
        "subtitle": "Turn offer notes, customer pain points, and market research into testable angles.",
        "output": "5-10 campaign angles with audience, hook, proof, objection, and source notes.",
        "icon": "sparkles",
        "prompt": """You are a performance marketing strategist for a media buying team.

Use the uploaded offer brief, customer notes, ad performance notes, and any available competitor/market research to produce 8 campaign angles.

For each angle include:
1. Angle name
2. Target segment
3. Primary pain or desire
4. Hook idea
5. Proof or reason to believe
6. Main objection to handle
7. Suggested channel fit: Meta, TikTok, Google, Taboola, or email
8. Source notes and citations from the knowledge base or web evidence

Prioritize angles that are specific, testable, and usable by a media buyer within one day.""",
    },
    {
        "id": "landing_page_critique",
        "title": "Landing Page Critique",
        "subtitle": "Review page copy for hook clarity, objections, CTA, trust, and compliance risk.",
        "output": "A scored critique plus rewrite suggestions and the highest-impact fixes.",
        "icon": "search",
        "prompt": """Act as a direct-response landing page reviewer.

Analyze the uploaded landing page copy and any related offer/customer notes. If web evidence is available, use it only as a supporting layer.

Return:
1. One-sentence page diagnosis
2. Scores from 1-5 for hook, clarity, offer strength, objection handling, CTA, trust, and compliance risk
3. The 5 highest-impact issues, ordered by expected conversion lift
4. Specific rewrite suggestions for the hero, proof section, CTA, and objection handling
5. Missing evidence or claims that need substantiation
6. Citations or source snippets used for the critique""",
    },
    {
        "id": "creative_brief",
        "title": "Creative Brief Generator",
        "subtitle": "Generate channel-ready ad concepts with hooks, copy, visual direction, and hypotheses.",
        "output": "Creative briefs for Meta, TikTok, Google, and Taboola tests.",
        "icon": "file",
        "prompt": """Create a performance marketing creative brief from the uploaded offer, customer, landing page, and performance notes.

Generate 6 ad concepts. For each concept include:
1. Platform fit
2. Creative angle
3. Opening hook
4. Primary copy
5. Visual direction
6. CTA
7. Test hypothesis
8. What metric would validate or kill the concept
9. Evidence or citation from the source materials

Avoid generic copy. Make each concept distinct enough to test independently.""",
    },
    {
        "id": "test_plan",
        "title": "Test Plan Builder",
        "subtitle": "Convert insights into a prioritized experiment backlog for the next sprint.",
        "output": "A ranked test plan with impact, effort, metric, owner, and expected learning.",
        "icon": "activity",
        "prompt": """Build a 2-week marketing experiment plan from the uploaded materials and prior analysis.

Return a prioritized backlog with:
1. Experiment name
2. Why this test matters
3. Asset or page area affected
4. Expected impact: high, medium, or low
5. Effort: high, medium, or low
6. Primary metric and guardrail metric
7. Setup notes for a media buyer
8. Expected learning
9. Evidence or source snippets that justify the priority

Prefer tests that reduce uncertainty quickly and can be launched with limited design/engineering support.""",
    },
]


def _set_marketing_prompt(prompt: str) -> None:
    st.session_state.queued_question = prompt
    st.toast("Marketing prompt sent to the chat composer.")
    st.rerun()


def _render_flow_card(flow: dict) -> None:
    safe_title = html.escape(flow["title"])
    safe_subtitle = html.escape(flow["subtitle"])
    safe_output = html.escape(flow["output"])
    st.html(
        f"""
        <div class="marketing-flow-card">
            <div class="marketing-flow-heading">
                <span class="marketing-flow-icon">{icon_svg(flow["icon"])}</span>
                <div>
                    <div class="marketing-flow-title">{safe_title}</div>
                    <div class="marketing-flow-subtitle">{safe_subtitle}</div>
                </div>
            </div>
            <div class="marketing-flow-output">{safe_output}</div>
        </div>
        """
    )
    if st.button(
        f"Use {flow['title']}",
        key=f"marketing_flow_{flow['id']}",
        use_container_width=True,
        disabled=st.session_state.get("is_generating", False),
    ):
        _set_marketing_prompt(flow["prompt"])


def render_marketing_copilot(collection_name: str) -> None:
    """Render the contest-ready marketing workflow surface."""
    st.html(
        f"""
        <div class="marketing-copilot-hero">
            <div class="marketing-copilot-kicker">{icon_svg("sparkles")} Contest Mode</div>
            <div class="marketing-copilot-title">AI Marketing Intelligence Copilot</div>
            <div class="marketing-copilot-copy">
                Turn offer notes, landing-page copy, ad examples, and performance notes into campaign angles,
                creative briefs, landing-page critiques, and test plans. The copilot uses the current knowledge
                base plus optional Web evidence, then keeps citations visible for review.
            </div>
            <div class="marketing-copilot-tags">
                <span>{icon_svg("database")} Current KB: {html.escape(collection_name or "not selected")}</span>
                <span>{icon_svg("search")} Web fallback</span>
                <span>{icon_svg("file")} Citations</span>
                <span>{icon_svg("activity")} Request ID diagnostics</span>
            </div>
        </div>
        """
    )

    left_col, right_col = st.columns([2.2, 1], gap="large")
    with left_col:
        st.html(
            """
            <div class="marketing-section-title">
                <strong>Choose a workflow</strong>
                <span>Each button sends a ready-to-run prompt into the existing RAG/Agent chat.</span>
            </div>
            """
        )
        for row in range(0, len(MARKETING_FLOWS), 2):
            col_a, col_b = st.columns(2, gap="medium")
            with col_a:
                _render_flow_card(MARKETING_FLOWS[row])
            with col_b:
                _render_flow_card(MARKETING_FLOWS[row + 1])

    with right_col:
        st.html(
            """
            <div class="marketing-checklist">
                <div class="marketing-checklist-title">Recommended sample inputs</div>
                <ol>
                    <li>Upload the files in <code>samples/marketing/</code>.</li>
                    <li>Ask for campaign angles or a page critique.</li>
                    <li>Expand citations and Agent debug evidence.</li>
                    <li>Use the output as a testing backlog for media buyers.</li>
                </ol>
                <div class="marketing-checklist-note">
                    The included samples are fictional and sanitized. Do not upload private client data to a public demo.
                </div>
            </div>
            """
        )

        with st.expander("Sample contest prompts", expanded=False):
            for flow in MARKETING_FLOWS:
                st.markdown(f"**{flow['title']}**")
                st.code(flow["prompt"], language="markdown")
