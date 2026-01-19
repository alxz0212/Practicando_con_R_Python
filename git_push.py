import subprocess
import os

def run_git_cmd(args):
    print(f"Running: {' '.join(args)}")
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    # 1. Init
    if not os.path.exists(".git"):
        run_git_cmd(["git", "init"])
    
    # 2. Add
    run_git_cmd(["git", "add", "."])
    
    # 3. Commit
    run_git_cmd(["git", "commit", "-m", "Subida inicial: Dashboards Python (Streamlit + Shiny)"])
    
    # 4. Branch
    run_git_cmd(["git", "branch", "-M", "main"])
    
    # 5. Remote (check if exists first to avoid error)
    # Removing just in case it points elsewhere
    subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
    run_git_cmd(["git", "remote", "add", "origin", "https://github.com/alxz0212/Practicando_con_R_Python.git"])
    
    # 6. Push
    print("Intentando hacer push... (Esto puede requerir autenticación en tu sistema)")
    success = run_git_cmd(["git", "push", "-u", "origin", "main"])
    
    if success:
        print("\n\u2705 ¡Subido exitosamente a GitHub!")
    else:
        print("\n\u274c Falló el push. Es posible que te falten credenciales o permisos.")
        print("Intenta ejecutar manualmente: git push -u origin main")

if __name__ == "__main__":
    main()
