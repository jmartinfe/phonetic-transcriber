export async function transcribe(text) {
    const response = await fetch("http://localhost:8000/transcription/formatted/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
    });

    if (!response.ok) {
        throw new Error("Error en la API");
    }

    return await response.json();
}