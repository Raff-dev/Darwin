# Darwin: The Evolution of Document Interaction

Darwin represents the next leap in document-based communication, offering a unique platform where users can upload documents and engage in insightful conversations with them. At its heart, Darwin harnesses the power of text embedding and the Pinecone vector database to understand and contextualize document content. This innovative approach allows for a more nuanced and interactive experience, as users explore and query their documents in a conversational manner. By integrating LangChain and OpenAI's GPT models, including the sophisticated GPT-3.5-turbo and GPT-4-1106-preview, Darwin delivers a groundbreaking way to interact with text, revolutionizing how we comprehend and engage with information.

## Features

🚀 **Interactive Document Conversations**: Dive into a new realm where chatting with documents becomes a reality. Our app leverages the power of OpenAI's GPT models to bring documents to life, enabling you to engage in meaningful, context-aware conversations as if you were talking to a human expert.

⚡ **Instantaneous, Streaming Responses**: Stay in the flow with real-time, streaming responses. Harnessing the robust streaming capabilities of the GPT-4-1106-preview model, our app ensures that your conversations flow seamlessly, providing instant responses that evolve as your dialogue progresses.

🌐 **Unified Full-Stack Experience**: Enjoy a harmonious blend of front and back-end technologies. Our Python-powered backend synergizes perfectly with our sleek TypeScript frontend, delivering a seamless, integrated user experience that connects you intuitively to the core functionalities of our app.

## Tech Stack

- [Python](https://www.python.org/): The backbone of our backend, Python brings its robust and versatile capabilities to the table.
- [React](https://reactjs.org/): Powering our frontend, React brings its renowned efficiency and flexibility, enabling us to create a dynamic, modern user interface.
- [TypeScript](https://www.typescriptlang.org/): Crafting our frontend, TypeScript offers a modern, type-safe experience.
- [FastAPI](https://fastapi.tiangolo.com/): FastAPI streamlines our backend framework, ensuring high performance and easy development.
- [Vite](https://vitejs.dev/): Vite accelerates our frontend build process, ensuring quick and efficient development cycles.
- [Docker](https://www.docker.com/): Embracing containerization, Docker encapsulates our application in a consistent, efficient environment.
- [Docker Compose](https://docs.docker.com/compose/): Docker Compose orchestrates our multi-container setup, simplifying configurations and deployments.
- [GitHub Actions](https://github.com/features/actions): Automating our CI/CD pipeline, GitHub Actions ensures smooth, continuous integration and delivery.
- [OpenAI](https://www.openai.com/): At the heart of our chat functionality lies OpenAI's GPT models, the core of our intelligent response generation.
- [Pinecone](https://www.pinecone.io/): Pinecone powers our document search functionality, enabling us to deliver relevant documents to our users.

## Running the Project

To embark on this journey, ensure you have Docker and Docker Compose installed. With these tools ready, initiate the application with the following incantation in the project's root sanctum:

```bash
docker-compose up --build
```

This mystical command conjures up all the services detailed in the docker-compose.yml grimoire. The application then materializes at `localhost:8000` (or the port you've predestined in the docker-compose.yml scroll).

License
Our creation is bestowed upon the world under the MIT license, inviting innovation and collaboration.
