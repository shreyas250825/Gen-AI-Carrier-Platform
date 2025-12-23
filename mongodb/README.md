# MongoDB Atlas Setup 🗄️

## 📋 Overview

This directory contains all MongoDB Atlas configuration and setup files for the GenAI Career Intelligence Platform.

## 📁 Files

- **`sample_data.json`** - Complete sample data for all collections
- **`setup_script.py`** - Automated setup script to insert data and create indexes
- **`config.py`** - MongoDB connection configuration and helper functions
- **`README.md`** - This documentation file

## 🚀 Quick Setup

### 1. Prerequisites
```bash
pip install pymongo dnspython
```

### 2. Environment Configuration
Add to your `.env` file:
```bash
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/genai_career?retryWrites=true&w=majority
```

### 3. Run Setup Script
```bash
cd mongodb
python setup_script.py
```

## 📊 Database Structure

### Collections
- `interview_sessions` - Interview results and feedback
- `job_fit_analyses` - Job fit analysis results  
- `user_profiles` - User information and preferences
- `aptitude_assessments` - Aptitude test results
- `resume_analyses` - Resume parsing results
- `system_analytics` - System metrics and usage data

### Sample Data Count
- Interview Sessions: 3 documents
- Job Fit Analyses: 2 documents
- User Profiles: 2 documents
- Aptitude Assessments: 1 document
- Resume Analyses: 1 document
- System Analytics: 1 document

## 🔧 Usage Examples

### Basic Connection
```python
from config import MongoDBConfig

config = MongoDBConfig()
db = config.get_database()
```

### Query Data
```python
# Get all interviews for a candidate
interviews = config.get_collection('interview_sessions').find(
    {"candidateName": "Shreyas"}
)

# Get high-scoring job fits
high_fits = config.get_collection('job_fit_analyses').find(
    {"overallFitScore": {"$gte": 80}}
)
```

### Insert New Data
```python
from config import insert_interview_session

new_interview = {
    "candidateName": "John Doe",
    "role": "Data Scientist",
    "score": 78,
    "feedback": "Good analytical skills"
}

result = insert_interview_session(new_interview)
```

## 🔍 Database Indexes

The setup script automatically creates these indexes:

```javascript
// Interview Sessions
db.interview_sessions.createIndex({"candidateName": 1})
db.interview_sessions.createIndex({"createdAt": -1})
db.interview_sessions.createIndex({"role": 1})
db.interview_sessions.createIndex({"score": -1})

// Job Fit Analyses  
db.job_fit_analyses.createIndex({"candidateName": 1})
db.job_fit_analyses.createIndex({"targetRole": 1})
db.job_fit_analyses.createIndex({"overallFitScore": -1})

// User Profiles
db.user_profiles.createIndex({"email": 1}, {unique: true})
db.user_profiles.createIndex({"name": 1})
```

## 📈 Analytics Queries

### Performance Analytics
```javascript
// Average scores by role
db.interview_sessions.aggregate([
  {$group: {_id: "$role", avgScore: {$avg: "$score"}}},
  {$sort: {avgScore: -1}}
])

// Top performing candidates
db.interview_sessions.aggregate([
  {$group: {_id: "$candidateName", maxScore: {$max: "$score"}}},
  {$sort: {maxScore: -1}},
  {$limit: 10}
])
```

## 🔒 Security

- ✅ Use MongoDB Atlas IP whitelist
- ✅ Enable authentication
- ✅ Use connection string with credentials
- ✅ Implement proper error handling

## 📞 Troubleshooting

**Connection Issues:**
```bash
# Test connection
python config.py
```

**Common Issues:**
- ❌ **Connection timeout**: Check IP whitelist in Atlas
- ❌ **Authentication failed**: Verify username/password
- ❌ **Database not found**: Ensure database name is correct

---

**🎯 Ready for GenAI Career Intelligence Platform!**