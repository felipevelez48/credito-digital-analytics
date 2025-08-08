## Título

**Medición del impacto de migrar el envío de estados de cuenta de físico a e‑mail.**

## Contexto

El envío físico cuesta ~50 MM/mes. Se propone e‑mail; el área de cartera teme una caída en la recuperación.

## Hipótesis

- H0: La tasa de pago puntual (a 30 días) es igual en físico y e‑mail.

- H1: La tasa de pago puntual cambia en e‑mail (preocupación: disminuye).

## Diseño experimental

- **Asignación:** A/B aleatoria 50/50, estratificada por segmento relevante (riesgo, antigüedad, zona, edad).

- **Periodo:** al menos N semanas/meses según tamaño de muestra.

- **Tamaño de muestra:** potencia 0.8, α=0.05, detectar Δ mínimo de 2 pp (se calcula con proporciones).

## Métricas

- **Primaria:** % pago puntual a 30 días.

- **Secundarias:** días de mora promedio, % pagos totales a 60/90 días, % reclamos por no recepción.

- **Salud del experimento:** tasa de apertura del e‑mail (si procede), bounce, entregabilidad.

## Análisis

- **ITT** (intention‑to‑treat): todos los asignados cuentan en su grupo.

- Prueba de proporciones para la métrica primaria; intervalos de confianza.

- Corte semanal con gráficos de tendencia.

- Segmentación: estimar heterogeneidad de efectos (A/B por clusters o covariables).

## Gobernanza y riesgos

- Comunicación previa al cliente + opción de preferencia de canal.

- Opt‑out sencillo, almacenamiento de consentimientos.

- Monitoreo de quejas/bounces; rollback si hay efecto severo.

## Entrega

- Informe con resultados + recomendación (mantener, revertir, o rollout gradual con holdout permanente para vigilancia).

