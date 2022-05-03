def path_to_windows_path(path):
    return path.replace('\\', '\\\\') if len(path.split("\\")) > 0 else path

with open(
    path_to_windows_path("J:\Mes_projets\9hiwa-(Flutter-Mobile-App)(Laravel-API)\9hiwa\9hiwa_API") + ".\\database\\migrations\\2021_10_17_234224_create_products_table.php", "r+") as f:
    while True:
        # f.seek(5, 0)
        if "Schema" in f.readline():
            break

