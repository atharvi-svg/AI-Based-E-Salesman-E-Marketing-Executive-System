
# AI-Based E-Salesman & E-Marketing Executive System

**Team:** Code Connect
**Course:** UE24CS341A – Software Engineering (Jackfruit SE Mini-Project)
**Project ID:** <fill in>

## Overview
A chat-based virtual sales assistant for a demo e-commerce store. The AI agent
answers product queries, gives rule-based personalized recommendations, scores
each customer conversation as a sales lead (Hot / Warm / Cold), and logs
everything in a simple built-in CRM module. Customers can also add products to
a simulated cart and complete a mock checkout.

This is a scoped-down academic version of the original problem statement —
see [`docs/SRS.md`](docs/SRS.md), Section 7, for what was intentionally left
out (voice interaction, real CRM integration, ML-based scoring, real payments)
and why.

## Features
- 💬 Text-based chat interface with intent detection (price, specs, comparison, offers)
- 🎯 Rule-based lead scoring with Hot / Warm / Cold classification
- 🛍️ Rule-based personalized product recommendations
- 🗂️ Built-in CRM: stores leads, chat transcripts, and scores
- 🛒 Simulated cart & checkout flow
- 📊 Admin dashboard to view and sort leads by score

## Tech Stack
| Layer | Technology |
|---|---|
| Backend | <e.g., Python/Flask or Node/Express> |
| Database | <e.g., SQLite/PostgreSQL> |
| Frontend | <e.g., HTML/CSS/JS or React> |
| Optional NLP | <e.g., hosted LLM API for free-text fallback> |

## Project Structure
