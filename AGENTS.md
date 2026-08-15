# AGENTS.md - Reglas operativas de R2

## Autoridad

Orden de precedencia:

1. Estado real verificable de Git, herramientas, CI y servidor.
2. Núcleo Operativo R2 v3.3.
3. `R2_STATE.md`.
4. Guía de Ejecución R2 v3.3.
5. Referencia Técnica R2 v3.3, cuando sea necesaria.
6. Este archivo.
7. Resúmenes, memoria e inferencias.

No afirmes estados sin evidencia del objeto exacto.

## Ejecución

- Lee `R2_STATE.md` antes de actuar.
- Ejecuta solo su único `Authorized next step` y el task autorizado aplicable.
- Una propuesta de task no es autorización.
- El builder no amplía permisos, capacidades o paths ni rebaja el riesgo.
- Detente ante autoridad ambigua, baseline ausente, evidencia incompleta o contradicción con el estado real.
- Red, secretos, instalaciones, borrados, staging, commits, push, merge, deploy y cambios remotos requieren autorización explícita.

## Risk floor

- Usa `policy/risk_floors.json` solo según el alcance permitido por su estado.
- PRE clasifica paths, capacidades y acciones previstos.
- POST comprueba que `BASE` sea ancestro de `HEAD` y clasifica el diff exacto `BASE..HEAD`.
- POST debe incluir borrados y ambos lados de renames con datos NUL-safe.
- Control plane desconocido: `D/STOP`. Path normal desconocido: mínimo `B`. `A` requiere clasificación explícita.
- Borrado: mínimo `D`. Rename: máximo entre origen y destino.
- El escalado semántico solo mantiene o sube la clase.
- Si PRE o POST supera la clase autorizada, bloquea y vuelve a autorización.

## Verificación

- Todo verificador crítico necesita un PASS conocido y un FAIL conocido por la razón esperada.
- `FAIL`, `SKIP`, `UNCERTAIN`, `CANCELLED`, `MISSING` y `NOT_EXECUTED` no son PASS cuando el control es obligatorio.
- `NOT_EXECUTED` bloquea, pero no demuestra fallo funcional.
- Registra comando, exit code, salida relevante, objeto observado y estado Git.
- La evidencia solo certifica el archivo, diff, commit, ejecución o configuración exactos observados.

## Separación

- Una tarea funcional normal no modifica simultáneamente implementación y acceptance-authority.
- El builder no autoriza su task, riesgo, alcance ni aceptación.
- El verifier informa hechos; no redefine el producto.
- El humano decide intención, demo, excepciones y gates críticos; no transporta comandos, código ni resultados entre agentes.

## Fuentes locales

- `R2_STATE.md`
- `docs/FEATURE_BRIEF.md`
- `policy/risk_floors.json`

`AGENTS.md` es control plane auxiliar: no sustituye autoridad superior ni constituye enforcement.
