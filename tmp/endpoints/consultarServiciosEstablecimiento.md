# Software Requirements Document

## Project Name: Productos Servicios Establecimiento API

## Overview

This project implements a REST API endpoint for consulting establishment services based on identification parameters. The endpoint `/productos/v1/servicios-establecimiento/consultar` allows clients to retrieve a list of companies/establishments associated with a specific identification type and number. The system follows Domain-Driven Design (DDD) architecture with a multi-module approach and integrates with AS400 legacy systems for data retrieval.

## Technology Stack

- **Language**: Java 21
- **Framework**: Spring Boot
- **Architecture**: DDD Architecture multi-module approach
- **Build Tool**: Maven
- **Data Access**: Spring Data JPA
- **Validation**: Bean Validation (JSR-303)
- **JSON Processing**: Jackson
- **Testing**: JUnit 5, Mockito

## Endpoint Details

**Method**: POST  
**Path**: `/productos/v1/servicios-establecimiento/consultar`  
**Content-Type**: application/json

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
    "numeroIdentificacion": "string"
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
    "listaEmpresas": [
      {
        "codigoCategoria": "string",
        "nombreComercio": "string",
        "rucComercio": "string"
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

This project **MUST** integrate with AS400 legacy systems using the `architecture-spring-model-as400` library. The following approach is **REQUIRED** and must be followed:

1. **Add Maven Repository**: Configure the Diners Club Azure DevOps Maven repository in `pom.xml`
2. **Add Dependency**: Include `architecture-spring-model-as400` version `1.0.0-SNAPSHOT`
3. **Use Standard Models**: Implement `RequestAS400<T>`, `ResponseAS400<T>`, and `HeaderAS400` classes
4. **Follow Integration Pattern**: Create AS400-specific DTOs implementing `Serializable`, build headers with AS400 configuration (programa, moduloRPG, libraryList), and always check for errors in `dinError` field
5. **Error Handling**: Implement proper error handling using `ErrorAS400` structure

The AS400 integration will be used to retrieve establishment services data from the legacy system based on the provided identification parameters.

## Proposed Project Structure

```
productos-service/
├── src/main/java/com/bank/productos/
│   ├── ProductosServiceApplication.java
│   ├── infrastructure/
│   │   ├── web/
│   │   │   ├── controller/
│   │   │   │   └── ServiciosEstablecimientoController.java
│   │   │   ├── dto/
│   │   │   │   ├── request/
│   │   │   │   │   ├── ConsultarServiciosEstablecimientoRequest.java
│   │   │   │   │   ├── DinHeaderRequest.java
│   │   │   │   │   ├── DinBodyConsultarRequest.java
│   │   │   │   │   └── PaginadoRequest.java
│   │   │   │   └── response/
│   │   │   │       ├── ConsultarServiciosEstablecimientoResponse.java
│   │   │   │       ├── DinHeaderResponse.java
│   │   │   │       ├── DinBodyConsultarResponse.java
│   │   │   │       ├── DinErrorResponse.java
│   │   │   │       ├── PaginadoResponse.java
│   │   │   │       └── EmpresaResponse.java
│   │   │   └── config/
│   │   │       └── WebConfig.java
│   │   └── persistence/
│   │       ├── repository/
│   │       │   └── ServiciosEstablecimientoRepository.java
│   │       ├── entity/
│   │       │   ├── ServicioEstablecimiento.java
│   │       │   └── Empresa.java
│   │       └── config/
│   │           └── DatabaseConfig.java
│   ├── domain/
│   │   ├── model/
│   │   │   ├── ServicioEstablecimiento.java
│   │   │   ├── Empresa.java
│   │   │   ├── TipoIdentificacion.java
│   │   │   └── NumeroIdentificacion.java
│   │   ├── service/
│   │   │   ├── ServiciosEstablecimientoService.java
│   │   │   └── impl/
│   │   │       └── ServiciosEstablecimientoServiceImpl.java
│   │   └── repository/
│   │       └── ServiciosEstablecimientoRepositoryPort.java
│   └── application/
│       ├── usecase/
│       │   └── ConsultarServiciosEstablecimientoUseCase.java
│       ├── port/
│       │   ├── in/
│       │   │   └── ConsultarServiciosEstablecimientoPort.java
│       │   └── out/
│       │       └── ServiciosEstablecimientoRepositoryPort.java
│       └── dto/
│           ├── ConsultarServiciosEstablecimientoCommand.java
│           └── ServiciosEstablecimientoResult.java
├── src/main/resources/
│   ├── application.yml
│   ├── application-dev.yml
│   └── application-prod.yml
├── src/test/java/com/bank/productos/
│   ├── infrastructure/web/controller/
│   │   └── ServiciosEstablecimientoControllerTest.java
│   ├── domain/service/
│   │   └── ServiciosEstablecimientoServiceTest.java
│   └── application/usecase/
│       └── ConsultarServiciosEstablecimientoUseCaseTest.java
└── pom.xml
```

## File-by-File Requirements

### Root Files
- **ProductosServiceApplication.java**: Create Spring Boot main application class with `@SpringBootApplication` annotation and main method.
- **pom.xml**: Configure Maven project with Java 21, Spring Boot dependencies, and mandatory AS400 architecture library.

### Infrastructure Layer - Web
- **ServiciosEstablecimientoController.java**: Implement REST controller with `@PostMapping` for `/productos/v1/servicios-establecimiento/consultar` endpoint.
- **ConsultarServiciosEstablecimientoRequest.java**: Create main request DTO with `dinHeader` and `dinBody` fields using validation annotations.
- **DinHeaderRequest.java**: Implement common header DTO with all transaction metadata fields and validation constraints.
- **DinBodyConsultarRequest.java**: Create request body DTO with `tipoIdentificacion` and `numeroIdentificacion` fields.
- **PaginadoRequest.java**: Implement pagination DTO with `cantRegistros`, `numTotalPag`, and `numPagActual` fields.
- **ConsultarServiciosEstablecimientoResponse.java**: Create main response DTO containing header, body, and error structures.
- **DinHeaderResponse.java**: Implement response header DTO mirroring the request header structure.
- **DinBodyConsultarResponse.java**: Create response body DTO with `listaEmpresas` field containing company list.
- **DinErrorResponse.java**: Implement error response DTO with all error fields for proper error handling.
- **PaginadoResponse.java**: Create pagination response DTO matching the request pagination structure.
- **EmpresaResponse.java**: Implement company DTO with `codigoCategoria`, `nombreComercio`, and `rucComercio` fields.
- **WebConfig.java**: Configure web layer settings and CORS if needed.

### Infrastructure Layer - Persistence
- **ServiciosEstablecimientoRepository.java**: Create JPA repository interface extending `JpaRepository` with custom query methods.
- **ServicioEstablecimiento.java**: Implement JPA entity for establishment services with proper annotations and relationships.
- **Empresa.java**: Create JPA entity for company data with appropriate field mappings.
- **DatabaseConfig.java**: Configure database connection and JPA settings.

### Domain Layer
- **ServicioEstablecimiento.java**: Create domain model representing establishment service business logic without persistence annotations.
- **Empresa.java**: Implement domain model for company with business rules and validation.
- **TipoIdentificacion.java**: Create value object for identification type with validation logic.
- **NumeroIdentificacion.java**: Implement value object for identification number with format validation.
- **ServiciosEstablecimientoService.java**: Define domain service interface with business operation methods.
- **ServiciosEstablecimientoServiceImpl.java**: Implement domain service with business logic and AS400 integration calls.
- **ServiciosEstablecimientoRepositoryPort.java**: Create repository port interface for domain layer abstraction.

### Application Layer
- **ConsultarServiciosEstablecimientoUseCase.java**: Implement use case orchestrating the consultation flow and calling domain services.
- **ConsultarServiciosEstablecimientoPort.java**: Define input port interface for the use case.
- **ServiciosEstablecimientoRepositoryPort.java**: Create output port interface for repository operations.
- **ConsultarServiciosEstablecimientoCommand.java**: Implement command DTO for use case input parameters.
- **ServiciosEstablecimientoResult.java**: Create result DTO for use case output data.

### Configuration Files
- **application.yml**: Configure main application properties including server port and logging levels.
- **application-dev.yml**: Set development environment specific configurations including database and AS400 connections.
- **application-prod.yml**: Configure production environment settings with appropriate security and performance parameters.

### Test Files
- **ServiciosEstablecimientoControllerTest.java**: Create unit tests for controller endpoints using MockMvc and proper test scenarios.
- **ServiciosEstablecimientoServiceTest.java**: Implement unit tests for domain service business logic with mocked dependencies.
- **ConsultarServiciosEstablecimientoUseCaseTest.java**: Create unit tests for use case orchestration and integration scenarios.