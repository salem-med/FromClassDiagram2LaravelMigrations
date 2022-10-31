

def path_to_windows_path(path):
    return path.replace('\\', '\\\\') if len(path.split("\\")) > 0 else path