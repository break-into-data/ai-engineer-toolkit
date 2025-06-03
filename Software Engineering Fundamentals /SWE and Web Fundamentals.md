This lesson dives into how web applications actually work—from frontend interfaces to backend logic and databases. Understanding how data moves across the web is crucial for any AI engineer aiming to build tools that are more than just local scripts. 

## 🎯 Learning Objectives

By completing this module, you'll be able to:

- Understand frontend/backend architecture
- Explore system design fundamentals
- Learn TypeScript basics for AI applications
- Master API concepts and implementation

---

## 📚 Day 12: Web Application Fundamentals

### Client-Side vs. Server-Side Development

### What You'll Learn:

- The distinction between frontend and backend
- How web applications communicate
- The request-response cycle

### Frontend (Client-Side)

- What users see and interact with (UI/UX)
- Runs in the user's browser
- Technologies: HTML, CSS, JavaScript, React, Vue, Angular
- Responsible for: Rendering UI, handling user interactions, making API calls

### Backend (Server-Side)

- Invisible to users but powers the application
- Runs on remote servers
- Technologies: Node.js, Python, Java, Go, etc.
- Responsible for: Business logic, data processing, authentication, database operations

### Frontend vs Backend

| Frontend (Client) | Backend (Server) |
| --- | --- |
| What user sees (UI) | Handles logic, databases |
| HTML, CSS, JS | Python, Node.js, Django, Express |
| Runs in browser | Runs on server |

Further Reading: https://www.fullstackfoundations.com/blog/client-side-vs-server-side

![ChatGPT Image May 1, 2025, 02_04_07 PM](https://github.com/user-attachments/assets/d4755402-bd4e-44c2-841c-95b0df007513)

*Image Resource: https://medium.com/@donotapply/client-side-vs-server-side-whats-the-difference-a933341cd60e*

### The Request-Response Cycle:

```mermaid
sequenceDiagram
    participant User
    participant Browser(Frontend/ Client side)
    participant Server
    participant Database

    User->>Browser(Frontend/ Client side): Clicks "Login"
    Browser(Frontend/ Client side)->>Server: POST /login {credentials}
    Server->>Database: Query user data
    Database->>Server: Return user record
    Server->>Browser(Frontend/ Client side): Response (success/error)
    Browser(Frontend/ Client side)->>User: Updates UI (dashboard/error)

```

![the_request_response_cycle.png](attachment:76752f86-a2b3-49f0-8f04-e47b82facc6c:25786552-348f-4832-91be-05ba41c46c63.png)

### Application Layers & Middleware

Web applications typically have several distinct layers:

### Presentation Layer

- User interfaces (websites, mobile apps)
- Handles rendering and user interaction
- Communicates with application layer via API

### Application Layer

- Core business logic and processing
- Handles requests from presentation layer
- Communicates with data layer

### Data Layer

- Database storage and retrieval
- Data persistence and management
- Structured or unstructured data storage

### Middleware

Software components that connect different application parts:

- Authentication middleware
- Logging middleware
- Error handling middleware
- API gateway

Further reading on Middleware - https://srivastavayushmaan1347.medium.com/understanding-middlewares-a-comprehensive-guide-with-practical-examples-c80383f888d5

**Different Layers of Modern Web Application Architecture**

![ChatGPT Image May 1, 2025, 02_07_23 PM.png](attachment:b35f582b-586d-47aa-b59d-61daefd9b5a1:ChatGPT_Image_May_1_2025_02_07_23_PM.png)

![Screenshot 2025-04-19 at 12.34.58 PM.png](attachment:38caae34-cd8c-4465-ac13-d633ff54a098:Screenshot_2025-04-19_at_12.34.58_PM.png)

*Image Resource:* https://www.sayonetech.com/blog/web-application-architecture/

Web Application Architecture Further Reading - https://www.sayonetech.com/blog/web-application-architecture/

### System Design Concepts

Reading - [System Design Basics](https://dev.to/kaustubhyerkade/system-design-fundamentals-a-complete-guide-for-beginners-3n95)

Key Components:

```mermaid
graph TD
    A[Client Application] -->|API Requests| B[API Gateway]
    B -->|Routes Requests| C[Application Servers]
    C -->|Read/Write Data| D[Database]
    C -->|Process| E[AI/ML Services]
    C -->|Store Files| F[File Storage]
    C -->|Cache Results| G[Cache]

```

![image.png](attachment:88614462-e72d-40d7-bf8b-6555d2384d32:image.png)

### Basic Application Data Flow:

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend API
    participant Database

    User->>Frontend: Makes request (click button)
    Frontend->>Backend API: Sends API request
    Backend API->>Database: Queries data
    Database->>Backend API: Returns data
    Backend API->>Frontend: Sends formatted response
    Frontend->>User: Updates UI with results

```

![image.png](attachment:c5a4c985-665b-4bf5-b7b7-6be15313fc9f:image.png)

### Example: AI-Powered Text Analysis App

```mermaid
graph LR
    A[User] -->|"1.Submits text"| B[Web Interface]
    B -->|"2.API Call"| C[Backend Server]
    C -->|"3.Analyze request"| D[AI Text Analysis API]
    D -->|"4.Results"| C
    C -->|"5.Store results"| E[Database]
    C -->|"6.Send response"| B
    B -->|"7.Display analysis"| A

```

![image.png](attachment:4c1a2b41-d8e5-4239-996c-40a045132ad7:image.png)

### Practice Activities:

1. **System Component Identification:**
    - For a familiar app (like Instagram or Spotify), identify the frontend components, backend components, and databases.
2. **Data Flow Mapping:**
    - Map out what happens when you post a comment on a social media platform, from UI to database and back.
3. **Layer Identification Exercise:**
    - For a note-taking app, identify what belongs in each layer (presentation, application, data).

### Resources:

- [Frontend vs Backend Development](https://www.fullstackfoundations.com/blog/client-side-vs-server-side)
- [Web Application Architecture](https://www.sayonetech.com/blog/web-application-architecture/)
- [Middleware](https://srivastavayushmaan1347.medium.com/understanding-middlewares-a-comprehensive-guide-with-practical-examples-c80383f888d5)
- [System Design Basics](https://dev.to/kaustubhyerkade/system-design-fundamentals-a-complete-guide-for-beginners-3n95)

---

### 🚀 Later in the bootcamp, this is the pipeline you’ll use to capture user input, process it using LLMs, and return AI results.
