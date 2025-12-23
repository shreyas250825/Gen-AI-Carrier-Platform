"""
MongoDB Atlas Configuration for GenAI Career Intelligence Platform
"""

import os
from pymongo import MongoClient
from datetime import datetime

class MongoDBConfig:
    """MongoDB Atlas configuration and connection management"""
    
    def __init__(self):
        # MongoDB Atlas connection string
        # Replace with your actual connection string
        self.MONGODB_URI = os.getenv(
            'MONGODB_URI', 
            'mongodb+srv://username:password@cluster.mongodb.net/genai_career?retryWrites=true&w=majority'
        )
        
        # Database name
        self.DATABASE_NAME = 'genai_career'
        
        # Collection names
        self.COLLECTIONS = {
            'interview_sessions': 'interview_sessions',
            'job_fit_analyses': 'job_fit_analyses', 
            'user_profiles': 'user_profiles',
            'aptitude_assessments': 'aptitude_assessments',
            'resume_analyses': 'resume_analyses',
            'system_analytics': 'system_analytics'
        }
    
    def get_client(self):
        """Get MongoDB client"""
        try:
            client = MongoClient(self.MONGODB_URI)
            # Test connection
            client.admin.command('ping')
            return client
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            return None
    
    def get_database(self):
        """Get database instance"""
        client = self.get_client()
        if client:
            return client[self.DATABASE_NAME]
        return None
    
    def get_collection(self, collection_name):
        """Get specific collection"""
        db = self.get_database()
        if db and collection_name in self.COLLECTIONS:
            return db[self.COLLECTIONS[collection_name]]
        return None

# Sample usage functions
def insert_interview_session(session_data):
    """Insert a new interview session"""
    config = MongoDBConfig()
    collection = config.get_collection('interview_sessions')
    
    if collection:
        # Add timestamp if not present
        if 'createdAt' not in session_data:
            session_data['createdAt'] = datetime.now().strftime('%Y-%m-%d')
        
        result = collection.insert_one(session_data)
        return str(result.inserted_id)
    return None

def insert_job_fit_analysis(analysis_data):
    """Insert a new job fit analysis"""
    config = MongoDBConfig()
    collection = config.get_collection('job_fit_analyses')
    
    if collection:
        # Add timestamp if not present
        if 'createdAt' not in analysis_data:
            analysis_data['createdAt'] = datetime.now().strftime('%Y-%m-%d')
        
        result = collection.insert_one(analysis_data)
        return str(result.inserted_id)
    return None

def get_user_interviews(candidate_name):
    """Get all interviews for a specific candidate"""
    config = MongoDBConfig()
    collection = config.get_collection('interview_sessions')
    
    if collection:
        return list(collection.find({"candidateName": candidate_name}))
    return []

def get_user_job_fits(candidate_name):
    """Get all job fit analyses for a specific candidate"""
    config = MongoDBConfig()
    collection = config.get_collection('job_fit_analyses')
    
    if collection:
        return list(collection.find({"candidateName": candidate_name}))
    return []

# Example usage
if __name__ == "__main__":
    # Test connection
    config = MongoDBConfig()
    db = config.get_database()
    
    if db:
        print("✅ Successfully connected to MongoDB Atlas!")
        print(f"📊 Database: {config.DATABASE_NAME}")
        print("📋 Available collections:")
        for key, value in config.COLLECTIONS.items():
            print(f"   • {key}: {value}")
    else:
        print("❌ Failed to connect to MongoDB Atlas")
        print("💡 Make sure to update the MONGODB_URI in your environment variables")