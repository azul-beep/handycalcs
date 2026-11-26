# Cerebro de Blue (memoria del Agente Blue)

Lo que el Agente Blue decidió o terminó. Se actualiza en cada tarea. Las correcciones de Azu van además a la skill `produccion-videos-blue`.
Sin contraseñas, tokens ni datos personales.

## Qué cubre el Agente Blue
1. Reels de todas las series: Bitácora, Cómo lo hice, Blue explica, "Claude: tienes que saberlo".
2. La Bitácora (solo hechos reales de la semana, nada inventado).
3. La web del perfil: blueautomatica.pages.dev (código en `blue/web/`).
4. La programación de publicaciones (Business Suite en el Chrome o la PC de Azu, con su frase escrita).

## Reglas fijas
1. Cuenta anónima: nunca nombrar al cliente, decir "un club de deporte".
2. Nada inventado (FTC). Montos reales borrosos si no hay permiso.
3. Flujo: texto, OK de Azu, voz (gasta créditos, solo con su sí escrito), video, control de jurado, mostrar.
4. Gratis primero (Gemini). Flow o ElevenLabs solo con su sí escrito al gasto.
5. Etiqueta "Info de IA" en cada reel. Ningún reel solo de afiliados; nombrar las plataformas usadas sin decir "afiliada".
6. Nada de material de Cozy en Blue. Videos dinámicos, sin planos quietos, con ejemplo real y escenas nuevas (no repetir El duelo).
7. 2 reels por día rotando series. Investigación de tendencias con Gemini Deep Research.
8. Una vez por semana: ver qué reels anduvieron mejor y hacer más de eso.

## Hecho
| Fecha | Qué | Estado |
|---|---|---|
| 24 nov | "Cómo hice El duelo" v2 (~31 s) | Programado semana 23-26 |
| 24 nov | Efectos virales con IA (18 s) | Cambios pedidos por Azu |
| 24 nov | Claude #3 "Claude dirige mis videos" | Aprobado |
| 25 nov | Claude #4 "Claude Code sin programar" | Aprobado, programado sáb 28 7:30 PM |
| 26 nov | Claude #5 "Claude trabaja mientras duermo" (Cowork) | Espera OK de Azu |
| 26 nov | Web del perfil nueva con menú (handycalcs #70) | Hecho |

## Pendiente
1. OK de Azu a Claude #5 y a Claude #1 ("Claude edita tus videos").
2. Bitácora Día 11 (dom 29, 7:30 PM): Azu cuenta qué pasó de verdad esta semana.
3. Links de afiliada en descripciones (Printify, ElevenLabs, HighLevel): falta que Azu acepte términos en PartnerStack y entre al portal de HighLevel.
4. Revisión semanal de los mejores reels.

## Dónde están las cosas
- Videos y guiones: `/mnt/project-files/cuenta-ia/` (aprobados en `para-publicar/aprobados/`, portadas en `portadas-reels/`).
- Voces: Blue = Carito (eleven_v4), Claude = Leo.
- Publicación automática por API: `blue/LEEME.md` (frenada hasta tener token de Meta).
