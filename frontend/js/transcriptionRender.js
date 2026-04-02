// transcriptionRender.js
// GitHub Copilot

/**
 * Render a transcription JSON into a paragraph with optional tooltips for alternatives.
 * @param {Object} data json object
 * @param {HTMLElement} container DOM element where render is inserted
 */
function renderTranscription(data, container, options = {}) {
    if (!container) throw new Error("container element required");

    // Inject styles if not already present
    injectTranscriptionStyles();

    // Clear out previous content
    container.innerHTML = "";

    const tokens = data.token_transcriptions || [];
    const showNotes = options.showNotes || false;

    // Create display paragraph
    const displayP = document.createElement("p");
    displayP.className = "display-line";

    let isFirst = true;
    let previousTokenType = null;

    tokens.forEach((token) => {
        // spacing rules
        // According to user: word and punct_open get a space before, punct and punct_close no space.
        // For the very first token, we don't want a leading space.
        // word should not have a space before if the previous token was punct_open
        const needsSpace =
            !isFirst &&
            (token.type === "punct_open" ||
             (token.type === "word" && previousTokenType !== "punct_open"));

        // For display paragraph
        if (needsSpace) {
            displayP.appendChild(document.createTextNode(" "));
        }

        const displayWrapper = document.createElement("span");
        displayWrapper.className = [
            "token",
            token.type,
            token.found ? "found" : "not-found",
        ].join(" ");

        const displaySpan = document.createElement("span");
        displaySpan.className = "token-display";
        displaySpan.textContent = showNotes ? token.display : token.flat_display;
        displayWrapper.appendChild(displaySpan);

        // optional tooltip for alternatives (hover/click)
        const hasAlt =
            Array.isArray(token.alternatives) && token.alternatives.length > 0;
        if (token.ipa) {
            displayWrapper.classList.add("has-alternatives");
            const tooltip = document.createElement("div");
            tooltip.className = "token-tooltip";
            tooltip.setAttribute("role", "tooltip");
            tooltip.style.display = "none";

            // IPA title
            const ipaTitle = document.createElement("div");
            ipaTitle.className = "token-tooltip-title";
            ipaTitle.textContent = "IPA:";
            tooltip.appendChild(ipaTitle);

            // Main IPA
            const mainRow = document.createElement("div");
            mainRow.className = "token-tooltip-row";
            const mainIpa = document.createElement("div");
            mainIpa.textContent = token.ipa;
            mainRow.appendChild(mainIpa);
            tooltip.appendChild(mainRow);

            // Alternatives if present
            if (hasAlt) {
                const altTitle = document.createElement("div");
                altTitle.className = "token-tooltip-title";
                altTitle.textContent = "Alternativas:";
                tooltip.appendChild(altTitle);

                token.alternatives.forEach((alt) => {
                    const row = document.createElement("div");
                    row.className = "token-tooltip-row";

                    const t1 = document.createElement("div");
                    t1.className = "tooltip-alt-transcription";
                    t1.textContent = showNotes ? alt.display : alt.flat_display;
                    t1.textContent += alt.ipa ? " : " + alt.ipa : "";
                    row.appendChild(t1);

                    tooltip.appendChild(row);
                });
            }

            displayWrapper.appendChild(tooltip);

            const showTooltip = () => (tooltip.style.display = "block");
            const hideTooltip = () => (tooltip.style.display = "none");
            displayWrapper.addEventListener("mouseenter", showTooltip);
            displayWrapper.addEventListener("mouseleave", hideTooltip);
            displayWrapper.addEventListener("focus", showTooltip);
            displayWrapper.addEventListener("blur", hideTooltip);
            displayWrapper.addEventListener("click", () => {
                tooltip.style.display = tooltip.style.display === "block" ? "none" : "block";
            });

            displayWrapper.setAttribute("tabindex", "0");
        }

        displayP.appendChild(displayWrapper);

        previousTokenType = token.type;
        isFirst = false;
    });

    container.appendChild(displayP);

    // Add notes section if showNotes and notes present
    if (showNotes && data.notes && Object.keys(data.notes).length > 0) {
        const notesDiv = document.createElement("div");
        notesDiv.className = "notes-section";

        for (const [key, value] of Object.entries(data.notes)) {
            const noteP = document.createElement("p");
            noteP.textContent = `${key}: ${value}`;
            notesDiv.appendChild(noteP);
        }

        container.appendChild(notesDiv);
    }
}

// Example style injection (optional)
function injectTranscriptionStyles() {
    const css = `
.display-line { margin: 0; line-height: 1.4; }
.token { position: relative; display: inline-block; }
.token-display { white-space: pre; font-family: inherit; font-size: inherit; color: inherit; }
.token.word .token-display,
.token.punct .token-display,
.token.punct_open .token-display,
.token.punct_close .token-display { }
.token-tooltip {
    position: absolute;
    z-index: 1000;
    bottom: 100%;
    left: 0;
    min-width: 150px;
    background: rgba(50, 50, 50, 0.95);
    color: white;
    border-radius: 4px;
    padding: 6px 8px;
    margin-bottom: 4px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    font-size: 0.85em;
}
.token-tooltip-row { margin-top: 4px; }
.token-tooltip-row:first-child { margin-top: 0; }
.token-tooltip-title { font-weight: bold; margin-bottom: 4px; }
.tooltip-main-ipa { font-weight: bold; }
.has-alternatives { cursor: auto; }
.has-alternatives:focus {
    outline: none;
}
.has-alternatives:hover,
.has-alternatives:focus,
.has-alternatives:active {
    background: none;
    color: inherit;
}
.found .token-display {}
.not-found .token-display { opacity: 0.6; }
.notes-section { margin-top: 1em; border-top: 1px solid #ccc; padding-top: 0.5em; }
.notes-section p { margin: 0.5em 0; }
`;
    const style = document.createElement("style");
    style.textContent = css;
    document.head.appendChild(style);
}

// Export for module usage
if (typeof module !== "undefined" && module.exports) {
    module.exports = { renderTranscription, injectTranscriptionStyles };
}

export { renderTranscription, injectTranscriptionStyles };