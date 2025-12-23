# GenAI Career Intelligence Platform  

### AWS ImpactX Challenge – IIT Bombay TechFest Finals

An AI-powered, cloud-native interview and career intelligence platform built using **Ollama Local AI** with **Gemini AI fallback** and **AWS S3 + MongoDB Atlas** to help candidates prepare for interviews, assess job readiness, and improve employability through real-time feedback and adaptive evaluation.

---

## 🚀 Overview

The **GenAI Career Intelligence Platform** simulates real-world interview scenarios by combining Local AI (Ollama), resume intelligence, behavioral analysis, and technical assessment. The platform features a **conversational interview system** and **dynamic job fit analysis** that creates natural and adaptive experiences powered by local AI for privacy and cost-effectiveness.

---

## ✨ Key Features (Powered by Ollama + AWS)

- **🤖 Conversational Interview System**  
  Dynamic 8-question interview flow where each question builds naturally on previous responses using Ollama local AI with Gemini fallback.

- **🎯 Dynamic Job Fit Analysis (NEW)**  
  Step-by-step workflow: Upload resume → Select/type role → Get AI-powered analysis with comprehensive recommendations.

- **📊 Real-Time Answer Evaluation & Scoring**  
  Instant feedback with technical, communication, confidence, and relevance scoring using advanced AI analysis.

- **📄 Enhanced Resume Parsing & Analysis**  
  Advanced parsing with 500+ technical keywords, accurate experience calculation (months/years), and comprehensive skill extraction.

- **🎯 Aptitude & Logical Reasoning Assessment**  
  Comprehensive aptitude testing with quantitative, logical, pattern recognition, and analytical questions.

- **💼 50+ Role Support + Custom Roles**  
  Predefined roles across all tech domains OR custom role input for personalized analysis.

- **📈 Adaptive Interview Flow**  
  Questions dynamically adjust based on candidate responses, role requirements, and conversation context.

- **📋 Comprehensive Performance Reports**  
  Detailed post-interview analysis with strengths, gaps, improvement suggestions, and career guidance.

- **🔄 Intelligent AI Architecture**  
  - **Primary**: Ollama Local AI (Privacy-focused, cost-effective)
  - **Fallback**: Gemini API (Cloud reliability)
  - **Deterministic**: Rule-based fallbacks (100% uptime)

- **🎨 Modern React Frontend**  
  Responsive, accessible UI with real-time feedback, step-by-step workflows, and seamless user experience.

- **⚡ High-Performance Backend**  
  FastAPI-based backend with robust error handling, session management, and comprehensive API documentation.

---

## 🆕 New Dynamic Job Fit Analysis

### **Step-by-Step Workflow (Like Interview Flow)**
1. **📤 Upload Resume**: Drag & drop or file selection (PDF, DOC, DOCX, TXT)
2. **🎯 Select Role**: Choose from 50+ predefined roles OR enter custom role
3. **🤖 AI Analysis**: Ollama processes job fit with real-time progress
4. **📊 Results**: Comprehensive analysis with scores and recommendations

### **Enhanced Features**
- **Real-time Parsing**: Advanced skill extraction with 500+ keywords
- **Smart Role Selection**: Auto-suggest based on resume analysis
- **Custom Role Support**: Enter any role title for analysis
- **Comprehensive Scoring**: Overall fit, skill match, experience match
- **Actionable Insights**: Next steps and career development guidance

---

## 🏗️ Simplified AWS Architecture

### **Cloud Services (Minimal & Cost-Effective)**
- **📦 Amazon S3**: Resume storage, report files, and static assets
- **🗄️ MongoDB Atlas**: User data, interview sessions, and analytics
- **🔐 AWS IAM**: Security and access management

### **AI Processing Architecture**
```
Primary: Ollama (Local) → Fallback: Gemini API → Deterministic Rules
```

### **Benefits of This Architecture**
- **💰 Cost-Effective**: Minimal AWS services, local AI processing
- **🔒 Privacy-Focused**: Resume data processed locally with Ollama
- **⚡ High Performance**: Local AI for faster response times
- **🛡️ Reliable**: Automatic fallback ensures 100% uptime
- **📈 Scalable**: Can easily add more AWS services as needed

---

---

## 🎯 Dynamic Job Fit Analysis - Complete Workflow

### **How It Works**

1. **📤 Upload Resume**
   - Drag & drop or click to select resume file
   - Supports PDF, DOC, DOCX, TXT formats (up to 10MB)
   - Real-time parsing with progress indicators

2. **🤖 AI-Powered Parsing**
   - Extracts 500+ technical skills across all domains
   - Calculates accurate experience (handles months/years correctly)
   - Identifies projects, education, and role estimation
   - Generates comprehensive candidate profile

3. **🎯 Role Selection**
   - Choose from 50+ predefined roles (Software Engineer to AI Engineer)
   - OR enter custom role title for personalized analysis
   - Smart recommendations based on parsed resume
   - Search and filter functionality

4. **⚡ Ollama AI Analysis**
   - Local AI processing for privacy and speed
   - Comprehensive job fit scoring (Overall, Skills, Experience)
   - Role-specific insights and recommendations
   - Confidence scoring and next steps

5. **📊 Detailed Results**
   - Overall fit percentage with color-coded recommendations
   - Matched skills vs. missing skills analysis
   - Experience alignment and growth potential
   - Actionable career development steps

### **API Endpoints**
```bash
GET  /api/job-fit/available-roles           # Get 50+ available roles
POST /api/job-fit/parse-resume              # Parse resume file
POST /api/job-fit/analyze-with-role         # Analyze job fit with Ollama
POST /api/job-fit/bulk-role-analysis        # Analyze multiple roles
```

### **Frontend Integration**
- Step-by-step workflow UI with progress indicators
- Real-time file upload and parsing feedback
- Dynamic role selection with search capabilities
- Comprehensive results display with actionable insights

---

## 🚀 Quick Start & Setup

### **Prerequisites**
- Python 3.8+ with pip
- Node.js 16+ with npm
- Ollama installed locally ([Installation Guide](https://ollama.ai))
- Git for version control

### **1. Ollama Setup (Required for AI Analysis)**
```bash
# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Download from https://ollama.ai/download

# Pull required model
ollama pull llama3.1:8b

# Verify installation
ollama list
```

### **2. Project Setup**
```bash
# Clone repository
git clone <repository-url>
cd gen-ai-carrier-platform

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create database tables
python create_tables.py

# Frontend setup
cd ../frontend
npm install
```

### **3. Environment Configuration**
```bash
# Backend environment (.env)
cd backend
cp .env.example .env

# Configure these variables:
GEMINI_API_KEY=your_gemini_api_key_here  # For fallback
OLLAMA_BASE_URL=http://localhost:11434   # Local Ollama
DATABASE_URL=sqlite:///./interview.db    # Local database
```

### **4. Run Development Environment**
```bash
# Terminal 1: Start Ollama (if not running as service)
ollama serve

# Terminal 2: Start Backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3: Start Frontend  
cd frontend
npm run dev

# Access application at http://localhost:3000
```

### **5. Test the System**
```bash
# Test dynamic job fit analysis
cd backend
python test_dynamic_job_fit.py

# Test complete system
python test_integration.py

# Check AI engine status
python check_status.py
```

---

## 📁 Project Structure

```
gen-ai-carrier-platform/
├── 📚 docs/                    # Documentation
│   ├── README.md              # Documentation hub
│   ├── ollama-setup.md        # Ollama integration guide
│   └── aws-architecture.md    # AWS deployment guide
├── 🧪 tests/                   # Testing files
│   ├── README.md              # Testing guide
│   └── test_complete_system.py
├── 🖥️ backend/                 # FastAPI backend
│   ├── app/
│   │   ├── ai_engines/        # Ollama + Gemini AI integration
│   │   │   ├── ollama_engine.py      # Local AI processing
│   │   │   ├── gemini_engine.py      # Cloud AI fallback
│   │   │   └── engine_router.py      # Intelligent AI routing
│   │   ├── routes/            # API endpoints
│   │   │   ├── job_fit_routes.py     # Dynamic job fit analysis
│   │   │   ├── interview_routes.py   # Interview management
│   │   │   └── resume_routes.py      # Resume processing
│   │   ├── services/          # Business logic
│   │   │   └── resume_service.py     # Enhanced resume parsing
│   │   └── schemas/           # Data models
│   ├── test_dynamic_job_fit.py       # Job fit testing
│   ├── check_status.py               # AI engine status
│   └── requirements.txt
├── 🎨 frontend/                # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── jobfit/               # Dynamic job fit UI
│   │   │   │   └── JobFitAnalysis.tsx
│   │   │   ├── interview/            # Interview interface
│   │   │   ├── dashboard/            # User dashboard
│   │   │   └── common/               # Shared components
│   │   └── styles/            # Modern design system
│   └── package.json
├── 📄 DYNAMIC_JOB_FIT_COMPLETE.md   # Feature documentation
└── 📄 README.md               # This file
```

---

## 🚀 Quick Start

### **📖 For Documentation**
- **[📚 Documentation Hub](./docs/README.md)** - Complete documentation index
- **[🎯 Getting Started Guide](./docs/start.md)** - Setup and installation
- **[✅ Migration Complete](./docs/GEMINI_MIGRATION_COMPLETE.md)** - Latest system updates

### **🧪 For Testing**
- **[🧪 Testing Suite](./tests/README.md)** - Complete testing guide
- **[🚀 System Test](./tests/test_complete_system.py)** - Run comprehensive system test
- **[🤖 AI Integration Test](./tests/test_gemini_integration.py)** - Test AI functionality

### **⚡ Quick Commands**
```bash
# Test the dynamic job fit system
python backend/test_dynamic_job_fit.py

# Test complete system functionality
python tests/test_complete_system.py

# Start backend server (with Ollama integration)
cd backend && python -m uvicorn app.main:app --reload

# Start frontend (with new job fit UI)
cd frontend && npm start

# Check Ollama status and AI engine routing
python backend/check_status.py
```

---

## 🏗️ AWS-Centric Architecture (Simplified & Cost-Effective)

### **Intelligent AI Processing**
- **Primary AI**: Ollama Local AI (Privacy-focused, cost-effective)
- **Fallback AI**: Gemini API (Cloud reliability when local AI unavailable)
- **Deterministic**: Rule-based responses (100% uptime guarantee)

### **AWS Services (Minimal Setup)**
- **📦 Amazon S3**: 
  - Resume file storage (PDF, DOC, DOCX, TXT)
  - Interview report storage
  - Static asset hosting
- **🗄️ MongoDB Atlas**: 
  - User profiles and authentication
  - Interview session data
  - Analytics and performance metrics
- **🔐 AWS IAM**: 
  - Security and access management
  - S3 bucket permissions

### **Architecture Benefits**
- **💰 Cost-Effective**: Only 2 AWS services needed
- **🔒 Privacy-First**: Local AI processing keeps data secure
- **⚡ High Performance**: Local AI for faster response times
- **🛡️ 100% Uptime**: Automatic fallback system
- **📈 Scalable**: Easy to add more AWS services later

### **Reliability & Fallback System**
```
Ollama (Local AI) → Gemini API (Cloud) → Deterministic Rules
```
If local AI fails, system automatically falls back to cloud AI, and ultimately to deterministic algorithms that always work.

---

## 🎯 Use Cases

- **Interview Preparation**: AI-powered mock interviews for students and job seekers
- **Job Fit Analysis**: Dynamic resume analysis against 50+ roles or custom positions  
- **Campus Placement**: Readiness assessment for university placement programs
- **Career Guidance**: Skill-gap analysis and personalized development recommendations
- **Enterprise Hiring**: AI-driven candidate evaluation for institutions and companies
- **Skill Development**: Identify missing skills and get actionable learning paths

---

## 🌍 Impact & Benefits

### **For Job Seekers**
- **🎯 Personalized Analysis**: AI-powered job fit analysis for any role
- **📈 Skill Development**: Identify gaps and get learning recommendations
- **🎤 Interview Practice**: Realistic mock interviews with instant feedback
- **🔒 Privacy Protection**: Local AI processing keeps resume data secure

### **For Organizations**
- **💰 Cost Reduction**: Local AI processing reduces API costs
- **⚡ Fast Processing**: Local AI for immediate candidate evaluation
- **📊 Comprehensive Insights**: Detailed candidate assessment and recommendations
- **🔄 Scalable Solution**: Handle multiple candidates simultaneously

### **Technical Benefits**
- **🛡️ 100% Uptime**: Automatic fallback ensures continuous service
- **🔒 Data Privacy**: Resume processing stays local with Ollama
- **💸 Cost Effective**: Minimal AWS services (S3 + MongoDB only)
- **⚡ High Performance**: Local AI for faster response times  

---

## 🧪 Current Status

- ✅ **Dynamic Job Fit Analysis implemented**
  - Step-by-step workflow (Upload → Select Role → AI Analysis → Results)
  - 50+ predefined roles + custom role support
  - Real-time resume parsing with 500+ technical keywords
  - Ollama-powered AI analysis with comprehensive scoring
- ✅ **Intelligent AI Architecture with automatic fallback**
  - Primary: Ollama Local AI (privacy-focused, cost-effective)
  - Fallback: Gemini API (cloud reliability)
  - Deterministic: Rule-based responses (100% uptime)
- ✅ **Enhanced resume parsing and job-fit analysis**
  - Advanced skill extraction and experience calculation
  - Accurate months/years conversion (fixed 4 months = 0.33 years)
  - Role estimation and comprehensive profile generation
- ✅ **Real-time feedback engine with comprehensive scoring**
- ✅ **Aptitude & Logical Reasoning Assessment**
- ✅ **Modern React frontend with step-by-step workflows**
- ✅ **Simplified AWS architecture (S3 + MongoDB Atlas)**
- 🔄 **Production deployment ready**

---

## 🏁 Built For

**AWS ImpactX Challenge – IIT Bombay TechFest**  
Team: *403 Forbidden*

### Judging Criteria

Submissions will be evaluated by a panel of experts based on the following criteria:

- **Innovation & Originality**: Is the idea novel and creative?
- **GenAI Application**: Is Generative AI used in a meaningful and core way?
- **Impact & Value**: Does the solution address a significant problem and offer a clear value proposition?
- **Feasibility & Team Capability**: Is the idea practical? Does the team (based on supporting materials) demonstrate the capability to build a prototype during Phase 2?
- **Clarity**: How clearly and effectively is the idea communicated in the deck and video?

*Participants are recommended to build the prototype using kiro.dev (to be instructed by the AWS experts during round 2)*

---

## 📌 Future Enhancements

- **🌐 Multi-language Support**: Interviews and analysis in multiple languages
- **🏢 Enterprise Dashboard**: Institution-level analytics and candidate management  
- **📚 Learning Pathways**: Personalized skill development based on job fit analysis
- **🤝 Integration APIs**: Connect with ATS systems and HR platforms
- **📱 Mobile Application**: Native mobile app for on-the-go interview practice
- **🎥 Video Analysis**: Advanced behavioral analysis using computer vision
- **🔊 Voice Analysis**: Speech pattern and communication skill assessment

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

## 💻 Usage Guide

### **Dynamic Job Fit Analysis**
1. **Access**: Navigate to "Job Fit Analysis" from dashboard or navbar
2. **Upload**: Drag & drop your resume or click to select file
3. **Parse**: Wait for AI to extract skills, experience, and profile data
4. **Select Role**: Choose from 50+ roles or enter custom role title
5. **Analyze**: Ollama AI processes job fit (30-60 seconds)
6. **Results**: Review comprehensive analysis with actionable recommendations

### **Interview Practice**
1. **Setup**: Create profile and upload resume for context
2. **Configure**: Select role, experience level, and interview type
3. **Interview**: Answer AI-generated questions with real-time feedback
4. **Evaluation**: Receive instant scoring and improvement suggestions
5. **Report**: Access detailed performance analysis and career guidance

### **Key Features**
- **🔒 Privacy-First**: Resume data processed locally with Ollama
- **⚡ Real-Time**: Instant feedback and progress indicators
- **🎯 Personalized**: Analysis tailored to specific roles and experience
- **📊 Comprehensive**: Detailed scoring and actionable recommendations
- **🛡️ Reliable**: Automatic fallback ensures continuous service

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

## 📄 License

This project is developed for academic, research, and hackathon purposes. Commercial usage is subject to licensing and approval.

## 🙏 Acknowledgments

- **AI Processing**: Powered by Ollama local AI with Gemini API fallback
- **Backend Framework**: Built with FastAPI for high-performance APIs
- **Frontend Framework**: React 18 with TypeScript for modern UI
- **Cloud Infrastructure**: AWS S3 for storage, MongoDB Atlas for data
- **UI Components**: Styled with Tailwind CSS and Lucide React icons
- **Development Environment**: Optimized for Kiro.dev platform
- **Challenge**: Developed for AWS ImpactX Challenge – IIT Bombay TechFest

### **Technology Stack**
- **🤖 AI**: Ollama (Primary) + Gemini API (Fallback)
- **☁️ Cloud**: AWS S3 + MongoDB Atlas (Minimal setup)
- **🖥️ Backend**: FastAPI + SQLAlchemy + Pydantic
- **🎨 Frontend**: React + TypeScript + Tailwind CSS
- **🔧 DevOps**: Docker + Docker Compose + Makefile
