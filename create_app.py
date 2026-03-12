import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python create_app.py <app_name>")
    sys.exit(1)

app_name = sys.argv[1]

base_dir = Path(__file__).resolve().parent
apps_dir = base_dir / "apps"
app_dir = apps_dir / app_name

folders = ["views", "services", "models", "urls"]

# Ensure apps/ exists
apps_dir.mkdir(exist_ok=True)

# Ensure apps/__init__.py exists
(apps_dir / "__init__.py").touch(exist_ok=True)

# Ensure apps/<app_name>/ exists
app_dir.mkdir(exist_ok=True)

# Optional: ensure app package itself has __init__.py
(app_dir / "__init__.py").touch(exist_ok=True)
(app_dir / "apps.py").touch(exist_ok=True)

# Create subfolders and their __init__.py files
for folder in folders:
    folder_path = app_dir / folder
    folder_path.mkdir(exist_ok=True)
    (folder_path / "__init__.py").touch(exist_ok=True)
