"""Generate a text file with the citation keys from a BibTeX source."""

from __future__ import annotations

import re
import sys
from pathlib import Path

CITATION_PATTERN = re.compile(r"@[^\s{]+\s*{\s*([^,\n]+)", re.MULTILINE)


def prompt_for_file(prompt: str, extension: str) -> Path:
    """Prompt the user for a file path with the expected extension."""

    try:
        raw_value = input(prompt).strip()
    except EOFError:
        print("No se proporcionó una ruta.")
        raise SystemExit(1)

    path = Path(raw_value).expanduser().resolve()

    if not path.exists():
        print(f"La ruta '{path}' no existe.")
        raise SystemExit(1)

    if not path.is_file():
        print(f"La ruta '{path}' no es un archivo.")
        raise SystemExit(1)

    if path.suffix.lower() != extension:
        print(f"El archivo debe tener la extensión {extension}.")
        raise SystemExit(1)

    return path


def prompt_for_output_path(default_path: Path) -> Path:
    """Ask the user for an output path, allowing Enter to accept the default."""

    try:
        raw_value = input(
            "Ingresa la ruta del archivo .txt de salida (Enter para usar el predeterminado): "
        ).strip()
    except EOFError:
        return default_path

    if not raw_value:
        return default_path

    path = Path(raw_value).expanduser().resolve()

    if path.exists() and not path.is_file():
        print(f"La ruta '{path}' no es un archivo de texto válido.")
        raise SystemExit(1)

    if path.suffix.lower() != ".txt":
        print("El archivo de salida debe tener la extensión .txt.")
        raise SystemExit(1)

    return path


def extract_citation_keys(content: str) -> list[str]:
    """Return the list of citation keys found in the BibTeX content."""

    keys = [match.group(1).strip() for match in CITATION_PATTERN.finditer(content)]
    # Remove any trailing braces or whitespace that might remain
    cleaned_keys = [key.rstrip("}") for key in keys if key]
    return cleaned_keys


def write_keys_to_file(keys: list[str], output_path: Path) -> None:
    """Write each citation key on a separate line in the output file."""

    output_path.write_text("\n".join(keys), encoding="utf-8")


def main() -> None:
    bib_path = prompt_for_file("Ingresa la ruta del archivo .bib: ", ".bib")

    default_output = bib_path.with_suffix(".txt")
    output_path = prompt_for_output_path(default_output)

    try:
        content = bib_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("No fue posible leer el archivo con codificación UTF-8.")
        raise SystemExit(1)

    citation_keys = extract_citation_keys(content)

    if not citation_keys:
        print("No se encontraron claves de citación en el archivo proporcionado.")
        return

    write_keys_to_file(citation_keys, output_path)
    print(f"Se guardaron {len(citation_keys)} claves en '{output_path}'.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
        sys.exit(130)
