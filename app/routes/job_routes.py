from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from bson import ObjectId
from pymongo.errors import PyMongoError
from app.database import job_collection, application_collection
import os


# Set upload folder
UPLOAD_FOLDER = "uploads/resumes"
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(
        ".", 1)[1].lower() in ALLOWED_EXTENSIONS


job_bp = Blueprint('job_bp', __name__, url_prefix='/jobs')


@job_bp.route('/explore', methods=['GET'], endpoint="explore")
def explore_api():
    try:
        # Get filter parameters
        keyword = request.args.get('keyword', '').strip().lower()
        location = request.args.get('location', '').strip().lower()
        job_type = request.args.get('type', '').strip()
        experience = request.args.get('experience', '').strip()
        salary_range = request.args.get('salaryRange', '').strip()

        # Build query
        query = {}
        if keyword:
            query['$or'] = [{
                'title': {
                    '$regex': keyword,
                    '$options': 'i'
                }
            }, {
                'description': {
                    '$regex': keyword,
                    '$options': 'i'
                }
            }]
        if location:
            query['location'] = {'$regex': location, '$options': 'i'}
        if job_type:
            query['type'] = job_type
        if experience:
            query['experience'] = experience
        if salary_range:
            query['salaryRange'] = salary_range

        # Ensure database connection
        if job_collection is None:
            return render_template("error.html",
                                   message="Database connection failed"), 500

        # Get total count
        total_jobs = job_collection.count_documents(query)

        # Handle pagination
        try:
            page = max(1, int(request.args.get('page', 1)))
        except ValueError:
            return render_template("error.html",
                                   message="Invalid page number"), 400

        per_page = 3
        skip = (page - 1) * per_page
        jobs = list(job_collection.find(query).skip(skip).limit(per_page))

        # Convert `_id` from ObjectId to string
        for job in jobs:
            job['_id'] = str(job['_id'])

        return render_template("explore.html",
                               jobs=jobs,
                               total=total_jobs,
                               page=page,
                               pages=(total_jobs + per_page - 1) // per_page)

    except PyMongoError as e:
        return render_template("error.html",
                               message=f"Database error: {str(e)}"), 500
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # Log full traceback
        return render_template("error.html",
                               message=f"Internal server error: {str(e)}"), 500


@job_bp.route('/<job_id>')
def get_job(job_id):
    try:
        # Validate and convert job_id
        try:
            job_object_id = ObjectId(job_id)
        except Exception:
            return "Invalid Job ID", 400

        job = job_collection.find_one({'_id': job_object_id})
        if job:
            job['_id'] = str(job['_id'])  # Convert ObjectId to string
            return render_template("job-details.html", job=job)

        return "Job not found", 404

    except PyMongoError as e:
        return f"Database error: {str(e)}", 500
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # Log full traceback
        return "Internal server error", 500


@job_bp.route("/apply", methods=["POST"], endpoint="apply")
def apply():
    try:
        job_id = request.form.get("job_id")
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        cover_letter = request.form.get("cover_letter")
        resume = request.files.get("resume")  # File input

        if not job_id or not full_name or not email or not phone or not cover_letter or not resume:
            flash("❌ Missing required fields. Please fill out all fields.", "error")
            return redirect(request.referrer)

        # Convert job_id to ObjectId
        job_object_id = ObjectId(job_id)

        # Save file
        resume_filename = f"{full_name.replace(' ', '_')}_resume.pdf"
        resume_path = os.path.join(UPLOAD_FOLDER, resume_filename)
        resume.save(resume_path)

        # Save application to MongoDB
        application_data = {
            "job_id": job_object_id,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "cover_letter": cover_letter,
            "resume_path": resume_path,  # Store file path
            "status": "Pending"
        }
        application_collection.insert_one(application_data)

        
        return redirect(url_for("job_bp.get_job", job_id=job_id))

    except Exception as e:
        
        flash("⚠️ An error occurred while submitting your application.", "error")
        return redirect(request.referrer)
