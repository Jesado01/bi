# API Requirements Document: Payment Order Confirmation Service

## Project Overview

This project implements a REST API service for retrieving payment order confirmations based on party identification and establishment directory information. The service provides active payment services for a given category and establishment, following Domain-Driven Design (DDD) architecture principles with multi-module approach.

## Technology Stack

- **Language**: Java 21
- **Framework**: Spring Boot
- **Architecture**: DDD Architecture multi-module approach
- **Build Tool**: Maven
- **Database**: JPA/Hibernate compatible database
- **Validation**: Bean Validation (JSR-303)
- **JSON Processing**: Jackson
- **Testing**: JUnit 5, Mockito

## API Endpoint Details

### Endpoint Information
- **Method**: POST
- **Path**: `/v1/order-confirmation/retrieve`
- **Operation ID**: `V1OrderConfirmationRetrieve_POST`
- **Content-Type**: application/json
- **Description**: Informa los servicios activos para el pago a partir de una categoria y un comercio.

### Required Headers
- `clientId` (string, required)
- `applicationId` (string, required) - Example: "ONBTCH"
- `channelId` (string, required) - Example: "IN"
- `language` (string, required)
- `portalId` (string, required)
- `ipAddress` (string, required) - Example: "10.0.0.0"

### Optional Headers
- `sessionId` (string)
- `device` (string) - Example: "ONB"
- `transactionId` (string) - Example: "PRUEBA5"
- `transactionDate` (string) - Example: "2023:02:24T09:23:06:486"
- `symmetricKey` (string)
- `userId` (string)
- `recordsAmount` (number) - Example: 0
- `pagesAmount` (number) - Example: 0
- `pagesCurrentIndex` (number) - Example: 1

## Request/Response Models

### Request Model: `retrieveOrderConfirmationRq`

```json
{
  "orderConfirmation": {
    "partyReference": {
      "partyIdentification": {
        "mainPartyIdentificationType": "integer",
        "mainIdentifierValue": "string"
      }
    },
    "establishmentDirectoryReference": {
      "categoryCode": "string",
      "categoryDescription": "string",
      "establishmentCode": "string",
      "banredEstablishmentCode": "string",
      "establishmentName": "string",
      "establishmentDescription": "string",
      "establishmentTaxId": "string"
    },
    "paymentOrderType": "string",
    "screenType": "string"
  }
}
```

### Response Model: `retrieveOrderConfirmationRs`

```json
{
  "orderConfirmation": {
    "serviceList": [
      {
        "serviceCode": "string",
        "banredServiceCode": "string",
        "serviceDescription": "string",
        "formId": "string",
        "imageUrl": "string",
        "paymentType": "string",
        "businessDayDate": "string",
        "maxFileUploadTime": "string",
        "brandList": [
          {
            "entityCode": "string",
            "brandCode": "string",
            "isDinersAccount": "string"
          }
        ]
      }
    ]
  }
}
```

### Error Response Model: `commonErrorRs`

```json
{
  "statusCode": "string",
  "status": "string",
  "message": ["string"],
  "statusType": "string",
  "transactionDate": "string",
  "transactionTime": "string",
  "providerCode": "string",
  "description": "string",
  "origin": "string"
}
```

## HTTP Status Codes and Error Responses

- **200 OK**: Successful response with service list
- **400 Bad Request**: Invalid request format or missing required fields
- **404 Not Found**: Requested resource not found
- **422 Unprocessable Content**: Request validation failed
- **500 Internal Server Error**: Server-side error

## Domain Models (Required for Domain Layer)

### Core Domain Models

#### OrderConfirmation
- **partyReference**: PartyReference
- **establishmentDirectoryReference**: EstablishmentDirectoryReference
- **paymentOrderType**: String (optional)
- **screenType**: String (optional)

#### PartyReference
- **partyIdentification**: PartyIdentification

#### PartyIdentification
- **mainPartyIdentificationType**: Integer (Tipo de identificación)
- **mainIdentifierValue**: String (Número de identificación)

#### EstablishmentDirectoryReference
- **categoryCode**: String (Código de categoría)
- **categoryDescription**: String (Descripción de la categoría)
- **establishmentCode**: String (Código del comercio)
- **banredEstablishmentCode**: String (Código Banred del comercio)
- **establishmentName**: String (Nombre del comercio)
- **establishmentDescription**: String (Descripción del comercio)
- **establishmentTaxId**: String (RUC del comercio)

#### ServiceDirectoryEntry
- **serviceCode**: String (Código del servicio)
- **banredServiceCode**: String (Código Banred del servicio)
- **serviceDescription**: String (Descripción del servicio)
- **formId**: String (ID del formulario)
- **imageUrl**: String (URL de la imagen)
- **paymentType**: String (Tipo de pago)
- **businessDayDate**: String (Fecha día hábil)
- **maxFileUploadTime**: String (Hora máxima para cargar archivo)
- **brandList**: List<BrandDirectoryEntry>

#### BrandDirectoryEntry
- **entityCode**: String (Código de la entidad)
- **brandCode**: String (Código de la marca)
- **isDinersAccount**: String (Indica si es cuenta Diners)

## Proposed Project Structure

## Proposed Project Structure

```
payment-order-confirmation-service/
├── pom.xml                                    (Parent POM)
├── domain/
│   ├── pom.xml
│   └── src/main/java/com/paymentservice/orderconfirmation/
│       ├── domain/
│       │   ├── model/
│       │   │   ├── OrderConfirmation.java
│       │   │   ├── PartyReference.java
│       │   │   ├── PartyIdentification.java
│       │   │   ├── EstablishmentDirectoryReference.java
│       │   │   ├── Service.java
│       │   │   └── Brand.java
│       │   ├── valueobject/
│       │   │   ├── ServiceCode.java
│       │   │   ├── CategoryCode.java
│       │   │   ├── EstablishmentCode.java
│       │   │   └── PaymentType.java
│       │   └── repository/
│       │       └── OrderConfirmationRepository.java
├── application/
│   ├── pom.xml
│   └── src/main/java/com/paymentservice/orderconfirmation/
│       ├── application/
│       │   ├── service/
│       │   │   └── OrderConfirmationService.java
│       │   ├── usecase/
│       │   │   └── RetrieveOrderConfirmationUseCase.java
│       │   └── dto/
│       │       ├── request/
│       │       │   └── RetrieveOrderConfirmationRequest.java
│       │       └── response/
│       │           ├── RetrieveOrderConfirmationResponse.java
│       │           └── CommonErrorResponse.java
└── infrastructure/
    ├── pom.xml
    └── src/main/java/com/paymentservice/orderconfirmation/
        ├── PaymentOrderConfirmationApplication.java    <-- Main class
        ├── infrastructure/
        │   ├── persistence/
        │   │   ├── entity/
        │   │   │   ├── OrderConfirmationEntity.java
        │   │   │   ├── ServiceEntity.java
        │   │   │   └── BrandEntity.java
        │   │   ├── repository/
        │   │   │   └── JpaOrderConfirmationRepository.java
        │   │   └── mapper/
        │   │       └── OrderConfirmationMapper.java
        │   └── config/
        │       ├── DatabaseConfig.java
        │       └── ValidationConfig.java
        └── presentation/
            └── api/
                ├── controller/
                │   └── OrderConfirmationController.java
                ├── dto/
                │   ├── request/
                │   │   └── RetrieveOrderConfirmationRq.java
                │   └── response/
                │       ├── RetrieveOrderConfirmationRs.java
                │       └── CommonErrorRs.java
                ├── mapper/
                │   └── OrderConfirmationApiMapper.java
                └── validation/
                    └── RequestValidator.java
```

## File-by-File Requirements

### Main Application
- **PaymentOrderServiceApplication.java**: Create Spring Boot main class with `@SpringBootApplication` annotation and main method to bootstrap the application.

### Infrastructure Layer - Web
- **OrderConfirmationController.java**: Implement REST controller with `@PostMapping("/v1/order-confirmation/retrieve")` endpoint, validate all required headers, handle request/response mapping, and implement proper error handling.
- **RetrieveOrderConfirmationRequest.java**: Create main request DTO with `orderConfirmation` field and validation annotations.
- **OrderConfirmationRequest.java**: Implement order confirmation DTO with `partyReference`, `establishmentDirectoryReference`, `paymentOrderType`, and `screenType` fields.
- **PartyReferenceRequest.java**: Create party reference DTO containing `partyIdentification` field.
- **PartyIdentificationRequest.java**: Implement party identification DTO with `mainPartyIdentificationType` (Integer) and `mainIdentifierValue` (String) fields with validation.
- **EstablishmentDirectoryReferenceRequest.java**: Create establishment directory DTO with all establishment-related fields and validation constraints.
- **RetrieveOrderConfirmationResponse.java**: Implement main response DTO with `orderConfirmation` field.
- **OrderConfirmationResponse.java**: Create order confirmation response DTO containing `serviceList` field.
- **ServiceDirectoryEntryResponse.java**: Implement service directory entry DTO with all service fields and `brandList`.
- **BrandDirectoryEntryResponse.java**: Create brand directory entry DTO with `entityCode`, `brandCode`, and `isDinersAccount` fields.
- **CommonErrorResponse.java**: Implement error response DTO with all error fields matching the OpenAPI specification.
- **WebConfig.java**: Configure web layer settings, CORS, and JSON serialization.

### Infrastructure Layer - Persistence
- **OrderConfirmationRepository.java**: Create JPA repository interface extending `JpaRepository` with custom query methods for order confirmation operations.
- **ServiceDirectoryRepository.java**: Implement JPA repository for service directory operations with complex queries.
- **OrderConfirmationEntity.java**: Create JPA entity for order confirmation with proper annotations and relationships.
- **ServiceDirectoryEntity.java**: Implement JPA entity for service directory with field mappings and relationships.
- **BrandDirectoryEntity.java**: Create JPA entity for brand directory with appropriate annotations.
- **OrderConfirmationRepositoryAdapter.java**: Implement repository adapter bridging domain repository port with JPA repositories.

### Infrastructure Layer - Exception Handling
- **GlobalExceptionHandler.java**: Implement global exception handler with `@ControllerAdvice` for all HTTP status codes (400, 404, 422, 500) with proper error response mapping.
- **PaymentOrderException.java**: Create custom exception class for payment order specific errors.

### Application Layer
- **OrderConfirmationApplicationService.java**: Create application service orchestrating use case execution and DTO transformations with `@Service` annotation.
- **RetrieveOrderConfirmationUseCase.java**: Implement use case with business logic for retrieving order confirmations based on party identification and establishment information.
- **RetrieveOrderConfirmationPort.java**: Define input port interface with `retrieveOrderConfirmation` method.
- **OrderConfirmationRepositoryPort.java**: Create output port interface defining repository operations needed by the domain.
- **OrderConfirmationMapper.java**: Implement MapStruct mapper for converting between DTOs and domain objects with proper mapping annotations.

### Domain Layer - Models
- **OrderConfirmation.java**: Create domain aggregate root with business logic, validation rules, and relationships to other domain objects.
- **PartyReference.java**: Implement domain entity for party reference with business constraints.
- **PartyIdentification.java**: Create domain entity for party identification with validation logic.
- **EstablishmentDirectoryReference.java**: Implement domain entity for establishment directory with business rules.
- **ServiceDirectoryEntry.java**: Create domain entity for service directory with validation and business logic.
- **BrandDirectoryEntry.java**: Implement domain entity for brand directory with appropriate constraints.

### Domain Layer - Value Objects
- **PartyIdentificationType.java**: Create value object for party identification type with validation rules.
- **IdentifierValue.java**: Implement value object for identifier value with format validation.
- **CategoryCode.java**: Create value object for category code with business constraints.
- **EstablishmentCode.java**: Implement value object for establishment code with validation logic.
- **ServiceCode.java**: Create value object for service code with appropriate validation.

### Domain Layer - Services & Exceptions
- **OrderConfirmationDomainService.java**: Implement domain service containing complex business logic that doesn't belong to a single entity.
- **OrderConfirmationNotFoundException.java**: Create specific exception for order confirmation not found scenarios.
- **InvalidPartyIdentificationException.java**: Implement exception for invalid party identification validation failures.

### Configuration Files
- **application.yml**: Configure main application properties including server port, database connection, and logging levels.
- **application-dev.yml**: Define development environment specific configurations with debug settings.
- **application-prod.yml**: Create production environment configurations with optimized settings.
- **pom.xml**: Configure Maven dependencies including Spring Boot, JPA, validation, MapStruct, and testing frameworks.

### Test Files
- **OrderConfirmationControllerTest.java**: Create integration tests for REST controller using `@WebMvcTest` and MockMvc with all HTTP status code scenarios.
- **RetrieveOrderConfirmationUseCaseTest.java**: Implement unit tests for use case logic with mocked dependencies and comprehensive test coverage.
- **OrderConfirmationDomainServiceTest.java**: Write unit tests for domain service business logic with edge cases and validation scenarios.

## Business Rules and Validations

1. **Party Identification Validation**: `mainPartyIdentificationType` must be a valid integer and `mainIdentifierValue` must be a non-empty string.
2. **Establishment Directory Validation**: All establishment fields must be validated for proper format and business constraints.
3. **Service Directory Filtering**: Services must be filtered based on category and establishment criteria.
4. **Brand Association**: Each service must have associated brands with proper entity and brand codes.
5. **Payment Type Validation**: Payment order type must be validated against allowed values.
6. **Error Handling**: All errors must follow the `commonErrorRs` structure with appropriate status codes and messages.

## External Dependencies

The service may require integration with external systems for retrieving service directory information and validating party identification data. All external integrations should follow the established patterns and include proper error handling and timeout configurations.