import sys, os, time, shutil, subprocess

def main():
    if len(sys.argv) < 3:
        print("Uso: updater.exe <caminho_exe_antigo> <caminho_novo_exe>")
        return

    old_exe = sys.argv[1]
    new_tmp = sys.argv[2]
    backup = old_exe + ".bak"

    print("Aguardando fechamento do app antigo...")
    for _ in range(30):
        try:
            os.rename(old_exe, old_exe)
            break
        except PermissionError:
            time.sleep(1)
    else:
        print("O app ainda está em execução. Abortando.")
        sys.exit(1)

    # Backup
    if os.path.exists(backup):
        os.remove(backup)
    shutil.move(old_exe, backup)

    # Mover novo exe
    shutil.move(new_tmp, old_exe)
    os.chmod(old_exe, 0o755)
    print("Atualização concluída. Reiniciando o app...")
    subprocess.Popen([old_exe])
    sys.exit(0)

if __name__ == "__main__":
    main()
