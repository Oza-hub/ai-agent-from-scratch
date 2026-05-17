# AI Agent From Scratch

A modular AI Agent architecture built from scratch focused on:

- Planning
- Tool orchestration
- Context engineering
- Structured memory
- Reliability
- Multi-source data integration

This project is not a simple chatbot wrapper around an LLM.

It is an evolving agentic system designed to progressively implement real-world AI agent engineering concepts through incremental architectural development and practical experimentation.

---

# Project Philosophy

The objective of this project is to learn and implement modern AI agent engineering concepts by building the architecture manually instead of relying entirely on external frameworks.

The system evolves following a structured learning roadmap focused on:

- Agent architecture
- Planning systems
- Tool usage patterns
- Context engineering
- Agent memory
- Reliability
- Observability
- Metacognition
- RAG systems
- Multi-agent orchestration

The implementation prioritizes:

- Architectural clarity
- Controlled complexity
- Modular design
- Explicit reasoning pipelines
- Reliability over shortcuts

---

# Current Development Phase

## Phase 1 — Architectural Consolidation

The project is currently focused on consolidating the core architecture of the agent before moving into advanced capabilities such as:

- RAG
- Multi-agent systems
- Metacognition
- Autonomous workflows
- Production orchestration

The current phase prioritizes:

- Structured entities
- Context consistency
- Canonical identity management
- Memory foundations
- Reliable orchestration
- Modular pipelines

---

# Current Capabilities

## Planning System

The agent can:

- Detect user intent
- Generate execution plans
- Execute multi-step workflows
- Coordinate tool calls
- Handle chained operations
- Execute map-style tool orchestration

Examples:

- Get destinations by region
- Retrieve weather for multiple destinations
- Retrieve contextual destination information
- Combine multi-source outputs

---

## Tool Orchestration

The architecture includes a modular tool execution layer:

- Tool registry
- Tool validation
- Tool normalization
- Structured execution
- Error handling
- Execution metrics

Tools are isolated from the planner logic to maintain modularity.

---

## Multi-Source Data Integration

The agent integrates multiple data sources:

### Local Sources

- Local destination database
- Local fallback data

### External APIs

#### OpenWeather API

Used for:

- Real-time weather
- Temperature
- Weather conditions

#### Wikipedia API

Used for:

- Destination descriptions
- Contextual information
- Knowledge enrichment

#### REST Countries API

Used for:

- Region-based destination discovery
- Country and capital extraction
- External fallback sourcing

---

# Structured Context Architecture

One of the major architectural evolutions of the project is the migration from primitive string-based context handling into structured entity management.

---

## Previous Architecture

Previously the system handled destinations as simple strings:

```python
["Paris", "Berlin"]
```

This approach caused:

- Context inconsistency
- Identity ambiguity
- Fragile memory handling
- Difficult ranking and orchestration
- Poor extensibility

---

## Current Architecture

The agent now uses canonical structured entities:

```python
{
    "id": "paris",
    "name": "Paris",
    "city": "Paris"
}
```

This architectural change enables:

- Canonical identity management
- Context consistency
- Reliable memory references
- Future semantic retrieval
- Safer orchestration pipelines
- Structured ranking systems

---

# Context Engineering

The current phase of the project heavily focuses on context engineering principles.

The system now includes:

- Canonical entity normalization
- Structured context propagation
- Context-aware execution
- Controlled context enrichment
- Memory-context coordination

The architecture progressively transitions from:

```text
tool output passing
```

toward:

```text
identity-aware contextual reasoning
```

---

# Entity Normalization System

The project now includes a dedicated normalization layer.

File:

```text
core/normalizer.py
```

Responsibilities:

- Canonical destination normalization
- Alias resolution
- Region normalization
- Structured entity creation
- Canonical ID generation

Examples:

| Input | Canonical Output |
|---|---|
| Tokio | Tokyo |
| París | Paris |
| Rio | Rio de Janeiro |

This layer is foundational for future memory and retrieval systems.

---

# Agent Memory System

The project already contains the foundation of agent memory management.

Current memory components:

## Conversation History

Tracks:

- User messages
- Agent responses

---

## Active Context

Stores:

- Current goal
- Recent entities
- Context continuity

Enables conversational continuity such as:

```text
User: dame el clima de tokio
User: y el de paris
```

---

## Entity Memory

Stores structured entities for future retrieval and contextual reasoning.

---

## Result Memory

Stores:

- Weather results
- Destination information
- Previous execution outputs

---

# Reliability Architecture

The project emphasizes reliable agent execution.

Current reliability features include:

---

## Validation Layers

- Tool validation
- Argument validation
- Plan validation
- Suspicious input detection

---

## Error Handling

Structured error architecture:

```python
{
    "status": "error",
    "error": {
        "type": "...",
        "message": "...",
        "retryable": True
    }
}
```

---

## Fallback Systems

The architecture supports:

- Local-first execution
- API fallback execution
- Controlled retries

---

## Cache Layer

File:

```text
core/cache.py
```

Supports:

- API response caching
- Reduced redundant calls
- Faster repeated requests

---

## Observability

The system tracks:

- Tool calls
- Tool failures
- Success rate
- Completeness
- Latency
- Execution quality

Example:

```python
{
    "goal": "multi_destination_weather",
    "tool_calls": 4,
    "success_rate": 1.0,
    "quality": "good",
    "latency_sec": 1.955
}
```

---

# Adaptive Planning

The planner supports adaptive execution patterns.

Capabilities include:

- Dynamic plan generation
- Multi-step workflows
- Conditional orchestration
- Map-style execution
- Context reuse

The system progressively moves toward more advanced planning and metacognitive behaviors.

---

# Project Structure

```text
ai-agent-from-scratch/
│
├── agent/
│   ├── agent.py
│   ├── planner.py
│   ├── evaluator.py
│   ├── plan_validator.py
│   ├── tool_executor.py
│   ├── tool_registry.py
│   └── tool_validator.py
│
├── core/
│   ├── cache.py
│   ├── context_manager.py
│   ├── entity_resolver.py
│   ├── normalizer.py
│   ├── ranker.py
│   └── state.py
│
├── services/
│   ├── destinations_service.py
│   └── ...
│
├── tools/
│   ├── weather.py
│   ├── destinations.py
│   ├── destination_info.py
│   ├── info_api.py
│   └── ...
│
├── data/
│   ├── destinations_db.py
│   └── weather_db.py
│
├── logs/
│
├── .env
├── .gitignore
├── main.py
└── README.md
```

---

# Current Architectural State

The project has evolved from:

```text
simple tool-based assistant
```

into:

```text
modular context-aware AI agent architecture
```

The system now includes:

- Structured entities
- Canonical identities
- Context consistency
- Multi-source orchestration
- Memory foundations
- Reliability layers
- Observability
- Modular planning

---

# Technologies Used

- Python
- OpenAI-compatible APIs
- OpenWeather API
- Wikipedia REST API
- REST Countries API
- Flask (support experiments)
- Requests
- dotenv

---

# Running The Project

## Clone Repository

```bash
git clone <repository_url>
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

---

## Activate Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create `.env`

```env
GH_TOKEN=your_token
GH_MODEL=openai/gpt-4.1-mini
GH_ENDPOINT=https://models.github.ai/inference

OPENWEATHER_API_KEY=your_key
```

---

## Run

```bash
python main.py
```

---

# Example Usage

```text
User: dame destinos en europa y clima
```

Output:

```text
Destinos disponibles:
- Paris
- Barcelona
- Berlin

Clima por destino:
Paris: cielo claro, 20°C
Barcelona: muy nuboso, 15°C
Berlin: cielo claro, 13°C
```

---

# Architectural Roadmap

## Phase 1 — Context Consolidation
- Structured entities
- Canonical identity
- Context consistency
- Reliability improvements

---

## Phase 2 — Memory Architecture
- Episodic memory
- Semantic memory
- Retrieval systems
- Context prioritization

---

## Phase 3 — Metacognition
- Reflection
- Replanning
- Confidence scoring
- Adaptive reasoning

---

## Phase 4 — RAG Integration
- Vector storage
- Semantic retrieval
- Long-term grounding
- Knowledge augmentation

---

## Phase 5 — Multi-Agent Systems
- Specialized agents
- Agent coordination
- Delegation
- Cooperative execution

---

# Educational Objective

This project exists primarily as a practical learning platform for modern AI agent engineering.

The goal is not only to build a functional assistant, but to deeply understand:

- How agents reason
- How planning systems operate
- How context is maintained
- How memory architectures evolve
- How reliable orchestration is built

The architecture intentionally evolves incrementally to expose real-world engineering challenges and solutions.

---

# Current Status

## Stable Features

- Planner
- Tool orchestration
- Weather integration
- Destination information
- Structured entities
- Canonical normalization
- Observability
- Context-aware execution

---

## In Progress

- Context manager migration
- Full structured memory integration
- Ranking system migration
- Advanced memory architecture

---

# License

Educational and experimental project.