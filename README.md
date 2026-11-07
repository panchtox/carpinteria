# Proyectos de carpintería

Página pública con los proyectos individuales de las clases de carpintería: https://panchtox.github.io/carpinteria/

## Agregar un proyecto

```bash
python agregar.py "Banqueta de pino" "Laura" foto1.jpg foto2.jpg
git add -A && git commit -m "Banqueta de pino (Laura)" && git push
```

La primera foto es la portada. Con `--nota "Inspiración · en proceso"` al final se marca una foto de referencia; cuando llega el resultado, se suman las fotos y se cambia la nota (`--nota ""` la borra). El script achica las fotos y les borra los metadatos (pueden traer la ubicación GPS). Para fotos `.heic` de iPhone: `pip install pillow-heif`.

El autor va sólo con el nombre. Publicar sólo con permiso de cada persona.
