## Architecture de la Base de Données (Méthode Merise)

### 1. Modèle Conceptuel de Données (MCD)
Ce diagramme illustre les règles de gestion métier et les cardinalités (0,n / 1,1) entre nos entités.

```mermaid
flowchart LR
    %% Entités
    U["UTILISATEUR<br>id<br>first_name<br>last_name<br>email<br>password<br>is_admin"]
    L["LIEU<br>id<br>title<br>description<br>price<br>latitude<br>longitude"]
    A["AVIS<br>id<br>text<br>rating"]
    C["COMMODITE<br>id<br>name"]

    %% Associations
    POSSEDE((POSSEDE))
    ECRIT((ECRIT))
    CONCERNE((CONCERNE))
    DISPOSE((DISPOSE))

    %% Cardinalités
    U ---|"0,n"| POSSEDE ---|"1,1"| L
    U ---|"0,n"| ECRIT ---|"1,1"| A
    L ---|"0,n"| CONCERNE ---|"1,1"| A
    L ---|"0,n"| DISPOSE ---|"0,n"| C
```

### 2. Modèle Logique de Données (MLD)
Ce diagramme traduit le MCD en tables relationnelles prêtes pour SQL, avec l'apparition des Clés Étrangères (FK) et de la table d'association `LIEU_COMMODITE` issue de la relation "0,n --- 0,n".

```mermaid
erDiagram
    UTILISATEUR {
        string id PK
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
    }

    LIEU {
        string id PK
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id FK
    }

    AVIS {
        string id PK
        string text
        int rating
        string user_id FK
        string place_id FK
    }

    COMMODITE {
        string id PK
        string name
    }

    LIEU_COMMODITE {
        string place_id PK,FK
        string amenity_id PK,FK
    }

    %% Relations
    UTILISATEUR ||--o{ LIEU : "possède (owner_id)"
    UTILISATEUR ||--o{ AVIS : "écrit (user_id)"
    LIEU ||--o{ AVIS : "reçoit (place_id)"
    LIEU ||--o{ LIEU_COMMODITE : "inclut"
    COMMODITE ||--o{ LIEU_COMMODITE : "est dans"
```
