#!/usr/bin/env python3
"""
MongoDB Atlas Setup Script for GenAI Career Intelligence Platform
"""

import json
import os
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

def connect_to_mongodb():
    """Connect to MongoDB Atlas"""
    # Replace with your MongoDB Atlas connection string
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://username:password@cluster.mongodb.net/genai_career?retryWrites=true&w=majority')
    
    try:
        client = MongoClient(MONGODB_URI)
        db = client.genai_career  # Database name
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully!")
        return db
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        return None

def insert_sample_data():
    """Insert sample data into MongoDB collections"""
    
    print("🚀 Inserting Sample Data into MongoDB Atlas")
    print("=" * 50)
    
    # Connect to database
    db = connect_to_mongodb()
    if not db:
        return False
    
    # Load sample data
    try:
        with open('sample_data.json', 'r') as f:
            sample_data = json.load(f)
    except FileNotFoundError:
        print("❌ Sample data file not found!")
        return False
    
    # Insert data into collections
    collections_inserted = 0
    
    for collection_name, documents in sample_data.items():
        try:
            collection = db[collection_name]
            
            # Convert string ObjectIds to actual ObjectIds
            for doc in documents:
                if '_id' in doc and isinstance(doc['_id'], str):
                    doc['_id'] = ObjectId(doc['_id'])
            
            # Insert documents
            if documents:
                result = collection.insert_many(documents)
                print(f"✅ Inserted {len(result.inserted_ids)} documents into '{collection_name}'")
                collections_inserted += 1
            else:
                print(f"⚠️  No documents to insert for '{collection_name}'")
                
        except Exception as e:
            print(f"❌ Error inserting into '{collection_name}': {e}")
    
    print("\n" + "=" * 50)
    print(f"🎉 Successfully inserted data into {collections_inserted} collections!")
    
    # Display collection stats
    print("\n📊 Collection Statistics:")
    for collection_name in sample_data.keys():
        try:
            count = db[collection_name].count_documents({})
            print(f"   {collection_name}: {count} documents")
        except Exception as e:
            print(f"   {collection_name}: Error getting count - {e}")
    
    return True

def create_indexes():
    """Create useful indexes for better performance"""
    
    print("\n🔍 Creating Database Indexes...")
    
    db = connect_to_mongodb()
    if not db:
        return False
    
    try:
        # Interview sessions indexes
        db.interview_sessions.create_index([("candidateName", 1)])
        db.interview_sessions.create_index([("createdAt", -1)])
        db.interview_sessions.create_index([("role", 1)])
        db.interview_sessions.create_index([("score", -1)])
        
        # Job fit analyses indexes
        db.job_fit_analyses.create_index([("candidateName", 1)])
        db.job_fit_analyses.create_index([("targetRole", 1)])
        db.job_fit_analyses.create_index([("overallFitScore", -1)])
        db.job_fit_analyses.create_index([("createdAt", -1)])
        
        # User profiles indexes
        db.user_profiles.create_index([("email", 1)], unique=True)
        db.user_profiles.create_index([("name", 1)])
        db.user_profiles.create_index([("currentRole", 1)])
        
        # Resume analyses indexes
        db.resume_analyses.create_index([("candidateName", 1)])
        db.resume_analyses.create_index([("uploadDate", -1)])
        
        # Aptitude assessments indexes
        db.aptitude_assessments.create_index([("candidateName", 1)])
        db.aptitude_assessments.create_index([("assessmentType", 1)])
        db.aptitude_assessments.create_index([("score", -1)])
        
        print("✅ Database indexes created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating indexes: {e}")
        return False

def verify_data():
    """Verify that data was inserted correctly"""
    
    print("\n🔍 Verifying Inserted Data...")
    
    db = connect_to_mongodb()
    if not db:
        return False
    
    try:
        # Sample queries to verify data
        print("\n📋 Sample Data Verification:")
        
        # Check interview sessions
        interview_count = db.interview_sessions.count_documents({})
        print(f"   📝 Interview Sessions: {interview_count}")
        
        if interview_count > 0:
            sample_interview = db.interview_sessions.find_one({"candidateName": "Shreyas"})
            if sample_interview:
                print(f"      ✅ Found interview for Shreyas with score: {sample_interview.get('score', 'N/A')}")
        
        # Check job fit analyses
        jobfit_count = db.job_fit_analyses.count_documents({})
        print(f"   🎯 Job Fit Analyses: {jobfit_count}")
        
        # Check user profiles
        users_count = db.user_profiles.count_documents({})
        print(f"   👤 User Profiles: {users_count}")
        
        # Check aptitude assessments
        aptitude_count = db.aptitude_assessments.count_documents({})
        print(f"   🧠 Aptitude Assessments: {aptitude_count}")
        
        # Check resume analyses
        resume_count = db.resume_analyses.count_documents({})
        print(f"   📄 Resume Analyses: {resume_count}")
        
        print("\n✅ Data verification completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def main():
    """Main function"""
    
    print("🎯 GenAI Career Intelligence Platform - MongoDB Setup")
    print("=" * 60)
    
    # Insert sample data
    if not insert_sample_data():
        print("❌ Failed to insert sample data")
        return
    
    # Create indexes
    if not create_indexes():
        print("⚠️  Failed to create indexes, but data was inserted")
    
    # Verify data
    if not verify_data():
        print("⚠️  Failed to verify data, but insertion may have succeeded")
    
    print("\n🎉 MongoDB Atlas setup completed!")
    print("\n💡 Next Steps:")
    print("   1. Update your application's MongoDB connection string")
    print("   2. Test the connection from your application")
    print("   3. Start using the GenAI Career Intelligence Platform!")
    
    print("\n📊 Sample Data Includes:")
    print("   • Interview sessions with detailed feedback")
    print("   • Job fit analyses with skill matching")
    print("   • User profiles with preferences and statistics")
    print("   • Aptitude assessment results")
    print("   • Resume analysis data")
    print("   • System analytics and metrics")

if __name__ == "__main__":
    main()