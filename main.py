import json
from subprocess import PIPE, run
import os


from utils.to_windows_path import path_to_windows_path
from src.generate_tables_startUML import generate_tables_from_file

def create_models(projectPath, tables):
    os.chdir(projectPath)
    created = []

    while len(tables) != len(created):
        cmd = ["php", "artisan", "make:model", table["name"], "-m"]
        output = run(" ".join(cmd), stdout=PIPE, stderr=PIPE, universal_newlines=True)

        result = output.stdout.split("\n")
        msg = result[0].strip()

        if "successfully" in msg:
            migration = result[1].split(":")[1].strip() + ".php"
            print(migration)
            add_migration_content(migration, table)


def save_tables_in_file(tables):
    json.dump(tables, open("tables.json", "w"))

def add_migration_content(migration, table):
    with open(".\\database\\migrations\\" + migration, "a") as f:
        while True:
            if "$table->id" in f.readline():
                break

        lines = []

        for attribute in table["attributes"]:
            lines.append("$table->{}({})".format(attribute["type"], attribute["name"]))

        f.writelines(lines)


tables = generate_tables_from_file(r"working_environnement.mdj")

for table in tables:
    print(table)

save_tables_in_file(tables)

create_models(
    "\\\\wsl.localhost\kali-linux\\home\\slm\\test-app",
    tables
)


