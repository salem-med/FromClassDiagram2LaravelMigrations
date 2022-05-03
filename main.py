import json
from subprocess import PIPE, run
import os

def generate_tables_from_file(classFile):
    tables = []
    cls = json.load(open(classFile, "r"))
    for i, element in enumerate(cls["ownedElements"][0]["ownedElements"]):

        if element["_type"] == "UMLClass":
            table = {
                "id": element["_id"], "name": element["name"],
                "attributes": [], "associations": []
            }

            if "attributes" in element.keys():
                for attribute in element["attributes"]:
                    critarias = {
                        "unique": attribute["isUnique"] if "isUnique" in attribute.keys() else False,
                        "id": attribute["isID"] if "isID" in attribute.keys() else False,
                    }
                    table["attributes"].append({
                        "name": attribute["name"],
                        "type": attribute["type"].lower() if "type" in attribute.keys() else "string",
                        "criterias": critarias
                    })
            if "ownedElements" in element.keys():
                for element in element["ownedElements"]:
                    if element["_type"] == "UMLGeneralization":
                        refParent = element["target"]["$ref"]
                        parents = [v for v in tables
                                  if v["id"] == refParent]
                        table["attributes"] = parents[0]["attributes"]
                    if element["_type"] == "UMLAssociation":
                        table["associations"].append({ "target": element["end2"]["reference"]["$ref"] })

            tables.append(table)

    return tables

def create_migrations(projectPath, tables):
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

        # else:

        # subprocess.call(["php", "artisan", "make:model", table["name"], "-m"])

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

def path_to_windows_path(path):
    return path.replace('\\', '\\\\') if len(path.split("\\")) > 0 else path

tables = generate_tables_from_file(
    path_to_windows_path("J:\Mes_projets\9hiwa-(Flutter-Mobile-App)(Laravel-API)\9hiwa\Conception\working_environnement.mdj"))

for table in tables:
    print(table)

save_tables_in_file(tables)

create_migrations(
    path_to_windows_path("J:\Mes_projets\9hiwa-(Flutter-Mobile-App)(Laravel-API)\9hiwa\9hiwa_API"),
    tables
)


