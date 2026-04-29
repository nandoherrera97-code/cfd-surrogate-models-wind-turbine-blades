import os
import re
import subprocess

if __name__ == "__main__":
 
    run = r"D:/Programa/blueCFD-Core-2020/ofuser-of8/run"
    carpetas=os.listdir(run)

    for carpeta in carpetas:
        ruta=os.path.join(run, carpeta)
        os.chdir(ruta)
        subprocess.run(["foamtoVTK"], check=True)
        