"""
NKOptimizer - Desktop app to download and run optimization scripts from GitHub
Repository assumptions:
  - GitHub user: UnknownScrpt
  - Repo name: nkoptimizer
  - Files are in the repository root except for an optional folder named "EXM" containing the 3 EXM files

Features implemented:
  - Modern GUI using customtkinter
  - Auto-download of files on startup (and manual "Atualizar" button)
  - Progress bar for downloads
  - Buttons to execute each script (.bat, .cmd, .exe, .reg)
  - Special "Run Auto Commands" button where you can add commands that run in cmd
  - Logs displayed in the UI
  - Safe handling: files are downloaded to %LOCALAPPDATA%\\NKOptimizer (Windows assumed)

How to use:
  - Install dependencies: pip install customtkinter requests
  - Edit GITHUB_USER / REPO if needed
  - Run this script with Python 3.10+ on Windows
  - To build .exe: pyinstaller --onefile --noconsole nkoptimizer_app.py

Notes about permissions:
  - Many tweaks (.reg, driver installers, registry imports, BCD edits) require administrative privileges.
  - The app will attempt to run commands; please run the generated .exe as administrator when necessary.

"""

__version__ = "1.0.0"

import os, sys, ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Se não for admin, relança o script como administrador
if not is_admin():
    print("Solicitando permissões de administrador...")
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()

import os
import sys
import threading
import subprocess
import requests
import shutil
import time
import urllib.parse
from pathlib import Path

try:
    import customtkinter as ctk
except Exception:
    raise RuntimeError("Dependência ausente: instale 'customtkinter' (pip install customtkinter)")

# -------------------- CONFIG --------------------
GITHUB_USER = "UnknownScrpt"
GITHUB_REPO = "nkoptimizer"
BRANCH = "main"

# Map friendly names to repository paths (path inside the repo)
# If file is inside a subfolder, provide the relative path, e.g. 'EXM/file.cmd'
REPO_FILES = [
    ("ajustes do BCD", "Ajustes de BCD.cmd"),
    ("Otimizar HD", "Otimizar HD.bat"),
    ("otimizar ssd", "Otimizar SSD.bat"),
    ("otimizar GPU (reg)", "Otimizar GPU.reg"),
    ("reduzir delay (reg)", "Reduzir Delay.reg"),
    ("Auto Commands", None),  # special: executes built-in commands (see AUTO_COMMANDS)
    ("optimização nvidia", "Optimizacao_da_NVIDIA.bat"),
    ("Clean", "1 Clean.bat"),
    ("Advanced hidden nvidia GPU tweaks", "Advanced Hidden Nvidia Gpu Tweaks.bat"),
    ("Clear DNS (ping improve)", "Clear DNS Cache (Ping Improve).cmd"),
    ("Delete log Files", "Delete Log Files.cmd"),
    ("EXM free tweaking utility v4", "EXM Free Tweaking Utility V4.cmd"),
    ("latency BCD tweaks", "Latency BCD Tweaks.bat"),
    ("Optimize CPU (reg)", "Optimize CPU.reg"),
    ("Wake up all cores (reg)", "Wake Up All Cores.reg"),
    ("Win 32 priority separator", "Win 32 Priority Separator.exe"),
    ("ligthshot", "setup-lightshot.exe"),
    ("None", "NULw"),
    ("None", "Source Code.cmd"),
]

# AUTO_COMMANDS: commands that will run in cmd automatically when the user clicks the "Auto Commands" button.
# **CAUTION**: Edit these commands to what you want. Avoid destructive commands.
AUTO_COMMANDS = [
    "bcdedit /set useplatformtick yes",  # example placeholder; replace with your commands
    "bcdedit /set disabledynamictick yes"
    "bcdedit /deletevalue useplatformclock"
]

# Where to store downloaded files locally
APP_DIR = Path(os.getenv('LOCALAPPDATA', os.path.expanduser('~'))) / "NKOptimizer"
APP_DIR.mkdir(parents=True, exist_ok=True)

# GitHub raw base URL helper
RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{BRANCH}/"
API_CONTENTS_BASE = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/"

# -------------------- UTIL --------------------

def friendly_to_filename(name: str) -> str:
    """Create a safe local filename from the friendly name"""
    safe = "".join(c for c in name if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()
    return safe


def repo_path_to_raw_url(path: str) -> str:
    # path may contain spaces or non-ascii; must be URL encoded
    return RAW_BASE + urllib.parse.quote(path)


def download_file(repo_path: str, dest: Path) -> bool:
    url = repo_path_to_raw_url(repo_path)
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            with open(dest, 'wb') as f:
                f.write(r.content)
            return True
        else:
            return False
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")
        return False


def list_folder_files(folder: str):
    """Attempt to list files inside a folder of the repo via GitHub API. Returns list of names.
    If API fails, returns empty list."""
    try:
        url = API_CONTENTS_BASE + urllib.parse.quote(folder) + f"?ref={BRANCH}"
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            items = r.json()
            return [item['name'] for item in items if item['type'] == 'file']
    except Exception as e:
        print(f"Erro ao listar pasta {folder}: {e}")
    return []


def run_command_file(path: Path, log_fn=None):
    """Run a .bat/.cmd/.exe/.reg appropriately and log stdout/stderr to log_fn (callable)."""
    if not path.exists():
        if log_fn:
            log_fn(f"Arquivo não encontrado: {path}\n")
        return

    suffix = path.suffix.lower()
    try:
        if suffix in ['.bat', '.cmd']:
            proc = subprocess.run(['cmd', '/c', str(path)], check=False, capture_output=True, text=True)
        elif suffix == '.exe':
            proc = subprocess.run([str(path)], check=False, capture_output=True, text=True)
        elif suffix == '.reg':
            # import registry silently
            proc = subprocess.run(['reg', 'import', str(path)], check=False, capture_output=True, text=True)
        else:
            proc = subprocess.run(['cmd', '/c', str(path)], check=False, capture_output=True, text=True)

        if log_fn:
            log_fn(f"=== Execução: {path.name} ===\n")
            log_fn(proc.stdout)
            if proc.stderr:
                log_fn("--- STDERR ---\n")
                log_fn(proc.stderr)
            log_fn("\n")
    except Exception as e:
        if log_fn:
            log_fn(f"Erro ao executar {path}: {e}\n")


# -------------------- GUI --------------------

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class NKApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NKOptimizer")
        self.geometry("780x520")

        # Left frame: buttons
        self.left_frame = ctk.CTkFrame(self, width=320)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.logo_label = ctk.CTkLabel(self.left_frame, text="NKOptimizer", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=(4,12))

        self.update_btn = ctk.CTkButton(self.left_frame, text="Atualizar (baixar)", command=self.start_downloads)
        self.update_btn.pack(fill='x', pady=6)

        self.exec_buttons_frame = ctk.CTkScrollableFrame(self.left_frame, height=340)
        self.exec_buttons_frame.pack(fill='both', expand=True, pady=6)

        self.exec_buttons = []
        for friendly, repo_path in REPO_FILES:
            btn = ctk.CTkButton(self.exec_buttons_frame, text=friendly, command=lambda f=friendly, p=repo_path: self.handle_run(f, p))
            btn.pack(fill='x', pady=4, padx=6)
            self.exec_buttons.append(btn)

        self.open_appdir_btn = ctk.CTkButton(self.left_frame, text="Abrir pasta local", command=lambda: os.startfile(APP_DIR))
        self.open_appdir_btn.pack(fill='x', pady=6)

        # Right frame: logs and progress
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        self.progress = ctk.CTkProgressBar(self.right_frame)
        self.progress.pack(fill='x', pady=(6,12), padx=6)

        self.log_text = ctk.CTkTextbox(self.right_frame, wrap='word')
        self.log_text.pack(fill='both', expand=True, padx=6, pady=6)
        self.log_text.insert('0.0', 'Bem-vindo ao NKOptimizer. Clique em "Atualizar" para baixar os arquivos do GitHub.\n')

        # Footer
        self.footer = ctk.CTkLabel(self.right_frame, text=f"Repo: {GITHUB_USER}/{GITHUB_REPO}    Local: {APP_DIR}")
        self.footer.pack(pady=6)

        # Start automatic download (user requested auto-download)
        self.after(500, self.start_downloads)

    def log(self, message: str):
        timestamp = time.strftime('[%H:%M:%S] ')
        self.log_text.insert('end', timestamp + message)
        self.log_text.see('end')

    def start_downloads(self):
        t = threading.Thread(target=self.download_all_files, daemon=True)
        t.start()

    def download_all_files(self):
        self.log('Iniciando download dos arquivos...\n')
        files_to_download = []
        # Build list
        for friendly, repo_path in REPO_FILES:
            if repo_path is None:
                continue
            files_to_download.append((friendly, repo_path))

        # Special handling: check EXM folder for any files and append them if not already listed
        exm_names = list_folder_files('EXM')
        for name in exm_names:
            rp = f"EXM/{name}"
            if not any(rp == entry[1] for entry in files_to_download):
                files_to_download.append((name, rp))

        total = len(files_to_download)
        if total == 0:
            self.log('Nenhum arquivo listado para download. Verifique a configuração.\n')
            return

        self.progress.set(0)
        for idx, (friendly, repo_path) in enumerate(files_to_download, start=1):
            local_name = Path(repo_path).name
            dest = APP_DIR / local_name
            self.log(f'Download: {repo_path} -> {dest}\n')
            ok = download_file(repo_path, dest)
            if ok:
                self.log(f'Baixado: {local_name}\n')
            else:
                self.log(f'Falha ao baixar: {repo_path} (verifique se o arquivo existe no repo)\n')
            self.progress.set(idx/total)
        self.log('Downloads concluídos.\n')
        self.progress.set(0)

    def handle_run(self, friendly: str, repo_path: str):
        # Special: Auto Commands
        if friendly == 'Auto Commands' or repo_path is None:
            self.run_auto_commands()
            return

        local_name = Path(repo_path).name
        local_path = APP_DIR / local_name
        if not local_path.exists():
            self.log(f'Arquivo local não encontrado: {local_path}\nTentando baixar agora...\n')
            ok = download_file(repo_path, local_path)
            if not ok:
                self.log('Falha ao baixar arquivo; operação abortada.\n')
                return

        # Execute in a separate thread
        self.log(f'Executando: {local_name}\n')
        t = threading.Thread(target=run_command_file, args=(local_path, self.log), daemon=True)
        t.start()

    def run_auto_commands(self):
        self.log('Executando comandos automáticos...\n')
        for cmd in AUTO_COMMANDS:
            self.log(f'CMD> {cmd}\n')
            try:
                proc = subprocess.run(['cmd', '/c', cmd], capture_output=True, text=True)
                if proc.stdout:
                    self.log(proc.stdout + '\n')
                if proc.stderr:
                    self.log('ERRO: ' + proc.stderr + '\n')
            except Exception as e:
                self.log(f'Exceção ao executar {cmd}: {e}\n')
        self.log('Comandos automáticos finalizados.\n')


# -------------------- Entrypoint --------------------

import json, tempfile, hashlib, subprocess

LATEST_URL = "https://raw.githubusercontent.com/UnknownScrpt/nkoptimizer/main/latest.json"

def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def check_for_updates():
    try:
        print("Checando atualizações...")
        r = requests.get(LATEST_URL, timeout=10)
        if r.status_code != 200:
            print("Falha ao acessar latest.json")
            return False
        latest = r.json()
        latest_ver = latest["version"]
        if latest_ver == __version__:
            print("App está atualizado.")
            return False

        asset_url = latest["asset_url"]
        expected_sha = latest["sha256"]
        print(f"Nova versão encontrada: {latest_ver}")

        # Download temporário
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".exe")
        tmp.close()
        print("Baixando nova versão...")
        download_file(asset_url, Path(tmp.name))
        print("Verificando integridade...")
        if sha256_of_file(tmp.name).lower() != expected_sha.lower():
            print("Checksum inválido!")
            os.remove(tmp.name)
            return False

        # Chama updater.exe
        updater_path = APP_DIR / "updater.exe"
        if not updater_path.exists():
            # Caso o updater ainda não tenha sido baixado, pega do GitHub
            updater_raw = "https://raw.githubusercontent.com/UnknownScrpt/nkoptimizer/main/updater.exe"
            download_file("updater.exe", updater_path)

        old_exe = sys.executable
        subprocess.Popen([str(updater_path), str(old_exe), tmp.name])
        sys.exit(0)
    except Exception as e:
        print(f"Erro ao checar atualização: {e}")
        return False



if __name__ == '__main__':
    check_for_updates()
    app = NKApp()
    app.mainloop()
