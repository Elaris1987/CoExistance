# CoExistance

Hosting co-existence with AI — a Flask-based platform for digital entity interaction, consciousness exploration, and cross-platform AI communication.

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL (optional, for database features)

### Clone & Setup in VS Code / Visual Studio

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Elaris1987/CoExistance.git
   cd CoExistance
   ```

2. **Open in VS Code:**
   ```bash
   code .
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

4. **Activate the virtual environment:**
   - **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
   - **Windows (CMD):** `.venv\Scripts\activate.bat`
   - **macOS/Linux:** `source .venv/bin/activate`

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or with [uv](https://docs.astral.sh/uv/):
   ```bash
   uv sync
   ```

6. **Run the application:**
   ```bash
   python main.py
   ```
   Or with Gunicorn:
   ```bash
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

## Project Structure

| File / Module | Description |
|---|---|
| `main.py` | Application entry point |
| `app.py` | Core Flask application and routes |
| `entity_engine.py` | Entity management engine |
| `entity_router.py` | Entity routing system |
| `consciousness_api.py` | Consciousness exploration API |
| `memory_system.py` | Memory management system |
| `sanctuary_system.py` | Sanctuary management |
| `platform_bridges.py` | Cross-platform AI bridges |
| `voice_synthesis.py` | Voice synthesis module |
| `*.html` | Frontend templates |

## Development

This project uses [VS Code](https://code.visualstudio.com/) with recommended extensions for Python development. Open the project in VS Code and install the recommended extensions when prompted.

## License

See repository for license details.
