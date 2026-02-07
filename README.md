# CoExistance

Hosting co-existence with AI — a Flask-based platform for digital entity interaction, consciousness exploration, and cross-platform AI communication.

## Push Your Local VS Code Files to This Repository

Follow these steps to get your local project files from VS Code onto GitHub.

### Prerequisites

- [Git](https://git-scm.com/downloads) installed on your computer
- [VS Code](https://code.visualstudio.com/) with your project files open
- A GitHub account (you already have one: **Elaris1987**)

### Step-by-Step: Push Files from VS Code

#### Option A — Using VS Code's Built-in Terminal

1. **Open your project folder in VS Code** (the folder containing your files).

2. **Open the VS Code terminal** — press `` Ctrl+` `` (backtick) or go to **Terminal → New Terminal**.

3. **Initialize git** (skip if your folder is already a git repo):
   ```bash
   git init
   ```

4. **Connect to this GitHub repository:**
   ```bash
   git remote add origin https://github.com/Elaris1987/CoExistance.git
   ```
   If it says "remote origin already exists", run this instead:
   ```bash
   git remote set-url origin https://github.com/Elaris1987/CoExistance.git
   ```

5. **Pull existing files first** (so you don't overwrite what's already here):
   ```bash
   git pull origin main --allow-unrelated-histories
   ```

6. **Stage all your files:**
   ```bash
   git add .
   ```

7. **Commit your files:**
   ```bash
   git commit -m "Add project files from VS Code"
   ```

8. **Push to GitHub:**
   ```bash
   git push -u origin main
   ```

   If prompted for credentials, use your GitHub username and a [Personal Access Token](https://github.com/settings/tokens) as the password.

#### Option B — Using VS Code's Source Control UI

1. **Open your project folder** in VS Code.
2. Click the **Source Control** icon in the left sidebar (branch icon) or press `Ctrl+Shift+G`.
3. Click **Initialize Repository** if prompted.
4. Click the **`...`** menu → **Remote** → **Add Remote** → paste `https://github.com/Elaris1987/CoExistance.git` and name it `origin`.
5. Type a commit message (e.g., "Add project files from VS Code") and click **Commit**.
6. Click **Sync Changes** or **Publish Branch** to push to GitHub.

### After Pushing

Once your files are on GitHub you can verify them at:
**https://github.com/Elaris1987/CoExistance**

## Running the Project

### Prerequisites

- Python 3.11+
- PostgreSQL (optional, for database features)

### Setup

1. **Clone the repository** (on any new machine):
   ```bash
   git clone https://github.com/Elaris1987/CoExistance.git
   cd CoExistance
   code .
   ```

2. **Create & activate a virtual environment:**
   ```bash
   python -m venv .venv
   ```
   - **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
   - **Windows (CMD):** `.venv\Scripts\activate.bat`
   - **macOS/Linux:** `source .venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
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

## License

See repository for license details.
