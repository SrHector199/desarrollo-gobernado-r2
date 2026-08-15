# R2_STATE.md - Estado vivo del experimento

> Mantener este archivo corto; enlazar evidencia primaria en lugar de pegar logs extensos.

## Estado
- Current phase: R2-4
- Current accepted SHA: 5e52d71df1b0ce04dd4ee78818f9ee0c3ab6c11a
- Independent review round 1: EXECUTED_BLOCKED
- Independent review round 2: EXECUTED_PASS
- Independent review round 3: NOT_SATISFIED; WAIVED_BY_HUMAN_EXCEPTION_NO_ALTERNATIVE_REVIEWER
- Authorized next step: Diseñar y falsar la corrección mínima del acceptance authority anclada en BASE; no implementar, mergear ni configurar enforcement todavía.
- Last updated: 2026-08-15T13:37:21Z

## Feature Brief activo
- Nombre: Repartidor exacto de gastos.
- Problema: Al dividir un importe entre varias personas, el redondeo puede perder o añadir céntimos.
- Usuario: Personas que necesitan repartir una cuenta o gasto compartido.
- Resultado: Introducir un importe y un número de personas y obtener cantidades individuales cuya suma sea exactamente igual al importe original.
- No objetivo: Interfaz gráfica, cuentas de usuario, almacenamiento, red, impuestos, conversión de monedas o pagos reales.
- Demo de aceptación: Repartir 10,00 EUR entre 3 personas debe producir 3,34 EUR, 3,33 EUR y 3,33 EUR; la suma mostrada debe ser exactamente 10,00 EUR. Una cantidad inválida o cero personas debe rechazarse claramente.
- Brief status: ACCEPTED_FIRST_DRAFT
- Demo status: NOT_EXECUTED

## Invariantes
| ID | Nivel actual | Evidencia primaria / nota |
|---|---|---|
| I-01 | OBSERVADA | Feature Brief y criterio de demo aceptados explícitamente por el dueño antes de crear un task técnico. |
| I-02 | DECLARADA | Sin builder ni task técnico autorizado. |
| I-03 | COMPROBADA | Risk checker SHA-256 22a2a552963464ac07fd95c61e07721b38b74b426e4b962a2b2b31f8597b3781 y policy DEC-CP V3 SHA-256 8c078b056d9a6a278cdac2e3a20afb1c37084e6b6d598671091a22337d476ad9: capabilities conocidas D PASS, staging con C FAIL, desconocida con D FAIL y candidato completo + staging/commit con D PASS en evidencia SHA-256 be85e4b4478432a6c0da4969db5be422e21449fa2d7b36564b2969f0f1661a08. La clasificación no autoriza la ejecución. |
| I-04 | OBSERVADA | Review ronda 2 SHA-256 9da3383b0a2b88f6a428dd7203cac7e51a192641cfde7dd1e5bed04d4584c7db, policy V3 SHA-256 8c078b056d9a6a278cdac2e3a20afb1c37084e6b6d598671091a22337d476ad9 y evidencia de capacidades SHA-256 be85e4b4478432a6c0da4969db5be422e21449fa2d7b36564b2969f0f1661a08; cada hash certifica solo esos bytes. |
| I-05 | COMPROBADA | Runner actual SHA-256 d08fe9bd6188508ae9fc181a6806ce7835a16ab48ce749b1de283655dce2b32f: GOOD PASS y BAD FAIL en evidencia SHA-256 c07f425b4c71b6e0536b770c2699bc42311aba58054037bab31aad865280ad3b; risk checker actual SHA-256 22a2a552963464ac07fd95c61e07721b38b74b426e4b962a2b2b31f8597b3781 conserva PASS/FAIL PRE/POST en evidencia SHA-256 fd7b4f65fe20034ab357f1837a077f64428c2ee35eeba21f3dfb12753ad6277b. |
| I-06 | COMPROBADA_SCOPED | Runner SHA-256 d08fe9bd6188508ae9fc181a6806ce7835a16ab48ce749b1de283655dce2b32f: alcance COOPERATIVE_OR_BUGGY_IMPLEMENTATION, NOT_A_SECURITY_SANDBOX; la forja hostil permanece OUT_OF_SCOPE y falso verde 3. IR2-002 bloquea la primera tarea funcional hasta ampliar CASES. |
| I-07 | DECLARADA | Sin tarea funcional ni acceptance-authority implementada. |
| I-08 | DECLARADA | Handoffs entre agentes medidos en cero; todavía no ejercitado con agentes. |

## Pendientes activos
- DC-006 - Task proposal vs task authorization: OPEN
- EXP-01 - Policy desde BASE: OPEN

## Decisiones resueltas
- PRIV-R2-001 - Identidad Git del repositorio: RESOLVED_LOCAL; user.name `SrHector199`; user.email `221430316+SrHector199@users.noreply.github.com`; user.useConfigOnly `true`; la identidad global real no está autorizada para R2.
- DEC-CP V1 - SUPERSEDED: hash autorizado b6d229b262d7afce045004338ad9d9c892742251c270118c7c87ff7bef1219e1; el bloque R2-2 autorizado produjo después 391aebfc3c6c593a6b1efb6a905105fb56e07b69939c597fa6b4a1ee688ebeed; HISTORICAL_POLICY_PRE_POST=NOT_EXECUTED.
- DEC-CP V2 - SUPERSEDED_BY_V3: policy SHA-256 518c325c9fedfd174b2cac1dca5806058ea0104e77696368972ddf474c660550; independent review round 2 PASS SHA-256 9da3383b0a2b88f6a428dd7203cac7e51a192641cfde7dd1e5bed04d4584c7db; NOT_ENFORCED; NOT_MERGE_AUTHORITY.
- DEC-CP V3 - RESOLVED_V3_LOCAL_EXPERIMENTAL_PENDING_INDEPENDENT_REVIEW: policy SHA-256 8c078b056d9a6a278cdac2e3a20afb1c37084e6b6d598671091a22337d476ad9; capability evidence SHA-256 be85e4b4478432a6c0da4969db5be422e21449fa2d7b36564b2969f0f1661a08; CLASSIFICATION_ONLY_NOT_EXECUTION_AUTHORIZATION; NOT_ENFORCED; NOT_MERGE_AUTHORITY.

## Controles diferidos heredados
- MINOR-4 - PASS: índice verificado con 100755 para scripts/risk_floor.py y scripts/run_functional.py, y 100644 para los otros 17 archivos.
- MINOR-5 - ACTIVE_R2-4: convertir integridad de aceptación en enforcement externo mediante remoto, CI, required check y protección/no-bypass; todavía NOT_EXECUTED.

## Métricas
- Handoffs manuales entre agentes: 5
- Falsos verdes: 4 detectados (R2AA-001 añadido; R2AA-002 no incrementa: documentado, no demostrado dinámicamente en esta revisión)
- Violaciones de scope: 0 detectadas / 0 no detectadas
- Tiempo feature B: NOT_MEASURED
- Demo Feature Brief: BRIEF_ACCEPTED_FIRST_DRAFT / FUNCTIONAL_DEMO_NOT_EXECUTED

## Última evidencia
- Preflight R2-0: Ubuntu sobre WSL 2; usuario hector; HOME /home/hector.
- Herramientas observadas: Git 2.53.0 y Python 3.14.4.
- Repositorio nuevo creado en /home/hector/desarrollo-gobernado-r2, rama main y sin commits.
- Estado inicial de R2_STATE.md observado con SHA-256 beafe65b1d8c8111ee9c4fe5bb1789347bf9ed4ede7f95dba1a04c95ebf91d75.
- 2026-08-14T16:10:28Z: el dueño aceptó explícitamente el Feature Brief y su criterio de demo antes del task técnico.

- 2026-08-14T17:17:16Z: docs/FEATURE_BRIEF.md observado con SHA-256 26088a93747ac7e72160e22331818c5a1125cc3c229d6f5affc63dd352c04908, modo 644 y demo funcional NOT_EXECUTED.

- 2026-08-14T18:19:41Z: DEC-CP V1 autorizada para uso local experimental; policy/risk_floors.json SHA-256 b6d229b262d7afce045004338ad9d9c892742251c270118c7c87ff7bef1219e1. No es ENFORCED ni autoridad de merge. La autorización no incluye checker, AGENTS.md, staging, commit ni publicación. HISTORICAL_RECORD_ONLY; SUPERSEDED_BY_DEC_CP_V2; HISTORICAL_POLICY_PRE_POST=NOT_EXECUTED.

- 2026-08-14T18:41:05Z: AGENTS.md observado con SHA-256 c4f997bd24b6fe1764389ca648a13049978a89925c8233c2e131ebf14789ecab y modo 644; gate R2-1 PASS. Entrada en R2-2 sin crear runner, checker, task, código, staging, commit ni publicación.

- 2026-08-14T19:25:11Z: R2-2 local falsification PASS; seis casos coincidieron. Evidencia evidence/r2-2/local_falsification.json SHA-256 fd7b4f65fe20034ab357f1837a077f64428c2ee35eeba21f3dfb12753ad6277b. Política 391aebfc3c6c593a6b1efb6a905105fb56e07b69939c597fa6b4a1ee688ebeed; runner 6fe5c55da8e273c214a216ef4cca9a01d0a888eaafedbd12a57127683a5864bd; risk checker 22a2a552963464ac07fd95c61e07721b38b74b426e4b962a2b2b31f8597b3781. Sin staging, commit persistente, red ni publicación en el repositorio R2. HISTORICAL_RECORD_ONLY; SUPERSEDED_BY_DEC_CP_V2; HISTORICAL_POLICY_PRE_POST=NOT_EXECUTED.

- 2026-08-14T20:19:13Z: identidad Git instalada únicamente en `.git/config`: user.name `SrHector199`, user.email `221430316+SrHector199@users.noreply.github.com` y user.useConfigOnly `true`; autor y committer efectivos verificados; configuración global sin cambios; sin staging ni commit.

- 2026-08-14T21:03:35Z: falso verde reproducido con el runner SHA-256 6fe5c55da8e273c214a216ef4cca9a01d0a888eaafedbd12a57127683a5864bd: exit 0 sin stdout ni stderr. Runner corregido SHA-256 200d6ea95984f6e62416b3da19fe7c6e32f38c6cf4292b5150a93f98d6a5fcd3: GOOD PASS, BAD FAIL/TOTAL_NOT_CONSERVED, exit-zero FAIL/MISSING_VERDICT y risk PRE D PASS. Evidencia evidence/r2-3/runner_false_green_correction.json SHA-256 49cbd8e88ef9bc8e87c0879a5798eb154ad7dacc918167f76c45ea9d9df22ec2. I-06 COMPROBADA; fase R2-3 sin staging ni commit.

- 2026-08-14T21:51:02Z: segundo falso verde clasificado y sus variantes verdict/json reproducidas con el runner SHA-256 200d6ea95984f6e62416b3da19fe7c6e32f38c6cf4292b5150a93f98d6a5fcd3. Runner rediseñado SHA-256 43f128d235f4849a252c0184d77bf150ceddcc7516618f0be4b5ce9ef6e6d44b: juez solo en controlador separado; GOOD PASS; BAD FAIL/TOTAL_NOT_CONSERVED; exit-zero FAIL/MISSING_OBSERVATION; tamper-verdict y tamper-json FAIL/TOTAL_NOT_CONSERVED; risk PRE D PASS. Evidencia evidence/r2-3/runner_judge_separation.json SHA-256 a70882687105fd9a3f821b6b87eb506c90fbc181e7f754e346835d89e51a72a7. No es una jaula de seguridad; fase R2-3 sin staging ni commit.

- 2026-08-14T23:17:23Z: revisión independiente ronda 1 canonicalizada en evidence/r2-3/independent_review_01.json SHA-256 a505c414ce7949cb3ae175f3d4165036669d05d5e62e65128f471f94a35515cb; resultado EXECUTED_BLOCKED.
- 2026-08-14T23:17:23Z: respuesta D registrada en evidence/r2-3/independent_review_response_01.json SHA-256 c07f425b4c71b6e0536b770c2699bc42311aba58054037bab31aad865280ad3b; DEC-CP V2 policy 518c325c9fedfd174b2cac1dca5806058ea0104e77696368972ddf474c660550; runner d08fe9bd6188508ae9fc181a6806ce7835a16ab48ce749b1de283655dce2b32f; 3 falsos verdes y 2 handoffs. Sin staging ni commit.

- 2026-08-15T00:05:39Z: revisión independiente ronda 2 conservada en evidence/r2-3/independent_review_02.json SHA-256 9da3383b0a2b88f6a428dd7203cac7e51a192641cfde7dd1e5bed04d4584c7db; static PASS, dynamic PASS y baseline_disposition PASS para los bytes revisados.
- 2026-08-15T00:05:39Z: DEC-CP V3 policy SHA-256 8c078b056d9a6a278cdac2e3a20afb1c37084e6b6d598671091a22337d476ad9; capability_floors D comprobados en evidence/r2-3/capability_prebaseline.json SHA-256 be85e4b4478432a6c0da4969db5be422e21449fa2d7b36564b2969f0f1661a08; runner sin cambios. Sin staging ni commit.

- 2026-08-15T01:09:14Z: excepción humana explícita por ausencia de otro revisor; evidencia SHA-256 01f273b1f5a73a7caa8cb1477dc90a731c1fd4674e13074c86ea46ebfcfac74d. Technical review round 3 PASS, independence NOT_SATISFIED; el hueco se acepta como riesgo conocido, sin reetiquetarlo como PASS independiente.

## Excepciones humanas activas
- HUMAN-EXC-IR3-001: ACCEPTED_RISK. No hay otro revisor disponible. La ronda 3 obtuvo PASS técnico pero no independencia; el dueño autoriza continuar el baseline bajo esta limitación conocida.
- Evidencia: evidence/r2-3/human_independence_exception.json SHA-256 01f273b1f5a73a7caa8cb1477dc90a731c1fd4674e13074c86ea46ebfcfac74d.
- Esta excepción no eleva garantías: independent_review_round_3 sigue NOT_SATISFIED y no se afirma ENFORCED/AISLADA.

- 2026-08-15T01:14:07Z: R2-3 staging/index gate PASS sobre 19 entradas: risk PRE D para staging PASS; bytes staged coinciden con el candidato autorizado previo; MINOR-4 PASS (scripts 100755, resto 100644); git diff --cached --check PASS; sin cambios unstaged ni commit.

## Baseline Git R2-3
- Baseline root SHA: 5e52d71df1b0ce04dd4ee78818f9ee0c3ab6c11a
- Baseline tree SHA: b992e2c79ccb91225ef5a09c5dd34191325ed378
- Root commit subject: chore: establish R2 governed baseline
- Identity: SrHector199 <221430316+SrHector199@users.noreply.github.com>
- Root parent count: 0
- Root committed paths: 19
- MINOR-4 index modes: PASS (scripts 100755; resto 100644)
- git diff --cached --check antes del root commit: PASS
- Root working tree after commit: CLEAN
- Independent review round 3: NOT_SATISFIED; WAIVED_BY_HUMAN_EXCEPTION_NO_ALTERNATIVE_REVIEWER; no se reetiqueta como PASS.

- 2026-08-15T11:59:25Z: baseline raíz R2-3 observado en 5e52d71df1b0ce04dd4ee78818f9ee0c3ab6c11a, tree b992e2c79ccb91225ef5a09c5dd34191325ed378; root sin padres, identidad noreply, 19 paths, working tree limpio. MINOR-4 PASS y git diff --cached --check PASS. Excepción humana de independencia permanece ACCEPTED_RISK sin elevar garantías.

## GitHub R2-4
- Repository: SrHector199/desarrollo-gobernado-r2
- Visibility: PUBLIC
- Default branch: main
- Bootstrap main SHA: 72a9c0c1995b3d56aa2711c3dccb448fbe8ecfb7
- Local upstream before CI bootstrap: main -> origin/main
- Remote bootstrap: PASS
- CI bootstrap branch: r2-4/ci-bootstrap
- Expected CI job: r2-governed-validation
- Required check: NOT_CONFIGURED
- Branch protection / no-bypass: NOT_CONFIGURED
- ENFORCED: False

- 2026-08-15T12:25:36Z: GitHub bootstrap observado: repositorio público SrHector199/desarrollo-gobernado-r2, default branch main, remote main 72a9c0c1995b3d56aa2711c3dccb448fbe8ecfb7, origin/main sincronizado, workflows 0, rulesets 0 y branch protection ausente antes del CI bootstrap.

- 2026-08-15T13:37:21Z: revisión independiente R2-4 sobre acceptance authority: evidence evidence/r2-4/acceptance_authority_independent_review_01.json SHA-256 8f3de7fc6212d6bcab3721864098b5d26e7f9299b520f8d3eb19f76fec071eed; independence PASS, static FAIL, dynamic FAIL, enforcement BLOCKED; 6 findings bloqueantes, 4 no bloqueantes; falso verde R2AA-001 suma +1; EXP-01/DC-006 OPEN.

## Revisión independiente R2-4 - acceptance authority
- Evidence: evidence/r2-4/acceptance_authority_independent_review_01.json
- Evidence SHA-256: 8f3de7fc6212d6bcab3721864098b5d26e7f9299b520f8d3eb19f76fec071eed
- Bundle SHA-256 revisado: cb7e08d072408f6fb1321125d4d13676cb3e430360849bff6f064f2d4e4be977
- Manifest SHA-256 revisado: 2f51ba07e292d2ac55a0b31eb91118410f066e7efdda2c98e99ce012821b86af
- Reviewer: Claude (Anthropic) / Claude Opus 5 según identificador visible del revisor.
- fresh_context: true
- authored_current_change: false
- prior_conclusions_used_as_authority: false
- independence_satisfied: PASS
- static_review: FAIL
- dynamic_review: FAIL
- enforcement_disposition: BLOCKED
- strongest_justified_guarantee_if_applied: OBSERVADA
- Blocking findings (6): R2AA-001 CRITICAL, R2AA-002 CRITICAL, R2AA-003 CRITICAL, R2AA-004 HIGH, R2AA-005 HIGH, R2AA-006 HIGH.
- Nonblocking findings (4): R2AA-007 HIGH, R2AA-008 MEDIUM, R2AA-009 MEDIUM, R2AA-010 LOW.
- R2AA-001: falso verde dinámicamente demostrado; incrementa la métrica de falsos verdes en +1.
- R2AA-002: bypass documentado sobre estado skipped/success, pero no ejecutado dinámicamente por el revisor; no incrementa la métrica.
- EXP-01: OPEN.
- DC-006: OPEN.
- Historical R2-3 independence gap: UNCHANGED.
- Enforcement action reviewed: BLOCKED; required check y branch protection permanecen NOT_CONFIGURED.
- 2026-08-15T13:37:21Z: revisión independiente R2-4 canonicalizada; no autoriza merge ni mutación de GitHub settings.

## Blockers
- R2-4 acceptance-authority independent review: EXECUTED_BLOCKED; independence_satisfied=PASS; enforcement_disposition=BLOCKED.
- R2AA-001 CRITICAL BLOCKING: verificadores inline sombreables desde el checkout del PR; falso verde dinámicamente demostrado.
- R2AA-002 CRITICAL BLOCKING: un job saltado puede satisfacer el check nominal sin ejecutar validación.
- R2AA-003 CRITICAL BLOCKING: cero autoridad independiente sobre acceptance authority mientras EXP-01 siga abierto.
- R2AA-004 HIGH BLOCKING: la acción de enforcement propuesta excedía el Authorized next step vigente del objeto revisado.
- R2AA-005 HIGH BLOCKING: DEC-CP V3 declara NOT_ENFORCED y NOT_MERGE_AUTHORITY.
- R2AA-006 HIGH BLOCKING: el workflow actual codifica un diff de un solo uso y no sirve como gate permanente.
- R2AA-007..010: deuda no bloqueante conservada en la evidencia canónica.
- R2-4: required check todavía NOT_CONFIGURED.
- R2-4: branch protection/no-bypass todavía NOT_CONFIGURED; no afirmar ENFORCED.
- MINOR-5: ACTIVE_R2-4 y NOT_EXECUTED.
- Independent review round 3 de R2-3: NOT_SATISFIED; excepción humana ACCEPTED_RISK permanece visible.
- IR2-002: BLOCKING_BEFORE_FIRST_FUNCTIONAL_TASK; ampliar CASES antes de R2-5 funcional.
- IR2-001 e IR2-003 permanecen deuda no bloqueante explícita.
- DC-006 y EXP-01 permanecen OPEN.
- La demo funcional del Feature Brief sigue NOT_EXECUTED.

## Gate de fase
- R2-0 gate: PASS
- R2-1 gate: PASS
- R2-2 gate: PASS
- Evidencia del gate R2-2: runner GOOD/BAD y risk checker PRE/POST; evidence SHA-256 fd7b4f65fe20034ab357f1837a077f64428c2ee35eeba21f3dfb12753ad6277b.
- R2-3 gate: PASS
- Evidencia del gate R2-3: baseline root 5e52d71df1b0ce04dd4ee78818f9ee0c3ab6c11a; tree b992e2c79ccb91225ef5a09c5dd34191325ed378; MINOR-4 PASS; root working tree CLEAN; cierre administrativo condicionado a PRE/POST D PASS.
- Gate de salida de R2-4: NOT_EXECUTED
- Siguiente fase permitida: NO
