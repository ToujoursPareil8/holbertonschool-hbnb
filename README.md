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
- [License](#license)

---

## Introduction
Project Overview

The HBnB Evolution project is a web-based vacation rental application designed to emulate core functionalities of platforms like Airbnb. The system allows users to create accounts, list properties, submit reviews, and share listings via external social media platforms.
Purpose and Scope

This document serves as the primary technical blueprint. Its goal is to guide the implementation phase by providing a clear representation of the system architecture, defining structural boundaries, core domain entities, and the dynamic flow of data for key operations.

---

## High-Level Package Diagram

The HBnB application utilizes a Three-Layer Architecture integrated with the Facade Design Pattern.
Extrait de code


    
Explanatory Notes

Purpose: To illustrate the separation of concerns.

Design Decisions: The Facade Pattern decouples the API from internal business rules, ensuring the presentation layer remains "thin" and only interacts with a single entry point.

---

## Business Logic Layer

This section details the static structure of the domain model.
Extrait de code


Explanatory Notes

Composition: Review instances are strictly composed within a Place, meaning they cannot exist without a parent property.

Utility Services: SocialMediaService is a stateless utility designed to format URLs for external platforms without requiring database persistence.

---

## API Interaction Flow
I. User Registration

---

II. Place Creation

---

III. Review Submission

---

IV. Fetching a List of Places

---

V. Social Media Sharing

---

## How to Use

(This section is intentionally left blank for project-specific deployment, installation, and usage instructions.)

---

## Authors

Jason Jean Louis, Farid Ghaib
