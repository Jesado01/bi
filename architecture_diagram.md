# Diagrama de Arquitectura del Proyecto BIAN

## Diagrama Completo del Sistema

```mermaid
graph TB
    subgraph "Entry Point"
        MAIN[main.py<br/>RabbitMQ Consumer]
    end

    subgraph "Configuration & Setup"
        SETUP[agent_setup.py<br/>setup_agent_framework]
        STATE[bian_core.py<br/>CoreBianState]
    end

    subgraph "Core Framework"
        FRAMEWORK[modular_agent_framework.py<br/>ModularAgentFramework]
        PROTOCOL[agent_module.py<br/>AgentModule Protocol]
    end

    subgraph "Agent Modules (agents/modules/)"
        FD[framework_detector.py<br/>FrameworkDetectorModule]
        RG[requirement_generator.py<br/>RequirementGeneratorModule]
        PS[project_structure.py<br/>ProjectStructureModule]
    end

    subgraph "Infrastructure Services"
        LLM[anthropic_llm_client.py<br/>AnthropicLLMClient]
        FS[file_system_reader.py<br/>FileSystemReader]
    end

    subgraph "External Systems"
        RABBIT[(RabbitMQ<br/>Message Broker)]
        ANTHROPIC[Anthropic API<br/>Claude Sonnet 4]
        FILES[File System<br/>Endpoints & BIAN Specs]
    end

    %% Main Flow
    RABBIT -->|Message| MAIN
    MAIN -->|Initialize| STATE
    MAIN -->|Setup| SETUP
    SETUP -->|Creates| FRAMEWORK
    SETUP -->|Registers| FD
    SETUP -->|Registers| RG
    SETUP -->|Registers| PS

    %% Framework Configuration
    FRAMEWORK -->|Uses| PROTOCOL
    FD -.->|Implements| PROTOCOL
    RG -.->|Implements| PROTOCOL
    PS -.->|Implements| PROTOCOL

    %% Module Dependencies
    RG -->|Depends on| FD
    PS -->|Depends on| FD
    PS -->|Depends on| RG

    %% Service Dependencies
    FD -->|Uses| LLM
    FD -->|Uses| FS
    RG -->|Uses| LLM
    RG -->|Uses| FS
    PS -->|Uses| LLM
    PS -->|Uses| FS

    %% External Connections
    LLM -->|API Calls| ANTHROPIC
    FS -->|Read Files| FILES
    MAIN -->|Publish Results| RABBIT

    %% State Flow
    STATE -.->|Shared State| FD
    STATE -.->|Shared State| RG
    STATE -.->|Shared State| PS

    %% Styling
    classDef entryPoint fill:#e1f5ff,stroke:#01579b,stroke-width:3px
    classDef core fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef modules fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef services fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef external fill:#fce4ec,stroke:#880e4f,stroke-width:2px

    class MAIN entryPoint
    class FRAMEWORK,PROTOCOL,STATE,SETUP core
    class FD,RG,PS modules
    class LLM,FS services
    class RABBIT,ANTHROPIC,FILES external
```

## Diagrama de Flujo de Ejecución

```mermaid
sequenceDiagram
    participant RMQ as RabbitMQ
    participant Main as main.py
    participant Setup as agent_setup
    participant FW as ModularAgentFramework
    participant FD as FrameworkDetector
    participant RG as RequirementGenerator
    participant PS as ProjectStructure
    participant LLM as AnthropicLLM
    participant FS as FileSystem

    RMQ->>Main: Message (paths)
    Main->>Setup: setup_agent_framework(state)
    Setup->>FW: Create framework
    Setup->>FW: register_module(FrameworkDetector)
    Setup->>FW: register_module(RequirementGenerator)
    Setup->>FW: register_module(ProjectStructure)
    FW->>FW: _update_execution_order()<br/>(topological sort)
    Main->>FW: start_analysis(state)
    FW->>FW: create_main_graph()

    Note over FW,PS: Execute modules in dependency order

    FW->>FD: detect_framework_and_language(state)
    FD->>FS: read_file(endpoint)
    FS-->>FD: file_content
    FD->>LLM: generate(detect framework prompt)
    LLM-->>FD: language, framework
    FD-->>FW: updated_state

    FW->>RG: generate_requirements(state)
    RG->>FS: read endpoints_directory()
    FS-->>RG: merged_content
    RG->>FS: load OpenAPI spec
    FS-->>RG: openapi_spec
    RG->>LLM: generate(requirements prompt)
    LLM-->>RG: generated_requirements
    RG-->>FW: updated_state

    FW->>PS: update_project_structure(state)
    PS->>FS: load_architecture_template()
    FS-->>PS: template
    PS->>LLM: generate(structure prompt)
    LLM-->>PS: updated_requirements
    PS-->>FW: final_state

    FW-->>Main: final_state
    Main->>FS: save_requirements()
    Main->>RMQ: publish(result)
```

## Diagrama del Sistema de Módulos

```mermaid
classDiagram
    class AgentModule {
        <<Protocol>>
        +module_name: str
        +dependencies: List[str]
        +add_nodes_to_graph(graph) Tuple[str, str]
        +get_entry_point() str
        +get_exit_point() str
        +log_loading() None
    }

    class ModularAgentFramework {
        -modules: Dict[str, AgentModule]
        -execution_order: List[str]
        +register_module(module)
        -_update_execution_order()
        +create_main_graph() StateGraph
        +start_analysis(state) Dict
        +visualize_graph(xray) Image
    }

    class CoreBianState {
        +requirements_folder: str
        +endpoint_json_path: str
        +bian_dir: str
        +endpoints_dir: str
        +target_language: str
        +target_framework: str
        +target_architecture: str
        +generated_requirements: str
        +updated_requirements: str
        +errors: List[str]
        +module_results: Dict
    }

    class FrameworkDetectorModule {
        -_module_name: "framework_detector"
        -_dependencies: []
        -file_reader: FileSystemReader
        -llm_client: AnthropicLLMClient
        +detect_framework_and_language(state)
    }

    class RequirementGeneratorModule {
        -_module_name: "requirement_generator"
        -_dependencies: ["framework_detector"]
        -file_reader: FileSystemReader
        -llm_client: AnthropicLLMClient
        +generate_requirements(state)
        -_read_endpoints_directory()
        -_load_openapi_spec(state)
    }

    class ProjectStructureModule {
        -_module_name: "project_structure"
        -_dependencies: ["framework_detector", "requirement_generator"]
        -file_reader: FileSystemReader
        -llm_client: AnthropicLLMClient
        +update_project_structure(state)
        -_load_architecture_template(language, arch)
        -_generate_structure_with_llm(...)
    }

    class AnthropicLLMClient {
        -api_key: str
        -model: str
        -client: Anthropic
        +generate(system_prompt, user_prompt, **kwargs)
        +generate_stream(system_prompt, user_prompt, **kwargs)
        +generate_with_callback(...)
    }

    class FileSystemReader {
        -base_path: Path
        +read_file(file_path) str
        +list_directory_contents(directory_path) list
        -_read_with_encoding_fallback(file_path)
        -_try_alternative_reads(full_path)
    }

    AgentModule <|.. FrameworkDetectorModule : implements
    AgentModule <|.. RequirementGeneratorModule : implements
    AgentModule <|.. ProjectStructureModule : implements

    ModularAgentFramework o-- AgentModule : manages
    ModularAgentFramework --> CoreBianState : uses

    FrameworkDetectorModule --> AnthropicLLMClient : uses
    FrameworkDetectorModule --> FileSystemReader : uses
    RequirementGeneratorModule --> AnthropicLLMClient : uses
    RequirementGeneratorModule --> FileSystemReader : uses
    ProjectStructureModule --> AnthropicLLMClient : uses
    ProjectStructureModule --> FileSystemReader : uses

    FrameworkDetectorModule ..> CoreBianState : updates
    RequirementGeneratorModule ..> CoreBianState : updates
    ProjectStructureModule ..> CoreBianState : updates
```

## Diagrama de Dependencias entre Módulos

```mermaid
graph LR
    subgraph "Module Dependency Chain"
        FD[FrameworkDetector<br/>dependencies: []]
        RG[RequirementGenerator<br/>dependencies: ['framework_detector']]
        PS[ProjectStructure<br/>dependencies: ['framework_detector', 'requirement_generator']]
    end

    FD -->|1. Execute First| RG
    RG -->|2. Execute Second| PS
    PS -->|3. Execute Last| END[END]

    style FD fill:#c8e6c9,stroke:#2e7d32
    style RG fill:#fff9c4,stroke:#f57f17
    style PS fill:#b3e5fc,stroke:#0277bd
    style END fill:#ffccbc,stroke:#d84315
```

## Diagrama del Grafo LangGraph Generado

```mermaid
graph TB
    START([START])
    FDN[framework_detector_node]
    RGN[requirement_generator_node]
    PSN[project_structure_node]
    END([END])

    START -->|Entry Point| FDN
    FDN -->|Updated State| RGN
    RGN -->|Updated State| PSN
    PSN -->|Final State| END

    subgraph "State Updates"
        S1[target_language<br/>target_framework]
        S2[generated_requirements]
        S3[updated_requirements]
    end

    FDN -.->|Updates| S1
    RGN -.->|Updates| S2
    PSN -.->|Updates| S3

    style START fill:#4caf50,stroke:#1b5e20,stroke-width:3px
    style END fill:#f44336,stroke:#b71c1c,stroke-width:3px
    style FDN fill:#e1bee7,stroke:#4a148c,stroke-width:2px
    style RGN fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    style PSN fill:#b3e5fc,stroke:#01579b,stroke-width:2px
```

## Diagrama de Datos - CoreBianState

```mermaid
graph TD
    subgraph "CoreBianState Structure"
        subgraph "Inputs"
            I1[requirements_folder: str]
            I2[endpoint_json_path: str]
            I3[bian_dir: str]
            I4[endpoints_dir: str]
        end

        subgraph "Detected Information"
            D1[target_language: str]
            D2[target_framework: str]
            D3[target_architecture: str]
        end

        subgraph "Generated Outputs"
            O1[generated_requirements: str]
            O2[updated_requirements: str]
        end

        subgraph "System State"
            S1[errors: List str]
            S2[module_results: Dict]
            S3[current_module: str]
        end
    end

    I3 --> FD[FrameworkDetector]
    I4 --> FD
    FD --> D1
    FD --> D2

    I3 --> RG[RequirementGenerator]
    I4 --> RG
    D1 --> RG
    D2 --> RG
    RG --> O1

    D1 --> PS[ProjectStructure]
    D3 --> PS
    O1 --> PS
    PS --> O2

    style I1 fill:#e3f2fd
    style I2 fill:#e3f2fd
    style I3 fill:#e3f2fd
    style I4 fill:#e3f2fd
    style D1 fill:#fff3e0
    style D2 fill:#fff3e0
    style D3 fill:#fff3e0
    style O1 fill:#e8f5e9
    style O2 fill:#e8f5e9
```

## Descripción de Componentes

### 1. **ModularAgentFramework**
- **Responsabilidad**: Orquestador central del sistema
- **Funciones clave**:
  - Registra módulos dinámicamente
  - Ordena ejecución basándose en dependencias (topological sort)
  - Crea y compila el grafo de LangGraph
  - Ejecuta el pipeline completo

### 2. **AgentModule (Protocol)**
- **Responsabilidad**: Interfaz que todos los módulos deben implementar
- **Garantiza**:
  - Cada módulo declara su nombre único
  - Cada módulo declara sus dependencias
  - Cada módulo puede añadir nodos al grafo
  - Cada módulo tiene puntos de entrada/salida

### 3. **Módulos Concretos**

#### a) **FrameworkDetectorModule**
- **Sin dependencias**
- **Función**: Detecta lenguaje y framework del código fuente
- **Input**: Archivos en `endpoints_dir`
- **Output**: `target_language`, `target_framework`

#### b) **RequirementGeneratorModule**
- **Depende de**: `framework_detector`
- **Función**: Genera requisitos analizando endpoints y especificación OpenAPI
- **Input**: Archivos de endpoints, especificación BIAN JSON
- **Output**: `generated_requirements`

#### c) **ProjectStructureModule**
- **Depende de**: `framework_detector`, `requirement_generator`
- **Función**: Actualiza estructura del proyecto usando templates de arquitectura
- **Input**: Requirements generados, templates de arquitectura
- **Output**: `updated_requirements`

### 4. **Servicios de Infraestructura**

#### a) **AnthropicLLMClient**
- Cliente para API de Anthropic Claude
- Soporta generación con streaming
- Manejo de tokens y temperatura configurable

#### b) **FileSystemReader**
- Lee archivos con múltiples encodings (UTF-8, Latin-1)
- Soporte para rutas largas en Windows
- Métodos alternativos de lectura para casos edge

### 5. **Flujo de Ejecución**
1. RabbitMQ recibe mensaje con rutas
2. `main.py` crea estado inicial
3. `agent_setup.py` configura framework y módulos
4. Framework ordena módulos por dependencias
5. Se crea grafo LangGraph con todos los nodos
6. Ejecución secuencial: FD → RG → PS
7. Guardado de resultados y publicación a RabbitMQ
