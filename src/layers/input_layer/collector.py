import pathlib
import re


def collect(source_type: str, source_value: str) -> str:
    if source_type == "text":
        return source_value.strip()

    if source_type == "url":
        cleaned = re.sub(r"https?://", "", source_value).strip("/")
        return f"Contenido simulado extraido de {cleaned}."

    if source_type == "file":
        path = pathlib.Path(source_value)
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"No se encontro el archivo: {source_value}")
        return path.read_text(encoding="utf-8")

    raise ValueError(f"Tipo de fuente no soportado: {source_type}")
