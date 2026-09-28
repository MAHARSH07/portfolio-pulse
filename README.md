# PortfolioPulse

AI-powered portfolio tracker and market intelligence platform with real-time portfolio synchronization, market data, personalized news analysis, alerts, and investment intelligence.

> **Status:** Active development  
> **Current milestone:** Portfolio synchronization, market data integration, instrument normalization, and database architecture  
> **Primary broker:** Groww  
> **Backend:** FastAPI + PostgreSQL + SQLAlchemy  
> **Frontend:** React (planned/in development)

---

## 1. Overview

PortfolioPulse is a personal portfolio intelligence platform designed to go beyond simply displaying stock prices and portfolio values.

The goal is to build a system that understands:

- What the user currently owns
- How much of each asset the user owns
- The user's average purchase price
- Current market prices
- Portfolio-level and holding-level P&L
- News relevant to the user's holdings
- Quarterly results
- Corporate announcements
- Corporate actions
- Important meetings and events
- Indian and international macroeconomic developments
- Market events that may affect the user's portfolio

The platform is intended to act as an **intelligence layer on top of a broker**, rather than as a trading or brokerage platform.

Groww remains the source of truth for the user's actual holdings and trades.

PortfolioPulse retrieves portfolio information, combines it with external market information, and uses deterministic financial logic together with AI reasoning to provide personalized insights.

---

## 2. Core Philosophy

PortfolioPulse follows three important architectural principles.

### 2.1 Broker is the source of truth

PortfolioPulse does not attempt to become a broker.

Groww remains responsible for:

- Actual holdings
- Executed trades
- Orders
- Average purchase prices
- Quantities

PortfolioPulse synchronizes this information and builds intelligence on top of it.

```text
Groww
  |
  | Portfolio synchronization
  v
PortfolioPulse
  |
  +-- Portfolio state
  +-- Market data
  +-- News
  +-- Results
  +-- Corporate events
  +-- AI analysis
```

---

### 2.2 Deterministic financial calculations

Financial values that can be calculated reliably should not be delegated to an LLM.

For example:

- Quantity
- Invested value
- Current value
- P&L
- P&L percentage
- Portfolio allocation
- Position size

These calculations belong in backend application code.

The AI layer should reason about the data rather than becoming the source of truth for numerical calculations.

```text
Backend
  |
  +-- Calculate portfolio value
  +-- Calculate P&L
  +-- Calculate allocation
  |
  v
Structured portfolio data
  |
  v
AI agent
  |
  +-- Interpret
  +-- Summarize
  +-- Find relevant information
```

---

### 2.3 Portfolio-centric intelligence

PortfolioPulse is not intended to be a generic financial news application.

The primary question is:

> "What information is relevant to my portfolio?"

For example, if the user owns KPIT Technologies, the system should prioritize:

- KPIT announcements
- KPIT quarterly results
- KPIT management commentary
- Relevant IT/automotive software industry developments
- Material corporate actions
- Important events affecting the company
- Macro developments that materially affect the company

Instead of simply showing a generic list of market headlines.

---

## 3. Current Architecture

The current system is primarily a backend foundation.

```text
                         +----------------------+
                         |        Groww         |
                         |  Broker / Source of  |
                         |       Truth          |
                         +----------+-----------+
                                    |
                                    | Holdings Sync
                                    v
                         +----------------------+
                         |     FastAPI API      |
                         |                      |
                         |  Broker Integration  |
                         |  Portfolio Service   |
                         |  Market Data Service |
                         +----------+-----------+
                                    |
                    +---------------+----------------+
                    |               |                |
                    v               v                v
              PostgreSQL       Market Data       Instruments
              Database          Providers        / Metadata
                    |               |
                    +---------------+----------------+
                                    |
                                    v
                              Portfolio State
                                    |
                                    v
                              Future AI Layer
                                    |
                    +---------------+----------------+
                    |               |                |
                    v               v                v
                  News          Results          Events
```

---

## 4. Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Pydantic Settings
- PostgreSQL
- Alembic

### Broker Integration

- Groww API
- `growwapi` Python SDK

### Market Data

- Groww market data where available
- Yahoo Finance (`yfinance`) as a fallback/delayed source

### Database

- PostgreSQL 16
- SQLAlchemy ORM
- Alembic migrations

### Frontend

- React
- Planned as the primary web interface

### AI / Future Intelligence Layer

The planned AI layer will use:

- LangGraph
- LangChain
- Local LLM through Ollama
- Qwen models
- External information/news retrieval

The AI layer is not yet implemented in the current milestone.

---

## 5. Project Structure

The current backend structure is approximately:

```text
portfolio-pulse/
│
├── backend/
│   │
│   ├── app/
│   │   ├── brokers/
│   │   │   ├── base.py
│   │   │   └── groww.py
│   │   │
│   │   ├── core/
│   │   │   └── config.py
│   │   │
│   │   ├── db/
│   │   │   └── database.py
│   │   │
│   │   ├── market_data/
│   │   │   ├── base.py
│   │   │   ├── price.py
│   │   │   ├── groww.py
│   │   │   ├── yfinance.py
│   │   │   └── service.py
│   │   │
│   │   ├── models/
│   │   │   ├── holding.py
│   │   │   ├── instrument.py
│   │   │   ├── transaction.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── repositories/
│   │   │   └── instrument_repository.py
│   │   │
│   │   ├── routers/
│   │   │   ├── groww.py
│   │   │   ├── portfolio.py
│   │   │   ├── sync.py
│   │   │   └── ...
│   │   │
│   │   ├── schemas/
│   │   │   ├── broker.py
│   │   │   ├── instrument.py
│   │   │   └── ...
│   │   │
│   │   ├── services/
│   │   │   ├── portfolio_service.py
│   │   │   ├── sync_service.py
│   │   │   └── instrument_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── alembic/
│   │   └── versions/
│   │
│   ├── scripts/
│   │   └── ...
│   │
│   ├── requirements.txt
│   └── .env
│
├── docker-compose.yml
├── README.md
└── ...
```

---

## 6. Database Architecture

PostgreSQL is currently used as the persistent data store.

The database runs through Docker on host port `5433`.

```text
Docker PostgreSQL
        |
        | localhost:5433
        |
FastAPI / SQLAlchemy
```

The database configuration is stored in the backend environment file.

Sensitive credentials such as broker API credentials are kept in `.env` and are not committed to Git.

---

## 7. Database Models

### 7.1 Instruments

The `instruments` table stores broker-provided metadata about financial instruments.

An instrument represents the security itself rather than the user's position in that security.

Current information includes:

- ISIN
- Trading symbol
- Groww symbol
- Name
- Exchange
- Exchange token
- Instrument type
- Segment
- Series
- Lot size
- Tick size
- Creation timestamp
- Update timestamp

Conceptually:

```text
Instrument
    |
    +-- KPITTECH
    +-- JWL
    +-- GOLDIETF
    +-- NIFTYBEES
    +-- ...
```

This prevents company/instrument metadata from being duplicated unnecessarily inside holdings.

---

## 8. Holdings

The `holdings` table represents the user's **current positions**.

A holding currently contains:

```text
id
instrument_id
symbol
quantity
average_price
broker
```

The important distinction is:

> A holding represents the current state of ownership.

For example:

```text
KPITTECH
Quantity: 33
Average price: ₹847.38
Broker: Groww
```

The current market price is deliberately **not stored in the holdings table**.

Market price is dynamic and belongs to the market-data layer.

---

## 9. Holding → Instrument Relationship

Holdings are linked to instruments through a foreign key:

```text
holdings.instrument_id
        |
        v
instruments.id
```

This allows the application to access metadata through SQLAlchemy relationships.

For example:

```python
holding.instrument.name
holding.instrument.isin
holding.instrument.exchange
```

This gives us a clean separation:

```text
Instrument
    |
    | What is this security?
    |
    +-- Name
    +-- ISIN
    +-- Exchange
    +-- Trading symbol


Holding
    |
    | What does the user currently own?
    |
    +-- Quantity
    +-- Average price
    +-- Broker
```

---

## 10. Portfolio Synchronization

PortfolioPulse currently supports synchronization of holdings from Groww.

The basic flow is:

```text
Groww API
    |
    v
GrowwClient
    |
    v
BrokerHolding
    |
    v
sync_holdings()
    |
    +-- Find/create instrument
    |
    +-- Update existing holding
    |
    +-- Create new holding
    |
    +-- Remove holdings no longer returned
    |
    v
PostgreSQL
```

The synchronization process ensures that the local portfolio reflects the current holdings returned by Groww.

---

### 10.1 Existing holding

If a holding already exists:

```text
Groww
  |
  | KPITTECH
  | Quantity = 33
  | Average price = 847.38
  |
  v
Existing local holding
  |
  +-- Update quantity
  +-- Update average price
  +-- Update instrument relationship
```

---

### 10.2 New holding

If Groww returns a security that does not exist locally:

```text
Groww
  |
  v
Instrument lookup
  |
  +-- Instrument exists → reuse it
  |
  +-- Instrument doesn't exist
          |
          v
      Fetch instrument metadata
          |
          v
      Create instrument
          |
          v
      Create holding
```

---

### 10.3 Sold-out holding

If a previously stored holding is no longer returned by Groww, the synchronization process removes it from the current holdings table.

This is appropriate because the holdings table represents **current positions**, not historical trades.

---

## 11. Why Transactions Are Not Currently Required

PortfolioPulse currently has a `TransactionModel`, but transaction synchronization is not yet implemented.

This is intentional.

A transaction represents historical activity:

```text
BUY 10 KPITTECH
BUY 10 KPITTECH
SELL 5 KPITTECH
```

Whereas a holding represents the current result:

```text
KPITTECH
Current quantity: 15
```

For the current PortfolioPulse functionality, current holdings are sufficient.

If the user buys or sells a stock:

```text
User trades in Groww
        |
        v
Groww holdings change
        |
        v
PortfolioPulse sync
        |
        v
Current holding updated
```

Therefore, transaction history is not required for the current portfolio snapshot.

Transactions will become useful later for features such as:

- Historical trade history
- Realized P&L
- Complete investment history
- Stocks previously owned
- Accumulation/distribution analysis
- Tax-oriented reporting
- Historical portfolio reconstruction

Transaction synchronization will be implemented once a reliable historical trade-data source is established.

---

## 12. Market Data Architecture

Market prices are intentionally separated from portfolio holdings.

The application defines a market-data abstraction:

```python
class MarketDataProvider:
    def get_prices(self, symbols):
        ...
```

This allows multiple market-data providers to be used without tightly coupling the portfolio service to a single provider.

---

## 13. Price Snapshot

Market prices are represented using a `PriceSnapshot`.

A price snapshot contains:

```text
symbol
price
timestamp
source
status
```

Price status can be:

```text
REAL_TIME
DELAYED
EOD
UNAVAILABLE
```

This is important because the application must not present delayed data as real-time data.

---

## 14. Market Data Fallback

The current market-data strategy is:

```text
                  +--------------+
                  | Groww Market |
                  |     Data     |
                  +------+-------+
                         |
                    Try first
                         |
              +----------+----------+
              |                     |
           Success                Failure
              |                     |
              v                     v
        Groww price          Yahoo Finance
        REAL_TIME             DELAYED
```

Groww market-price access currently returns an access-forbidden response for the user's API account.

Therefore, the system gracefully falls back to Yahoo Finance.

The fallback is explicitly marked as delayed rather than pretending it is real-time.

---

## 15. Current Portfolio Calculation

The portfolio service combines:

1. Stored holdings
2. Instrument metadata
3. Current market data

Conceptually:

```text
Holding
   +
Instrument
   +
Current Market Price
   |
   v
Portfolio Position
```

A portfolio position contains information such as:

```text
Symbol
Company name
Quantity
Average price
Current price
Price source
Price status
Price timestamp
```

---

## 16. Portfolio P&L

PortfolioPulse calculates the current portfolio state from the synchronized holdings and current market prices.

For an individual holding:

```text
Invested Value
    = Quantity × Average Price

Current Value
    = Quantity × Current Price

P&L
    = Current Value - Invested Value

P&L %
    = (P&L / Invested Value) × 100
```

For the complete portfolio:

```text
Total Invested Value
    = Sum of all holding invested values

Total Current Value
    = Sum of all current holding values

Portfolio P&L
    = Total Current Value - Total Invested Value
```

These calculations are performed by backend application logic rather than an LLM.

---

## 17. Current Portfolio Data Flow

The current end-to-end flow is:

```text
                    Groww
                      |
                      | Holdings
                      v
                GrowwClient
                      |
                      v
              Synchronization
                      |
                      v
                PostgreSQL
                      |
                      v
              PortfolioService
                      |
                      +--------> Instrument metadata
                      |
                      +--------> MarketDataService
                                      |
                                      +-- Groww
                                      |
                                      +-- yfinance fallback
                      |
                      v
                Portfolio API
                      |
                      v
                  Frontend
```

---

## 18. Groww Integration

Groww is currently integrated through the official Python SDK.

The integration currently supports:

- Authentication
- User profile retrieval
- Holdings retrieval
- Instrument lookup

Instrument lookup provides metadata such as:

- Trading symbol
- Groww symbol
- ISIN
- Exchange
- Exchange token
- Instrument type
- Segment
- Name
- Lot size
- Tick size

---

## 19. API Endpoints

The backend currently exposes endpoints for areas including:

### Health

```text
GET /
GET /health
GET /db-health
```

### Groww

```text
GET /brokers/groww/holdings
```

### Portfolio

```text
GET /portfolio
```

### Synchronization

```text
POST /sync/portfolio
```

The exact endpoint list may expand as additional modules are implemented.

---

## 20. Alembic Database Migrations

Database schema changes are managed using Alembic.

The current migration history includes:

```text
baseline_existing_schema
        ↓
remove_current_price_from_holdings
        ↓
add_instruments_table
        ↓
link_holdings_to_instruments
        ↓
populate_holding_instrument_references
        ↓
require_instrument_for_holdings
        ↓
remove_company_name_from_holdings
```

The current database migration head is:

```text
a7cf0760b310
```

Migration history should be preserved rather than manually modifying the production/database schema.

---

## 21. Why Current Price Is Not Stored in Holdings

A previous version of the holdings model stored `current_price`.

This was removed because market price is not permanent portfolio state.

For example:

```text
10:00 AM → ₹500
11:00 AM → ₹505
12:00 PM → ₹498
```

If `current_price` were stored directly in holdings, the value could become stale.

Instead:

```text
Holdings
    |
    +-- quantity
    +-- average price

Market Data
    |
    +-- current price
    +-- timestamp
    +-- source
    +-- status
```

This separation allows market data to be refreshed independently.

---

## 22. AI Intelligence Layer — Planned Architecture

The next major stage of PortfolioPulse is the AI intelligence layer.

The AI should not replace the backend.

Instead:

```text
Backend
   |
   | Structured financial facts
   v
AI Agent
   |
   +-- Retrieve relevant information
   +-- Analyze news
   +-- Analyze results
   +-- Explain events
   +-- Summarize developments
   +-- Personalize information to portfolio
```

The planned architecture will use an agent-based approach, potentially using LangGraph and LangChain.

A local LLM through Ollama is planned as the reasoning engine.

---

## 23. Why Portfolio Data + AI Is Powerful

The AI does not need transaction history to start providing useful portfolio intelligence.

The current portfolio state already provides:

```text
Stock
Quantity
Average price
Current price
Current value
P&L
P&L %
```

The AI can combine this with external information.

For example:

```text
Portfolio data
      +
Latest company news
      +
Quarterly results
      +
Corporate announcements
      +
Sector developments
      +
Macro events
      |
      v
AI reasoning
      |
      v
Personalized portfolio intelligence
```

---

## 24. Example AI Queries

The future AI assistant should be able to answer questions such as:

### Portfolio news

```text
"Any important news about my holdings today?"
```

### Company-specific

```text
"What's happening with KPIT?"
```

### Results

```text
"Show me the latest quarterly results of the companies I own."
```

### Events

```text
"Are there any important corporate announcements from my holdings?"
```

### Portfolio analysis

```text
"Why is my portfolio down today?"
```

### Market intelligence

```text
"What happened in the market today that affects my portfolio?"
```

### Morning briefing

```text
"Give me a morning briefing for my portfolio."
```

The agent should retrieve relevant information rather than relying solely on information contained in the model.

---

## 25. Personalized News Retrieval

A key feature of PortfolioPulse will be **portfolio-aware news retrieval**.

Instead of:

```text
Get all financial news
        ↓
Show everything
```

the system should work more like:

```text
Current holdings
      |
      +-- KPITTECH
      +-- CONTROLPR
      +-- GOLDIETF
      +-- JWL
      +-- ...
      |
      v
Identify relevant entities
      |
      v
Retrieve current information
      |
      +-- Company news
      +-- Results
      +-- Announcements
      +-- Corporate actions
      +-- Sector news
      +-- Macro news
      |
      v
AI relevance analysis
      |
      v
Portfolio-specific response
```

This keeps the system focused on information that matters to the user.

---

## 26. Future Alert System

Once manual AI queries work reliably, the same architecture can be automated.

For example:

```text
New information appears
        |
        v
Is it related to user's holdings?
        |
       YES
        |
        v
Determine importance
        |
        v
Does it materially matter?
        |
       YES
        |
        v
Generate personalized alert
```

An alert could eventually contain:

```text
Important Portfolio Alert

KPIT Technologies

A new company announcement has been detected.

Your position:
33 shares
Current P&L: ...

Why this may matter:
...

Source:
...
```

The goal is to avoid sending every headline.

The system should prioritize **material and relevant information**.

---

## 27. Future Scheduled Intelligence

The platform can later support scheduled workflows such as:

### Daily portfolio sync

```text
Scheduled job
     ↓
Sync Groww holdings
     ↓
Update portfolio
```

### Morning briefing

```text
Scheduled job
     ↓
Sync portfolio
     ↓
Fetch relevant news
     ↓
Analyze
     ↓
Generate morning briefing
```

### Evening briefing

```text
Market close
     ↓
Collect relevant developments
     ↓
Analyze portfolio impact
     ↓
Generate summary
```

### Event monitoring

```text
Continuous / periodic retrieval
     ↓
Detect new relevant information
     ↓
Analyze importance
     ↓
Send alert if required
```

These automation features will be added after the underlying AI and information-retrieval workflow is reliable.

---

## 28. Current Scope vs Future Scope

### Implemented

- FastAPI backend foundation
- PostgreSQL database
- Docker PostgreSQL setup
- Environment-based configuration
- Groww authentication
- Groww holdings retrieval
- Groww instrument lookup
- Holdings synchronization
- Instrument model
- Holding → Instrument relationship
- SQLAlchemy repositories/services
- Alembic migrations
- Market-data abstraction
- Groww market-data provider
- Yahoo Finance fallback
- Price source/status tracking
- Portfolio calculation
- Portfolio P&L
- Current portfolio API
- Database health endpoint
- Separation of broker, portfolio, instrument, and market-data responsibilities

### Currently being designed

- Transaction synchronization
- AI agent architecture
- News retrieval
- Portfolio-aware information retrieval

### Planned

#### AI

- LangGraph agent
- LangChain integration
- Ollama
- Local Qwen model
- Tool-based information retrieval
- Portfolio-aware reasoning

#### Intelligence

- Company news
- Quarterly results
- Corporate announcements
- Corporate actions
- Earnings/events
- Management commentary
- Sector developments
- Indian macroeconomic news
- International macroeconomic news

#### Automation

- Daily portfolio synchronization
- Morning briefing
- Post-market briefing
- News monitoring
- Smart portfolio alerts
- Event reminders

#### Frontend

- React dashboard
- Portfolio overview
- Holding details
- P&L visualization
- News feed
- AI assistant
- Alerts
- Event calendar

#### Future mobile application

A future iPhone application can reuse the FastAPI backend.

```text
                   FastAPI Backend
                   /             \
                  /               \
                 v                 v
        React Web App         iPhone App
```

This avoids duplicating core financial/business logic across platforms.

---

## 29. Design Decisions Made So Far

### Decision 1 — Groww as source of truth

PortfolioPulse does not maintain an independent trading ledger for current holdings.

---

### Decision 2 — Market price outside holdings

Current prices are dynamic market data and therefore are not persisted as holding state.

---

### Decision 3 — Instrument normalization

Company/instrument metadata belongs to the `instruments` table rather than being duplicated inside every holding.

---

### Decision 4 — Foreign key relationship

Holdings reference instruments through `instrument_id`.

---

### Decision 5 — Provider abstraction

Market data and broker integrations use abstractions so additional providers can be added later.

---

### Decision 6 — Delayed data is explicitly labeled

If the primary real-time provider is unavailable, fallback data is returned with an appropriate status such as:

```text
DELAYED
```

rather than being presented as real-time data.

---

### Decision 7 — Transactions are not a blocker

Current portfolio functionality only requires synchronized holdings.

Transaction history will be implemented when reliable historical trade retrieval is available.

---

### Decision 8 — AI does not perform deterministic financial calculations

The backend remains responsible for numerical financial calculations.

The AI is responsible for reasoning, interpretation, retrieval, summarization, and personalization.

---

## 30. Security

Sensitive credentials must never be committed to Git.

Environment variables are used for:

```text
DATABASE_URL
GROWW_API_KEY
GROWW_API_SECRET
```

The `.env` file should remain ignored by Git.

If a credential is accidentally committed, it should be rotated immediately.

---

## 31. Running the Project

### Start PostgreSQL

From the project root:

```bash
docker compose up -d
```

Check containers:

```bash
docker compose ps
```

---

### Start the backend

Navigate to the backend:

```bash
cd backend
```

Activate the virtual environment if applicable.

Then run:

```bash
uvicorn app.main:app --reload
```

The API should be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 32. Database Migrations

To check the current migration:

```bash
alembic current
```

To view migration history:

```bash
alembic history
```

To apply migrations:

```bash
alembic upgrade head
```

New schema changes should be introduced through Alembic migrations.

---

## 33. Development Philosophy

PortfolioPulse is being developed incrementally.

Each major architectural feature should:

1. Have a clear purpose
2. Be implemented independently where possible
3. Be tested
4. Be integrated into the existing architecture
5. Be documented
6. Be committed as a meaningful Git milestone

Small unrelated changes should not be bundled together.

---

## 34. Current Milestone

The current milestone establishes a reliable foundation for PortfolioPulse.

The system can now:

```text
Authenticate with Groww
        ↓
Retrieve current holdings
        ↓
Synchronize holdings
        ↓
Normalize instrument metadata
        ↓
Store portfolio state in PostgreSQL
        ↓
Retrieve current market prices
        ↓
Use fallback market data when required
        ↓
Calculate portfolio value and P&L
        ↓
Expose portfolio information through FastAPI
```

This gives the project a reliable **current portfolio state**.

The next major stage is to build the **intelligence layer** on top of this foundation.

---

## 35. Next Development Direction

The next major development focus is:

```text
Current Portfolio
       ↓
AI Agent
       ↓
Information Retrieval
       ↓
Portfolio-Relevant News
       ↓
Results / Events / Announcements
       ↓
Personalized Analysis
```

After this workflow is working reliably, automation can be introduced:

```text
Manual AI analysis
       ↓
Scheduled analysis
       ↓
Daily briefings
       ↓
News monitoring
       ↓
Smart alerts
```

The objective is to evolve PortfolioPulse from a **portfolio tracker** into a **personal portfolio intelligence system**.

---

## License

This project is currently a personal development project.

License information will be added when the project is prepared for public distribution.