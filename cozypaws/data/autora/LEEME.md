# Fotos de la autora (Azu con perros)

Poné acá las fotos (jpg, png o webp). Se ordenan por nombre: la primera (por ejemplo `01-principal.jpg`) va en la página
About y en el bloque "Meet the maker" del inicio; las demás forman la galería "Life with dogs".

Dos formas de subirlas, las dos gratis y sin Claude:
1. Desde GitHub: entrá a la carpeta `cozypaws/data/autora/` del repo, "Add file" > "Upload files", arrastrá las fotos y "Commit changes". La web se rearma sola en unos minutos.
2. Desde un hilo de Claude: dejarlas en `/mnt/project-files/cozypaws-trafico/fotos-autora/` y correr `python3 cozypaws/sync.py --fotos`.

El build las achica a 1200 px y las gira bien solas. Mientras no haya fotos, se muestra el logo ilustrado.
