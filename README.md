# langchain_project

Static GitHub Pages frontend that calls Ollama for summary + facts generation.

GitHub Pages URL:
- `https://chukwunonsoikenwa.github.io/langchain_project/`

## Run with Ollama + GitHub Pages

1. Pull and run your model locally:
```bash
ollama pull gemma3:270m
export OLLAMA_ORIGINS="https://chukwunonsoikenwa.github.io"
ollama serve
```

2. Expose Ollama on HTTPS (example with Cloudflare Tunnel):
```bash
cloudflared tunnel --url http://localhost:11434
```

3. Open your GitHub Pages app and set `Ollama Base URL` to the HTTPS tunnel URL:
- `https://chukwunonsoikenwa.github.io/langchain_project/`

## Why this is required

GitHub Pages is served over HTTPS. Browsers block requests from HTTPS pages to plain HTTP endpoints such as `http://127.0.0.1:11434` (mixed-content restriction). Using an HTTPS tunnel avoids this.
