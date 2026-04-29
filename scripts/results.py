import os
import re
import subprocess
import shutil



base=os.getcwd()
run=os.path.join(base,"run")
carpetas=os.listdir(run)
results=os.path.join(base,"results")


comando = ["pvbatch", "macro.py"]
carpetas=os.listdir(run)

while len(carpetas)>0:
    subprocess.run(comando, check=True)
    print("Eliminando carpetas")

    if len(carpetas)>10:
        for j in range (10):
            src=os.path.join(run,carpetas[j])
            dst = os.path.join(results, carpetas[j])
            shutil.move(src,dst)
            
    else:
        for j in range (len(carpetas)):
            src=os.path.join(run,carpetas[j])
            dst = os.path.join(results, carpetas[j])
            shutil.move(src,dst)
    carpetas=os.listdir(run)
        
