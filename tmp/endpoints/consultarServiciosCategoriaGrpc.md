# Project Name: Servicios Categoria gRPC Service

## Overview

This project implements a gRPC service for consulting service categories based on identification type, identification number, category code, and payment type. The service follows Domain-Driven Design (DDD) architecture with a multi-module approach, providing the `consultarServiciosCategoria` operation through Protocol Buffers communication.

## Technology Stack

- **Language**: Java 21
- **Framework**: Spring Boot
- **Architecture**: DDD Architecture multi-module approach
- **Communication Protocol**: gRPC with Protocol Buffers
- **Port**: 9000

## Endpoint Details

**Service**: gRPC Service  
**Port**: 9000  
**Protocol**: gRPC  
**Style**: Protocol Buffers  
**Operation**: consultarServiciosCategoria

### Request Structure
```protobuf
message ServiciosCategoriaRequest {
  Header dinHeader = 1;
  BodyResquestServiciosCategoria dinBody = 2;
}

message Header {
  string aplicacionId = 1;
  string canalId = 2;
  string sesionId = 3;
  string dispositivo = 4;
  string idioma = 5;
  string portalId = 6;
  string uuid = 7;
  string ip = 8;
  string horaTransaccion = 9;
  string llaveSimetrica = 10;
  string usuario = 11;
  PaginadoHeader paginado = 12;
  repeated TagsHeader tags = 13;
}

message BodyResquestServiciosCategoria {
  string tipoIdentificacion = 1;
  string numeroIdentificacion = 2;
  string codCategoriaServicio = 3;
  string tipoPago = 4;
}
```

### Response Structure
```protobuf
message ServiciosCategoriaResponse {
  Header dinHeader = 1;
  BodyResponseServiciosCategoria dinBody = 2;
  Error dinError = 3;
}

message BodyResponseServiciosCategoria {
  repeated Categorias listaCategorias = 1;
}

message Categorias {
  string codigoCategoria = 1;
  string descripcionCategoria = 2;
  string descripcionLargaCategoria = 3;
  string linkImagen = 4;
}
```

## External Dependencies

### AS400 Integration (MANDATORY)

This service requires integration with AS400 systems using the `architecture-spring-model-as400` library. The following approach is **REQUIRED** and must be followed:

- **Dependency**: `ec.com.dinersclub.architecture:architecture-spring-model-as400:1.0.0-SNAPSHOT`
- **Repository**: Azure DevOps Maven repository (`https://pkgs.dev.azure.com/devopsdc-1/a4ba58b4-b78e-4a80-8a19-597b84b9e314/_packaging/MavenCentral/maven/v1`)
- **Usage**: Implement `RequestAS400<T>` and `ResponseAS400<T>` wrappers with `HeaderAS400` for all AS400 communications
- **Error Handling**: Use `ErrorAS400` for standardized error management
- **Configuration**: Set programa, moduloRPG, and libraryList in HeaderAS400 for AS400 program execution

The AS400 integration must use the standardized classes and follow the complete usage guide provided. Alternative approaches are not permitted.

## Proposed Project Structure

```
src/main/java/com/company/servicios/
├── application/
│   ├── port/
│   │   ├── in/
│   │   │   └── ConsultarServiciosCategoriaUseCase.java
│   │   └── out/
│   │       └── ServiciosCategoriaRepositoryPort.java
│   └── service/
│       └── ConsultarServiciosCategoriaService.java
├── domain/
│   ├── model/
│   │   ├── Categoria.java
│   │   └── ServiciosCategoriaQuery.java
│   └── exception/
│       └── ServiciosCategoriaException.java
└── infrastructure/
    ├── adapter/
    │   ├── in/
    │   │   └── grpc/
    │   │       ├── ServiciosCategoriaGrpcController.java
    │   │       └── ServiciosCategoriaGrpcMapper.java
    │   └── out/
    │       └── persistence/
    │           ├── ServiciosCategoriaRepositoryAdapter.java
    │           └── ServiciosCategoriaJpaRepository.java
    └── config/
        └── GrpcServerConfig.java
src/main/proto/
└── servicios_categoria.proto
src/main/resources/
└── application.yml
```

## File-by-File Requirements

### Protocol Buffers Definition
- **src/main/proto/servicios_categoria.proto**: Define all Protocol Buffer messages including ServiciosCategoriaRequest, ServiciosCategoriaResponse, Header, body messages, Categorias, Error, PaginadoHeader, and TagsHeader with exact field mappings from the endpoint specification.

### gRPC Infrastructure Layer
- **src/main/java/com/company/servicios/infrastructure/adapter/in/grpc/ServiciosCategoriaGrpcController.java**: Implement the gRPC service interface with consultarServiciosCategoria method, validate request headers and body, delegate to use case, and handle gRPC-specific error responses.
- **src/main/java/com/company/servicios/infrastructure/adapter/in/grpc/ServiciosCategoriaGrpcMapper.java**: Create bidirectional mapping methods between gRPC messages and domain objects, including request-to-query mapping and domain-to-response mapping with proper error handling.

### Application Layer
- **src/main/java/com/company/servicios/application/port/in/ConsultarServiciosCategoriaUseCase.java**: Define the input port interface with consultarServiciosCategoria method accepting ServiciosCategoriaQuery and returning List<Categoria>.
- **src/main/java/com/company/servicios/application/service/ConsultarServiciosCategoriaService.java**: Implement the use case with business logic validation, orchestrate repository calls, and handle business exceptions with proper error mapping.
- **src/main/java/com/company/servicios/application/port/out/ServiciosCategoriaRepositoryPort.java**: Define the output port interface with methods for finding categories by identification type, number, category code, and payment type.

### Domain Layer
- **src/main/java/com/company/servicios/domain/model/ServiciosCategoriaQuery.java**: Create domain query object with tipoIdentificacion, numeroIdentificacion, codCategoriaServicio, tipoPago fields including validation rules and business constraints.
- **src/main/java/com/company/servicios/domain/model/Categoria.java**: Define domain entity with codigoCategoria, descripcionCategoria, descripcionLargaCategoria, linkImagen fields including domain validation and business rules.
- **src/main/java/com/company/servicios/domain/exception/ServiciosCategoriaException.java**: Create custom domain exception with error codes, messages, and proper exception hierarchy for business rule violations.

### Persistence Infrastructure Layer
- **src/main/java/com/company/servicios/infrastructure/adapter/out/persistence/ServiciosCategoriaRepositoryAdapter.java**: Implement the repository port using AS400 integration with RequestAS400/ResponseAS400 wrappers, proper HeaderAS400 configuration, and domain object mapping.
- **src/main/java/com/company/servicios/infrastructure/adapter/out/persistence/ServiciosCategoriaJpaRepository.java**: Define JPA repository interface extending JpaRepository with custom query methods for complex category searches and AS400 integration support.

### Configuration
- **src/main/java/com/company/servicios/infrastructure/config/GrpcServerConfig.java**: Configure gRPC server on port 9000, register service implementations, and set up interceptors for logging and error handling.
- **src/main/resources/application.yml**: Configure gRPC server properties (port 9000), AS400 connection settings, database configuration, logging levels, and service-specific properties.