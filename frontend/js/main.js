// main.js
import { renderTranscription } from './transcriptionRender.js';

document.addEventListener('DOMContentLoaded', () => {
    const transcribeBtn = document.getElementById('btn');
    const inputText = document.getElementById('inputText');
    const resultDiv = document.getElementById('output');
    const toggleLink = document.getElementById('show-notes-toggle');
    let lastData = null;
    let isShowingNotes = false;
    let lastText = '';

    // Initially hide the toggle link
    toggleLink.style.display = 'none';

    const render = () => {
        if (lastData) {
            const showNotes = isShowingNotes;
            renderTranscription(lastData, resultDiv, { showNotes });
        }
    };

    toggleLink.addEventListener('click', (e) => {
        e.preventDefault();
        isShowingNotes = !isShowingNotes;
        toggleLink.textContent = isShowingNotes ? 'ocultar notas' : 'mostrar notas';
        render();
    });

    transcribeBtn.addEventListener('click', async () => {
        const text = inputText.value.trim();
        if (!text) {
            alert('Please enter text to transcribe.');
            return;
        }

        // If text hasn't changed, just re-render
        if (text === lastText) {
            render();
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/transcription/formatted/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text })
            });

            if (!response.ok) {
                throw new Error('Failed to transcribe');
            }

            const data = await response.json();
            lastData = data;
            lastText = text;
            // Show the toggle link after successful transcription
            toggleLink.style.display = 'inline';
            render();
        } catch (error) {
            resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
            // Hide the toggle link on error
            toggleLink.style.display = 'none';
        }
    });
});
     