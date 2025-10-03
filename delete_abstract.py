"""Utility script to remove the `abstract` field from a BibTeX file."""

from __future__ import annotations

import sys
from pathlib import Path


def prompt_for_path() -> Path:
	"""Ask the user for a .bib file path and return it as a Path object."""

	try:
		raw_input = input("Ingresa la ruta del archivo .bib: ").strip()
	except EOFError:
		print("No se proporcionó una ruta.")
		raise SystemExit(1)

	path = Path(raw_input).expanduser().resolve()

	if not path.exists():
		print(f"La ruta '{path}' no existe.")
		raise SystemExit(1)

	if not path.is_file():
		print(f"La ruta '{path}' no es un archivo.")
		raise SystemExit(1)

	if path.suffix.lower() != ".bib":
		print("El archivo debe tener la extensión .bib.")
		raise SystemExit(1)

	return path


def remove_abstract_fields(content: str) -> str:
	"""Return the BibTeX content without any `abstract` fields."""

	lines = content.splitlines(keepends=True)
	cleaned_lines: list[str] = []
	skipping = False
	brace_balance = 0

	for line in lines:
		if not skipping:
			stripped = line.lstrip()
			if stripped.lower().startswith("abstract") and "=" in stripped:
				skipping = True
				brace_balance = stripped.count("{") - stripped.count("}")
				if brace_balance <= 0:
					skipping = False
				continue
		else:
			brace_balance += line.count("{") - line.count("}")
			if brace_balance <= 0:
				skipping = False
			continue

		cleaned_lines.append(line)

	return "".join(cleaned_lines)


def main() -> None:
	bib_path = prompt_for_path()

	try:
		original_content = bib_path.read_text(encoding="utf-8")
	except UnicodeDecodeError:
		print("No fue posible leer el archivo con codificación UTF-8.")
		raise SystemExit(1)

	updated_content = remove_abstract_fields(original_content)

	if updated_content == original_content:
		print("No se encontraron campos 'abstract' para eliminar.")
		return

	bib_path.write_text(updated_content, encoding="utf-8")
	print("Campos 'abstract' eliminados correctamente.")


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\nOperación cancelada por el usuario.")
		sys.exit(130)
