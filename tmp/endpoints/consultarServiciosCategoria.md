# Project Name: Productos Service - Servicios Categoria API

## Overview

This project implements a REST API endpoint for querying service categories (servicios categoria) within a banking products domain. The endpoint allows clients to retrieve categorized services based on customer identification, category codes, and payment types, following a Domain-Driven Design (DDD) architecture with multi-module approach.

## Technology Stack

- **Language**: Java 21
- **Framework**: Spring Boot
- **Architecture**: DDD Architecture multi-module approach
- **Build Tool**: Maven
- **Database**: JPA/Hibernate compatible database
- **Testing**: JUnit 5, Spring Boot Test

## Endpoint Details

**Method**: POST  
**Path**: `/productos/v1/servicios-categoria/consultar`  
**Operation**: consultarServiciosCategoria  
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

This project **MUST** integrate with AS400 systems using the `architecture-spring-model-as400` library. The integration approach described in the usage guide is **REQUIRED** and must be followed exactly:

- **Dependency**: `ec.com.dinersclub.architecture:architecture-spring-model-as400:1.0.0-SNAPSHOT`
- **Repository**: Azure DevOps Maven repository (https://pkgs.dev.azure.com/devopsdc-1/a4ba58b4-b78e-4a80-8a19-597b84b9e314/_packaging/MavenCentral/maven/v1)
- **Usage**: Use `RequestAS400<T>`, `ResponseAS400<T>`, and `HeaderAS400` classes for all AS400 communications
- **Configuration**: Configure AS400 program names, RPG modules, and library lists in HeaderAS400
- **Error Handling**: Use `ErrorAS400` for standardized error processing

## Proposed Project Structure

```
productos-service/
├── src/main/java/com/bank/productos/
│   ├── ProductosServiceApplication.java
│   ├── infrastructure/
│   │   ├── web/
│   │   │   ├── controller/
│   │   │   │   └── ServiciosCategoriaController.java
│   │   │   └── dto/
│   │   │       ├── request/
│   │   │       │   ├── ConsultarServiciosCategoriaRequest.java
│   │   │       │   ├── DinHeaderRequest.java
│   │   │       │   ├── DinBodyConsultarRequest.java
│   │   │       │   └── PaginadoRequest.java
│   │   │       └── response/
│   │   │           ├── ConsultarServiciosCategoriaResponse.java
│   │   │           ├── DinHeaderResponse.java
│   │   │           ├── DinBodyConsultarResponse.java
│   │   │           ├── CategoriaServicioDto.java
│   │   │           ├── DinErrorResponse.java
│   │   │           └── PaginadoResponse.java
│   │   ├── mapper/
│   │   │   └── ServiciosCategoriaMapper.java
│   │   ├── persistence/
│   │   │   ├── repository/
│   │   │   │   └── ServiciosCategoriaRepository.java
│   │   │   ├── entity/
│   │   │   │   └── CategoriaServicioEntity.java
│   │   │   └── adapter/
│   │   │       └── ServiciosCategoriaRepositoryAdapter.java
│   │   ├── external/
│   │   │   └── client/
│   │   │       └── ServiciosCategoriaExternalClient.java
│   │   └── config/
│   │       ├── WebConfig.java
│   │       └── DatabaseConfig.java
│   ├── application/
│   │   ├── service/
│   │   │   └── ServiciosCategoriaApplicationService.java
│   │   ├── usecase/
│   │   │   └── ConsultarServiciosCategoriaUseCase.java
│   │   └── port/
│   │       ├── in/
│   │       │   └── ConsultarServiciosCategoriaPort.java
│   │       └── out/
│   │           ├── ServiciosCategoriaRepositoryPort.java
│   │           └── ServiciosCategoriaExternalPort.java
│   └── domain/
│       ├── model/
│       │   ├── CategoriaServicio.java
│       │   ├── Cliente.java
│       │   └── Paginacion.java
│       ├── valueobject/
│       │   ├── TipoIdentificacion.java
│       │   ├── NumeroIdentificacion.java
│       │   ├── CodigoCategoriaServicio.java
│       │   └── TipoPago.java
│       └── exception/
│           ├── ServiciosCategoriaException.java
│           └── ClienteNotFoundException.java
├── src/main/resources/
│   ├── application.yml
│   ├── application-dev.yml
│   ├── application-prod.yml
│   └── db/migration/
│       └── V1__create_categoria_servicio_table.sql
├── src/test/java/com/bank/productos/
│   ├── infrastructure/web/controller/
│   │   └── ServiciosCategoriaControllerTest.java
│   ├── application/usecase/
│   │   └── ConsultarServiciosCategoriaUseCaseTest.java
│   └── domain/model/
│       └── CategoriaServicioTest.java
└── pom.xml
```

## File-by-File Requirements

### Main Application
- **ProductosServiceApplication.java**: Create Spring Boot main class with @SpringBootApplication annotation and main method to bootstrap the application.

### Infrastructure Layer - Web
- **ServiciosCategoriaController.java**: Implement REST controller with @RestController and @RequestMapping("/productos/v1/servicios-categoria") annotations, exposing POST /consultar endpoint.
- **ConsultarServiciosCategoriaRequest.java**: Create request DTO with dinHeader and dinBody fields, applying @Valid and @JsonProperty annotations.
- **DinHeaderRequest.java**: Define common header structure with all required fields and validation annotations like @NotBlank.
- **DinBodyConsultarRequest.java**: Create body DTO with tipoIdentificacion, numeroIdentificacion, codCategoriaServicio, and tipoPago fields with appropriate validations.
- **PaginadoRequest.java**: Define pagination request DTO with cantRegistros, numTotalPag, and numPagActual fields.
- **ConsultarServiciosCategoriaResponse.java**: Create response DTO containing dinHeader, dinBody, and dinError fields with @JsonProperty annotations.
- **DinHeaderResponse.java**: Define response header structure mirroring the request header structure.
- **DinBodyConsultarResponse.java**: Create response body DTO containing listaCategorias field as List<CategoriaServicioDto>.
- **CategoriaServicioDto.java**: Define category DTO with codigoCategoria, descripcionCategoria, descripcionLargaCategoria, and linkImagen fields.
- **DinErrorResponse.java**: Create error response DTO with tipo, fecha, codigo, origen, codigoErrorProveedor, mensaje, and detalle fields.
- **PaginadoResponse.java**: Define pagination response DTO mirroring the request pagination structure.

### Infrastructure Layer - Mapping
- **ServiciosCategoriaMapper.java**: Implement MapStruct mapper interface to convert between DTOs and domain objects with @Mapper annotation.

### Infrastructure Layer - Persistence
- **ServiciosCategoriaRepository.java**: Create JPA repository interface extending JpaRepository with custom query methods for categoria servicio operations.
- **CategoriaServicioEntity.java**: Define JPA entity with @Entity annotation and appropriate field mappings for categoria servicio table.
- **ServiciosCategoriaRepositoryAdapter.java**: Implement repository adapter that bridges domain repository port with JPA repository, applying @Component annotation.

### Infrastructure Layer - External
- **ServiciosCategoriaExternalClient.java**: Implement AS400 external client using the MANDATORY architecture-spring-model-as400 library with RequestAS400 and ResponseAS400 wrappers.

### Infrastructure Layer - Configuration
- **WebConfig.java**: Create web configuration class with @Configuration annotation for web-related beans and settings.
- **DatabaseConfig.java**: Define database configuration class with @Configuration annotation for JPA and transaction management setup.

### Application Layer
- **ServiciosCategoriaApplicationService.java**: Create application service orchestrator with @Service annotation that coordinates use cases and handles cross-cutting concerns.
- **ConsultarServiciosCategoriaUseCase.java**: Implement use case with business logic for consultar servicios categoria operation, applying @Component annotation.
- **ConsultarServiciosCategoriaPort.java**: Define input port interface with execute method for the consultar operation.
- **ServiciosCategoriaRepositoryPort.java**: Create output port interface defining repository operations needed by the domain.
- **ServiciosCategoriaExternalPort.java**: Define output port interface for external service communications.

### Domain Layer
- **CategoriaServicio.java**: Create domain model with business logic and validation rules, implementing domain behavior methods.
- **Cliente.java**: Define client domain model with identification and validation logic.
- **Paginacion.java**: Create pagination domain model with page calculation and validation logic.
- **TipoIdentificacion.java**: Implement value object for tipo identificacion with validation and business rules.
- **NumeroIdentificacion.java**: Create value object for numero identificacion with format validation and business logic.
- **CodigoCategoriaServicio.java**: Define value object for categoria servicio code with validation rules.
- **TipoPago.java**: Implement value object for tipo pago with allowed values and validation.
- **ServiciosCategoriaException.java**: Create domain exception extending RuntimeException for servicios categoria specific errors.
- **ClienteNotFoundException.java**: Define specific exception for cliente not found scenarios extending ServiciosCategoriaException.

### Resources
- **application.yml**: Configure main application properties including server port, database connection, and AS400 integration settings.
- **application-dev.yml**: Define development environment specific configurations with debug settings and local database.
- **application-prod.yml**: Create production environment configurations with optimized settings and production database.
- **V1__create_categoria_servicio_table.sql**: Write Flyway migration script to create categoria_servicio table with appropriate indexes and constraints.

### Testing
- **ServiciosCategoriaControllerTest.java**: Create integration tests for the REST controller using @WebMvcTest and MockMvc.
- **ConsultarServiciosCategoriaUseCaseTest.java**: Implement unit tests for the use case with @ExtendWith(MockitoExtension.class) and mock dependencies.
- **CategoriaServicioTest.java**: Write unit tests for domain model validation and business logic using JUnit 5.

### Build Configuration
- **pom.xml**: Configure Maven build with Java 21, Spring Boot dependencies, AS400 library dependency, and required plugins for compilation and testing.