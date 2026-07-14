# InsightFlow

Production-quality SaaS foundation for a business intelligence platform.

## Overview

InsightFlow is structured using clean architecture principles. This repository
contains the project scaffold only — no dashboards, analytics, forecasting,
machine learning, charts, or AI features are implemented yet.

## Project Structure

```
InsightFlow/
├── app.py              # Streamlit entry point
├── config.py           # Configuration container
├── settings.py         # Environment-aware settings
├── constants.py        # Static application constants
├── assets/             # Static assets (images, icons)
├── components/         # Reusable UI components
├── pages/              # Streamlit page modules
├── database/           # Data access layer
├── services/           # Application / domain services
├── models/             # Data models and schemas
├── utils/              # Shared utility functions
├── styles/             # Custom styling assets
├── analytics/          # Analytics module (placeholder)
├── forecasting/        # Forecasting module (placeholder)
├── reports/            # Reporting module (placeholder)
├── exports/            # Export module (placeholder)
├── data/               # Local data storage
├── docs/               # Project documentation
└── tests/              # Test suite
```

## Requirements

- Python 3.10+
- pip

## Getting Started

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # macOS / Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   streamlit run app.py
   ```

## Development

- Follow PEP 8 style guidelines.
- Keep business logic out of `app.py`; route through services and components.
- Add feature code only within the appropriate layer directory.

## License

Proprietary — all rights reserved.
