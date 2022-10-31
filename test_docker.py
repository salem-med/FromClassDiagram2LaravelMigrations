import os
from subprocess import PIPE, run


os.chdir("\\\\wsl.localhost\kali-linux\\home\\slm\\test-app\\database\\migrations")

cmd = ["php", "artisan", "make:model", "test", "-m"]
output = run(" ".join(cmd), stdout=PIPE, stderr=PIPE, universal_newlines=True)


print(output)