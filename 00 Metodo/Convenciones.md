---
tags: [decomp, metodo, convenciones]
creado: 2026-10-15
---

# 📐 Convenciones

## Notas
- **Una nota por función** en `30 Proyectos/<proyecto>/Funciones/<NombreFunción>.md`,
  con el nombre exacto del símbolo (sin espacios), creada desde [[Plantilla - Funcion]].
- Toda nota lleva frontmatter con `tags` y `creado` (AAAA-MM-DD).
- Si un nombre de función está repetido (funciones `static`), el nombre de la nota es
  `<Nombre> (<archivo.c>)`.

## Direcciones
- Siempre en hex con prefijo y 8 dígitos: `0x0806957c`.
- Indicar **de qué versión** es cada dirección: `USA 0x080aa7a4` / `ES 0x080aa7b8`.
- Las direcciones Thumb van **pares** en las notas; el bit 0 = 1 solo existe en las
  semillas y en los punteros de función (interworking).

## Estado de una función (`estado:` en el frontmatter)
| Valor | Significado |
|---|---|
| `nombrada` | Tiene nombre portado, sin revisar |
| `leida` | Pseudocódigo leído y comparado con la referencia |
| `entendida` | Parámetros, structs, tablas y constantes identificados |
| `documentada` | Nota completa con explicación y lecciones |

## Confianza
- **Observado**: lo devolvió una herramienta (cita la evidencia/comando).
- **Inferido**: deducción nuestra (dilo explícitamente).
- **Desconocido**: queda pendiente; no se rellena con suposiciones.
