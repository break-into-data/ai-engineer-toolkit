To wrap up this module, you’ll learn how applications talk to each other using APIs. Whether you’re pulling data from OpenAI or saving chat history to a server, APIs are the glue that connects everything together. You’ll also explore REST vs GraphQL, giving you insight into how modern apps move data across the web. This ties together everything you’ve learned—from development to deployment—with real-world communication between tools.

### What is an API?

An **Application Programming Interface (API)** is a set of rules and protocols that allows different software applications to communicate with each other.

- Enables communication between software systems
- Defines methods and data formats for interaction
- Abstracts complex functionality behind simple interfaces
- Powers modern web and mobile applications

### API Fundamentals

### API Visualization:

This diagram shows how your application connects to various external services (AI, Weather, Database) through API requests and responses.

```mermaid
graph TD
    A[Your Application] -->|API Request| B[AI Service]
    B -->|API Response| A
    A -->|API Request| C[Weather Service]
    C -->|API Response| A
    A -->|API Request| D[Database Service]
    D -->|API Response| A

```

### REST vs GraphQL APIs

### REST APIs:

- **RE**presentational **S**tate **T**ransfer
- Resource-based architecture
- Uses standard HTTP methods (GET, POST, PUT, DELETE)
- Each endpoint represents a resource

```
https://api.example.com/users         # Get all users
https://api.example.com/users/42      # Get user with ID 42
https://api.example.com/users/42/posts # Get posts from user 42

```

### GraphQL APIs:

- Query language for APIs
- Single endpoint for all operations
- Client specifies exactly what data it needs
- Reduces over-fetching and under-fetching
- Advantages for AI applications with varying data needs

```graphql
query {
  user(id: "42") {
    name
    email
    posts {
      title
      createdAt
    }
  }
}

```

### Comparison:

| Feature | REST | GraphQL |
| --- | --- | --- |
| Endpoints | Multiple | Single |
| Data Fetching | Can over/under fetch | Request exactly what you need |
| Caching | Built into HTTP | Requires additional setup |
| File Uploads | Native support | Requires special handling |
| Learning Curve | Moderate | Steeper |
| Usage in AI | Common for simple AI services | Good for complex AI data needs |

### HTTP Basics

### HTTP Methods:

Shows the four main HTTP methods (GET, POST, PUT/DELETE, DELETE) and what each one does in an API context.

```mermaid
graph TD
    A[GET] -->|"Retrieve data (safe, no side effects)"| B[Example: Get user profile]
    C[POST] -->|"Create new resources"| D[Example: Create new AI prediction]
    E[PUT/PATCH] -->|"Update existing resources"| F[Example: Update AI model settings]
    G[DELETE] -->|"Remove resources"| H[Example: Delete saved prediction]

```

### Common Status Codes:

- **2xx Success**
    - 200: OK
    - 201: Created
    - 204: No Content
- **4xx Client Errors**
    - 400: Bad Request
    - 401: Unauthorized
    - 404: Not Found
- **5xx Server Errors**
    - 500: Internal Server Error
    - 503: Service Unavailable

### Working with APIs in Practice

*Note - If you are new to API calls, copy these blocks of code into Cursor and prompt in the chat to explain the code to familiarize this structure.* 

### Making API Requests (JavaScript/TypeScript):

Demonstrates making an asynchronous API call using fetch, with proper error handling and authentication headers.

```tsx
// Using fetch API
async function getAIPrediction(inputText: string): Promise<any> {
  try {
    const response = await fetch('https://api.aiservice.com/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_API_KEY'
      },
      body: JSON.stringify({ text: inputText })
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to get AI prediction:', error);
    throw error;
  }
}

// Usage
getAIPrediction("Analyze this customer feedback")
  .then(result => console.log(result))
  .catch(error => console.error(error));

```

### Using Axios Library:

Shows an alternative way to make API calls using the Axios library, with similar structure but cleaner syntax.

```tsx
import axios from 'axios';

async function classifyImage(imageUrl: string): Promise<any> {
  try {
    const response = await axios.post('https://api.aiservice.com/image/classify', {
      url: imageUrl
    }, {
      headers: {
        'Authorization': 'Bearer YOUR_API_KEY'
      }
    });

    return response.data;
  } catch (error) {
    console.error('Image classification failed:', error);
    throw error;
  }
}

```

### API Authentication Methods:

Three code snippets showing different ways to authenticate API requests: API keys, Bearer tokens, and OAuth 2.0.

1. **API Keys**
    
    ```tsx
    headers: {
      'X-API-Key': 'your_api_key_here'
    }
    
    ```
    
2. **Bearer Tokens (JWT)**
    
    ```tsx
    headers: {
      'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    }
    
    ```
    
3. **OAuth 2.0**
    
    ```tsx
    // First get a token, then use it in requests
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
    
    ```
    

### Practice Activities:

1. **API Exploration:**
    - Test public APIs using Postman or similar tools
2. **API Request Challenge:**
    - Write code to fetch and display data from a simple API
3. **AI API Simulation:**
    - Create a mock AI service API and client application

### Resources:

- [REST API Tutorial](https://restfulapi.net/)
- [GraphQL Documentation](https://graphql.org/learn/)
- [Public APIs for Practice](https://github.com/public-apis/public-apis)
- [Postman Learning Center](https://learning.postman.com/)

## 🚀 Building a Full AI Application

In the bootcamp, you'll combine all these concepts to build production-ready AI applications with:

### Modern Application Architecture:

Illustrates the complete architecture of an AI application with user-facing components, API layer, AI processing, and data storage all working together.

```mermaid
flowchart TD
    subgraph "User-Facing Application"
        UI[UI Components]
        State[State Management]
    end

    subgraph "API Layer"
        Endpoints[API Endpoints]
        Middleware[API Middleware]
        Validation[Input Validation]
    end

    subgraph "AI Processing"
        Models[AI Models]
        Inference[Inference Engine]
        Cache[Response Cache]
    end

    subgraph "Data Layer"
        DB[Database]
        Storage[File Storage]
    end

    UI <-->|User Interaction| State
    State <-->|API Requests| Endpoints
    Endpoints --> Middleware
    Middleware --> Validation
    Validation <--> Models
    Models <--> Inference
    Inference <--> Cache
    Models <--> DB
    Models <--> Storage

```

This preparatory content has equipped you with the fundamentals of web applications, TypeScript, and APIs - all essential for building AI-powered applications.

In the full bootcamp, we'll dive deeper and build complete AI applications with:

- Beautiful, responsive user interfaces
- Robust API layers
- Integration with powerful AI services
- Implement production best practices (error handling, testing, deployment)
- Deploy your application to the cloud

You’ll soon create a beautiful AI app that fetches responses from an LLM via your own API endpoints and shows them in a slick UI.

**Can't wait to see what you'll build!**
