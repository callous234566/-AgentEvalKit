"""前端 JavaScript 注入：输入框增强、复制按钮、快捷键、滚动控制。"""

import base64
import html
import json

import streamlit.components.v1 as components


def inject_chat_enhancement_script(input_history: list = None, dark_mode: bool = False):
    """注入前端增强脚本：输入框自增高、复制回答、重新生成和自动滚动。"""
    history_payload = base64.b64encode(
        json.dumps((input_history or [])[-20:], ensure_ascii=False).encode("utf-8")
    ).decode("ascii")
    dark_mode_json = "true" if dark_mode else "false"
    components.html(
        """
        <script>
        (function () {
            const parentWindow = window.parent;
            const doc = parentWindow.document;
            parentWindow.__ragInputHistory = JSON.parse(decodeURIComponent(Array.from(parentWindow.atob("__INPUT_HISTORY__"), function (ch) {
                return "%" + ("00" + ch.charCodeAt(0).toString(16)).slice(-2);
            }).join("")));
            parentWindow.__ragInputHistoryIndex = parentWindow.__ragInputHistory.length;
            doc.body.classList.toggle("rag-dark", __DARK_MODE__);

            if (parentWindow.__ragUiObserver) {
                parentWindow.__ragUiObserver.disconnect();
            }
            if (parentWindow.__ragComposerResizeObserver) {
                parentWindow.__ragComposerResizeObserver.disconnect();
            }
            if (parentWindow.__ragComposerResizeHandler) {
                parentWindow.removeEventListener("resize", parentWindow.__ragComposerResizeHandler);
            }

            function decodeBase64Utf8(value) {
                const binary = parentWindow.atob(value || "");
                const bytes = Array.from(binary, function (ch) {
                    return "%" + ("00" + ch.charCodeAt(0).toString(16)).slice(-2);
                }).join("");
                return decodeURIComponent(bytes);
            }

            function resizeTextarea(textarea) {
                const style = parentWindow.getComputedStyle(textarea);
                const lineHeight = parseFloat(style.lineHeight) || 22;
                const paddingTop = parseFloat(style.paddingTop) || 0;
                const paddingBottom = parseFloat(style.paddingBottom) || 0;
                const borderTop = parseFloat(style.borderTopWidth) || 0;
                const borderBottom = parseFloat(style.borderBottomWidth) || 0;
                const minHeight = 52;
                const maxHeight = Math.ceil(lineHeight * 5 + paddingTop + paddingBottom + borderTop + borderBottom);

                textarea.style.height = "auto";
                const nextHeight = Math.max(minHeight, Math.min(textarea.scrollHeight, maxHeight));
                textarea.style.height = nextHeight + "px";
                textarea.style.overflowY = textarea.scrollHeight > maxHeight ? "auto" : "hidden";
            }

            function setupTextareaResize() {
                doc.querySelectorAll('div[data-testid="stTextArea"] textarea').forEach(function (textarea) {
                    if (textarea.dataset.ragAutoResize === "1") {
                        resizeTextarea(textarea);
                    } else {
                        textarea.dataset.ragAutoResize = "1";
                        textarea.rows = 1;
                        textarea.addEventListener("input", function () {
                            resizeTextarea(textarea);
                        });
                        textarea.addEventListener("keydown", function (event) {
                            handleInputHistory(event, textarea);
                        });
                    }
                    resizeTextarea(textarea);
                });
            }

            function setTextareaValue(textarea, value) {
                const setter = Object.getOwnPropertyDescriptor(parentWindow.HTMLTextAreaElement.prototype, "value").set;
                setter.call(textarea, value);
                textarea.dispatchEvent(new Event("input", { bubbles: true }));
                resizeTextarea(textarea);
            }

            function handleInputHistory(event, textarea) {
                const history = parentWindow.__ragInputHistory || [];
                if (!history.length || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) {
                    return;
                }
                if (event.key === "ArrowUp") {
                    event.preventDefault();
                    if (parentWindow.__ragInputHistoryIndex === history.length) {
                        parentWindow.__ragInputDraft = textarea.value || "";
                    }
                    parentWindow.__ragInputHistoryIndex = Math.max(0, parentWindow.__ragInputHistoryIndex - 1);
                    setTextareaValue(textarea, history[parentWindow.__ragInputHistoryIndex] || "");
                } else if (event.key === "ArrowDown") {
                    event.preventDefault();
                    parentWindow.__ragInputHistoryIndex = Math.min(history.length, parentWindow.__ragInputHistoryIndex + 1);
                    const nextValue = parentWindow.__ragInputHistoryIndex === history.length
                        ? (parentWindow.__ragInputDraft || "")
                        : (history[parentWindow.__ragInputHistoryIndex] || "");
                    setTextareaValue(textarea, nextValue);
                }
            }

            function copyWithFallback(text) {
                if (parentWindow.navigator.clipboard && parentWindow.navigator.clipboard.writeText) {
                    return parentWindow.navigator.clipboard.writeText(text);
                }

                const temp = doc.createElement("textarea");
                temp.value = text;
                temp.setAttribute("readonly", "");
                temp.style.position = "fixed";
                temp.style.left = "-9999px";
                doc.body.appendChild(temp);
                temp.select();
                doc.execCommand("copy");
                if (temp.parentNode) {
                    temp.parentNode.removeChild(temp);
                }
                return Promise.resolve();
            }

            function setupActionButtons() {
                doc.querySelectorAll(".answer-copy-btn:not([data-rag-bound='1']), .source-copy-btn:not([data-rag-bound='1'])").forEach(function (button) {
                    button.dataset.ragBound = "1";
                    button.addEventListener("click", function () {
                        if (button.disabled) {
                            return;
                        }
                        const originalText = button.textContent;
                        const text = decodeBase64Utf8(button.dataset.copy || "");
                        copyWithFallback(text).then(function () {
                            button.textContent = "已复制";
                            button.classList.add("copied");
                            setTimeout(function () {
                                button.textContent = originalText;
                                button.classList.remove("copied");
                            }, 1400);
                        }).catch(function () {
                            button.textContent = "复制失败";
                            setTimeout(function () {
                                button.textContent = originalText;
                            }, 1400);
                        });
                    });
                });

                doc.querySelectorAll(".answer-regenerate-btn:not([data-rag-bound='1'])").forEach(function (button) {
                    button.dataset.ragBound = "1";
                    button.addEventListener("click", function () {
                        if (button.disabled) {
                            return;
                        }
                        const idx = button.dataset.messageIndex;
                        if (!idx) {
                            return;
                        }
                        const trigger = doc.querySelector("div[class*='st-key-regen_trigger_" + idx + "'] button");
                        if (trigger) {
                            trigger.click();
                        }
                    });
                });
            }

            function setupAccessibleLabels() {
                function labelButtons(selector, label, disabledLabel, options) {
                    const opts = options || {};
                    doc.querySelectorAll(selector).forEach(function (button) {
                        const text = button.disabled && disabledLabel ? disabledLabel : label;
                        button.setAttribute("aria-label", text);
                        if (opts.title !== false) {
                            button.setAttribute("title", text);
                        } else {
                            button.removeAttribute("title");
                        }
                    });
                }

                labelButtons(
                    "[data-testid='stSidebar'] div[class*='st-key-collection_row_more_'] button",
                    "打开知识库操作菜单",
                    null,
                    { title: false }
                );
                labelButtons(
                    "[data-testid='stSidebar'] div[class*='st-key-session_row_more_'] button",
                    "打开会话操作菜单",
                    null,
                    { title: false }
                );
                doc.querySelectorAll(
                    "[data-testid='stSidebar'] div[class*='st-key-collection_row_select_'] button, " +
                    "[data-testid='stSidebar'] div[class*='st-key-session_row_select_'] button"
                ).forEach(function (button) {
                    button.removeAttribute("title");
                });
                labelButtons(
                    "div[class*='st-key-upload_remove_visible_'] button",
                    "从上传队列移除文件"
                );
                labelButtons(
                    "div[class*='st-key-upload_process_button'] button",
                    "开始上传并处理等待中的文件",
                    "当前没有等待处理的文件"
                );
                labelButtons(
                    "div[class*='st-key-send_button'] button",
                    "发送消息，快捷键 Ctrl 加 Enter"
                );
                labelButtons(
                    "div[class*='st-key-stop_generation_button'] button",
                    "停止当前回答生成"
                );
                labelButtons(
                    "div[class*='st-key-clear_button'] button",
                    "重置当前会话"
                );
                labelButtons(
                    "div[class*='st-key-toolbar_select_all'] button",
                    "全选或取消全选当前文档列表"
                );
                labelButtons(
                    "div[class*='st-key-toolbar_delete'] button",
                    "删除已选择文档",
                    "请先选择文档再删除"
                );
                labelButtons(
                    "div[class*='st-key-toolbar_disable'] button",
                    "禁用已选择文档，使其不参与问答检索",
                    "请先选择可禁用文档"
                );
                labelButtons(
                    "div[class*='st-key-toolbar_enable'] button",
                    "启用已选择文档，使其重新参与问答检索",
                    "请先选择可启用文档"
                );
                labelButtons(
                    "div[class*='st-key-chat_export_markdown'] button",
                    "导出当前会话为 Markdown"
                );
                labelButtons(
                    "div[class*='st-key-chat_export_pdf'] button",
                    "导出当前会话为 PDF"
                );
                labelButtons(
                    "div[class*='st-key-theme_toggle_btn'] button",
                    "切换深色或浅色模式"
                );
            }

            function setupShortcuts() {
                if (parentWindow.__ragShortcutBound) {
                    return;
                }
                parentWindow.__ragShortcutBound = true;
                doc.addEventListener("keydown", function (event) {
                    const textarea = doc.querySelector('div[data-testid="stTextArea"] textarea');
                    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
                        event.preventDefault();
                        const sendButton = doc.querySelector("div[class*='st-key-send_button'] button");
                        if (sendButton && !sendButton.disabled) {
                            sendButton.click();
                        }
                    } else if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "n") {
                        event.preventDefault();
                        const newSessionButton = doc.querySelector("div[class*='st-key-new_session_btn'] button");
                        if (newSessionButton && !newSessionButton.disabled) {
                            newSessionButton.click();
                        }
                    } else if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "l") {
                        event.preventDefault();
                        const clearButton = doc.querySelector("div[class*='st-key-clear_button'] button");
                        if (clearButton && !clearButton.disabled) {
                            clearButton.click();
                        }
                    } else if (event.key === "Escape" && textarea) {
                        setTextareaValue(textarea, "");
                    }
                });
            }

            function removeImmediateLoadingFeedback() {
                const feedback = doc.getElementById("rag-immediate-loading");
                if (feedback && feedback.parentNode) {
                    feedback.parentNode.removeChild(feedback);
                }
                parentWindow.__ragImmediateLoadingShownAt = 0;
            }

            function syncImmediateLoadingFeedback() {
                const feedback = doc.getElementById("rag-immediate-loading");
                const composer = doc.querySelector("div[class*='st-key-chat_input_area']");
                if (!feedback || !composer) {
                    return;
                }
                const rect = composer.getBoundingClientRect();
                feedback.style.left = Math.max(12, rect.left) + "px";
                feedback.style.width = Math.max(280, rect.width) + "px";
                feedback.style.bottom = Math.max(12, parentWindow.innerHeight - rect.top + 10) + "px";
            }

            function showImmediateLoadingFeedback() {
                if (doc.getElementById("rag-immediate-loading")) {
                    syncImmediateLoadingFeedback();
                    return;
                }
                const feedback = doc.createElement("div");
                feedback.id = "rag-immediate-loading";
                feedback.className = "rag-immediate-loading";
                feedback.setAttribute("role", "status");
                feedback.setAttribute("aria-live", "polite");
                feedback.innerHTML = [
                    '<span class="rag-loading-icon" aria-hidden="true"></span>',
                    '<span class="rag-loading-copy"><strong>正在检索知识库</strong><small>正在匹配相关资料，请稍候</small></span>',
                    '<span class="rag-loading-skeleton" aria-hidden="true"><i></i><i></i><i></i></span>'
                ].join("");
                doc.body.appendChild(feedback);
                parentWindow.__ragImmediateLoadingShownAt = Date.now();
                syncImmediateLoadingFeedback();
                parentWindow.setTimeout(setupImmediateLoadingFeedback, 1600);
            }

            function setupImmediateLoadingFeedback() {
                const hasRealProgress = doc.querySelector(".process-step.active");
                const textarea = doc.querySelector('div[data-testid="stTextArea"] textarea');
                const isGenerating = Boolean(doc.querySelector("div[class*='st-key-stop_generation_button']"));
                const shownFor = Date.now() - (parentWindow.__ragImmediateLoadingShownAt || 0);

                if (hasRealProgress || (shownFor > 1200 && textarea && !textarea.disabled && !isGenerating)) {
                    removeImmediateLoadingFeedback();
                }

                doc.querySelectorAll(
                    "div[class*='st-key-send_button'] button, " +
                    "div[class*='st-key-quick_prompt_'] button, " +
                    "div[class*='st-key-sample_question_'] button"
                ).forEach(function (button) {
                    if (button.dataset.ragLoadingBound === "1") {
                        return;
                    }
                    button.dataset.ragLoadingBound = "1";
                    button.addEventListener("click", function () {
                        if (!button.disabled) {
                            showImmediateLoadingFeedback();
                        }
                    });
                });
                doc.querySelectorAll("div[class*='st-key-stop_generation_button'] button").forEach(function (button) {
                    if (button.dataset.ragLoadingStopBound === "1") {
                        return;
                    }
                    button.dataset.ragLoadingStopBound = "1";
                    button.addEventListener("click", function () {
                        removeImmediateLoadingFeedback();
                        syncLatestAnswerButton();
                    });
                });
            }

            function isNearChatBottom() {
                const marker = doc.getElementById("rag-chat-bottom-live") || doc.getElementById("rag-chat-bottom");
                if (!marker) {
                    return true;
                }
                const viewportHeight = doc.documentElement.clientHeight || parentWindow.innerHeight || 0;
                return marker.getBoundingClientRect().bottom <= viewportHeight + 180;
            }

            function scrollToLatestAnswer() {
                const target = doc.getElementById("rag-chat-bottom-live") || doc.getElementById("rag-chat-bottom");
                if (!target) {
                    return;
                }
                parentWindow.__ragAutoFollowChat = true;
                parentWindow.__ragUserScrolledAfterQuestion = false;
                target.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
                parentWindow.setTimeout(function () {
                    parentWindow.scrollTo({
                        top: Math.max(doc.body.scrollHeight, doc.documentElement.scrollHeight),
                        behavior: "smooth"
                    });
                }, 80);
            }

            function syncLatestAnswerButton() {
                const button = doc.getElementById("rag-latest-answer-button");
                const composer = doc.querySelector("div[class*='st-key-chat_input_area']");
                if (!button || !composer) {
                    return;
                }
                const composerRect = composer.getBoundingClientRect();
                const isGenerating = Boolean(doc.querySelector("div[class*='st-key-stop_generation_button']"));
                const shouldShow = !isNearChatBottom();
                button.classList.toggle("visible", shouldShow);
                button.setAttribute("aria-hidden", shouldShow ? "false" : "true");
                button.tabIndex = shouldShow ? 0 : -1;
                button.style.left = Math.max(12, composerRect.left + composerRect.width / 2) + "px";
                button.style.bottom = Math.max(12, parentWindow.innerHeight - composerRect.top + 10) + "px";
                button.querySelector("span").textContent = isGenerating ? "回答生成中 · 查看最新" : "查看最新回答";
            }

            function setupLatestAnswerButton() {
                let button = doc.getElementById("rag-latest-answer-button");
                if (!button) {
                    button = doc.createElement("button");
                    button.id = "rag-latest-answer-button";
                    button.className = "rag-latest-answer-button";
                    button.type = "button";
                    button.setAttribute("aria-label", "滚动到最新回答");
                    button.setAttribute("title", "滚动到最新回答");
                    button.innerHTML = '<i aria-hidden="true"></i><span>查看最新回答</span>';
                    button.addEventListener("click", scrollToLatestAnswer);
                    doc.body.appendChild(button);
                }
                syncLatestAnswerButton();
            }

            function setupManualScrollTracking() {
                if (parentWindow.__ragManualScrollBound) {
                    return;
                }
                parentWindow.__ragManualScrollBound = true;
                if (typeof parentWindow.__ragAutoFollowChat !== "boolean") {
                    parentWindow.__ragAutoFollowChat = true;
                }

                doc.addEventListener("wheel", function (event) {
                    if (event.deltaY < 0) {
                        parentWindow.__ragAutoFollowChat = false;
                    } else if (isNearChatBottom()) {
                        parentWindow.__ragAutoFollowChat = true;
                    }
                    syncLatestAnswerButton();
                }, { passive: true });
                doc.addEventListener("touchmove", function () {
                    parentWindow.__ragAutoFollowChat = isNearChatBottom();
                    syncLatestAnswerButton();
                }, { passive: true });
                doc.addEventListener("keydown", function (event) {
                    if (["ArrowUp", "PageUp", "Home"].includes(event.key)) {
                        parentWindow.__ragAutoFollowChat = false;
                    } else if (event.key === "End") {
                        parentWindow.__ragAutoFollowChat = true;
                    }
                    syncLatestAnswerButton();
                });
                doc.addEventListener("scroll", syncLatestAnswerButton, { passive: true, capture: true });
            }

            function syncChatComposer() {
                const composer = doc.querySelector("div[class*='st-key-chat_input_area']");
                const block = doc.querySelector(".stApp > .main > .block-container")
                    || doc.querySelector("[data-testid='stAppViewBlockContainer']")
                    || doc.querySelector(".block-container");
                if (!composer || !block) {
                    return;
                }

                const viewportWidth = doc.documentElement.clientWidth || parentWindow.innerWidth;
                const gutter = viewportWidth <= 900 ? 12 : 24;
                const blockRect = block.getBoundingClientRect();
                const left = Math.max(gutter, blockRect.left);
                const width = Math.max(280, Math.min(blockRect.width, viewportWidth - left - gutter));
                const composerHeight = Math.ceil(composer.getBoundingClientRect().height);

                doc.documentElement.style.setProperty("--rag-chat-composer-left", left + "px");
                doc.documentElement.style.setProperty("--rag-chat-composer-width", width + "px");
                doc.documentElement.style.setProperty("--rag-chat-composer-space", Math.max(180, composerHeight + 40) + "px");
                syncImmediateLoadingFeedback();
                syncLatestAnswerButton();
            }

            function setupComposerPosition() {
                syncChatComposer();
                if (parentWindow.__ragComposerResizeObserver) {
                    parentWindow.__ragComposerResizeObserver.disconnect();
                }
                if (parentWindow.ResizeObserver) {
                    const composer = doc.querySelector("div[class*='st-key-chat_input_area']");
                    const block = doc.querySelector(".stApp > .main > .block-container")
                        || doc.querySelector("[data-testid='stAppViewBlockContainer']")
                        || doc.querySelector(".block-container");
                    parentWindow.__ragComposerResizeObserver = new parentWindow.ResizeObserver(syncChatComposer);
                    if (composer) {
                        parentWindow.__ragComposerResizeObserver.observe(composer);
                    }
                    if (block) {
                        parentWindow.__ragComposerResizeObserver.observe(block);
                    }
                }
            }

            function refreshEnhancements() {
                setupTextareaResize();
                setupActionButtons();
                setupAccessibleLabels();
                setupImmediateLoadingFeedback();
                setupComposerPosition();
                setupLatestAnswerButton();
            }

            refreshEnhancements();
            setupShortcuts();
            setupManualScrollTracking();
            parentWindow.__ragComposerResizeHandler = syncChatComposer;
            parentWindow.addEventListener("resize", parentWindow.__ragComposerResizeHandler);
            setTimeout(refreshEnhancements, 120);
            setTimeout(refreshEnhancements, 500);

            parentWindow.__ragUiObserver = new MutationObserver((function () {
                let debounceTimer = null;
                return function () {
                    if (debounceTimer) {
                        clearTimeout(debounceTimer);
                    }
                    debounceTimer = setTimeout(function () {
                        debounceTimer = null;
                        refreshEnhancements();
                    }, 80);
                };
            })());
            parentWindow.__ragUiObserver.observe(doc.body, {
                childList: true,
                subtree: true
            });
        })();
        </script>
        """.replace("__INPUT_HISTORY__", history_payload).replace("__DARK_MODE__", dark_mode_json),
        height=0,
        width=0,
    )


def render_one_time_latest_scroll(request_id: int, phase: str, respect_manual_scroll: bool = False):
    """Render a one-time client scroll to the latest chat anchor."""
    manual_guard = (
        "if (parentWindow.__ragUserScrolledAfterQuestion) { return; }"
        if respect_manual_scroll
        else ""
    )
    components.html(
        f"""
        <script>
        (function () {{
            const parentWindow = window.parent;
            const doc = parentWindow.document;
            const requestKey = "{html.escape(str(request_id))}-{html.escape(phase)}";
            if (parentWindow.__ragHandledScrollRequest === requestKey) {{
                return;
            }}
            parentWindow.__ragHandledScrollRequest = requestKey;
            {manual_guard}

            const marker = doc.getElementById("rag-message-" + requestKey);
            const bottomMarker = doc.getElementById("rag-chat-bottom-live") || doc.getElementById("rag-chat-bottom");
            const target = bottomMarker || marker;
            if (!target) {{
                return;
            }}

            function scrollElementToBottom(element) {{
                if (!element) {{
                    return;
                }}
                try {{
                    element.scrollTop = element.scrollHeight;
                }} catch (error) {{}}
            }}

            function forceChatBottom(behavior) {{
                const appView = doc.querySelector("[data-testid='stAppViewContainer']");
                const main = doc.querySelector(".stApp > .main");
                const block = doc.querySelector(".stApp > .main > .block-container")
                    || doc.querySelector("[data-testid='stAppViewBlockContainer']")
                    || doc.querySelector(".block-container");
                [doc.scrollingElement, doc.documentElement, doc.body, appView, main, block].forEach(scrollElementToBottom);
                target.scrollIntoView({{
                    behavior: behavior || "auto",
                    block: "end",
                    inline: "nearest"
                }});
                [doc.scrollingElement, doc.documentElement, doc.body, appView, main, block].forEach(scrollElementToBottom);
                parentWindow.scrollTo({{
                    top: Math.max(doc.body.scrollHeight, doc.documentElement.scrollHeight),
                    behavior: behavior || "auto"
                }});
            }}

            [40, 120, 320, 760].forEach(function (delay, index) {{
                parentWindow.setTimeout(function () {{
                    forceChatBottom(index === 0 ? "auto" : "smooth");
                }}, delay);
            }});

            if ("{html.escape(phase)}" === "question") {{
                parentWindow.__ragAutoFollowChat = true;
                parentWindow.__ragUserScrolledAfterQuestion = false;
                const markManualScroll = function () {{
                    parentWindow.__ragUserScrolledAfterQuestion = true;
                }};
                parentWindow.setTimeout(function () {{
                    const markManualKeyScroll = function (event) {{
                        if (["ArrowUp", "ArrowDown", "PageUp", "PageDown", "Home", "End", " "].includes(event.key)) {{
                            markManualScroll();
                            doc.removeEventListener("keydown", markManualKeyScroll);
                        }}
                    }};
                    doc.addEventListener("wheel", markManualScroll, {{ once: true, passive: true }});
                    doc.addEventListener("touchmove", markManualScroll, {{ once: true, passive: true }});
                    doc.addEventListener("mousedown", markManualScroll, {{ once: true }});
                    doc.addEventListener("keydown", markManualKeyScroll);
                }}, 300);
            }}
        }})();
        </script>
        """,
        height=0,
        width=0,
    )


def render_force_chat_bottom(respect_manual_scroll: bool = True) -> None:
    """Force the chat viewport to the latest bottom sentinel during streaming."""
    manual_guard = (
        "if (parentWindow.__ragAutoFollowChat === false) { return; }"
        if respect_manual_scroll
        else "parentWindow.__ragAutoFollowChat = true;"
    )
    components.html(
        """
        <script>
        (function () {
            const parentWindow = window.parent;
            const doc = parentWindow.document;
            __MANUAL_GUARD__
            const target = doc.getElementById("rag-chat-bottom-live") || doc.getElementById("rag-chat-bottom");
            if (!target) {
                return;
            }
            function scrollElementToBottom(element) {
                if (!element) {
                    return;
                }
                try {
                    element.scrollTop = element.scrollHeight;
                } catch (error) {}
            }
            const appView = doc.querySelector("[data-testid='stAppViewContainer']");
            const main = doc.querySelector(".stApp > .main");
            const block = doc.querySelector(".stApp > .main > .block-container")
                || doc.querySelector("[data-testid='stAppViewBlockContainer']")
                || doc.querySelector(".block-container");
            [doc.scrollingElement, doc.documentElement, doc.body, appView, main, block].forEach(scrollElementToBottom);
            target.scrollIntoView({ behavior: "auto", block: "end", inline: "nearest" });
            [doc.scrollingElement, doc.documentElement, doc.body, appView, main, block].forEach(scrollElementToBottom);
            parentWindow.scrollTo({ top: Math.max(doc.body.scrollHeight, doc.documentElement.scrollHeight), behavior: "auto" });
        })();
        </script>
        """.replace("__MANUAL_GUARD__", manual_guard),
        height=0,
        width=0,
    )
