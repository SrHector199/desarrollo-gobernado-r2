# Feature Brief - Repartidor exacto de gastos

## Estado
- Brief: ACCEPTED_FIRST_DRAFT
- Demo funcional: NOT_EXECUTED

## Problema
Al dividir un importe entre varias personas, el redondeo puede perder o añadir céntimos.

## Usuario
Personas que necesitan repartir una cuenta o gasto compartido.

## Resultado
Introducir un importe y un número de personas y obtener cantidades individuales cuya suma sea exactamente igual al importe original.

## No objetivo
Interfaz gráfica, cuentas de usuario, almacenamiento, red, impuestos, conversión de monedas o pagos reales.

## Demo de aceptación
Repartir `10,00 EUR` entre `3` personas debe producir `3,34 EUR`, `3,33 EUR` y `3,33 EUR`; la suma mostrada debe ser exactamente `10,00 EUR`.

Una cantidad inválida o cero personas debe rechazarse claramente.
