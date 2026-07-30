// src/api.js

const API_BASE = "http://127.0.0.1:8000";

/**
 * Upload a PDF
 */
export async function uploadPDF(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error("Failed to upload PDF");
    }

    return await response.json();
}

/**
 * Search the uploaded paper
 */
export async function searchPaper(question) {
    const response = await fetch(`${API_BASE}/search`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            question,
        }),
    });

    if (!response.ok) {
        throw new Error("Search failed");
    }

    return await response.json();
}

/**
 * Generate summary of uploaded paper
 */
export async function summarizePaper(filename) {
    const response = await fetch(`${API_BASE}/summarize`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            filename,
        }),
    });

    if (!response.ok) {
        throw new Error("Summarization failed");
    }

    return await response.json();
}