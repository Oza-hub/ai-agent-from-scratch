import os

def save_to_file(content: str, filename: str = "logs/output.txt"):

    # ===== VALIDACIÓN =====
    if not content:
        return {
            "success": False,
            "error": "missing_content",
            "data": None
        }

    try:
        # ===== CREAR CARPETA SI NO EXISTE =====
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # ===== ESCRITURA =====
        with open(filename, "a", encoding="utf-8") as f:
            f.write(content + "\n")

        return {
            "success": True,
            "data": {
                "file": filename,
                "content": content
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": "write_error",
            "data": None,
            "details": str(e)
        }