# SmartMail AI

**An Intelligent AI-Powered Email Reply Assistant**

SmartMail AI is an AI-powered email assistant designed to simplify email management. It analyzes incoming emails, understands their intent and context, and generates relevant, professional email replies using Large Language Models (LLMs).

Built with FastAPI, LangGraph, LangChain, and Groq, SmartMail AI provides an efficient workflow for email analysis, reply generation, and history management.

## Key Features

- **AI Email Analysis:** Identifies email intent, category, sentiment, and priority.
- **Email Summarization:** Generates concise summaries and extracts key points.
- **Smart Reply Generation:** Creates context-aware email replies.
- **Multiple Writing Tones:** Professional, Friendly, and Formal.
- **Flexible Reply Length:** Short, Medium, and Detailed.
- **Email History:** Stores and retrieves previously processed emails.
- **History Management:** View individual records and delete saved history.
- **REST API:** Backend APIs powered by FastAPI.
- **AI Workflow Orchestration:** Uses LangGraph to manage the email processing workflow.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API |
| LangGraph | AI workflow orchestration |
| LangChain | LLM integration |
| Groq | AI inference |
| SQLite | Local database |
| SQLAlchemy | Database ORM |
| HTML, CSS, JavaScript | Frontend |

## Application Workflow

1. User enters an email.
2. SmartMail AI analyzes the email.
3. AI identifies intent, category, sentiment, and priority.
4. A summary and key points are generated.
5. The AI generates a reply based on the selected tone and length.
6. The result is displayed to the user.
7. Email details and generated replies are stored in SQLite.



## Security

- API credentials are managed through environment variables.
- Email content is treated as untrusted input.
- Generated replies are drafts and are not automatically sent.

## Project Status

**Current Status: Core Application Working**

Implemented and manually verified:
- Groq LLM integration
- Structured email analysis
- AI reply generation
- Email generation API
- SQLite history storage
- History retrieval and deletion
- Frontend integration

Further testing, improvements, and deployment are planned.

## Future Enhancements

- Advanced email intelligence
- Improved reply quality and context handling
- Automated email integrations
- Additional AI-powered productivity features
- Production deployment

## License

This project is currently developed as a personal project. License details will be added separately.

---

**SmartMail AI — Making Email Communication Smarter with AI.**