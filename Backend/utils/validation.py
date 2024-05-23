def validate_file(filename):
    allowed_extensions = ['.docx', '.doc']
    return any(filename.endswith(ext) for ext in allowed_extensions)
