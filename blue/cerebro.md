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
9. Cierres sin "¿Me sigues?" (Azu 26 nov): adelanto concreto de lo que viene.
10. Todo reel sale YA con música puesta en CapCut, sin preguntar (Azu 27 nov). Sirven temas de uso personal o comercial. Música baja bajo la voz, con fundidos.
11. Serie de Claude: se recrean Shorts virales que ya funcionaron (mismos planos, tiempos, gancho y cierre), con palabras propias de Blue y solo hechos reales.

## Hecho
| Fecha | Qué | Estado |
|---|---|---|
| 24 nov | "Cómo hice El duelo" v2 (~31 s) | Programado semana 23-26 |
| 24 nov | Efectos virales con IA (18 s) | Cambios pedidos por Azu |
| 24 nov | Claude #3 "Claude dirige mis videos" | Aprobado |
| 25 nov | Claude #4 "Claude Code sin programar" | Aprobado, programado sáb 28 7:30 PM |
| 26 nov | Claude #5 "Claude trabaja mientras duermo" (Cowork) | v3 con estudio de mercado, aprobado 26 nov |
| 26 nov | Web del perfil nueva con menú (handycalcs #70) | Hecho |

## Programación
- Esquema semanal: Bitácora a las 7:30 PM. A las 12 PM rotan: Must know (lun y jue), Blue explica (mar y vie), Cómo lo hice (mié y sáb), Blue prueba (dom).
- Claude #4 programado sáb 28, 7:30 PM.
- Bitácora Día 11 (dom 29, 7:30 PM): tema = el cliente (club de deporte, sin nombrarlo) firmó por 1.200 USD de setup + 1.500 USD por mes. El Día 9 ya contó el contrato y los 1.200; el mensual va en el Día 11. Texto propuesto, espera OK. Contador "ganado" = solo lo cobrado.

## Afiliados
- Con link activo: ElevenLabs, GoHighLevel, systeme.io. Printify aprobado.
- El perfil de Instagram tiene un solo link (la web), verificado el 26 nov.

## Créditos gastados
- ElevenLabs: Claude #4 345, Claude #5 408 + 139 (frase del estudio de mercado, 26 nov, con el sí de Azu).
- Flow: 10 (escena de la laptop de Claude #4).

## Pendiente
1. OK de Azu a Claude #1 ("Claude edita tus videos").
2. Poner música en CapCut a #4 (sáb 28), Día 11 (dom 29), #5 (lun 30) y reel #6 "Claude Code en 60 segundos"; reemplazar los programados.
3. Reel #9 "Por qué todos se van de ChatGPT a Claude": tira aprobada, falta su decisión sobre el texto antes de grabar.
3. Links de afiliada en descripciones (Printify, ElevenLabs, HighLevel): falta que Azu acepte términos en PartnerStack y entre al portal de HighLevel.
4. Revisión semanal de los mejores reels.

## Dónde están las cosas
- Videos y guiones: `/mnt/project-files/cuenta-ia/` (aprobados en `para-publicar/aprobados/`, portadas en `portadas-reels/`).
- Voces: Blue = Carito (eleven_v4), Claude = Leo.
- Publicación automática por API: `blue/LEEME.md` (frenada hasta tener token de Meta).
