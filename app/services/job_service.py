from bson import ObjectId
from typing import List, Optional
from app.database import job_collection
from app.models.job import Job

def add_job(job_data: dict) -> Optional[Job]:
    job = job_collection.insert_one(job_data)
    new_job = job_collection.find_one({"_id": job.inserted_id})
    if new_job:
        new_job["_id"] = str(new_job["_id"])  
        return Job(**new_job)
    return None

def retrieve_jobs() -> List[Job]:
    jobs = []
    for job in job_collection.find():
        job["_id"] = str(job["_id"])  # Convert ObjectId to string
        jobs.append(Job(**job))
    return jobs

def retrieve_job(id: str) -> Optional[Job]:
    try:
        job = job_collection.find_one({"_id": ObjectId(id)})
        if job:
            job["_id"] = str(job["_id"])  
            return Job(**job)
    except Exception:
        return None
    return None

def update_job(id: str, data: dict) -> bool:
    if not data:
        return False
    try:
        updated_job = job_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return updated_job.modified_count > 0
    except Exception:
        return False

def delete_job(id: str) -> bool:
    try:
        deleted_job = job_collection.delete_one({"_id": ObjectId(id)})
        return deleted_job.deleted_count > 0
    except Exception:
        return False
