# PortfolioPulse

**AI-powered portfolio tracking and market intelligence.**

PortfolioPulse is a personal portfolio intelligence platform built with React, FastAPI, and PostgreSQL. It synchronizes portfolio holdings from Groww, retrieves market data and financial news, and connects economic events with potential portfolio exposures.

The goal is to go beyond displaying prices and portfolio values by helping users understand what is happening in the market and why it may matter to their holdings.

## Project Status

**Current stage:** Feature development and final validation.

| Area | Current capabilities |
|---|---|
| Portfolio management | Groww holdings retrieval and synchronization |
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | PostgreSQL with Alembic migrations |
| Market data | Groww provider with Yahoo Finance fallback |
| Market dashboard | Indian indices, commodities, and global markets |
| Market news | News feed organized by market category |
| Economic events | Scheduled macroeconomic events, importance, and potential market impact |
| Portfolio relevance | Rule-based event matching against mapped holding exposures |
| Holding explanations | Individual explanations of potential exposure to economic events |
| Frontend | React-based web interface |
| AI intelligence | LangChain/LangGraph and local Ollama-based capabilities, where configured |

Feature availability can depend on external providers, local configuration, and API access. Market data may be delayed.

## Table of Contents

1. [Overview](#1-overview)
2. [Core Principles](#2-core-principles)
3. [Technology Stack](#3-technology-stack)
4. [Architecture](#4-architecture)
5. [Implemented Features](#5-implemented-features)
6. [Market Intelligence](#6-market-intelligence)
7. [Database Design](#7-database-design)
8. [Groww Integration and Synchronization](#8-groww-integration-and-synchronization)
9. [Market Data](#9-market-data)
10. [API Endpoints](#10-api-endpoints)
11. [Project Structure](#11-project-structure)
12. [Prerequisites](#12-prerequisites)
13. [Environment Configuration](#13-environment-configuration)
14. [Running the Application](#14-running-the-application)
15. [Database Migrations](#15-database-migrations)
16. [Testing and Verification](#16-testing-and-verification)
17. [Security](#17-security)
18. [Known Limitations](#18-known-limitations)
19. [Future Improvements](#19-future-improvements)
20. [Development Principles](#20-development-principles)
21. [License](#21-license)

---

## 1. Overview

PortfolioPulse acts as an intelligence layer on top of a broker rather than as a brokerage or trading platform.

Groww remains the source of truth for actual holdings and executed trades. PortfolioPulse retrieves available portfolio information, stores synchronized holdings, retrieves market information, and provides portfolio-focused context.

The platform aims to answer questions such as:

- What do I currently own?
- What is my portfolio worth?
- What are my holdings' current P&L and P&L percentages?
- What is happening in Indian and global markets?
- Which economic events may be relevant to my holdings?
- Why might a particular event matter to a holding?
- What market news should I pay attention to?

PortfolioPulse is a personal development project. Its market and event explanations provide informational context, not guaranteed predictions or personalized financial advice.

## 2. Core Principles

### 2.1 Groww is the source of truth

Groww is responsible for actual holdings, quantities, average purchase prices, and executed trades.

PortfolioPulse synchronizes available holdings data rather than independently maintaining a competing trading ledger.

### 2.2 Financial calculations are deterministic

Reliable financial calculations belong in backend application logic, not in an LLM.

Examples include:

- Invested value
- Current value
- Profit and loss
- P&L percentage
- Portfolio allocation

### 2.3 Market prices are separate from holdings

Holdings represent ownership state. Market prices change over time and are retrieved through the market-data layer.

This separation allows prices and their source/status metadata to be refreshed independently.

### 2.4 Portfolio-centric intelligence

Market information is more useful when its potential relevance to a user's holdings is clear.

PortfolioPulse uses mapped holding exposures and deterministic matching rules to identify possible connections between economic events and portfolio holdings.

These matches represent potential relationships, not confirmed causation or predictions of price direction.

## 3. Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Pydantic Settings
- Alembic

### Database

- PostgreSQL
- Docker Compose
- SQLAlchemy ORM
- Alembic database migrations

### Broker integration

- Groww API
- `growwapi` Python SDK

### Market data and news

- Groww market-data integration, where available
- Yahoo Finance through `yfinance` as a fallback
- External economic-event sources
- External financial-news sources

### Frontend

- React
- JavaScript
- CSS
- Lucide React icons

### AI and information retrieval

The project's AI-related components use or are designed around:

- LangChain
- LangGraph
- Ollama
- Local Qwen models
- External information retrieval

Availability and behavior depend on the configured implementation and local model environment.

## 4. Architecture

```text
                     Groww
                       |
                       | Holdings retrieval
                       v
                FastAPI Backend
                       |
            +----------+----------+
            |          |          |
            v          v          v
        Portfolio   Market Data  Sync Services
        Services    and News
            |          |
            v          v
       PostgreSQL   External Providers
            |
            v
       Portfolio API
            |
            v
        React UI
            |
            v
    Market Intelligence
    - Market overview
    - Financial news
    - Economic events
    - Portfolio relevance
    - Holding explanations
```

The backend owns portfolio data processing, database access, API responses, and deterministic matching logic. The frontend presents the resulting information.

AI components can provide additional interpretation, but they should not replace deterministic calculations or authoritative portfolio data.

## 5. Implemented Features

### Portfolio and data foundation

- FastAPI backend
- PostgreSQL database
- Docker-based database setup
- Environment-based configuration
- Groww authentication and holdings retrieval
- Holdings synchronization
- Instrument metadata normalization
- SQLAlchemy models and services
- Alembic database migrations
- Portfolio calculations and P&L
- Market-data provider abstraction
- Price-source and price-status tracking

### Market dashboard

- Indian market indices
- Commodity prices
- Major global indices
- Market data refresh
- Market news grouped by category
- Scheduled economic events
- Event importance and potential market-impact descriptions
- Expandable portfolio-relevance details
- Matched holding names, symbols, and exposure types
- Individual holding explanations for potential event relevance
- Source links for news and economic events

The market dashboard's actual data depends on external provider availability and the configured integrations.

## 6. Market Intelligence

The market intelligence functionality combines economic-event metadata with mapped portfolio exposures.

### Economic events

Events can include information such as:

- Title and country
- Event category
- Scheduled date
- Description
- Importance
- Potential market impact
- Source and source URL

### Portfolio relevance

The backend applies deterministic rules to map events to potentially relevant sectors and asset classes.

Examples of exposure categories include:

- Banking
- Financial services
- Technology
- Manufacturing
- Industrials
- Energy
- Gold and silver
- Broad-market equities
- Mid-cap equities

The rules are maintained in the backend's event-source modules.

For each matched holding, the response can include:

- Symbol and company name
- Mapped exposure
- Relevance category
- `holding_explanation`

The frontend displays these details when the user expands an event's portfolio-relevance section.

**Important limitation:** Sector mapping and event relevance are rule-based approximations. A match does not establish that an event will materially affect a security, nor does it predict whether its price will rise or fall.

## 7. Database Design

PostgreSQL stores persistent application data.

The database runs through Docker on host port `5433` in the current development configuration.

### Instruments

The instruments table stores security metadata, such as:

- Trading symbol
- Name
- ISIN
- Exchange
- Instrument type
- Segment
- Exchange token and other available metadata

### Holdings

The holdings table represents current ownership state, including information such as:

- Instrument relationship
- Symbol
- Quantity
- Average purchase price
- Broker

Instrument metadata is separated from the holding itself to reduce duplication.

### Current prices

Current prices are retrieved through the market-data layer rather than treated as permanent holding attributes.

### Transactions

A transaction model exists, but complete historical transaction synchronization is not currently a prerequisite for the portfolio snapshot.

Historical trade synchronization, realized P&L, and historical portfolio reconstruction require additional work before they can be considered complete features.

## 8. Groww Integration and Synchronization

Groww is the primary broker integration.

The intended synchronization flow is:

```text
Groww API
    |
    v
Retrieve holdings
    |
    v
Normalize instrument metadata
    |
    v
Create or update instrument records
    |
    v
Create or update current holdings
    |
    v
PostgreSQL
```

The local holdings state is based on the holdings returned by the broker synchronization process.

**Operational caution:** Verify the current broker response and synchronization behavior before relying on it. In particular, confirm how empty responses, failed requests, and holdings no longer returned by the broker are handled.

Groww market-price access may be restricted for a particular account or endpoint even when holdings retrieval works. Market-price functionality should therefore be verified independently.

## 9. Market Data

PortfolioPulse uses a provider abstraction for market data.

The current strategy attempts to use Groww market data where available and falls back to Yahoo Finance when required.

Price information can include:

- Symbol
- Price
- Timestamp
- Source
- Status

Possible statuses include real-time, delayed, end-of-day, or unavailable, depending on the provider implementation.

The application should not label delayed prices as real-time.

External data providers can impose access restrictions, rate limits, or delays. Availability and freshness should be checked before interpreting market values.

## 10. API Endpoints

The backend includes endpoints in the following areas.

| Area | Endpoint | Purpose |
|---|---|---|
| Health | `GET /` | Basic application endpoint |
| Health | `GET /health` | Application health |
| Database | `GET /db-health` | Database connectivity check |
| Groww | `GET /brokers/groww/holdings` | Retrieve broker holdings |
| Portfolio | `GET /portfolio` | Retrieve portfolio information |
| Synchronization | `POST /sync/portfolio` | Synchronize portfolio holdings |
| Market | `GET /market` | Retrieve market overview data |
| Market news | `GET /market/news` | Retrieve market news |
| Economic events | `GET /market/events` | Retrieve economic events and portfolio relevance |

Check the current API documentation at `http://127.0.0.1:8000/docs` for exact request and response schemas.

The endpoint list above reflects the known application routes; consult the running API documentation if implementation details change.

## 11. Project Structure

The repository is organized into backend, frontend, database configuration, and supporting files.

```text
portfolio-pulse/
├── backend/
│   ├── app/
│   │   ├── brokers/
│   │   ├── core/
│   │   ├── db/
│   │   ├── market_data/
│   │   │   └── event_sources/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── alembic/
│   │   └── versions/
│   ├── scripts/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   └── App.css
│   └── package.json
├── docker-compose.yml
├── README.md
└── .gitignore
```

This is a high-level structure; additional files and modules may exist in the repository.

## 12. Prerequisites

Install the following before running the application:

- Git
- Python version compatible with the backend dependencies
- Node.js and npm
- Docker Desktop with Docker Compose
- Access to the required Groww API credentials
- Any external API credentials required by the enabled integrations
- Ollama and the configured local model if using local LLM functionality

Use the dependency files in the repository as the authoritative source for exact package versions.

## 13. Environment Configuration

Create or update the backend environment file according to the settings defined in the application.

Typical settings include:

```dotenv
DATABASE_URL=your_database_connection_string
GROWW_API_KEY=your_groww_api_key
GROWW_API_SECRET=your_groww_api_secret
```

Other variables may be required by the current application configuration or enabled integrations.

Do not copy real credentials into this README, source files, screenshots, or public issue reports.

The `.env` file should remain excluded from Git. Use a local `.env.example` containing placeholder values if you want to document the required settings.

## 14. Running the Application

Run each command from the appropriate directory.

### 14.1 Start PostgreSQL

From the repository root:

```powershell
docker compose up -d
docker compose ps
```

Verify that the PostgreSQL container is running and that its configured host port is available.

The current development configuration uses port `5433` on the host.

### 14.2 Start the backend

Open a terminal:

```powershell
cd backend
```

Activate your existing virtual environment if you use one, and install dependencies if necessary.

For example, on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If the virtual environment has a different location or name, activate that environment instead.

Start FastAPI:

```powershell
uvicorn app.main:app --reload
```

The backend should be available at:

- API: `http://127.0.0.1:8000`
- Swagger documentation: `http://127.0.0.1:8000/docs`

Confirm that the backend can connect to PostgreSQL before testing database-dependent routes.

### 14.3 Start the frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Use the local URL printed by the frontend development server.

The current frontend calls the backend at `http://127.0.0.1:8000`. If the backend URL changes, update the frontend configuration consistently.

### 14.4 Local AI components

If using the local Ollama integration, start Ollama and ensure the configured model is available.

AI functionality may require additional local configuration. A working frontend or backend does not, by itself, prove that every AI workflow is available.

## 15. Database Migrations

Alembic is used to manage database schema changes.

From the backend directory, using the configured Python environment:

Check the current migration:

```powershell
alembic current
```

View migration history:

```powershell
alembic history
```

Apply migrations:

```powershell
alembic upgrade head
```

New schema changes should be introduced through migrations rather than by manually changing the database schema.

Review migration history and back up important data before applying changes to a database containing information you need to preserve.

## 16. Testing and Verification

Before considering a release complete, verify the following.

### Frontend

```powershell
cd frontend
npm run build
```

Confirm that the production build completes successfully.

### Backend and database

- Start the backend without import or configuration errors.
- Check `/health` and `/db-health`.
- Confirm the application can read from PostgreSQL.
- Confirm `/docs` loads and exposes the expected routes.

### Portfolio synchronization

- Verify Groww authentication.
- Retrieve holdings successfully.
- Confirm synchronization updates the local portfolio correctly.
- Verify that failed or empty broker responses do not unexpectedly corrupt portfolio state.

### Market intelligence

- Verify `/market`, `/market/news`, and `/market/events`.
- Confirm economic events return valid response structures.
- Confirm matched holdings include their exposure and explanation fields where applicable.
- Test events with matched holdings and events with no matches.
- Confirm expandable portfolio details work in the frontend.

### Repository

```powershell
git status
git log -1 --oneline
```

Confirm that intended changes are committed and pushed, and that no unintended files or credentials are tracked.

Only report a check as passed after actually running it.

## 17. Security

- Keep API credentials in environment variables.
- Never commit `.env` or real API keys.
- Use placeholders in example configuration files.
- Avoid logging secrets or sensitive broker responses.
- Rotate any credential accidentally committed or exposed.
- Review external API permissions and access restrictions.
- Do not expose a locally configured development server publicly without appropriate security controls.

## 18. Known Limitations

- Groww market-price access may be restricted; the fallback provider may return delayed data.
- Market prices and news depend on external providers and their availability.
- Economic-event matching uses deterministic rules and mapped exposures, not a complete financial risk model.
- Individual holding explanations describe potential relationships and are not price predictions.
- Sector mappings may be incomplete or approximate.
- Full historical transaction synchronization and realized P&L are not established as complete capabilities.
- AI behavior depends on the implemented workflow, local model availability, and external retrieval integrations.
- Production deployment, automated monitoring, and comprehensive automated test coverage should be verified separately before describing the project as production-ready.

## 19. Future Improvements

Potential future work includes:

- Broader automated tests for backend services and API routes
- Improved error handling and observability
- More complete validation of instrument and sector mappings
- Portfolio-aware news retrieval and ranking
- Additional corporate results, announcements, and corporate actions
- Historical transaction synchronization and realized P&L
- Enhanced AI-assisted portfolio analysis
- Scheduled portfolio briefings and notifications
- Production deployment and monitoring

These items are future improvements rather than prerequisites for running the current application.

## 20. Development Principles

PortfolioPulse follows these principles:

1. Keep Groww as the source of truth for actual holdings.
2. Perform deterministic financial calculations in application code.
3. Separate portfolio state from dynamic market data.
4. Keep broker, portfolio, market-data, and UI responsibilities distinct.
5. Clearly identify delayed or unavailable data.
6. Treat AI output as interpretation, not authoritative financial data.
7. Test changes before committing them.
8. Keep documentation aligned with implemented behavior.

## 21. License

This is currently a personal development project. A license has not yet been specified. Add an appropriate license before distributing the project publicly.
