# Fotos y capturas para redes

Aquí viven las imágenes que **no** genera `scripts/build.py`: capturas de pantalla, fotografías y exportaciones hechas a mano en Canva. El workflow `build.yml` nunca toca esta carpeta.

## Convención

```
fotos/
  redes/
    post-05-terminal-windows.png
    post-12-lanzamiento-instagram-1080x1350.png
  autor/
    elmer-retrato-1080.jpg
```

- Nombre: `post-<ID del Calendario de contenido en Notion>-<descripción corta>[-anchoxalto].<ext>`. Minúsculas, sin espacios, sin acentos ni ñ.
- Formatos: PNG para capturas, JPG para fotos. Tamaño máximo razonable: 2 MB.
- Instagram pide 1080 × 1350 (4:5) o 1080 × 1080; LinkedIn y Threads aceptan cualquier proporción.

## URL pública

Una vez en `main`, cada archivo se sirve en:

```
https://raw.githubusercontent.com/elingenierodedatos/brand/main/fotos/redes/<archivo>
```

Esa URL es la que se pega en la columna **Imagen fuente** del Calendario de contenido y la que usa Buffer. Las imágenes pegadas en Notion no sirven para publicar: su URL es privada y caduca.

## Flujo

1. La imagen se pega en la fila del post en Notion, como registro.
2. Desde la computadora: copiar el archivo aquí con el nombre de la convención, commit y push a `main`.
3. Claude toma la URL pública y programa el post en Buffer.
