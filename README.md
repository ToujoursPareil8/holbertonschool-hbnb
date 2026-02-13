Technical Design Document: HBnB Evolution
Table of Contents

    Introduction

    High-Level Architecture

    Business Logic Layer

    API Interaction Flow

        I. User Registration

        II. Place Creation

        III. Review Submission

        IV. Fetching a List of Places

        V. Social Media Sharing

    How to Use

    Authors

Introduction
Project Overview

The HBnB Evolution project is a web-based vacation rental application designed to emulate core functionalities of platforms like Airbnb. The system allows users to create accounts, list properties, submit reviews, and share listings via external social media platforms.
Purpose and Scope

This document serves as the primary technical blueprint. Its goal is to guide the implementation phase by providing a clear representation of the system architecture, defining structural boundaries, core domain entities, and the dynamic flow of data for key operations.
High-Level Architecture

The HBnB application utilizes a Three-Layer Architecture integrated with the Facade Design Pattern.
Extrait de code

classDiagram
    classDef layer fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef interface fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,stroke-dasharray: 5 5;
    
    namespace Presentation_Layer {
        class Service_API {
            +handle_request()
            +format_response()
        }
    }

    namespace Business_Logic_Layer {
        class HBnB_Facade {
            <<Interface>>
            +register_user()
            +create_place()
            +add_review()
            +get_place_share_link()
        }
        class Domain_Models {
            +User
            +Place
            +Review
            +Amenity
        }
        class External_Services {
            +SocialMediaService
        }
    }

    namespace Persistence_Layer {
        class Repository {
            +save()
            +get()
            +update()
            +delete()
        }
        class Database_Access {
            <<Data Store>>
        }
    }

    Service_API --> HBnB_Facade : Calls (Facade Pattern)
    HBnB_Facade --> Domain_Models : Manipulates
    HBnB_Facade --> External_Services : Uses (Utilities)
    HBnB_Facade --> Repository : Persists Data
    Repository --> Database_Access : SQL/NoSQL Ops

    class Service_API layer
    class HBnB_Facade interface
    class Domain_Models layer
    class External_Services layer
    class Repository layer

Explanatory Notes

    Purpose: To illustrate the separation of concerns.

    Design Decisions: The Facade Pattern decouples the API from internal business rules, ensuring the presentation layer remains "thin" and only interacts with a single entry point.

Business Logic Layer

This section details the static structure of the domain model.
Extrait de code

classDiagram
    class BaseModel {
        +UUID4 id
        +datetime created_at
        +datetime updated_at
        +save()
        +update(data)
    }

    class User {
        +string email
        +string password
        +string first_name
        +string last_name
        +bool is_admin
        +authenticate()
    }

    class Place {
        +string title
        +string description
        +float price
        +float latitude
        +float longitude
        +string owner_id
        +list reviews
        +list amenities
        +get_share_metadata()
    }

    class Review {
        +string text
        +int rating
        +string user_id
        +string place_id
    }

    class Amenity {
        +string name
        +string description
    }

    class SocialMediaService {
        <<Utility>>
        +dict PLATFORMS
        +generate_url(title, url, platform)$
    }

    User --|> BaseModel
    Place --|> BaseModel
    Review --|> BaseModel
    Amenity --|> BaseModel

    User "1" --o "0..*" Place : owns
    User "1" --o "0..*" Review : writes
    Place "1" *-- "0..*" Review : contains
    Place "0..*" -- "0..*" Amenity : has
    
    Place ..> SocialMediaService : supplies data to

Explanatory Notes

    Composition: Review instances are strictly composed within a Place, meaning they cannot exist without a parent property.

    Utility Services: SocialMediaService is a stateless utility designed to format URLs for external platforms without requiring database persistence.

API Interaction Flow
I. User Registration
Extrait de code

sequenceDiagram
    participant Client
    participant API as API Layer
    participant Facade as HBnB Facade
    participant DB as Persistence Layer
    participant Model as User Model

    Client->>API: POST /users (data)
    API->>Facade: register_user(data)
    
    Facade->>DB: get_by_attribute("email", data.email)
    DB-->>Facade: Returns None (Email unique)
    
    alt Email is Unique
        Facade->>Model: Create User(data)
        Model-->>Facade: User Instance
        Facade->>DB: save(User)
        DB-->>Facade: Success
        Facade-->>API: Return User DTO
        API-->>Client: 201 Created
    else Email Exists
        Facade-->>API: Error (Conflict)
        API-->>Client: 400 Bad Request
    end

II. Place Creation
Extrait de code

sequenceDiagram
    participant Client
    participant API as API Layer
    participant Facade as HBnB Facade
    participant DB as Persistence Layer
    participant Model as Place Model

    Client->>API: POST /places (data)
    API->>Facade: create_place(data)
    
    Facade->>DB: get_by_id(data.owner_id, "User")
    DB-->>Facade: User Object / None

    alt Owner Exists
        Facade->>Model: Create Place(data)
        Model-->>Facade: Place Instance
        Facade->>DB: save(Place)
        DB-->>Facade: Success
        Facade-->>API: Return Place DTO
        API-->>Client: 201 Created
    else Owner Not Found
        Facade-->>API: Error (Invalid)
        API-->>Client: 404 Not Found
    end

III. Review Submission
Extrait de code

sequenceDiagram
    participant Client
    participant API as API Layer
    participant Facade as HBnB Facade
    participant DB as Persistence Layer
    participant Model as Review Model

    Client->>API: POST /reviews (data)
    API->>Facade: add_review(data)

    par Validate Entities
        Facade->>DB: get_by_id(data.user_id, "User")
        Facade->>DB: get_by_id(data.place_id, "Place")
    end
    DB-->>Facade: User & Place exist

    Facade->>Model: Create Review(data)
    Model-->>Facade: Review Instance
    Facade->>DB: save(Review)
    DB-->>Facade: Success

    Facade-->>API: Return Review DTO
    API-->>Client: 201 Created

IV. Fetching a List of Places
Extrait de code

sequenceDiagram
    participant Client
    participant API as API Layer
    participant Facade as HBnB Facade
    participant DB as Persistence Layer
    participant Model as Place Model

    Client->>API: GET /places?price_max=100
    API->>Facade: get_all_places(filters={'price_max': 100})
    
    Facade->>DB: get_all("Place")
    DB-->>Facade: List of [Place Instances]
    
    loop Filtering and Mapping
        Facade->>Model: validate_filters(place, filters)
        alt Matches Criteria
            Model-->>Facade: True
            Facade->>Facade: Add to result_list
        else Doesn't Match
            Model-->>Facade: False
        end
    end
    
    Facade-->>API: List of Place DTOs
    API-->>Client: 200 OK (JSON List)

V. Social Media Sharing
Extrait de code

sequenceDiagram
    participant Client
    participant API as API Layer
    participant Facade as HBnB Facade
    participant DB as Persistence Layer
    participant Model as Place Model
    participant Service as SocialMediaService

    Client->>API: GET /places/{id}/share?platform=twitter
    API->>Facade: get_place_share_link(id, "twitter")
    
    Facade->>DB: get_by_id(id, "Place")
    DB-->>Facade: Place Instance
    
    Facade->>Model: get_share_metadata()
    Model-->>Facade: {title, base_url}
    
    Facade->>Service: generate_url(title, base_url, "twitter")
    Note over Service: Specific URL Encoding
    Service-->>Facade: formatted_share_url
    
    Facade-->>API: formatted_share_url
    API-->>Client: 200 OK (JSON with link)

How to Use

(This section is intentionally left blank for project-specific deployment, installation, and usage instructions.)
Authors

    [Your Name/Team Name] - Technical Architect & UML Designer
