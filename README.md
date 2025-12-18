# Gen AI Carrier Platform

A comprehensive platform for simulating mock interviews using AI technologies. This project provides an interactive environment for users to practice interviews, receive feedback, and improve their skills through real-time analysis of technical and behavioral performance.

**Project Status**: 70% Complete

## Competition Information

This project is being developed for **Techfest 2025** - AWS Gen AI Challenge. Selected teams will be invited to Techfest 2025 for the in-person prototyping round.

### Challenge Phases  

#### Phase 2: Build & Prototype
- **Build**: Teams will build and refine their solutions using AWS tools and services
- **Mentor**: AWS mentors and domain experts will provide technical and strategic guidance
- **Present**: The challenge will conclude with final presentations and demos

*Participants are recommended to build the prototype using kiro.dev (to be instructed by the AWS experts during round 2)*

### Judging Criteria

Submissions will be evaluated by a panel of experts based on the following criteria:

- **Innovation & Originality**: Is the idea novel and creative?
- **GenAI Application**: Is Generative AI used in a meaningful and core way?
- **Impact & Value**: Does the solution address a significant problem and offer a clear value proposition?
- **Feasibility & Team Capability**: Is the idea practical? Does the team (based on supporting materials) demonstrate the capability to build a prototype during Phase 2?
- **Clarity**: How clearly and effectively is the idea communicated in the deck and video?


## Features

- **AI-Powered Interview Questions**: Dynamic question generation based on role and experience level
- **Real-time Feedback**: Instant evaluation of answers with detailed scoring
- **Resume Analysis**: Automated parsing and analysis of uploaded resumes
- **Behavioral Assessment**: Facial expression and speech pattern analysis
- **Technical Evaluation**: Code and technical knowledge assessment
- **Adaptive Questioning**: Questions adjust based on user performance
- **Comprehensive Reports**: Detailed feedback with improvement suggestions
- **Video Recording**: Session recording for review and analysis
- **Multi-modal Interface**: Voice and text input options

## Project Structure

```
gen-ai-carrier-platform/
├── backend/                          # Python FastAPI Backend
│   ├── app/                          # Main application code
│   │   ├── ai_engines/               # AI processing engines
│   │   ├── middleware/               # FastAPI middleware
│   │   ├── models/                   # SQLAlchemy models
│   │   ├── routes/                   # API route handlers
│   │   ├── schemas/                  # Pydantic schemas
│   │   ├── services/                 # Business logic services
│   │   ├── utils/                    # Utility functions
│   │   ├── config.py                 # Application configuration
│   │   ├── constants.py              # Application constants
│   │   ├── database.py               # Database configuration
│   │   └── main.py                   # FastAPI application entry point
│   ├── data/                         # Data storage
│   │   ├── demos/                    # Demo data files
│   │   └── uploads/                  # User uploaded files
│   ├── inferred_models/              # AI model inference
│   ├── logs/                         # Application logs
│   ├── static/                       # Static files
│   ├── venv/                         # Python virtual environment
│   ├── .env                          # Environment variables
│   ├── create_tables.py              # Database table creation script
│   ├── interview.db                  # SQLite database file
│   ├── OPENROUTER_MIGRATION.md       # Migration documentation
│   ├── pyproject.toml                # Python project configuration
│   └── requirements.txt              # Python dependencies
├── chrome-extension/                 # Chrome Extension for Video/Camera
│   ├── background.js                 # Extension background script
│   ├── injected.js                   # Content script injection
│   ├── manifest.json                 # Extension manifest
│   ├── popup.html                    # Extension popup UI
│   └── popup.js                      # Popup functionality
├── frontend/                         # React TypeScript Frontend
│   ├── .vercel/                      # Vercel deployment config
│   ├── dist/                         # Build output directory
│   ├── node_modules/                 # Node.js dependencies
│   ├── public/                       # Static assets
│   │   ├── assets/                   # Public assets
│   │   ├── videos/                   # Video files
│   │   └── vite.svg                  # Vite logo
│   ├── src/                          # Source code
│   │   ├── components/               # React components
│   │   │   ├── about/                # About page components
│   │   │   ├── auth/                 # Authentication components
│   │   │   ├── common/               # Shared components
│   │   │   ├── dashboard/            # Dashboard components
│   │   │   ├── feedback/             # Feedback-related components
│   │   │   ├── interview/            # Interview interface components
│   │   │   ├── landing/              # Landing page components
│   │   │   ├── layout/               # Layout components
│   │   │   ├── profile/              # Profile setup components
│   │   │   └── reports/              # Report components
│   │   ├── hooks/                    # Custom React hooks
│   │   │   ├── useAvatar.ts          # Avatar management hook
│   │   │   ├── useFaceTracking.ts    # Face tracking hook
│   │   │   ├── useInterview.ts       # Interview management hook
│   │   │   ├── useSpeech.ts          # Speech recognition hook
│   │   │   └── useWebcam.ts          # Webcam management hook
│   │   ├── services/                 # Service layer
│   │   │   ├── api.ts                # API service functions
│   │   │   ├── llm.ts                # LLM service integration
│   │   │   ├── metrics.ts            # Metrics collection service
│   │   │   └── socket.ts             # WebSocket service
│   │   ├── styles/                   # Stylesheets
│   │   │   ├── animations.css        # Animation styles
│   │   │   ├── components.css        # Component-specific styles
│   │   │   └── globals.css           # Global styles
│   │   ├── types/                    # TypeScript type definitions
│   │   ├── utils/                    # Utility functions
│   │   │   ├── constants.ts          # Application constants
│   │   │   ├── formatters.ts         # Data formatting utilities
│   │   │   └── helpers.ts            # General helper functions
│   │   ├── views/                    # View components
│   │   ├── App.tsx                   # Main React application component
│   │   ├── main.tsx                  # React application entry point
│   │   ├── style.css                 # Main stylesheet
│   │   └── typescript.svg            # TypeScript logo
│   ├── .gitignore                    # Git ignore rules
│   ├── index.html                    # HTML template
│   ├── package.json                  # Node.js dependencies and scripts
│   ├── package-lock.json             # Dependency lock file
│   ├── postcss.config.js             # PostCSS configuration
│   ├── tailwind.config.js            # Tailwind CSS configuration
│   ├── TODO.md                       # Frontend development tasks
│   ├── tsconfig.json                 # TypeScript configuration
│   ├── vercel.json                   # Vercel deployment config
│   └── vite.config.ts                # Vite build configuration
├── scripts/                          # Build and deployment scripts
├── venv/                             # Root virtual environment
├── working examples/                 # Working code examples
├── .env                              # Root environment variables
├── .gitignore                        # Git ignore rules
├── docker-compose.dev.yml            # Development Docker Compose
├── docker-compose.prod.yml           # Production Docker Compose
├── Makefile                          # Build automation scripts
├── postman_collection.json           # API testing collection
├── render.yaml                       # Render deployment config
├── start.md                          # Getting started guide
├── test_imports.py                   # Import testing script
├── test_openrouter.py                # OpenRouter API testing
├── test_resume_upload.py             # Resume upload testing
├── test_system.py                    # System testing script
├── TODO.md                           # Project-wide development tasks
├── TODO_FIXES.md                     # Bug fixes and improvements
└── README.md                         # This file
```

## Key Components

### Backend Architecture

#### Core Application (`backend/app/`)
- **`main.py`**: FastAPI application entry point with route registration and middleware setup
- **`config.py`**: Environment-based configuration management
- **`database.py`**: SQLAlchemy database connection and session management
- **`constants.py`**: Application-wide constants and enumerations

#### Modular Structure
- **`ai_engines/`**: AI processing engines for behavioral and technical analysis
- **`middleware/`**: FastAPI middleware for authentication and CORS
- **`models/`**: SQLAlchemy models for database entities
- **`routes/`**: API route handlers for different functionalities
- **`schemas/`**: Pydantic schemas for request/response validation
- **`services/`**: Business logic services and integrations
- **`utils/`**: Utility functions for various operations

#### Data Management
- **`data/demos/`**: Demo data and sample files
- **`data/uploads/`**: User-uploaded resume and media files
- **`interview.db`**: SQLite database for development
- **`logs/`**: Application logging directory

### Frontend Architecture

#### Component Organization (`frontend/src/components/`)
- **`about/`**: About page and information components
- **`auth/`**: Authentication and user management
- **`common/`**: Reusable UI components and utilities
- **`dashboard/`**: User dashboard and overview
- **`feedback/`**: Interview feedback and analysis display
- **`interview/`**: Core interview interface and controls
- **`landing/`**: Landing page and marketing components
- **`layout/`**: Application layout and navigation
- **`profile/`**: User profile setup and management
- **`reports/`**: Report viewing and comparison tools

#### React Hooks (`frontend/src/hooks/`)
- **`useInterview.ts`**: Interview state management and API integration
- **`useWebcam.ts`**: Webcam access and video recording
- **`useSpeech.ts`**: Speech recognition and synthesis
- **`useFaceTracking.ts`**: Facial expression analysis
- **`useAvatar.ts`**: AI avatar animation control

#### Services & Utilities
- **`services/`**: API client, LLM integration, metrics, and WebSocket services
- **`styles/`**: CSS files for animations, components, and global styles
- **`utils/`**: Helper functions, constants, and formatters
- **`types/`**: TypeScript type definitions

### Chrome Extension
- **`manifest.json`**: Extension configuration and permissions
- **`background.js`**: Background service worker
- **`popup.html/js`**: Extension popup interface
- **`injected.js`**: Content script for webpage interaction

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **AI/ML**: Custom engines for behavioral and technical analysis
- **Authentication**: JWT-based auth middleware
- **API Documentation**: Automatic OpenAPI/Swagger generation

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS with custom animations
- **State Management**: React hooks and context
- **Real-time Features**: WebSocket integration
- **Media Processing**: WebRTC for video/audio

### DevOps
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Docker Compose for development/production
- **Build Automation**: Makefile for common tasks

## Setup and Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker and Docker Compose
- Git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gen-ai-carrier-platform
   ```

2. **Install Chrome Extension (Required for Video/Camera)**
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode" in the top right corner
   - Click "Load unpacked" and select the `chrome-extension` folder
   - Note the extension ID from the extension card
   - Update the extensionId in `frontend/src/hooks/useWebcam.ts` with the actual ID

3. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python create_tables.py
   ```

4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

5. **Environment Configuration**
   - Configure `.env` files in both root and backend directories
   - Set up API keys for AI services (OpenAI, OpenRouter, etc.)
   - Review `backend/OPENROUTER_MIGRATION.md` for API configuration details

6. **Run Development Environment**
   ```bash
   # Using Docker Compose (recommended)
   docker-compose -f docker-compose.dev.yml up

   # Or run manually
   # Backend: cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   # Frontend: cd frontend && npm run dev
   ```

7. **Testing Setup**
   ```bash
   # Run system tests
   python test_system.py
   python test_imports.py
   python test_openrouter.py
   python test_resume_upload.py
   ```

### Production Deployment

1. **Build Production Images**
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

2. **Deploy**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## API Documentation

The API provides comprehensive endpoints for managing interviews, reports, and resume analysis. Full API documentation is available through the built-in Swagger UI when running the backend server.

### Core Endpoints

#### Interview Management
- **Start Interview**: Initialize new interview session
- **Submit Answer**: Process user responses with real-time evaluation
- **Get Report**: Retrieve comprehensive performance analysis

#### Resume Processing
- **Upload Resume**: Parse and analyze resume content
- **Get Analysis**: Retrieve resume insights and recommendations

#### Metrics & Reports
- **Performance Metrics**: Real-time performance tracking
- **Historical Reports**: Access previous interview sessions

## Usage

1. **User Registration**: Create account and set up profile
2. **Resume Upload**: Upload resume for initial analysis
3. **Interview Setup**: Select role and experience level
4. **Interview Session**: Answer AI-generated questions
5. **Real-time Feedback**: Receive immediate analysis and suggestions
6. **Final Report**: Review comprehensive performance report

## Development

### Running Tests
```bash
# Backend tests
cd backend && python -m pytest

# Frontend tests
cd frontend && npm test
```

### Code Quality
```bash
# Backend linting
cd backend && flake8

# Frontend linting
cd frontend && npm run lint
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript strict mode for frontend
- Write comprehensive tests for new features
- Update documentation for API changes
- Ensure cross-browser compatibility

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with FastAPI and React
- AI capabilities powered by OpenAI GPT models
- UI components styled with Tailwind CSS
- Icons from Lucide React
