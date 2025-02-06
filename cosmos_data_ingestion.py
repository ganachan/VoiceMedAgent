from db_config import get_db_connection

# Connect to the database and collections
db = get_db_connection()
users_collection = db["users"]
groups_collection = db["groups"]

# Sample data for users
users = [
    {
        "_id": "user789",
        "userName": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "role": "Physiotherapist",
        "description": "Specialist in physical therapy and rehabilitation",
        "groups": ["Rehabilitation Group"],
        "createdAt": "2025-01-18T14:00:00Z",
        "updatedAt": "2025-01-19T10:00:00Z"
    },
    {
        "_id": "user890",
        "userName": "Michael Smith",
        "email": "michael.smith@example.com",
        "role": "Surgeon",
        "description": "Experienced in general and laparoscopic surgeries",
        "groups": ["Surgery Group"],
        "createdAt": "2025-01-15T08:30:00Z",
        "updatedAt": "2025-01-16T11:00:00Z"
    },
    {
        "_id": "user901",
        "userName": "Emily Davis",
        "email": "emily.davis@example.com",
        "role": "Pharmacist",
        "description": "Expert in pharmaceutical care and medication management",
        "groups": ["Pharmacy Group"],
        "createdAt": "2025-01-19T12:00:00Z",
        "updatedAt": "2025-01-20T09:00:00Z"
    },
    {
        "_id": "user345",
        "userName": "Chris Brown",
        "email": "chris.brown@example.com",
        "role": "Radiologist",
        "description": "Specializes in diagnostic imaging and X-rays",
        "groups": ["Radiology Group"],
        "createdAt": "2025-01-10T07:00:00Z",
        "updatedAt": "2025-01-11T06:00:00Z"
    },
    {
        "_id": "user567",
        "userName": "Samantha Green",
        "email": "samantha.green@example.com",
        "role": "Pediatrician",
        "description": "Provides medical care for children and adolescents",
        "groups": ["Pediatrics Group"],
        "createdAt": "2025-01-13T10:15:00Z",
        "updatedAt": "2025-01-14T09:30:00Z"
    },
    {
        "_id": "user678",
        "userName": "Robert Taylor",
        "email": "robert.taylor@example.com",
        "role": "Anesthesiologist",
        "description": "Manages anesthesia and pain during surgeries",
        "groups": ["Anesthesia Group"],
        "createdAt": "2025-01-12T09:45:00Z",
        "updatedAt": "2025-01-13T08:30:00Z"
    },
    {
        "_id": "user112",
        "userName": "Linda Wilson",
        "email": "linda.wilson@example.com",
        "role": "Dietitian",
        "description": "Expert in nutrition and dietary counseling",
        "groups": ["Nutrition Group"],
        "createdAt": "2025-01-16T15:00:00Z",
        "updatedAt": "2025-01-17T11:00:00Z"
    },
    {
        "_id": "user223",
        "userName": "James White",
        "email": "james.white@example.com",
        "role": "Orthopedic Surgeon",
        "description": "Specialist in musculoskeletal system surgeries",
        "groups": ["Orthopedics Group"],
        "createdAt": "2025-01-14T13:20:00Z",
        "updatedAt": "2025-01-15T09:00:00Z"
    }
]

# Insert data into the users collection
for user in users:
    users_collection.update_one(
        {"_id": user["_id"]},  # Filter by _id
        {"$set": user},        # Insert or update the document
        upsert=True            # Create the document if it doesn't exist
    )
    print(f"Upserted user with _id {user['_id']}.")

# Sample data for groups
groups = [
    {
        "_id": "group123",
        "groupName": "ICU Group",
        "description": "Critical care unit for high-priority patients",
        "members": ["user123"],  # User IDs from the users collection
        "createdAt": "2025-01-22T09:00:00Z",
        "updatedAt": "2025-01-22T10:15:00Z"
    },
    {
        "_id": "group456",
        "groupName": "Cardiology Group",
        "description": "Specialized group for cardiology-related treatments",
        "members": ["user456"],
        "createdAt": "2025-01-20T08:30:00Z",
        "updatedAt": "2025-01-21T08:30:00Z"
    },
    {
        "_id": "group789",
        "groupName": "Rehabilitation Group",
        "description": "Focuses on physical therapy and rehabilitation",
        "members": ["user789"],
        "createdAt": "2025-01-18T14:00:00Z",
        "updatedAt": "2025-01-19T10:00:00Z"
    },
    {
        "_id": "group890",
        "groupName": "Surgery Group",
        "description": "Group for general and laparoscopic surgeries",
        "members": ["user890"],
        "createdAt": "2025-01-15T08:30:00Z",
        "updatedAt": "2025-01-16T11:00:00Z"
    },
    {
        "_id": "group901",
        "groupName": "Pharmacy Group",
        "description": "Handles pharmaceutical care and medication management",
        "members": ["user901"],
        "createdAt": "2025-01-19T12:00:00Z",
        "updatedAt": "2025-01-20T09:00:00Z"
    },
    {
        "_id": "group345",
        "groupName": "Radiology Group",
        "description": "Specializes in diagnostic imaging and X-rays",
        "members": ["user345"],
        "createdAt": "2025-01-10T07:00:00Z",
        "updatedAt": "2025-01-11T06:00:00Z"
    },
    {
        "_id": "group567",
        "groupName": "Pediatrics Group",
        "description": "Provides medical care for children and adolescents",
        "members": ["user567"],
        "createdAt": "2025-01-13T10:15:00Z",
        "updatedAt": "2025-01-14T09:30:00Z"
    },
    {
        "_id": "group678",
        "groupName": "Anesthesia Group",
        "description": "Focuses on anesthesia and pain management during surgeries",
        "members": ["user678"],
        "createdAt": "2025-01-12T09:45:00Z",
        "updatedAt": "2025-01-13T08:30:00Z"
    },
    {
        "_id": "group112",
        "groupName": "Nutrition Group",
        "description": "Group for dietary counseling and nutrition",
        "members": ["user112"],
        "createdAt": "2025-01-16T15:00:00Z",
        "updatedAt": "2025-01-17T11:00:00Z"
    },
    {
        "_id": "group223",
        "groupName": "Orthopedics Group",
        "description": "Handles musculoskeletal system surgeries",
        "members": ["user223"],
        "createdAt": "2025-01-14T13:20:00Z",
        "updatedAt": "2025-01-15T09:00:00Z"
    }
]

# Insert data into the groups collection
for group in groups:
    groups_collection.update_one(
        {"_id": group["_id"]},  # Filter by _id
        {"$set": group},        # Insert or update the document
        upsert=True             # Create the document if it doesn't exist
    )
    print(f"Upserted group with _id {group['_id']}.")
