# Implementation Plan: AI/Spec-Driven Book with RAG Chatbot

**Branch**: `1-ai-book-rag` | **Date**: 2025-12-12 | **Spec**: specs/1-ai-book-rag/spec.md
**Input**: Feature specification from `/specs/1-ai-book-rag/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the implementation for creating an AI/spec-driven book using Docusaurus, integrated with a RAG chatbot, user authentication, content personalization, and Urdu translation capabilities. The technical approach involves a Docusaurus frontend, a FastAPI backend, Neon Serverless Postgres for user data, and Qdrant Cloud for vector embeddings, leveraging OpenAI Agents / ChatKit SDKs.

## Technical Context

**Language/Version**: Python 3.11+ (for FastAPI), JavaScript/TypeScript (for Docusaurus, React)
**Primary Dependencies**: Docusaurus, React, FastAPI, OpenAI Agents / ChatKit SDKs, Neon Serverless Postgres client, Qdrant client, BetterAuth SDK/library
**Storage**: Neon Serverless Postgres (user data), Qdrant Cloud (vector embeddings for book content)
**Testing**: Jest/React Testing Library (frontend), pytest (backend), Cypress/Playwright (e2e)
**Target Platform**: Web (Docusaurus hosted on GitHub Pages, FastAPI backend deployed as a serverless function or container)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: RAG chatbot responses within 3 seconds (SC-002), smooth Docusaurus navigation and content loading
**Constraints**: No extra features beyond specified principles, real-time RAG response, personalization and translation persist per session (from spec.md)
**Scale/Scope**: Initial deployment supporting multiple chapters, RAG chatbot for all content, user authentication for personalization/translation, handling of potentially large chapter content for embedding and translation.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **AI/Spec-Driven Book Creation**: The plan aligns with creating a Docusaurus book and deploying it to GitHub Pages.
- **Integrated RAG Chatbot**: The plan includes integration of a RAG chatbot.
- **Tech Stack for Chatbot**: The plan explicitly uses FastAPI, Neon Serverless Postgres, and Qdrant Cloud Free Tier, and OpenAI Agents / ChatKit SDKs.
- **Signup/Signin with User Background**: The plan includes BetterAuth for authentication and collecting user software/hardware background.
- **Per-Chapter Content Personalization**: The plan incorporates personalization of chapter content.
- **Per-Chapter Urdu Translation**: The plan includes Urdu translation functionality.

All principles from the constitution are addressed and adhered to in this plan.

## Project Structure

### Documentation (this feature)

```text
specs/1-ai-book-rag/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
book/
├── docusaurus.config.js
├── src/
│   ├── components/      # React components for personalization, translation, chatbot UI
│   ├── pages/           # Docusaurus pages (e.g., login, profile)
│   ├── theme/           # Docusaurus theme overrides
│   └── docs/            # Markdown/MDX book chapters
├── static/
└── package.json

backend/
├── app/                 # FastAPI application
│   ├── api/             # API endpoints (auth, personalization, translation, chatbot)
│   ├── core/            # Core logic (auth, database interaction, RAG)
│   ├── models/          # Pydantic models for data validation
│   └── main.py
├── scripts/             # (Optional) Data ingestion, embedding generation
├── tests/
└── requirements.txt

```

**Structure Decision**: A monorepo-like structure with `book/` for the Docusaurus frontend and `backend/` for the FastAPI application. This separation allows for independent development and deployment of the frontend book and the backend services. The `book/src/components` will house interactive elements, while `book/src/docs` will contain the core book content. The `backend/app` will organize the FastAPI application into API, core logic, and data models.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
