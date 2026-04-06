# AI Agent Planner (From Scratch)

Agente IA construido desde cero con arquitectura agentic moderna:

- ✔ Planner (razonamiento estructurado)
- ✔ Tool Calling
- ✔ Evaluación (metacognición)
- ✔ Adaptive Planning (retry + replan)
- ✔ Observabilidad
- ✔ Integración con APIs reales (OpenWeather)

---

## Capacidades

El agente es capaz de:

- Interpretar intención del usuario
- Generar planes dinámicos
- Ejecutar tools externas
- Evaluar resultados (quality, completeness, success_rate)
- Adaptarse automáticamente ante fallos
- Evitar alucinaciones (no inventa datos)

---

## Arquitectura

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

Este archivo NO se incluye por seguridad.

Uso
python main.py

Ejemplos:

dame destinos en europa y clima
dame destinos en asia
dame destinos en europa con info
Observabilidad

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
Adaptive Planning

El agente puede:

Reintentar ejecución si falla
Simplificar el plan si no hay datos suficientes
Ajustar la respuesta dinámicamente
Filosofía del sistema

Prefiere fallar de forma conservadora
antes que acertar por casualidad.

Limitaciones actuales
NLP limitado (no todos los sinónimos)
No hay A2A (multi-agente)
MCP parcial (tools locales + APIs directas)
Roadmap
 Tool Registry dinámico (MCP real)
 Integración de múltiples APIs (fallback real)
 Multi-agent system (A2A)
 Evaluación offline automatizada
 Exposición como API (NLWeb)
Estado del proyecto

✔ Arquitectura sólida
✔ Adaptive Planning implementado
✔ Integración con datos reales
✔ Listo para evolución a sistema multi-agente



Recent Improvements: Multi-Source Intelligence Layer

This phase focused on evolving the agent from a rule-based system into a multi-source, production-oriented architecture, integrating real-world APIs, structured data handling, and resilience mechanisms.

External API Integrations

The agent now retrieves real-time data from external providers:

Weather: Integrated with OpenWeather API for live climate data
Destinations: Hybrid approach using local data + external API fallback
Information: Integrated Wikipedia API for contextual knowledge

This allows the system to move beyond static responses and operate with dynamic, real-world data.

Data Model Evolution

The system transitioned from simple string-based entities to structured data:

{
  "name": "France",
  "city": "Paris"
}

This change enables:

Consistent interaction between tools
Better compatibility across APIs
Elimination of semantic mismatches (e.g., country vs city issues)
Planner Enhancements

The planner was upgraded to:

Handle structured inputs (dict-based entities)
Normalize outputs from different tools
Prevent data inconsistencies (e.g., avoiding unhashable types)
Support multi-step execution with map operations
Caching Layer

A caching mechanism was introduced to:

Reduce redundant API calls
Improve latency
Increase system stability

Cache is currently in-memory and designed to be easily replaceable (e.g., Redis).

Error Handling & Resilience

The system now includes:

Structured error responses across all tools
Retry logic for transient failures
Adaptive planning (fallback execution when failures occur)
Graceful degradation (partial results instead of total failure)
Observability

Execution metrics are tracked for each request:

tool_calls
tool_errors
success_rate
completeness
latency

This enables debugging, performance monitoring, and future optimization.

Multi-Source Architecture

The agent now follows a layered data strategy:

LOCAL → CACHE → API → FALLBACK

This design ensures:

Speed (local/cache)
Coverage (external APIs)
Reliability (fallback mechanisms)
Current Capabilities

The agent can now:

Retrieve destinations by region
Fetch real-time weather data
Provide contextual information about destinations
Handle partial failures without breaking execution
Combine multiple data sources into a single coherent response
Known Limitations
Entity ambiguity (e.g., "Paris" may refer to non-city entities)
No ranking or prioritization of destinations yet
Limited city coverage (no global city database yet)
Next Steps
Destination ranking and relevance filtering
Entity disambiguation (city vs other meanings)
Integration of a global cities database
Persistent storage (PostgreSQL / vector DB)
Multi-agent orchestration (A2A)

Si quieres, en el siguiente paso te ayudo a:

convertir ese README en uno nivel portafolio / empleo real (impacto + arquitectura + diagramas)

este es el readme actual complementa
# AI Agent Planner (From Scratch)

Agente IA construido desde cero con arquitectura agentic moderna:




‍Autor 
OZA

Proyecto desarrollado como parte de formación en arquitectura de agentes IA.







