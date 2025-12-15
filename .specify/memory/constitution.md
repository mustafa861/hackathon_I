<!-- Sync Impact Report:
Version change: N/A → 1.0.0
List of modified principles: None
Added sections: None
Removed sections: None
Templates requiring updates: ⚠ .specify/templates/plan-template.md, ⚠ .specify/templates/spec-template.md, ⚠ .specify/templates/tasks-template.md, ⚠ .specify/templates/commands/*.md
Follow-up TODOs: None
-->
# AI/Spec-Driven Book Creation Constitution

## Core Principles

### AI/Spec-Driven Book Creation
Create a book using Docusaurus and deploy it to GitHub Pages.

### Integrated RAG Chatbot
Embed a Retrieval-Augmented Generation (RAG) chatbot within the book to answer questions about the content, including user-selected text.

### Tech Stack for Chatbot
Use OpenAI Agents / ChatKit SDKs, FastAPI backend, Neon Serverless Postgres, and Qdrant Cloud Free Tier for vector storage.

### Signup/Signin with User Background
Implement authentication using BetterAuth and collect user software/hardware background for personalization.

### Per-Chapter Content Personalization
Logged-in users can personalize chapter content via a button at the start of each chapter.

### Per-Chapter Urdu Translation
Logged-in users can translate chapter content into Urdu via a button at the start of each chapter.

## Governance
Constitution supersedes all other practices; Amendments require documentation, approval, migration plan.
All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2025-12-12 | **Last Amended**: 2025-12-12
