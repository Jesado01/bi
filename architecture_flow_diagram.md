# Diagrama de Flujo del Sistema BIAN - Análisis y Generación de Requisitos

## Flujo Principal del Sistema

```mermaid
graph LR
    %% === INPUTS (Blue) ===
    subgraph INPUTS["📥 ENTRADAS"]
        EP[Endpoints Directory<br/>Archivos .md]
        BIAN[BIAN Directory<br/>OpenAPI Spec JSON]
        ARCH[Templates de<br/>Arquitectura<br/>opcional]
    end

    %% === CENTRAL ORCHESTRATOR (Green) ===
    ORCHESTRATOR[🎯 ModularAgentFramework<br/>Orquestador Central]

    %% === PROCESSING MODULES (Orange) ===
    subgraph MODULES["🔧 MÓDULOS DE PROCESAMIENTO"]
        M1[Detección de<br/>Framework & Lenguaje]
        M2[Generación de<br/>Requisitos]
        M3[Actualización de<br/>Estructura de Proyecto]
    end

    %% === INFRASTRUCTURE SERVICES (Gray) ===
    subgraph SERVICES["⚙️ SERVICIOS DE INFRAESTRUCTURA"]
        LLM[Anthropic LLM Client<br/>Claude Sonnet 4]
        FS[FileSystem Reader<br/>Sistema de Archivos]
    end

    %% === INTERMEDIATE STATE (Purple) ===
    STATE[📊 CoreBianState<br/>Estado Compartido]

    %% === OUTPUTS PER MODULE (Pink/Magenta) ===
    subgraph OUTPUTS["📤 SALIDAS POR MÓDULO"]
        O1[Módulo 1<br/>target_language<br/>target_framework]
        O2[Módulo 2<br/>generated_requirements<br/>Requisitos Completos]
        O3[Módulo 3<br/>updated_requirements<br/>Con Estructura de Proyecto]
    end

    %% === FINAL OUTPUT (Green) ===
    FINAL[✅ Requisitos Finales<br/>Listos para Generación<br/>de Código]

    %% === CONNECTIONS ===
    EP --> ORCHESTRATOR
    BIAN --> ORCHESTRATOR
    ARCH -.->|opcional| ORCHESTRATOR

    ORCHESTRATOR --> M1
    ORCHESTRATOR --> M2
    ORCHESTRATOR --> M3

    M1 --> STATE
    M2 --> STATE
    M3 --> STATE

    STATE --> O1
    STATE --> O2
    STATE --> O3

    M1 --> LLM
    M2 --> LLM
    M3 --> LLM

    M1 --> FS
    M2 --> FS
    M3 --> FS

    LLM -.-> SERVICES
    FS -.-> SERVICES

    O1 --> FINAL
    O2 --> FINAL
    O3 --> FINAL

    %% === STYLING ===
    classDef inputStyle fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    classDef orchestratorStyle fill:#7CB342,stroke:#558B2F,stroke-width:4px,color:#fff
    classDef moduleStyle fill:#FF9800,stroke:#E65100,stroke-width:3px,color:#fff
    classDef serviceStyle fill:#607D8B,stroke:#37474F,stroke-width:2px,color:#fff
    classDef stateStyle fill:#9C27B0,stroke:#6A1B9A,stroke-width:3px,color:#fff
    classDef outputStyle fill:#E91E63,stroke:#880E4F,stroke-width:3px,color:#fff
    classDef finalStyle fill:#4CAF50,stroke:#2E7D32,stroke-width:4px,color:#fff

    class EP,BIAN,ARCH inputStyle
    class ORCHESTRATOR orchestratorStyle
    class M1,M2,M3 moduleStyle
    class LLM,FS serviceStyle
    class STATE stateStyle
    class O1,O2,O3 outputStyle
    class FINAL finalStyle
```

## Flujo Detallado con Secuencia de Ejecución

```mermaid
graph TD
    %% === PHASE 1: INPUT ===
    START([🚀 INICIO<br/>Mensaje RabbitMQ])

    %% === INPUTS ===
    INPUT1[📄 Endpoints Directory<br/>tmp/endpoints/*.md]
    INPUT2[📋 BIAN Specification<br/>tmp/bian/*.json]
    INPUT3[📐 Architecture Templates<br/>tmp/architectures/]

    %% === ORCHESTRATOR ===
    ORCH[🎯 ModularAgentFramework<br/>setup_agent_framework]

    %% === MODULE 1 ===
    subgraph MODULE1["🔍 MÓDULO 1: Framework Detector"]
        M1_START[Inicio Módulo 1]
        M1_READ[Lee primer archivo<br/>de endpoints]
        M1_LLM[Consulta LLM:<br/>Detectar lenguaje y framework]
        M1_UPDATE[Actualiza State:<br/>target_language<br/>target_framework]
        M1_END[Fin Módulo 1]
    end

    %% === MODULE 2 ===
    subgraph MODULE2["📝 MÓDULO 2: Requirement Generator"]
        M2_START[Inicio Módulo 2]
        M2_READ1[Lee todos los<br/>archivos de endpoints]
        M2_READ2[Lee OpenAPI<br/>Specification]
        M2_LLM[Consulta LLM:<br/>Generar requisitos completos]
        M2_UPDATE[Actualiza State:<br/>generated_requirements]
        M2_END[Fin Módulo 2]
    end

    %% === MODULE 3 ===
    subgraph MODULE3["🏗️ MÓDULO 3: Project Structure"]
        M3_START[Inicio Módulo 3]
        M3_READ[Lee template de<br/>arquitectura]
        M3_LLM[Consulta LLM:<br/>Adaptar estructura al proyecto]
        M3_UPDATE[Actualiza State:<br/>updated_requirements]
        M3_END[Fin Módulo 3]
    end

    %% === SERVICES ===
    LLM[(🤖 Anthropic LLM<br/>Claude Sonnet 4)]
    FS[(📁 FileSystem<br/>Reader)]

    %% === STATE ===
    STATE[💾 CoreBianState<br/>Estado Compartido]

    %% === OUTPUTS ===
    OUT1[📊 Output 1:<br/>Java / Spring Boot<br/>detectado]
    OUT2[📊 Output 2:<br/>Requisitos de API<br/>generados]
    OUT3[📊 Output 3:<br/>Requisitos con<br/>estructura multimodule]

    %% === FINAL ===
    SAVE[💾 Guardar archivos:<br/>api_requirements.md<br/>updated_requirements.md]
    PUBLISH[📤 Publicar resultado<br/>a RabbitMQ]
    END([✅ FIN])

    %% === CONNECTIONS ===
    START --> INPUT1
    START --> INPUT2
    START --> INPUT3

    INPUT1 --> ORCH
    INPUT2 --> ORCH
    INPUT3 -.->|opcional| ORCH

    ORCH --> M1_START

    %% Module 1 Flow
    M1_START --> M1_READ
    M1_READ --> FS
    FS --> M1_LLM
    M1_LLM --> LLM
    LLM --> M1_UPDATE
    M1_UPDATE --> STATE
    STATE --> M1_END
    M1_END --> OUT1

    %% Module 2 Flow
    M1_END --> M2_START
    M2_START --> M2_READ1
    M2_READ1 --> FS
    M2_START --> M2_READ2
    M2_READ2 --> FS
    FS --> M2_LLM
    M2_LLM --> LLM
    LLM --> M2_UPDATE
    M2_UPDATE --> STATE
    STATE --> M2_END
    M2_END --> OUT2

    %% Module 3 Flow
    M2_END --> M3_START
    M3_START --> M3_READ
    M3_READ --> FS
    FS --> M3_LLM
    M3_LLM --> LLM
    LLM --> M3_UPDATE
    M3_UPDATE --> STATE
    STATE --> M3_END
    M3_END --> OUT3

    %% Final Flow
    OUT1 --> SAVE
    OUT2 --> SAVE
    OUT3 --> SAVE
    SAVE --> PUBLISH
    PUBLISH --> END

    %% === STYLING ===
    classDef startEnd fill:#4CAF50,stroke:#2E7D32,stroke-width:4px,color:#fff,font-weight:bold
    classDef input fill:#2196F3,stroke:#1565C0,stroke-width:3px,color:#fff
    classDef orchestrator fill:#8BC34A,stroke:#558B2F,stroke-width:3px,color:#fff
    classDef module1 fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef module2 fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef module3 fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef service fill:#607D8B,stroke:#37474F,stroke-width:2px,color:#fff
    classDef state fill:#9C27B0,stroke:#6A1B9A,stroke-width:3px,color:#fff
    classDef output fill:#E91E63,stroke:#880E4F,stroke-width:3px,color:#fff
    classDef final fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff

    class START,END startEnd
    class INPUT1,INPUT2,INPUT3 input
    class ORCH orchestrator
    class M1_START,M1_READ,M1_LLM,M1_UPDATE,M1_END module1
    class M2_START,M2_READ1,M2_READ2,M2_LLM,M2_UPDATE,M2_END module2
    class M3_START,M3_READ,M3_LLM,M3_UPDATE,M3_END module3
    class LLM,FS service
    class STATE state
    class OUT1,OUT2,OUT3 output
    class SAVE,PUBLISH final
```

## Diagrama Simplificado al Estilo del Original

```mermaid
graph LR
    %% === INPUTS ===
    A1[📄 Endpoints<br/>Directory]
    A2[📋 BIAN OpenAPI<br/>Specification]
    A3[📐 Architecture<br/>Templates<br/>opcional]

    %% === ORCHESTRATOR ===
    B[🎯 Agente<br/>Orquestador<br/>ModularAgentFramework]

    %% === PROCESSING ===
    C1[🔍 Detección de<br/>Framework]
    C2[📝 Generación de<br/>Requisitos]
    C3[🏗️ Estructura de<br/>Proyecto]

    %% === INFRASTRUCTURE ===
    D[⚙️ Servicios<br/>Anthropic LLM<br/>FileSystem]

    %% === INTERMEDIATE OUTPUT ===
    E[💾 Estado<br/>Procesado]

    %% === INDIVIDUAL OUTPUTS ===
    F1[📊 Detección<br/>Language & Framework]
    F2[📊 Requisitos<br/>API Completos]
    F3[📊 Requisitos<br/>con Estructura]

    %% === FINAL OUTPUT ===
    G[✅ Documentos<br/>Listos para<br/>Generador]

    %% === CONNECTIONS ===
    A1 --> B
    A2 --> B
    A3 -.->|opcional| B

    B --> C1
    B --> C2
    B --> C3

    C1 --> D
    C2 --> D
    C3 --> D

    D -.-> B

    C1 --> E
    C2 --> E
    C3 --> E

    E --> F1
    E --> F2
    E --> F3

    F1 --> G
    F2 --> G
    F3 --> G

    %% === STYLING ===
    style A1 fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    style A2 fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    style A3 fill:#FFC107,stroke:#F57F17,stroke-width:3px,color:#000

    style B fill:#7CB342,stroke:#558B2F,stroke-width:4px,color:#fff

    style C1 fill:#FF9800,stroke:#E65100,stroke-width:3px,color:#fff
    style C2 fill:#FF9800,stroke:#E65100,stroke-width:3px,color:#fff
    style C3 fill:#FF9800,stroke:#E65100,stroke-width:3px,color:#fff

    style D fill:#607D8B,stroke:#37474F,stroke-width:3px,color:#fff

    style E fill:#9C27B0,stroke:#6A1B9A,stroke-width:3px,color:#fff

    style F1 fill:#E91E63,stroke:#880E4F,stroke-width:3px,color:#fff
    style F2 fill:#E91E63,stroke:#880E4F,stroke-width:3px,color:#fff
    style F3 fill:#E91E63,stroke:#880E4F,stroke-width:3px,color:#fff

    style G fill:#4CAF50,stroke:#2E7D32,stroke-width:4px,color:#fff
```

## Descripción del Flujo

### 📥 **Fase 1: ENTRADAS**
1. **Endpoints Directory** (`tmp/endpoints/*.md`): Archivos con descripción de endpoints
2. **BIAN OpenAPI Specification** (`tmp/bian/*.json`): Especificación formal de la API
3. **Architecture Templates** (`tmp/architectures/`): Templates opcionales de estructura de proyecto

### 🎯 **Fase 2: ORQUESTACIÓN**
El **ModularAgentFramework** coordina la ejecución de los módulos en orden de dependencias:
- Registra todos los módulos
- Realiza ordenamiento topológico
- Crea el grafo de ejecución de LangGraph
- Ejecuta el pipeline completo

### 🔧 **Fase 3: PROCESAMIENTO (3 Módulos)**

#### 🔍 **Módulo 1: Framework Detector**
- **Dependencias**: Ninguna
- **Entrada**: Primer archivo de endpoints
- **Proceso**:
  - Lee archivo con FileSystemReader
  - Consulta Anthropic LLM para detectar lenguaje y framework
  - Actualiza `target_language` y `target_framework` en el estado
- **Salida**: Java, Spring Boot, Python, etc.

#### 📝 **Módulo 2: Requirement Generator**
- **Dependencias**: Framework Detector
- **Entrada**:
  - Todos los archivos de endpoints
  - OpenAPI specification
  - Lenguaje y framework detectados
- **Proceso**:
  - Lee y fusiona todos los endpoints
  - Carga especificación OpenAPI
  - Consulta LLM para generar requisitos completos
  - Actualiza `generated_requirements` en el estado
- **Salida**: Documento de requisitos completo en markdown

#### 🏗️ **Módulo 3: Project Structure**
- **Dependencias**: Framework Detector, Requirement Generator
- **Entrada**:
  - Requisitos generados
  - Template de arquitectura (según lenguaje detectado)
- **Proceso**:
  - Carga template de arquitectura apropiado
  - Consulta LLM para adaptar estructura al proyecto
  - Reemplaza sección de estructura en requisitos
  - Actualiza `updated_requirements` en el estado
- **Salida**: Requisitos con estructura de proyecto definida

### ⚙️ **Fase 4: SERVICIOS DE INFRAESTRUCTURA**
- **Anthropic LLM Client**: Realiza todas las consultas a Claude Sonnet 4
- **FileSystem Reader**: Maneja lectura de archivos con múltiples encodings

### 💾 **Fase 5: ESTADO COMPARTIDO**
**CoreBianState** mantiene:
- Rutas de entrada
- Información detectada (lenguaje, framework, arquitectura)
- Requisitos generados en cada paso
- Errores y resultados por módulo

### 📊 **Fase 6: SALIDAS POR MÓDULO**
Cada módulo contribuye con información específica al estado compartido:
1. **Detección**: `target_language`, `target_framework`
2. **Requisitos**: `generated_requirements`
3. **Estructura**: `updated_requirements`

### ✅ **Fase 7: SALIDA FINAL**
- **api_requirements.md**: Requisitos generados por el módulo 2
- **updated_requirements.md**: Requisitos finales con estructura de proyecto
- **Publicación a RabbitMQ**: Notificación al siguiente servicio en la cadena
