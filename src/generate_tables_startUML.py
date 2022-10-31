import json

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
                    print(attribute)
                    critarias = {
                        "unique": attribute["isUnique"] if "isUnique" in attribute.keys() else False,
                        "id": attribute["isID"] if "isID" in attribute.keys() else False,
                    }
                    typeAttribute = "string"
                    if "type" in attribute.keys():
                        if type(attribute["type"]) is not dict:
                            typeAttribute = attribute["type"]
                        # else:

                    table["attributes"].append({
                        "name": attribute["name"],
                        "type": typeAttribute.lower(),
                        "criterias": critarias
                    })
            if "ownedElements" in element.keys():
                for element in element["ownedElements"]:
                    if element["_type"] == "UMLGeneralization":
                        refParent = element["target"]["$ref"]
                        parents = [v for v in tables
                                  if v["id"] == refParent]
                        if len(parents) > 0:
                            table["attributes"] = parents[0]["attributes"]
                    if element["_type"] == "UMLAssociation":
                        table["associations"].append({ "target": element["end2"]["reference"]["$ref"] })

            tables.append(table)

        # elif element["_type"] == "UMLEnumeration":
        #     pass

    return tables