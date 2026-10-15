Identidad visual de EL INGENIERO DE DATOS. Todos los SVG, PNG y favicons salen de `scripts/build.py`; el workflow `build.yml` los regenera y los sube a `main`. Escribe todos tus comentarios en español.

Revisa solo defectos introducidos por este PR. Prioriza:

1. **Archivos generados editados a mano.** Un cambio en `logo/`, `png/`, `social/` o `favicon/` sin el cambio correspondiente en `scripts/` se perderá en la próxima generación.
2. **Medidas por red.** Cada pieza del diccionario `SOCIAL` debe respetar la medida de su plataforma y la tabla del README debe coincidir.
3. **Paleta y contraste.** Solo los colores del README. El amarillo `#F5B800` nunca va como texto sobre fondo claro; sobre botón amarillo el texto va en marino.
4. **Logo.** Sin cambios de proporción, sin rotar, sin sombras ni degradados, con su margen libre.
5. **Marca.** El nombre siempre EL INGENIERO DE DATOS, sin ®.
6. **Reproducibilidad del script** en Linux (necesita `libcairo2`) y dependencias fijadas en `requirements.txt`.

Cada hallazgo lleva severidad, evidencia, impacto y una corrección concreta. Si no hay hallazgos materiales, dilo claramente.
