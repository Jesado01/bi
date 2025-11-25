# Project Name: Productos Service - Servicios Subcategoría Consultation

## Overview

This project implements a REST API endpoint for consulting subcategory services based on identification type, identification number, and payment type. The endpoint follows DDD architecture principles with a multi-module approach, providing a clean separation between domain logic, application services, and infrastructure concerns. The service integrates with AS400 systems to retrieve service information and returns a paginated list of available services.

## Technology Stack

- **Language**: Java 21
- **Framework**: Spring Boot
- **Architecture**: DDD Architecture multi-module approach
- **Build Tool**: Maven
- **Database**: JPA/Hibernate compatible database
- **External Integration**: AS400 systems

## Endpoint Details

- **Method**: POST
- **Path**: `/productos/v1/servicios-subcategoria/consultar`
- **Operation**: consultarServiciosSubCategoria
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
    "listaServicios": [
      {
        "codigoServicio": "string",
        "descripcionServicio": "string",
        "tipoPago": "string"
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

This service **MUST** integrate with AS400 systems using the `architecture-spring-model-as400` library. The integration approach described in the usage guide is **REQUIRED** and must be followed exactly:

- **Dependency**: `ec.com.dinersclub.architecture:architecture-spring-model-as400:1.0.0-SNAPSHOT`
- **Repository**: Azure DevOps Maven repository (https://pkgs.dev.azure.com/devopsdc-1/a4ba58b4-b78e-4a80-8a19-597b84b9e314/_packaging/MavenCentral/maven/v1)
- **Required Components**: 
  - `HeaderAS400` for AS400 operation metadata
  - `RequestAS400<T>` for wrapping requests
  - `ResponseAS400<T>` for handling responses
  - `ErrorAS400` for error management
- **Implementation**: Create AS400-specific DTOs implementing `Serializable`, build headers with program/module configuration, and handle responses with proper error checking

## Proposed Project Structure

```
productos-service/
├── src/main/java/com/bank/productos/
│   ├── ProductosServiceApplication.java
│   ├── infrastructure/
│   │   ├── web/
│   │   │   ├── controller/
│   │   │   │   └── ServiciosSubcategoriaController.java
│   │   │   └── dto/
│   │   │       ├── request/
│   │   │       │   ├── ConsultarServiciosSubcategoriaRequestDto.java
│   │   │       │   └── ConsultarServiciosSubcategoriaBodyDto.java
│   │   │       └── response/
│   │   │           ├── ConsultarServiciosSubcategoriaResponseDto.java
│   │   │           ├── ConsultarServiciosSubcategoriaBodyResponseDto.java
│   │   │           └── ServicioDto.java
│   │   ├── persistence/
│   │   │   ├── repository/
│   │   │   │   └── ServiciosSubcategoriaRepository.java
│   │   │   └── entity/
│   │   │       └── ServicioEntity.java
│   │   └── external/
│   │       └── client/
│   │           └── ServiciosExternalClient.java
│   ├── application/
│   │   ├── service/
│   │   │   └── ServiciosSubcategoriaApplicationService.java
│   │   ├── usecase/
│   │   │   └── ConsultarServiciosSubcategoriaUseCase.java
│   │   └── port/
│   │       ├── in/
│   │       │   └── ConsultarServiciosSubcategoriaPort.java
│   │       └── out/
│   │           ├── ServiciosSubcategoriaRepositoryPort.java
│   │           └── ServiciosExternalPort.java
│   ├── domain/
│   │   ├── model/
│   │   │   ├── Servicio.java
│   │   │   ├── TipoIdentificacion.java
│   │   │   └── TipoPago.java
│   │   ├── service/
│   │   │   └── ServiciosDomainService.java
│   │   └── exception/
│   │       └── ServiciosSubcategoriaException.java
│   └── shared/
│       ├── dto/
│       │   └── common/
│       │       ├── DinHeaderDto.java
│       │       ├── DinErrorDto.java
│       │       └── PaginadoDto.java
│       ├── exception/
│       │   └── GlobalExceptionHandler.java
│       └── config/
│           └── WebConfig.java
├── src/main/resources/
│   ├── application.yml
│   ├── application-dev.yml
│   └── application-prod.yml
├── src/test/java/com/bank/productos/
│   ├── infrastructure/web/controller/
│   │   └── ServiciosSubcategoriaControllerTest.java
│   ├── application/usecase/
│   │   └── ConsultarServiciosSubcategoriaUseCaseTest.java
│   └── domain/service/
│       └── ServiciosDomainServiceTest.java
└── pom.xml
```

## File-by-File Requirements

### Main Application
- **ProductosServiceApplication.java**: Create Spring Boot main class with `@SpringBootApplication` annotation and standard main method.

### Infrastructure Layer - Web
- **ServiciosSubcategoriaController.java**: Implement REST controller with `@PostMapping("/productos/v1/servicios-subcategoria/consultar")` endpoint that delegates to application service.
- **ConsultarServiciosSubcategoriaRequestDto.java**: Create request DTO with `dinHeader` and `dinBody` fields, including Bean Validation annotations.
- **ConsultarServiciosSubcategoriaBodyDto.java**: Define request body DTO with `tipoIdentificacion`, `numeroIdentificacion`, and `tipoPago` fields.
- **ConsultarServiciosSubcategoriaResponseDto.java**: Create response DTO structure with `dinHeader`, `dinBody`, and `dinError` fields.
- **ConsultarServiciosSubcategoriaBodyResponseDto.java**: Implement response body DTO containing `List<ServicioDto> listaServicios`.
- **ServicioDto.java**: Define service DTO with `codigoServicio`, `descripcionServicio`, and `tipoPago` fields.

### Infrastructure Layer - Persistence
- **ServiciosSubcategoriaRepository.java**: Create JPA repository interface extending appropriate base repository with custom query methods.
- **ServicioEntity.java**: Implement JPA entity representing service data with proper annotations and field mappings.

### Infrastructure Layer - External
- **ServiciosExternalClient.java**: Implement AS400 client using the mandatory `architecture-spring-model-as400` library with proper request/response handling.

### Application Layer
- **ServiciosSubcategoriaApplicationService.java**: Create application service that orchestrates use case execution and DTO transformations.
- **ConsultarServiciosSubcategoriaUseCase.java**: Implement use case with business logic for consulting services based on identification and payment type.
- **ConsultarServiciosSubcategoriaPort.java**: Define input port interface for the consultation use case.
- **ServiciosSubcategoriaRepositoryPort.java**: Create output port interface for repository operations.
- **ServiciosExternalPort.java**: Define output port interface for external AS400 service integration.

### Domain Layer
- **Servicio.java**: Implement domain entity with business logic, validation rules, and value object relationships.
- **TipoIdentificacion.java**: Create value object for identification type with validation and business rules.
- **TipoPago.java**: Implement value object for payment type with appropriate constraints and validation.
- **ServiciosDomainService.java**: Create domain service containing complex business logic that doesn't belong to a single entity.
- **ServiciosSubcategoriaException.java**: Define domain-specific exception class with appropriate error codes and messages.

### Shared Layer
- **DinHeaderDto.java**: Implement common header DTO with all required fields including pagination support.
- **DinErrorDto.java**: Create standard error DTO structure with comprehensive error information fields.
- **PaginadoDto.java**: Define pagination DTO with record count, total pages, and current page fields.
- **GlobalExceptionHandler.java**: Implement global exception handler using `@ControllerAdvice` for consistent error responses.
- **WebConfig.java**: Create web configuration class with necessary Spring MVC configurations.

### Configuration Files
- **application.yml**: Configure main application properties including server port, database connection, and AS400 integration settings.
- **application-dev.yml**: Define development-specific configuration overrides for local development environment.
- **application-prod.yml**: Set production configuration with appropriate security and performance settings.
- **pom.xml**: Configure Maven dependencies including Spring Boot, AS400 library, JPA, validation, and testing frameworks.

### Test Files
- **ServiciosSubcategoriaControllerTest.java**: Create integration tests for the REST controller using MockMvc and proper test scenarios.
- **ConsultarServiciosSubcategoriaUseCaseTest.java**: Implement unit tests for use case logic with mocked dependencies and edge cases.
- **ServiciosDomainServiceTest.java**: Write unit tests for domain service business logic with comprehensive test coverage.