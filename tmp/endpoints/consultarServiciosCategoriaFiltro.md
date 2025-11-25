# Productos Service - Servicios Categoria Consultation

## Project Name
**productos-service**

## Overview
This service provides a REST API endpoint for consulting service categories with filtering capabilities. The endpoint `/productos/v1/servicios-categoria/filtro` allows clients to retrieve categorized services based on identification type, identification number, category code, and payment type filters. The service follows Domain-Driven Design (DDD) architecture principles with a multi-module approach and integrates with AS400 legacy systems for data retrieval.

## Technology Stack
- **Language**: Java 21
- **Framework**: Spring Boot
- **Architecture**: DDD Architecture multi-module approach
- **Build Tool**: Maven
- **Database**: JPA/Hibernate
- **Mapping**: MapStruct
- **Validation**: Bean Validation
- **Documentation**: OpenAPI/Swagger

## Endpoint Details
- **Method**: POST
- **Path**: `/productos/v1/servicios-categoria/filtro`
- **Operation**: consultarServiciosCategoria (with filtering)
- **Content-Type**: application/json

### Request Structure
```json
{
  "dinHeader": {
    "aplicacionId": "string",
    "canalId": "string",
    "sesionId": "string",
    "dispositivo": "string",
    "idioma": "string",
    "portalId": "string",
    "uuid": "string",
    "ip": "string",
    "horaTransaccion": "string",
    "llaveSimetrica": "string",
    "usuario": "string",
    "paginado": {
      "cantRegistros": "number",
      "numTotalPag": "number",
      "numPagActual": "number"
    }
  },
  "dinBody": {
    "tipoIdentificacion": "string",
    "numeroIdentificacion": "string",
    "codCategoriaServicio": "string",
    "tipoPago": "string"
  }
}
```

### Response Structure
```json
{
  "dinHeader": {
    "aplicacionId": "string",
    "canalId": "string",
    "sesionId": "string",
    "dispositivo": "string",
    "idioma": "string",
    "portalId": "string",
    "uuid": "string",
    "ip": "string",
    "horaTransaccion": "string",
    "llaveSimetrica": "string",
    "usuario": "string",
    "paginado": {
      "cantRegistros": "number",
      "numTotalPag": "number",
      "numPagActual": "number"
    }
  },
  "dinBody": {
    "listaCategorias": [
      {
        "codigoCategoria": "string",
        "descripcionCategoria": "string",
        "descripcionLargaCategoria": "string", 
        "linkImagen": "string"
      }
    ]
  },
  "dinError": {
    "tipo": "string",
    "fecha": "string",
    "codigo": "string",
    "origen": "string",
    "codigoErrorProveedor": "string",
    "mensaje": "string",
    "detalle": "string"
  }
}
```

## External Dependencies

### AS400 Integration (MANDATORY)
This service **MUST** integrate with AS400 legacy systems using the `architecture-spring-model-as400` library. The integration approach described in the usage guide is **REQUIRED** and must be followed exactly:

- **Dependency**: `ec.com.dinersclub.architecture:architecture-spring-model-as400:1.0.0-SNAPSHOT`
- **Repository**: Azure DevOps Maven repository (https://pkgs.dev.azure.com/devopsdc-1/a4ba58b4-b78e-4a80-8a19-597b84b9e314/_packaging/MavenCentral/maven/v1)
- **Required Components**: 
  - `HeaderAS400` for AS400 operation metadata
  - `RequestAS400<T>` for wrapping AS400 requests
  - `ResponseAS400<T>` for handling AS400 responses
  - `ErrorAS400` for AS400-specific error handling
- **Integration Pattern**: Use the generic wrapper approach with proper error handling and header configuration as specified in the usage guide
- **Configuration**: Must include programa, moduloRPG, libraryList, and other AS400-specific parameters

## Proposed Project Structure
```
productos-service/
├── src/
│   └── main/
│       └── java/
│           └── com/
│               └── bank/
│                   └── productos/
│                       ├── ProductosServiceApplication.java
│                       ├── application/
│                       │   ├── dto/
│                       │   │   ├── common/
│                       │   │   │   ├── DinHeaderDto.java
│                       │   │   │   ├── PaginadoDto.java
│                       │   │   │   └── DinErrorDto.java
│                       │   │   ├── request/
│                       │   │   │   ├── ConsultarServiciosCategoriaRequestDto.java
│                       │   │   │   └── ConsultarServiciosCategoriaBodyDto.java
│                       │   │   └── response/
│                       │   │       ├── ConsultarServiciosCategoriaResponseDto.java
│                       │   │       ├── ConsultarServiciosCategoriaBodyResponseDto.java
│                       │   │       └── CategoriaServicioDto.java
│                       │   ├── service/
│                       │   │   ├── ServiciosCategoriaApplicationService.java
│                       │   │   └── impl/
│                       │   │       └── ServiciosCategoriaApplicationServiceImpl.java
│                       │   └── mapper/
│                       │       ├── ServiciosCategoriaMapper.java
│                       │       └── CommonMapper.java
│                       ├── domain/
│                       │   ├── model/
│                       │   │   ├── ServicioCategoria.java
│                       │   │   ├── CategoriaServicio.java
│                       │   │   ├── TipoIdentificacion.java
│                       │   │   ├── TipoPago.java
│                       │   │   └── valueobject/
│                       │   │       ├── CodigoCategoria.java
│                       │   │       ├── NumeroIdentificacion.java
│                       │   │       └── DescripcionCategoria.java
│                       │   ├── repository/
│                       │   │   └── ServiciosCategoriaRepository.java
│                       │   └── service/
│                       │       ├── ServiciosCategoriaService.java
│                       │       └── impl/
│                       │           └── ServiciosCategoriaServiceImpl.java
│                       └── infrastructure/
│                           ├── controller/
│                           │   └── ServiciosCategoriaController.java
│                           ├── repository/
│                           │   ├── ServiciosCategoriaRepositoryImpl.java
│                           │   └── entity/
│                           │       ├── ServicioCategoriaEntity.java
│                           │       └── CategoriaServicioEntity.java
│                           ├── config/
│                           │   ├── DatabaseConfig.java
│                           │   └── WebConfig.java
│                           └── exception/
│                               ├── GlobalExceptionHandler.java
│                               ├── ServiciosCategoriaException.java
│                               └── ErrorCode.java
```

## File-by-File Requirements

### Main Application
- **ProductosServiceApplication.java**: Create Spring Boot main application class with @SpringBootApplication annotation and configure component scanning for all packages.

### Application Layer - DTOs
- **DinHeaderDto.java**: Implement common DTO for request/response header containing all specified fields (aplicacionId, canalId, sesionId, etc.) with proper validation annotations.
- **PaginadoDto.java**: Create DTO for pagination information with cantRegistros, numTotalPag, numPagActual fields and validation constraints.
- **DinErrorDto.java**: Implement DTO for error information with all error fields and proper serialization annotations.
- **ConsultarServiciosCategoriaRequestDto.java**: Create main request DTO containing dinHeader and dinBody fields with validation.
- **ConsultarServiciosCategoriaBodyDto.java**: Implement request body DTO with filtering fields (tipoIdentificacion, numeroIdentificacion, etc.) and validation rules.
- **ConsultarServiciosCategoriaResponseDto.java**: Create main response DTO containing dinHeader, dinBody, and dinError fields.
- **ConsultarServiciosCategoriaBodyResponseDto.java**: Implement response body DTO containing listaCategorias field.
- **CategoriaServicioDto.java**: Create DTO for category information with all specified fields and proper JSON serialization.

### Application Layer - Services
- **ServiciosCategoriaApplicationService.java**: Define application service interface with consultarServiciosCategoria method signature.
- **ServiciosCategoriaApplicationServiceImpl.java**: Implement application service with business orchestration, AS400 integration, and error handling logic.

### Application Layer - Mappers
- **ServiciosCategoriaMapper.java**: Create MapStruct mapper for converting between DTOs and domain objects with proper mapping annotations.
- **CommonMapper.java**: Implement common mapper for shared mapping operations like headers, pagination, and error handling.

### Domain Layer - Models
- **ServicioCategoria.java**: Create domain aggregate root representing a service category with business rules and invariants.
- **CategoriaServicio.java**: Implement domain entity representing category details with business logic.
- **TipoIdentificacion.java**: Create domain value object for identification type with validation and business rules.
- **TipoPago.java**: Implement domain value object for payment type with validation logic.

### Domain Layer - Value Objects
- **CodigoCategoria.java**: Create value object for category code with validation and immutability.
- **NumeroIdentificacion.java**: Implement value object for identification number with validation rules.
- **DescripcionCategoria.java**: Create value object for category description with business constraints.

### Domain Layer - Repository & Service
- **ServiciosCategoriaRepository.java**: Define domain repository interface for category services data access operations.
- **ServiciosCategoriaService.java**: Create domain service interface for core business logic operations.
- **ServiciosCategoriaServiceImpl.java**: Implement domain service with business rules and domain logic.

### Infrastructure Layer - Controller
- **ServiciosCategoriaController.java**: Implement REST controller handling POST requests for /productos/v1/servicios-categoria/filtro endpoint with proper error handling.

### Infrastructure Layer - Repository
- **ServiciosCategoriaRepositoryImpl.java**: Create repository implementation integrating with AS400 using the mandatory architecture-spring-model-as400 library.
- **ServicioCategoriaEntity.java**: Implement JPA entity for service category persistence with proper annotations.
- **CategoriaServicioEntity.java**: Create JPA entity for category details persistence with relationships.

### Infrastructure Layer - Configuration
- **DatabaseConfig.java**: Configure database connection, JPA settings, and transaction management.
- **WebConfig.java**: Set up web configuration for REST endpoints, CORS, and JSON serialization.

### Infrastructure Layer - Exception Handling
- **GlobalExceptionHandler.java**: Implement global exception handler for REST API error responses with proper HTTP status codes.
- **ServiciosCategoriaException.java**: Create custom exception for category services operations with error codes.
- **ErrorCode.java**: Define enum with error codes for the service including AS400 integration errors.