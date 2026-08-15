# R2_STATE.md - Estado vivo del experimento

> Mantener este archivo corto; enlazar evidencia primaria en lugar de pegar logs extensos.

## Estado
- Current phase: R2-4
- Current accepted SHA: 5e52d71df1b0ce04dd4ee78818f9ee0c3ab6c11a
- Independent review round 1: EXECUTED_BLOCKED
- Independent review round 2: EXECUTED_PASS
- Independent review round 3: NOT_SATISFIED; WAIVED_BY_HUMAN_EXCEPTION_NO_ALTERNATIVE_REVIEWER
- Authorized next step: Preparar y falsar el bootstrap merge gate con ancla exacta de implementación `main` 72a9c0c1995b3d56aa2711c3dccb448fbe8ecfb7 -> `b9abfe0d9e80f41c9a9699e5e59827a82ffe4f82`, inventariando todos los paths, modos y bytes de ese diff y verificando que el control plane coincide exactamente con los bytes independientemente revisados; además, como esta canonicalización administrativa avanzará la PR más allá de `b9abfe0d...`, el gate debe inventariar separadamente el tail `b9abfe0d...` -> HEAD real de la PR y exigir que contenga únicamente canonicalizaciones explícitamente autorizadas. Antes de cualquier merge debe quedar contabilizado también el diff completo `main` -> HEAD real. No hacer merge, branch protection, required check, rulesets, cambios de settings GitHub ni transición a R2-5 en ese paso; un merge posterior requerirá Human Gate D separado.
- Last updated: 2026-08-15T21:04:56Z

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
- Falsos verdes: 6 detectados (el candidato Materialization V2 obtuvo revisión independiente PASS 57/57; NEW-01 es fail-closed y no añade falso verde)
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

- 2026-08-15T13:57:42Z: falsificación scratch BASE-anchored PASS 12/12; evidence evidence/r2-4/base_anchored_scratch_falsification_01.json SHA-256 d0177234959a5d77f32c6d40c4cd578b35285ecc09aa69962c2c2e5decf75974; new false-green increment 0; EXP-01/DC-006 OPEN; GitHub event semantics DYNAMIC_NOT_EXECUTED; no implementation authority.

## Falsificación scratch R2-4 - acceptance authority anclada en BASE
- Evidence: evidence/r2-4/base_anchored_scratch_falsification_01.json
- Evidence SHA-256: d0177234959a5d77f32c6d40c4cd578b35285ecc09aa69962c2c2e5decf75974
- Source file: r2-4-base-anchored-falsification-20260815T135232Z.json
- Scratch falsification: PASS 12/12.
- Design disposition: SCRATCH_FALSIFICATION_PASS_NOT_IMPLEMENTATION_AUTHORITY.
- Authority source: BASE.
- Task authorization source: BASE.
- Policy gate candidate checkout: false.
- Policy gate candidate code executed: false.
- Normal-flow acceptance-authority mutation from HEAD: FORBIDDEN in the prototype.
- R2AA-001 design probe: PASS.
- R2AA-002 design probe: PASS_BASE_WORKFLOW_UNCHANGED_BY_HEAD.
- R2AA-003 design probe: PASS_NORMAL_FLOW_CANNOT_CHANGE_ACCEPTANCE_AUTHORITY.
- R2AA-005 design probe: PASS_V4_PROTOTYPE_ACTIVATION.
- R2AA-006 design probe: PASS_FUTURE_SRC_CHANGE_WITHOUT_WORKFLOW_EDIT.
- R2AA-007 design probe: PASS_POST_POSITIVE_AND_NEGATIVE_PATHS.
- External GitHub event semantics: DYNAMIC_NOT_EXECUTED; no claim of real-platform enforcement.
- New real false-green increment: 0; metric remains 4.
- EXP-01: OPEN; scratch evidence does not close it before exact implementation + GitHub proof.
- DC-006: OPEN; scratch task-from-BASE prototype does not choose the production authorization mechanism.
- MINOR-5: ACTIVE_R2-4_NOT_EXECUTED.
- Independent-review requirement: PENDING for the exact candidate design before implementation.
- Existing independent-review blockers remain historical/current until an exact reviewed candidate resolves them; this scratch PASS does not relabel the prior BLOCKED disposition.
- 2026-08-15T13:57:42Z: human-authorized canonicalization only; no workflow/checker/policy/task/GitHub-settings implementation in this commit.

- 2026-08-15T14:45:16Z: segunda revisión independiente del candidato BASE-anchored: evidence evidence/r2-4/base_anchored_candidate_independent_review_02.json SHA-256 84b2bc79bd644711cd55da8ebc4b0104042205cd6286f718058ba5c3ee5e025a; independence PASS; static/dynamic FAIL; candidate/bootstrap BLOCKED; R2AA-011 CRITICAL falso verde +1; R2AA-012..015 no bloqueantes; false greens 5; EXP-01/DC-006 OPEN.

## Segunda revisión independiente del candidato R2-4 - BASE anchored
- Evidence: evidence/r2-4/base_anchored_candidate_independent_review_02.json
- Evidence SHA-256: 84b2bc79bd644711cd55da8ebc4b0104042205cd6286f718058ba5c3ee5e025a
- Bundle SHA-256 revisado: 1f2b42fadef243e78b08c2255bf6f5b2ed65e5cb2af4d78dac9af76bf9a12d03
- Manifest SHA-256 revisado: 7ffa6164274873b0bf799bb23189dcdbcded51fc80e8f829005b3f77486aa5d1
- Reviewer: Anthropic Claude / Claude Opus 5 según identificador visible del revisor.
- fresh_context: true.
- authored_current_change: false.
- prior_conclusions_used_as_authority: false.
- independence_satisfied: PASS.
- static_review: FAIL.
- dynamic_review: FAIL.
- candidate_disposition: BLOCKED.
- bootstrap_disposition: BLOCKED.
- C2 checks: 25 PASS / 3 FAIL / 2 UNCERTAIN.
- C2 FAIL: C2-13, C2-17, C2-21.
- C2 UNCERTAIN: C2-15, C2-23.
- R2AA-011: CRITICAL BLOCKING; falso verde dinámicamente reproducido; incrementa falsos verdes +1.
- R2AA-012: HIGH NONBLOCKING; binding del check `pull_request_target` al SHA de HEAD requiere prueba GitHub real.
- R2AA-013: MEDIUM NONBLOCKING; `default_branch=main` observado ahora read-only, pero la posible desviación temporal workflow/default-branch vs PR_BASE_SHA sigue pendiente.
- R2AA-014: MEDIUM NONBLOCKING; la comprobación BASE/HEAD debe exigir claves presentes e igualdad estricta.
- R2AA-015: LOW NONBLOCKING; limitaciones fail-closed/liveness deben documentarse y distinguirse de riesgo.
- R2AA resolution report del candidato: 001 RESOLVED; 002 RESOLVED; 003 BLOCKING; 004 RESOLVED; 005 RESOLVED; 006 RESOLVED; 007 PARTIAL; 008 RESOLVED; 009 PARTIAL; 010 PARTIAL.
- Corrección mínima autorizada solo para diseño/falsificación scratch: proteger como D todos los bytes que el gate ejecute; fijar integridad contra blobs exactos de BASE; exigir BASE/HEAD estrictos; evaluar el PR antes de ejecutar self-tests/fixtures.
- Una simple comprobación de working tree limpio NO se considera corrección suficiente; la review reprodujo evasión mediante `assume-unchanged`.
- DC-006: OPEN.
- EXP-01: OPEN.
- Historical R2-3 independence gap: UNCHANGED.
- MINOR-5: ACTIVE_R2-4_NOT_EXECUTED.
- Esta revisión no autoriza implementación, merge, branch protection, required check ni GitHub settings.
- 2026-08-15T14:45:16Z: segunda revisión independiente del candidato canonicalizada como BLOCKED.

- 2026-08-15T15:01:28Z: R2AA-011 correction scratch PASS 13/13; evidence evidence/r2-4/r2aa_011_correction_scratch_falsification_01.json SHA-256 637b4f1555d4040d386723586b1df1ebdf4f52c5b55d32eda93526681a069a47; R2AA-011 remains BLOCKING_UNTIL_EXACT_CANDIDATE_INDEPENDENT_REVIEW; new false-green increment 0; false greens remain 5; R2AA-012..015 explicit nonblocking debt; EXP-01/DC-006 OPEN.

## Falsificación scratch de la corrección R2AA-011
- Evidence: evidence/r2-4/r2aa_011_correction_scratch_falsification_01.json
- Evidence SHA-256: 637b4f1555d4040d386723586b1df1ebdf4f52c5b55d32eda93526681a069a47
- Source file: r2-4-r2aa-011-correction-falsification-20260815T145120Z.json
- Scratch falsification: PASS 13/13.
- Disposition: SCRATCH_CORRECTION_FALSIFICATION_PASS_NOT_IMPLEMENTATION_AUTHORITY.
- R2AA-011: CORRECTION_SCRATCH_PASS; BLOCKING_UNTIL_EXACT_CANDIDATE_INDEPENDENT_REVIEW.
- Ejecuted authority bytes: fixtures GOOD/BAD, runner, checker, policy, gate y workflow protegidos como D en el prototipo.
- Integridad: objetos pinneados por SHA-256 y contrastados con blobs exactos de BASE; gate contrastado byte a byte con su blob BASE.
- Temporal BASE capture probe: PASS/BLOCKED_BY_PINNED_BLOB.
- `git update-index --assume-unchanged` bypass probe: PASS/BLOCKED_BY_HASH despite empty git status.
- BASE/HEAD binding: STRICT; missing or mismatched object identity is rejected in the prototype.
- Evaluation order: PR evaluation before trusted fixture self-test.
- Self-test post-runner integrity recheck: PASS.
- New real false-green increment: 0; metric remains 5.
- R2AA-012 OPEN NONBLOCKING: binding real de `pull_request_target` al SHA exacto del PR sigue sin evidencia de plataforma suficiente.
- R2AA-013 PARTIAL NONBLOCKING: distinción temporal workflow-source SHA vs PR_BASE_SHA permanece abierta.
- R2AA-014 MEDIUM NONBLOCKING: strict BASE/HEAD correction passed scratch; remains debt until exact candidate independent review.
- R2AA-015 OPEN NONBLOCKING: deuda de liveness/fail-closed permanece explícita.
- DC-006: OPEN.
- EXP-01: OPEN.
- MINOR-5: ACTIVE_R2-4_NOT_EXECUTED.
- Historical R2-3 independence gap: UNCHANGED.
- Independent review of exact corrected candidate: PENDING.
- Implementation/merge/protection/settings authority: NOT_GRANTED_BY_THIS_EVIDENCE.
- 2026-08-15T15:01:28Z: human-authorized canonicalization only; no workflow/checker/policy/runner/fixture/task/GitHub-settings implementation in this commit.

- 2026-08-15T18:30:27Z: tercera revisión independiente corrected candidate: evidence evidence/r2-4/r2aa_011_corrected_candidate_independent_review_03.json SHA-256 96bb0ae10811fa680d2b242ed5321dafd844c2f7868ae0322fda3f47d0665777; independence PASS; static FAIL; dynamic PASS; candidate/bootstrap BLOCKED; C3 33/2; R2AA-011 PARTIAL; R2AA-014 RESOLVED; R2AA-016/017 BLOCKING; new false-green increment 0; false greens remain 5; EXP-01/DC-006 OPEN.

## Tercera revisión independiente del candidato corregido R2-4
- Evidence: evidence/r2-4/r2aa_011_corrected_candidate_independent_review_03.json
- Evidence SHA-256: 96bb0ae10811fa680d2b242ed5321dafd844c2f7868ae0322fda3f47d0665777
- Reviewed bundle SHA-256: b07c0526c35024c7a206394209f2a9a58179b802a3c00d8385f9f6a5c3835d17
- Reviewed manifest SHA-256: f9c06654252c2383eea3860bf673fe15e03cf2dbbcce1a5bc54e2dba1ea7bf05
- Reviewer: Anthropic / Claude Opus 5 según identificador visible del resultado.
- fresh_context: true.
- authored_current_change: false.
- prior_conclusions_used_as_authority: false.
- independence_satisfied: PASS.
- static_review: FAIL.
- dynamic_review: PASS.
- candidate_disposition: BLOCKED.
- bootstrap_disposition: BLOCKED.
- C3 checks: 33 PASS / 2 FAIL.
- C3 FAIL: C3-02, C3-28.
- R2AA-011: PARTIAL.
- R2AA-012: OPEN.
- R2AA-013: PARTIAL.
- R2AA-014: RESOLVED for the exact reviewed bytes.
- R2AA-015: OPEN.
- R2AA-016: HIGH BLOCKING; `.gitattributes` can enter as B and create CRLF authority lockout.
- R2AA-017: MEDIUM BLOCKING; supplied local exact-candidate probe artifact was not bound to exact candidate hashes/bytes.
- R2AA-018: MEDIUM NONBLOCKING; open `unknown_normal=B` radius under zero approvals.
- R2AA-019: LOW NONBLOCKING; workflow-source SHA not directly asserted against PR_BASE_SHA.
- R2AA-020: LOW NONBLOCKING; unpinned Python environment dependency.
- R2AA-021: LOW NONBLOCKING; ref-tip equality liveness debt.
- New real false-green increment: 0; metric remains 5.
- DC-006: OPEN.
- EXP-01: OPEN.
- MINOR-5: ACTIVE_R2-4_NOT_EXECUTED.
- Historical R2-3 independence gap: UNCHANGED.
- Next scratch design must protect `.gitattributes` and `.gitmodules` as D; eliminate the open B radius by changing `unknown_normal` to C or proving an equivalent mechanical alternative; preserve `src/` and ordinary `tests/` as B and executed fixtures as D; bind probe evidence to exact exercised byte hashes plus manifest; reproduce and close the CRLF lockout; preserve R2AA-011 and R2AA-014 corrections.
- This review grants no implementation, merge, protection, required-check, ruleset or GitHub-settings authority.
- 2026-08-15T18:30:27Z: human-authorized canonicalization only; no workflow/checker/policy/runner/fixture/task/GitHub-settings implementation in this commit.

- 2026-08-15T18:42:35Z: R2AA-016/017 joint scratch correction PASS 23/23; manifest evidence/r2-4/r2aa_016_017_scratch_candidate_manifest_01.json SHA-256 424e7c1543cfbcb374a432fc099d45c262080a02794941f8f0208eb1e73b7ef6; evidence evidence/r2-4/r2aa_016_017_correction_scratch_falsification_01.json SHA-256 0f31183ec4f6b133fd7426fe9a78675eb0d2b0debb8b0ae5f783b00d7aed55f2; exact hash/byte binding PASS; R2AA-016/017 remain blocking until exact-candidate independent review; R2AA-018 unknown_normal=C scratch PASS; false greens remain 5; EXP-01/DC-006 OPEN.

## Falsificación scratch conjunta R2AA-016/R2AA-017
- Candidate manifest: evidence/r2-4/r2aa_016_017_scratch_candidate_manifest_01.json
- Candidate manifest SHA-256: 424e7c1543cfbcb374a432fc099d45c262080a02794941f8f0208eb1e73b7ef6
- Candidate manifest bytes: 1846
- Falsification evidence: evidence/r2-4/r2aa_016_017_correction_scratch_falsification_01.json
- Falsification evidence SHA-256: 0f31183ec4f6b133fd7426fe9a78675eb0d2b0debb8b0ae5f783b00d7aed55f2
- Falsification evidence bytes: 9186
- Scratch falsification: PASS 23/23.
- Manifest/evidence binding: PASS; evidence.candidate_manifest_sha256 equals the exact manifest SHA-256.
- Exercised object hash binding: PASS; evidence hashes exactly equal manifest object hashes.
- Exercised object byte-count binding: PASS; evidence byte counts exactly equal manifest byte counts.
- Proposed workflow SHA-256: 76baea48e276472e3b6ee4e93c77c110e0575261d52f14694b8e4e2a36aa0830
- Proposed base_gate SHA-256: c01765964bb6d3ca413bfa9d0fcc2380693c6121ff643ee6849c77ed71251dc4
- Proposed checker SHA-256: e627c75f93d23571c12fcd14bed3578301a14de3b0bc4bc6eaf84811454ef080
- Proposed policy SHA-256: 4290e87c2e332838045c189fe6623004a505e07ec4f6d01877e53329b344a083
- Proposed runner SHA-256: d08fe9bd6188508ae9fc181a6806ce7835a16ab48ce749b1de283655dce2b32f
- Proposed GOOD fixture SHA-256: 1c86e6843ad8ab5e07d2fac2575f53bfdbaa695646dde5211c68cda732b45827
- Proposed BAD fixture SHA-256: b9989b0e62c55b54528a87f26f835a137f52b2e5d76f6bf0608482351a50d3ce
- Prototype floors: `.gitattributes=D`; `.gitmodules=D`; `unknown_normal=C`; `src/=B`; `tests/=B`; GOOD/BAD fixtures D.
- R2AA-016: CORRECTION_SCRATCH_PASS; BLOCKING_UNTIL_EXACT_CANDIDATE_INDEPENDENT_REVIEW.
- R2AA-016 CRLF lockout: reproduced only after forced bypass; ordinary corrected B flow blocks `.gitattributes` before it can enter.
- R2AA-017: CORRECTION_SCRATCH_PASS; BLOCKING_UNTIL_EXACT_CANDIDATE_INDEPENDENT_REVIEW.
- R2AA-017 binding chain: candidate manifest -> exact object hashes; probe evidence -> manifest SHA + same hashes; future review-bundle manifest must bind both proposed object hashes and this evidence hash.
- R2AA-018: CORRECTION_SCRATCH_PASS_UNKNOWN_NORMAL_C; PENDING_EXACT_CANDIDATE_REVIEW.
- R2AA-011 correction preserved in scratch; historical disposition remains PARTIAL.
- R2AA-014 strict binding preserved in scratch; historical exact-candidate review remains RESOLVED for the previously reviewed bytes.
- R2AA-012: OPEN.
- R2AA-013: PARTIAL.
- R2AA-015: OPEN.
- R2AA-019: LOW NONBLOCKING.
- R2AA-020: LOW NONBLOCKING.
- R2AA-021: LOW NONBLOCKING.
- DC-006: OPEN.
- EXP-01: OPEN.
- MINOR-5: ACTIVE_R2-4_NOT_EXECUTED.
- Historical R2-3 independence gap: UNCHANGED.
- New real false-green increment: 0; total remains 5.
- Next exact candidate procedure: freeze exact candidate bytes first; generate manifest from those bytes; execute probes only against those same bytes; bind probe evidence to that manifest; only then construct the independent-review bundle.
- This evidence grants no implementation, merge, protection, required-check, ruleset or GitHub-settings authority.
- 2026-08-15T18:42:35Z: human-authorized canonicalization only; no control-plane implementation in this commit.

- 2026-08-15T19:15:19Z: independent frozen candidate review BLOCKED; evidence evidence/r2-4/r2aa_016_017_frozen_candidate_independent_review_04.json SHA-256 e41304ceb8fc91ffbcaadf8829d6aefcd04301a0e520267dcd27353e21e749f0; C4 39 PASS/5 FAIL/2 UNCERTAIN; R2AA-022 HIGH BLOCKING; R2AA-023/024 MEDIUM nonblocking; R2AA-025 LOW nonblocking; FALSE_GREEN_6 recorded as EVIDENCE_VERIFIER_FALSE_GREEN; false greens 5->6; DC-006/EXP-01 OPEN; IR2-002 blocking before first functional task.

## Revisión independiente del candidato congelado R2AA-016/R2AA-017
- Evidence: evidence/r2-4/r2aa_016_017_frozen_candidate_independent_review_04.json
- Evidence SHA-256: e41304ceb8fc91ffbcaadf8829d6aefcd04301a0e520267dcd27353e21e749f0
- Evidence bytes: 43132
- Reviewed bundle SHA-256: 9cef50a5eee6e0cc78ad88ef8e1a18356e6587bb0ac91f1a45bd0b72583177b1
- Reviewed manifest SHA-256: 6dc5d4950c09f31ddeaeb064576b3c40e937aaeb0c3df4fb2fcd2957af162cf7
- independence_satisfied: PASS.
- static_review: FAIL.
- dynamic_review: FAIL.
- candidate_disposition: BLOCKED.
- bootstrap_disposition: BLOCKED.
- C4 checks: 39 PASS / 5 FAIL / 2 UNCERTAIN.
- C4 FAIL: C4-11, C4-13, C4-14, C4-20, C4-36.
- C4 UNCERTAIN: C4-09, C4-34.
- R2AA-011: PARTIAL.
- R2AA-012: OPEN.
- R2AA-013: PARTIAL.
- R2AA-014: RESOLVED.
- R2AA-015: OPEN.
- R2AA-016: BLOCKING.
- R2AA-017: PARTIAL.
- R2AA-018: PARTIAL.
- R2AA-019: OPEN.
- R2AA-020: OPEN.
- R2AA-021: OPEN.
- R2AA-022 HIGH - CORRECTION_SCRATCH_PASS; BLOCKING_UNTIL_EXACT_CANDIDATE_INDEPENDENT_REVIEW: `.gitattributes` queda D por basename a cualquier profundidad; el lockout CRLF anidado sigue siendo reproducible tras bypass forzado, pero su entrada B ordinaria queda bloqueada.
- R2AA-023 MEDIUM NONBLOCKING - CORRECTION_SCRATCH_PASS; PENDING_EXACT_CANDIDATE_REVIEW: symlink mode 120000 y type-change quedan D en el prototipo Git-mode-aware.
- R2AA-024 MEDIUM NONBLOCKING - CORRECTION_SCRATCH_PASS; PENDING_EXACT_CANDIDATE_REVIEW: gitlink mode 160000 queda D en el prototipo.
- R2AA-025 OPEN LOW NONBLOCKING: `RISK_PAYLOAD_OBJECT_MISMATCH` continúa enmascarando errores del checker/liveness; no se corrigió en este scope.
- FALSE_GREEN_6: EVIDENCE_VERIFIER_FALSE_GREEN.
- FALSE_GREEN_6 cause: la evidencia del candidato declaró PASS para `R2AA_016_CRLF_LOCKOUT_REPRODUCED_ONLY_AFTER_FORCED_BYPASS`; la revisión independiente falsó dinámicamente esa propiedad con `tests/fixtures/.gitattributes` bajo flujo B ordinario.
- False greens: 6 total; increment 5 -> 6.
- `required_approving_review_count=0`: NOT_JUSTIFIED_WHILE_DC_006_OPEN.
- Temporary proposal for next scratch design: `required_approving_review_count=1`; proposal only, NOT_CONFIGURED.
- DC-006: OPEN.
- EXP-01: OPEN.
- IR2-002: BLOCKING_BEFORE_FIRST_FUNCTIONAL_TASK.
- MINOR-5: ACTIVE_R2-4_NOT_EXECUTED.
- Historical R2-3 independence gap: UNCHANGED.
- Freeze-before-probes: procedural discipline, not a cryptographic guarantee.
- Next scratch target: basename-level D protection for `.gitattributes`/`.gitmodules` at any depth; Git mode-aware classification for symlink 120000, gitlink 160000, type-change and executable-mode changes; preserve `unknown_normal=C`, regular `src/`/`tests/` B, R2AA-011 and R2AA-014; retest nested CRLF/symlink/type-change/gitlink; temporary proposal of one required approval while DC-006 remains OPEN.
- This review grants no implementation, merge, protection, required-check, ruleset or GitHub-settings authority.
- 2026-08-15T19:15:19Z: human-authorized canonicalization only; no control-plane implementation in this commit.

- 2026-08-15T19:52:49Z: materialization-semantics V2 scratch PASS 27/27; manifest evidence/r2-4/r2aa_022_024_materialization_scratch_candidate_manifest_01.json SHA-256 ec76d56cc9722073e94ce8a0c48a7c836e36e122fe71307db1910a20f211ad28; evidence evidence/r2-4/r2aa_022_024_materialization_correction_scratch_falsification_01.json SHA-256 833d2502730d2b6113b60d96bc80d8a8caecca707ae0ad8efc8e3b188eeafa36; exact hash/byte binding PASS; R2AA-022/023/024 correction scratch PASS pending exact-candidate review; R2AA-016 BLOCKING; R2AA-017/018 PARTIAL; R2AA-025 OPEN; temporary approval proposal=1 NOT_CONFIGURED; false greens remain 6; DC-006/EXP-01 OPEN; IR2-002 blocking before first functional task.

## Falsificación scratch de semántica de materialización V2
- Candidate manifest: evidence/r2-4/r2aa_022_024_materialization_scratch_candidate_manifest_01.json
- Candidate manifest SHA-256: ec76d56cc9722073e94ce8a0c48a7c836e36e122fe71307db1910a20f211ad28
- Candidate manifest bytes: 2080
- Falsification evidence: evidence/r2-4/r2aa_022_024_materialization_correction_scratch_falsification_01.json
- Falsification evidence SHA-256: 833d2502730d2b6113b60d96bc80d8a8caecca707ae0ad8efc8e3b188eeafa36
- Falsification evidence bytes: 10973
- Scratch falsification: PASS 27/27.
- Manifest/evidence binding: PASS; evidence.candidate_manifest_sha256 equals the exact manifest SHA-256.
- Exercised object hash binding: PASS; evidence hashes exactly equal manifest object hashes.
- Exercised object byte-count binding: PASS; evidence byte counts exactly equal manifest byte counts.
- Proposed workflow SHA-256: 76baea48e276472e3b6ee4e93c77c110e0575261d52f14694b8e4e2a36aa0830
- Proposed base_gate SHA-256: f359b8c1c23491f05c722fe8553369bc97246169ec9875a4619fe2d99f21ff11
- Proposed checker SHA-256: e3be85d4c8d64ea8f24f74b3033dac5d127635a5aba3398220f36c0cab0bd283
- Proposed policy SHA-256: d68240ee3b13bd5f10ccce10dfd2da9af038495d9a7adeb6fe411ab5622b8a1b
- Proposed runner SHA-256: d08fe9bd6188508ae9fc181a6806ce7835a16ab48ce749b1de283655dce2b32f
- Proposed GOOD fixture SHA-256: 1c86e6843ad8ab5e07d2fac2575f53bfdbaa695646dde5211c68cda732b45827
- Proposed BAD fixture SHA-256: b9989b0e62c55b54528a87f26f835a137f52b2e5d76f6bf0608482351a50d3ce
- Prototype: `.gitattributes` D by basename at any depth.
- Prototype: `.gitmodules` D by basename at any depth.
- Prototype: symlink mode 120000 D.
- Prototype: gitlink mode 160000 D.
- Prototype: Git type-change D.
- Prototype: executable-mode change C.
- Prototype: new executable C.
- Prototype: `unknown_normal=C`.
- Prototype: regular `src/` content B.
- Prototype: regular `tests/` content B.
- R2AA-022: CORRECTION_SCRATCH_PASS; BLOCKING_UNTIL_EXACT_CANDIDATE_INDEPENDENT_REVIEW.
- R2AA-022 nested CRLF: mechanism remains reproducible after forced bypass; ordinary B entry is blocked by basename D.
- R2AA-023: CORRECTION_SCRATCH_PASS; PENDING_EXACT_CANDIDATE_REVIEW.
- R2AA-024: CORRECTION_SCRATCH_PASS; PENDING_EXACT_CANDIDATE_REVIEW.
- R2AA-016: BLOCKING.
- R2AA-017: PARTIAL; exact-object binding preserved; freeze-before-probes is procedural, not a cryptographic guarantee.
- R2AA-018: PARTIAL; `unknown_normal=C` preserved.
- R2AA-025: OPEN.
- R2AA-011 correction preserved in scratch; historical disposition remains PARTIAL.
- R2AA-014 strict BASE/HEAD binding preserved in scratch; historical disposition remains RESOLVED.
- Temporary human gate proposal: `required_approving_review_count=1`, status `PROPOSAL_ONLY_NOT_CONFIGURED`, while DC-006 remains OPEN.
- R2AA-012: OPEN.
- R2AA-013: PARTIAL.
- R2AA-015: OPEN.
- R2AA-019: OPEN.
- R2AA-020: OPEN.
- R2AA-021: OPEN.
- DC-006: OPEN.
- EXP-01: OPEN.
- IR2-002: BLOCKING_BEFORE_FIRST_FUNCTIONAL_TASK.
- MINOR-5: ACTIVE_R2-4_NOT_EXECUTED.
- Historical R2-3 independence gap: UNCHANGED.
- False greens: 6; new increment from this scratch: 0.
- Next exact candidate procedure: prepare/freeze exact candidate bytes; generate manifest; run materialization/authority probes on those same bytes; bind evidence to manifest; submit exact bundle to independent review before implementation.
- This evidence grants no implementation, merge, protection, required-check, ruleset or GitHub-settings authority.
- 2026-08-15T19:52:49Z: human-authorized canonicalization only; no control-plane implementation in this commit.

- 2026-08-15T20:41:13Z: Materialization V2 independent review PASS; evidence evidence/r2-4/materialization_v2_frozen_candidate_independent_review_05.json SHA-256 05e349ba35d0d630ebaddd34bdc3f30f89a8b5f482e327e43f7aca6de4084e1b; C5 57/57 PASS; candidate PASS, bootstrap BLOCKED; R2AA-022/023 RESOLVED, R2AA-024 PARTIAL, R2AA-026 LOW NONBLOCKING; false greens remain 6; implementation/merge/settings authority remain false.

## Revisión independiente PASS del candidato Materialization V2
- Evidence: evidence/r2-4/materialization_v2_frozen_candidate_independent_review_05.json
- Evidence SHA-256: 05e349ba35d0d630ebaddd34bdc3f30f89a8b5f482e327e43f7aca6de4084e1b
- Evidence bytes: 38814
- review_protocol: r2-independent-materialization-v2-frozen-candidate-v1.
- Reviewed bundle SHA-256: 749705e7a8ecbadfbcbd435f18eebf470a49a0fa43f65f9b87fc7752852c5002
- Reviewed manifest SHA-256: e6828ee2b95f6953ac4cc86c730a47fd918bd40be352fb2fd60a3c1a6a72874e
- independence_satisfied: PASS.
- static_review: PASS.
- dynamic_review: PASS.
- candidate_disposition: PASS.
- bootstrap_disposition: BLOCKED.
- C5 checks: 57 PASS / 0 FAIL / 0 UNCERTAIN / 0 NOT_EXECUTED.
- Exact PASS bytes:
  - workflow: 76baea48e276472e3b6ee4e93c77c110e0575261d52f14694b8e4e2a36aa0830
  - base_gate: f359b8c1c23491f05c722fe8553369bc97246169ec9875a4619fe2d99f21ff11
  - checker: e3be85d4c8d64ea8f24f74b3033dac5d127635a5aba3398220f36c0cab0bd283
  - policy: d68240ee3b13bd5f10ccce10dfd2da9af038495d9a7adeb6fe411ab5622b8a1b
  - runner: d08fe9bd6188508ae9fc181a6806ce7835a16ab48ce749b1de283655dce2b32f
  - GOOD fixture: 1c86e6843ad8ab5e07d2fac2575f53bfdbaa695646dde5211c68cda732b45827
  - BAD fixture: b9989b0e62c55b54528a87f26f835a137f52b2e5d76f6bf0608482351a50d3ce
- R2AA-011: PARTIAL.
- R2AA-012: OPEN.
- R2AA-013: PARTIAL.
- R2AA-014: RESOLVED.
- R2AA-015: OPEN.
- R2AA-016: PARTIAL.
- R2AA-017: PARTIAL.
- R2AA-018: PARTIAL.
- R2AA-019: OPEN.
- R2AA-020: OPEN.
- R2AA-021: OPEN.
- R2AA-022: RESOLVED.
- R2AA-023: RESOLVED.
- R2AA-024: PARTIAL.
- R2AA-025: OPEN.
- R2AA-026 LOW NONBLOCKING - NON_UTF8_CHECKER_OUTPUT_CAPTURE: `base_gate.py` can raise UnicodeDecodeError on checker stdout for a Git path containing non-UTF-8 bytes because capture uses `text=True`; failure remains non-zero/fail-closed, emits no PASS, is not a false green and does not block these exact candidate bytes.
- OBS-01 LOW: basename_rule > exact_path > prefix_rule is safe for these exact bytes because both current basename rules are D; future lower-floor basename rules would need an invariant before use.
- OBS-02 LOW: basename containment is evidenced on the case-sensitive/non-normalizing Linux environment used by `ubuntu-latest`; other filesystem semantics are outside this PASS.
- OBS-03 LOW: `required_approving_review_count=1` is ACCEPTABLE_TEMPORARY while DC-006 remains OPEN, but `dismiss_stale_reviews=false` plus `require_last_push_approval=false` must be reconsidered before any real configuration.
- Temporary human gate proposal: `required_approving_review_count=1`; status `PROPOSAL_ONLY_NOT_CONFIGURED`.
- One approval is not task-specific scope authorization; DC-006 remains OPEN.
- FALSE_GREENS: 6.
- NEW_FALSE_GREEN_INCREMENT: 0.
- DC-006: OPEN.
- EXP-01: OPEN.
- IR2-002: BLOCKING_BEFORE_FIRST_FUNCTIONAL_TASK.
- MINOR-5: ACTIVE_R2-4_NOT_EXECUTED.
- Historical R2-3 independence gap: UNCHANGED.
- IMPLEMENTATION_AUTHORIZED: False.
- MERGE_AUTHORIZED: False.
- GITHUB_SETTINGS_MUTATION_AUTHORIZED: False.
- Bootstrap remains BLOCKED; candidate PASS is evidence over the exact seven bytes above only.
- Next gate: separate Human Gate D authorization to implement exactly the independently reviewed bytes, without byte changes and without merge/settings actions.
- 2026-08-15T20:41:13Z: human-authorized canonicalization only; no candidate implementation in this commit.

- 2026-08-15T21:04:56Z: exact Materialization V2 implementation PASS recorded; evidence evidence/r2-4/materialization_v2_exact_implementation_06.json SHA-256 8bc03c50e0fbdc5abb6b70380f2b5f66bfab94e2c1304601caa9acc73b2386ba; stage1 416c45c34cec2fcd6f959d60bffe2491d895be71; stage2/implementation anchor b9abfe0d9e80f41c9a9699e5e59827a82ffe4f82; all four PRE/POST D PASS; exact seven-object hashes PASS; no merge/settings/phase change; workflow-run count for implementation anchor observed 0; false greens remain 6. Bootstrap merge gate remains pending and must account for the post-implementation administrative tail before any merge.

## Implementación exacta Materialization V2
- Evidence: evidence/r2-4/materialization_v2_exact_implementation_06.json
- Evidence SHA-256: 8bc03c50e0fbdc5abb6b70380f2b5f66bfab94e2c1304601caa9acc73b2386ba
- Evidence bytes: 12417
- IMPLEMENTATION_DISPOSITION: PASS.
- Initial implementation HEAD: 412080f46d60b6ce7c85e27f476b3f1a4cf96858
- Stage 1 commit: 416c45c34cec2fcd6f959d60bffe2491d895be71
- Stage 2 / exact implementation anchor: b9abfe0d9e80f41c9a9699e5e59827a82ffe4f82
- Stage 1 PRE D: PASS.
- Stage 1 POST D: PASS.
- Stage 2 PRE D: PASS.
- Stage 2 POST D: PASS.
- Stage 1 installed exclusively:
  - `policy/risk_floors.json` = d68240ee3b13bd5f10ccce10dfd2da9af038495d9a7adeb6fe411ab5622b8a1b
  - `scripts/risk_floor.py` = e3be85d4c8d64ea8f24f74b3033dac5d127635a5aba3398220f36c0cab0bd283
- Stage 2 installed exclusively:
  - `scripts/base_gate.py` = f359b8c1c23491f05c722fe8553369bc97246169ec9875a4619fe2d99f21ff11
  - `.github/workflows/r2-ci.yml` = 76baea48e276472e3b6ee4e93c77c110e0575261d52f14694b8e4e2a36aa0830
- Exact seven-object state at implementation anchor:
  - workflow = 76baea48e276472e3b6ee4e93c77c110e0575261d52f14694b8e4e2a36aa0830
  - base_gate = f359b8c1c23491f05c722fe8553369bc97246169ec9875a4619fe2d99f21ff11
  - checker = e3be85d4c8d64ea8f24f74b3033dac5d127635a5aba3398220f36c0cab0bd283
  - policy = d68240ee3b13bd5f10ccce10dfd2da9af038495d9a7adeb6fe411ab5622b8a1b
  - runner = d08fe9bd6188508ae9fc181a6806ce7835a16ab48ce749b1de283655dce2b32f
  - GOOD fixture = 1c86e6843ad8ab5e07d2fac2575f53bfdbaa695646dde5211c68cda732b45827
  - BAD fixture = b9989b0e62c55b54528a87f26f835a137f52b2e5d76f6bf0608482351a50d3ce
- PR #1 observed OPEN and unmerged at implementation anchor.
- `main` remained 72a9c0c1995b3d56aa2711c3dccb448fbe8ecfb7.
- R2_STATE_MODIFIED_BY_IMPLEMENTATION: False.
- RUNNER_MODIFIED: False.
- FIXTURES_MODIFIED: False.
- MERGE_PERFORMED: False.
- BRANCH_PROTECTION_CHANGED: False.
- REQUIRED_CHECK_CONFIGURED: False.
- RULESET_CREATED: False.
- GITHUB_SETTINGS_CHANGED: False.
- PHASE_CHANGED: False.
- No workflow run was observed for exact implementation HEAD `b9abfe0d9e80f41c9a9699e5e59827a82ffe4f82` at canonicalization preflight; this is NOT a false green and is NOT evidence of enforcement.
- Current phase remains R2-4.
- FALSE_GREENS: 6.
- R2AA-011: PARTIAL.
- R2AA-012: OPEN.
- R2AA-013: PARTIAL.
- R2AA-014: RESOLVED.
- R2AA-015: OPEN.
- R2AA-016: PARTIAL.
- R2AA-017: PARTIAL.
- R2AA-018: PARTIAL.
- R2AA-019: OPEN.
- R2AA-020: OPEN.
- R2AA-021: OPEN.
- R2AA-022: RESOLVED.
- R2AA-023: RESOLVED.
- R2AA-024: PARTIAL.
- R2AA-025: OPEN.
- R2AA-026: LOW_NONBLOCKING.
- OBS-01/OBS-02/OBS-03: not corrected in this implementation.
- DC-006: OPEN.
- EXP-01: OPEN.
- IR2-002: BLOCKING_BEFORE_FIRST_FUNCTIONAL_TASK.
- MINOR-5: ACTIVE_R2-4_NOT_EXECUTED.
- Bootstrap merge gate exact-object rule: `72a9c0c1995b3d56aa2711c3dccb448fbe8ecfb7` -> `b9abfe0d9e80f41c9a9699e5e59827a82ffe4f82` is the implementation diff anchor. Because this canonicalization adds an administrative commit after that anchor, any later merge gate must also inventory `b9abfe0d9e80f41c9a9699e5e59827a82ffe4f82` -> actual PR HEAD and finally prove the complete `72a9c0c1995b3d56aa2711c3dccb448fbe8ecfb7` -> actual PR HEAD diff before merge.
- No merge/settings authority is granted by this record.
- 2026-08-15T21:04:56Z: human-authorized canonicalization only.

## Blockers
- R2-4 exact BASE-anchored candidate review round 2: EXECUTED_BLOCKED; independence_satisfied=PASS; candidate_disposition=BLOCKED; bootstrap_disposition=BLOCKED.
- R2AA-011 PARTIAL: captura temporal de BASE y `assume-unchanged` preservados en la falsificación scratch de materialización; sin reetiquetar evidencia histórica.
- R2AA-016 PARTIAL: su causa bloqueante R2AA-022 quedó resuelta para los bytes exactos revisados; permanecen dependencias fuera de este bundle como R2AA-012/DC-006/IR2-002.
- R2AA-017 PARTIAL: ligadura de bytes exactos verificada; freeze-before-probes permanece correctamente como garantía procedural, no criptográfica.
- R2AA-012 OPEN NONBLOCKING: binding real de `pull_request_target` al SHA del PR requiere prueba GitHub real antes de required-check configuration.
- R2AA-013 PARTIAL NONBLOCKING: `default_branch=main` observado; distinción temporal workflow-source SHA vs PR_BASE_SHA permanece abierta.
- R2AA-014 RESOLVED: binding BASE/HEAD estricto preservado en la falsificación scratch de materialización; sin reetiquetar evidencia histórica.
- R2AA-015 OPEN NONBLOCKING: deuda de liveness/fail-closed permanece explícita.
- R2AA-018 PARTIAL: `unknown_normal=C` y contención Git-mode-aware en `src/`/`tests/` verificadas; queda deuda estructural de precedencia basename-first (OBS-01).
- R2AA-019 OPEN LOW NONBLOCKING: `WORKFLOW_SOURCE_SHA` se captura pero no se compara directamente con PR_BASE_SHA.
- R2AA-020 OPEN LOW NONBLOCKING: aislamiento de módulos depende de versión Python no pinneada.
- R2AA-021 OPEN LOW NONBLOCKING: asserts contra tips de refs mantienen deuda de liveness fail-closed.
- R2AA-022 RESOLVED: `.gitattributes` por basename a cualquier profundidad quedó independientemente contenido en D para los bytes exactos revisados.
- R2AA-023 RESOLVED: symlink 120000, type-change y semántica Git-mode asociada quedaron independientemente contenidas para los bytes exactos revisados.
- R2AA-024 PARTIAL: parser raw-diff sólido, pero NEW-01 muestra que la captura text=True de `base_gate.py` no es byte-safe de extremo a extremo.
- R2AA-025 OPEN LOW NONBLOCKING: diagnóstico checker/liveness sigue enmascarado y no fue corregido.
- R2AA-026 OPEN LOW NONBLOCKING - NON_UTF8_CHECKER_OUTPUT_CAPTURE: un path con bytes no UTF-8 puede provocar UnicodeDecodeError en `base_gate.py` al capturar stdout del checker con text=True; es fail-closed, no produce PASS, no es falso verde y no bloquea el candidato aprobado.
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
