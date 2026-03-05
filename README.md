![E-Commerce_API icon](https://github.com/Revasall/E-Commerce_FastAPI/blob/master/images/e-commerce_api_image.png)

# **E-Commerce FastAPI** 




E-commerce FastAPI is a robust backend API for online retail platforms, demonstrating the competent creation and interaction of complex data models, seamless integration with external services, and secure user authentication. All built with a focus on performance and scalability.

## **Tech Stack**
![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![fastapi](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

- **Framework**: FastAPI (Asynchronous Python web framework)
- **Database & ORM**: PostgreSQL with asyncpg, SQLAlchemy 2.0 (Mapped Declarative Models), Alembic for migrations.
- **Security**: JWT (JSON Web Tokens) for authentication, Argon2 for high-security password hashing.
- **Payment Integration**: Yookassa SDK for automated payment processing.
Stability & Protection: SlowAPI for rate limiting and DDoS protection.
- **DevOps**: Docker & Docker Compose for containerization and easy deployment.
- **Testing**: Pytest with an asynchronous SQLite in-memory database.

Other libraries and technologies used can be found in requirements.txt.

## Features

- __Secure Authentication (JWT & OAuth2)__
  - OAuth2 with Password Grant: Implemented standard-compliant login flow with Access and Refresh tokens.
  - Password Hashing: Industry-standard security using the Passlib library (bcrypt) to ensure no raw passwords are ever stored.
  - Stateless Authorization: Custom middleware/dependencies to verify, decrypt, and validate JWT tokens for secure resource access.

- __Asynchronous CRUD Operations__
  - Full lifecycle management for users, categories, products, carts, and orders using FastAPI and SQLAlchemy.
  - Optimized for high performance with fully asynchronous database interactions.

- __Robust Service Architecture__
  - Implemented Service Layer pattern with Pydantic schemas for clean separation of concerns.
  - Centralized business logic for authentication, complex data transformations, and the checkout workflow (cart-to-order conversion).

- __Security & Payments__
  - Rate Limiting: Every endpoint is protected against brute-force and DDoS attacks.
  - Payment Webhooks: Integrated asynchronous payment confirmation system for reliable order status synchronization.
 
- __Seamless Payment Integration__
  - YooKassa Gateway: Fully integrated payment processing supporting multiple payment methods for a smooth checkout experience.
  - Asynchronous Fulfillment: Robust webhook handling to capture real-time payment confirmations and automatically update order statuses.
  - Idempotency & Security: Designed to handle sensitive transaction data securely, ensuring reliable processing and preventing duplicate charges.
 
- __Comprehensive Testing Suite__
  - Pytest Framework: A robust suite of unit and integration tests covering core business logic and API endpoints.
  - Asynchronous Test Environment: Utilizes a dedicated In-Memory SQLite database with an asynchronous engine to ensure fast and isolated test execution.
  - Mocking & Fixtures: Extensively uses Pytest fixtures and Mock sessions to simulate external service responses (like payment gateways) and manage database state without side effects.

 ## Project Architecture
 **Decription**: The project is built using Layered Architecture. This allows for the separation of HTTP request processing logic from business logic and database interactions, making the code clean and suitable for testing, editing, and scaling.

![Architecture scheme](https://github.com/Revasall/E-Commerce_FastAPI/blob/master/images/architecture.png)
### **Main layers**:
- **API Layer (Endpoints)**:
  - Accepts HTTP requests.
  - Uses FastAPI Dependencies to validate tokens and retrieve the current user.
  - Calls methods from the Service Layer. Does not contain complex business logic.

- **Service Layer (Business Logic)**:
  - The "brains" of the application. Calculations, access rights checks, and complex operations occur here.

- **Data Access Layer (Models & Repository)**:
  - SQLAlchemy 2.0 models describing the table structure.
  - Uses asynchronous sessions for non-blocking interaction with PostgreSQL.

- **Schemas (Pydantic)**:
  - Define data contracts. Incoming data (DTO) is validated before processing, and outgoing data is filtered (for example, to avoid sending a password hash in the response).

The project follows a modular layered architecture to ensure separation of concerns and scalability.

### Database Schema
![DB Architecture](https://github.com/Revasall/E-Commerce_FastAPI/blob/master/images/DB%20architecture.png)

The database is designed with strict relational integrity. Key features include:
* **Order Snapshots:** Product prices are captured at the moment of purchase in `Order Items` to preserve historical accuracy.
* **Asynchronous Access:** Full compatibility with `asyncpg` for non-blocking DB operations.
* **Strict Typing:** Extensive use of PostgreSQL Enums for Order Statuses and User Roles.


 
