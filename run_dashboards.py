import subprocess
import time
import webbrowser
import sys

def main():
    print("Iniciando Dashboard 01 (Streamlit)...")
    # Streamlit por defecto usa puerto 8501
    p1 = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "01_Dashboard.py", "--server.port=8501", "--server.headless=true"])
    
    print("Iniciando Dashboard 02 (Shiny/Uvicorn)...")
    # Shiny/Uvicorn en puerto 8050
    p2 = subprocess.Popen([sys.executable, "-m", "uvicorn", "02_Dashboard:app", "--port", "8050"])
    
    print("Esperando a que los servidores arranquen...")
    time.sleep(5)
    
    # Abrir navegadores
    webbrowser.open("http://localhost:8501")
    webbrowser.open("http://localhost:8050")
    
    print("\n ambos dashboards están corriendo.")
    print("Presiona Ctrl+C en esta terminal para detener ambos procesos.")
    
    try:
        p1.wait()
        p2.wait()
    except KeyboardInterrupt:
        print("\nDeteniendo servicios...")
        p1.terminate()
        p2.terminate()
        print("Servicios detenidos.")

if __name__ == "__main__":
    main()
