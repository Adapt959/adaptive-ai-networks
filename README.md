# Adaptive AI Networks

This repository contains a local FastAPI command-center backend and the existing
AI-themed 2048 browser demo. The demo files and gameplay remain unchanged.

## Run the command-center backend

Requires Python 3.10+ and a running Ollama instance. From the repository root:

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell (use instead of the line above):
# .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Open http://127.0.0.1:8001/docs to try the API. GET `/` reports backend process
health; it does not verify Ollama availability. POST `/models/chat` accepts
`{"model":"llama3.1","prompt":"Hello"}` and returns Ollama's chat response.
POST `/commands/run` accepts
`{"command":"Analyze this lead","context":{"city":"Austin"}}` and returns
`selected_model` plus `result`. Commands generate text only; they do not execute
shell commands, modify files, or send outreach.

Start Ollama using its desktop app or `ollama serve`. Install the models you
want with `ollama pull llama3.1`, `ollama pull qwen2.5-coder`, and
`ollama pull deepseek-r1`. The original routing checks `code` or `script` first,
then `analyze` or `reason`, and otherwise uses the default model.

Configuration uses server environment variables:

| Variable | Default |
| --- | --- |
| `OLLAMA_BASE_URL` | `http://localhost:11434` |
| `OLLAMA_DEFAULT_MODEL` | `llama3.1` |
| `OLLAMA_CODE_MODEL` | `qwen2.5-coder` |
| `OLLAMA_REASON_MODEL` | `deepseek-r1` |

Use an exact installed model name, including its tag if needed. To use one model
for every command category, set all three model variables to that name.
PowerShell example before starting Uvicorn:

```powershell
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_DEFAULT_MODEL = "llama3.1"
$env:OLLAMA_CODE_MODEL = "qwen2.5-coder"
$env:OLLAMA_REASON_MODEL = "deepseek-r1"
```

On macOS/Linux use `export OLLAMA_BASE_URL=http://localhost:11434` and the same
pattern for model variables. `.env.example` is a reference; `.env` is not loaded
automatically. Optional file loading requires `python -m pip install python-dotenv`
and adding `--env-file .env` to Uvicorn. Keep credentials out of Git.
`localhost` refers to the machine running the backend, so a remote backend
requires a reachable Ollama server address.

Ollama failures return 503 (unreachable), 504 (120-second timeout), or 502
(upstream error or invalid response). Empty or whitespace-only inputs return 422.
This backend has no authentication and is intended for loopback/local use.
Add authentication and appropriate access controls before exposing it remotely.

## Verify and apply the restoration

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Tests mock Ollama, so no models or network access are needed. To verify the real
connection, use `/docs` to submit a chat request with an installed model.

The restoration recovers the intended code from commit messages `d82e511`,
`4da1e48`, `0d173df`, and `41f5100`: their Python files were blank or placed in a
nested directory that was later removed. The restored package adds configuration,
validation, and upstream error handling.

To apply the accompanying patch to an unchanged checkout at `8630c5a`:

```bash
git apply --check restore-command-center.patch
git apply restore-command-center.patch
```

# AI 2048 - Adaptive AI Networks Edition

An AI-themed version of the classic 2048 puzzle game, customized with modern branding and a sleek blue color scheme. This version showcases the intersection of AI and interactive gaming.

**Presented by [Adaptive AI Networks](https://github.com/Adapt959/adaptive-ai-networks)**

## About This Project

This is a customized version of the popular 2048 game, featuring:
- 🎨 Modern AI-themed blue color palette
- 🚀 Sleek, professional design
- 📱 Fully responsive mobile experience
- ⚡ Smooth animations and transitions

Play the classic number puzzle game with a fresh AI-inspired aesthetic!

## How to Play

Use your **arrow keys** (or swipe on mobile) to move the tiles. When two tiles with the same number touch, they merge into one! The goal is to reach the **2048 tile**.

## Brand Colors

This version uses the Adaptive AI Networks color palette:
- **Primary Blue**: #2563EB - Main UI elements and mid-range tiles
- **Secondary Dark**: #111827 - Game container and high-value tiles
- **Accent Cyan**: #06B6D4 - Buttons and special tiles
- **Background**: #F8FAFC - Clean, modern background
- **Text**: #0F172A - High contrast text

## Features

- 🎮 Classic 2048 gameplay mechanics
- 💾 Best score tracking with local storage
- 📱 Touch/swipe support for mobile devices
- 🎨 AI-themed color gradient for tiles
- ✨ Smooth animations and transitions
- 🏆 Win/lose state detection

## Local Development

```bash
# Clone the repository
git clone https://github.com/Adapt959/adaptive-ai-networks.git
cd adaptive-ai-networks

# Open index.html in your browser
# Or use a local server:
python -m http.server 8000
```

Then navigate to `http://localhost:8000` in your browser.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

Please ensure your changes maintain the AI theme and color consistency.

## Credits

This customized version is based on the original 2048 game:
- **Original Game**: Created by [Gabriele Cirulli](https://github.com/gabrielecirulli/2048)
- **Based on**: [1024 by Veewo Studio](https://play.google.com/store/apps/details?id=com.veewo.a1024)
- **Inspired by**: [Threes by Asher Vollmer](https://asherv.com/threes/)

Special thanks to all the original contributors who made the base game possible:
- [Anna Harren](https://github.com/iirelu/) and [sigod](https://github.com/sigod) - Original repository maintainers
- [TimPetricola](https://github.com/TimPetricola) - Best score storage
- [chrisprice](https://github.com/chrisprice) - Mobile swipe handling
- And many other contributors to the original project

## License

This project maintains the [MIT license](LICENSE.txt) from the original 2048 game.

## About Adaptive AI Networks

This customization showcases modern web design with AI-themed branding. For more projects and information, visit our [GitHub profile](https://github.com/Adapt959).

---

**Enjoy the game! Can you reach 2048?** 🎮
