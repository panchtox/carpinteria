"""Agrega un proyecto a la página.

Uso:  python agregar.py "Banqueta de pino" "Laura" foto1.jpg foto2.jpg ...

Achica cada foto a 1600 px de lado mayor, la guarda como JPG en fotos/<proyecto>/ y le borra
los metadatos (EXIF), que pueden traer la ubicación GPS. La primera foto es la portada.
Si el proyecto ya existe (mismo nombre y autor), le suma las fotos nuevas.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

from PIL import Image, ImageOps

try:  # fotos de iPhone (.heic)
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

AQUI = Path(__file__).parent
LADO = 1600


def slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    proyecto, autor, fotos = sys.argv[1].strip(), sys.argv[2].strip(), sys.argv[3:]
    datos = json.loads((AQUI / "proyectos.json").read_text(encoding="utf-8"))
    p = next((x for x in datos if x["proyecto"] == proyecto and x["autor"] == autor), None)
    if p is None:
        p = {"proyecto": proyecto, "autor": autor, "fotos": []}
        datos.append(p)
    carpeta = AQUI / "fotos" / slug(f"{proyecto}-{autor}")
    carpeta.mkdir(parents=True, exist_ok=True)
    for f in fotos:
        im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")   # endereza según el EXIF, después lo descarta
        im.thumbnail((LADO, LADO))
        destino = carpeta / f"{len(p['fotos']) + 1:02d}.jpg"
        im.save(destino, "JPEG", quality=84, optimize=True, progressive=True)
        p["fotos"].append(destino.relative_to(AQUI).as_posix())
        print(f"{f} -> {destino.relative_to(AQUI)}  ({destino.stat().st_size // 1024} KB)")
    (AQUI / "proyectos.json").write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{proyecto} · {autor}: {len(p['fotos'])} fotos. Proyectos en la página: {len(datos)}")


if __name__ == "__main__":
    main()
