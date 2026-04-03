# 🧠 AI Agent Planner (From Scratch)

Agente IA construido desde cero con arquitectura agentic moderna:

- ✔ Planner (razonamiento estructurado)
- ✔ Tool Calling
- ✔ Evaluación (metacognición)
- ✔ Adaptive Planning (retry + replan)
- ✔ Observabilidad
- ✔ Integración con APIs reales (OpenWeather)

---

## 🚀 Capacidades

El agente es capaz de:

- Interpretar intención del usuario
- Generar planes dinámicos
- Ejecutar tools externas
- Evaluar resultados (quality, completeness, success_rate)
- Adaptarse automáticamente ante fallos
- Evitar alucinaciones (no inventa datos)

---

## 🧠 Arquitectura

User
↓
Input Processor
↓
Planner
↓
Execute Plan → Tools (API / Local)
↓
Evaluate (metacognition)
↓
Adaptive Planning (retry / replan)
↓
Response


---

Configuración

Crear archivo .env:

OPENWEATHER_API_KEY=tu_api_key

⚠️ Este archivo NO se incluye por seguridad.

▶️ Uso
python main.py

Ejemplos:

dame destinos en europa y clima
dame destinos en asia
dame destinos en europa con info
📊 Observabilidad

El agente registra:

tool_calls
tool_errors
success_rate
completeness
quality
latency

Ejemplo:

[OBSERVABILITY] {
  'goal': 'multi_destination_weather',
  'tool_calls': 4,
  'quality': 'good'
}
🔁 Adaptive Planning

El agente puede:

Reintentar ejecución si falla
Simplificar el plan si no hay datos suficientes
Ajustar la respuesta dinámicamente
🧪 Filosofía del sistema

Prefiere fallar de forma conservadora
antes que acertar por casualidad.

⚠️ Limitaciones actuales
NLP limitado (no todos los sinónimos)
No hay A2A (multi-agente)
MCP parcial (tools locales + APIs directas)
🚀 Roadmap
 Tool Registry dinámico (MCP real)
 Integración de múltiples APIs (fallback real)
 Multi-agent system (A2A)
 Evaluación offline automatizada
 Exposición como API (NLWeb)
📌 Estado del proyecto

✔ Arquitectura sólida
✔ Adaptive Planning implementado
✔ Integración con datos reales
✔ Listo para evolución a sistema multi-agente

👨‍Autor 
OZA

Proyecto desarrollado como parte de formación en arquitectura de agentes IA.







