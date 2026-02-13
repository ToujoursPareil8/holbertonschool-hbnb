Technical Design Document: HBnB Evolution

## Table of Contents

- [Introduction](#introduction)
- [High-Level Package Diagram](#high-level-package-diagram)
- [Class Diagram for Business Logic Layer](#class-diagram-for-business-logic-layer)
- [Diagram Legend](#Diagram-Legend)
- [Sequence Diagrams for API Calls](#sequence-diagrams-for-api-calls)
- [Legend - UML Sequence Diagram](#Legend-UML-Sequence-Diagram)
- [HBNB Project - Technical Documentation](#HBNB-Project-Technical-Documentation)
- [How to Use](#how-to-use)
- [Tool Used](#Tool-used)
- [Author](#author)


---

## Introduction
Project Overview

The HBnB Evolution project is a web-based vacation rental application designed to emulate core functionalities of platforms like Airbnb. The system allows users to create accounts, list properties, submit reviews, and share listings via external social media platforms.
Purpose and Scope

This document serves as the primary technical blueprint. Its goal is to guide the implementation phase by providing a clear representation of the system architecture, defining structural boundaries, core domain entities, and the dynamic flow of data for key operations.

---
## Diagram Legend 

| Symbol / Notation        | Description                                                                                |
|--------------------------|--------------------------------------------------------------------------------------------|
| `1 → *`                  | One-to-Many relationship (e.g., one `User` owns many `Places`).                            |
| `* → *`                  | Many-to-Many relationship (e.g., a `Place` offers multiple `Amenities`, and vice versa).   |
| `1 → 1`                  | One-to-One relationship.                                                                   |
| `0 → 1`                  | Optional relationship (zero or one).                                                       |
| `0 → *`                  | Optional One-to-Many (e.g., an entity may have zero or more related items).                |
| ➝ (Solid Arrow)          | Association (basic link between classes).                                                  |
| ◆ (Empty Diamond)        | Aggregation (shared ownership; lifetime of contained object is independent).               |
| ◼︎ (Filled Diamond)       | Composition (strong ownership; if the container is destroyed, so is the contained object). |
| △ (Triangle Arrow)       | Inheritance / Generalization (one class inherits from another).                            |

---

## High-Level Package Diagram
<img width="7222" height="5045" alt="hbnb_hlp_v2" src="https://github.com/user-attachments/assets/48c0da62-cdc9-41d6-937d-4d8fcc4ef007" />

The HBnB application utilizes a Three-Layer Architecture integrated with the Facade Design Pattern.
Extrait de code


    
Explanatory Notes

Purpose: To illustrate the separation of concerns.

Design Decisions: The Facade Pattern decouples the API from internal business rules, ensuring the presentation layer remains "thin" and only interacts with a single entry point.

---

## Business Logic Layer

<img width="4235" height="5420" alt="Christmas Shopping Decision-2026-02-13-094341" src="https://github.com/user-attachments/assets/af749bab-1346-49aa-923a-aa0665d24891" />

This section details the static structure of the domain model.


Explanatory Notes

Composition: Review instances are strictly composed within a Place, meaning they cannot exist without a parent property.

Utility Services: SocialMediaService is a stateless utility designed to format URLs for external platforms without requiring database persistence.

---

## Sequence Diagram

I. User Registration
<img width="6427" height="4405" alt="sequence_user_registration" src="https://github.com/user-attachments/assets/04380ae7-aa31-4d47-80a7-ceb8eb29ed23" />



II. Place Creation
<img width="6277" height="4395" alt="sequence_placeCreation" src="https://github.com/user-attachments/assets/150a7fec-d0bd-44a6-ac9b-10d9c80f8f17" />




III. Review Submission
<img width="6242" height="3940" alt="sequence_reviewSubmissions" src="https://github.com/user-attachments/assets/00a87930-e8b1-4c22-b3ef-4357fdfbc465" />



IV. Fetching a List of Places
<img width="7107" height="4350" alt="sequence_fetchingList" src="https://github.com/user-attachments/assets/1de9e980-b197-4a7c-9acf-e8827cf421a4" />



V. Social Media Sharing
<img width="8192" height="3551" alt="sequence_SocialMediaSharing" src="https://github.com/user-attachments/assets/16b47d17-83c6-40d7-aeb3-a0f025d1f423" />

## Legend - UML Sequence Diagram 

| Symbol                    | Meaning                                                                    |
|---------------------------|----------------------------------------------------------------------------|
| Actor                     | External entity (e.g., user) that interacts with the system.               |
| `->`                      | Synchronous message or method call.                                        |
| `-->`                     | Asynchronous message.                                                      |
| `-->>` or dashed arrow    | Return message or response.                                                |
| `alt` / `opt` / `loop`    | Control blocks: alternative, optional, or loop.                            |
| `activate` / `deactivate` | Object's activation bar (lifeline emphasis).                               |
| Lifeline (vertical line)  | Represents the lifespan of a participant during the interaction.           |

---

## How to Use

(This section is intentionally left blank for project-specific deployment, installation, and usage instructions.)

---

## Authors

Jason Jean Louis, Farid Ghaib
