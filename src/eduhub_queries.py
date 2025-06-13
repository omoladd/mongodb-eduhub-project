from pymongo import MongoClient
import json
from helper import Helper
from pymongo.errors import DuplicateKeyError, WriteError


class EdHubDB:
    def __init__(self):
        # Initialize helperclass
        self.helper = Helper()

        # File paths
        self.schemas_path = "../data/schema_validation.json"
        self.sample_data_path = "../data/sample_data.json"

        self.connection_url = "mongodb://localhost:27017/"
        self.database_name = "eduhub_db"
        self.client = MongoClient(self.connection_url)
        self.db = self.client[self.database_name]

        # drop existing collections to start afresh
        for collection in self.db.list_collection_names():
            self.db[collection].drop()

        # collections
        self.users_col = self.db["users"]
        self.courses_col = self.db["courses"]
        self.enrollments_col = self.db["enrollments"]
        self.lessons_col = self.db["lessons"]
        self.assignments_col = self.db["assignments"]
        self.submissions_col = self.db["submissions"]

    # Part 1
    def load_schemas(self):
        """Load validation schemas from JSON file"""
        try:
            with open(self.schemas_path, "r") as f:
                schemas = json.load(f)
            return schemas
        except FileNotFoundError:
            raise FileNotFoundError(f"Schema file not found: {self.schemas_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in schema file: {self.schemas_path}")

    def build_collection(self):
        """Setup collections and validations from JSON files"""

        schemas = self.load_schemas()

        try:
            for collection_name, validator in schemas.items():
                self.db.create_collection(collection_name, validator=validator)
                print(f"Created collection: {collection_name}")
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise

    # Part 2
    def seed_database(self):
        """Seed all collections with sample data, converting date fields using schema."""
        try:
            with open(self.sample_data_path, "r") as f:
                data = json.load(f)
            with open(self.schemas_path, "r") as f:
                schemas = json.load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(str(e))
        except json.JSONDecodeError as e:
            raise ValueError(str(e))

        for collection_name, documents in data.items():
            if isinstance(documents, list) and collection_name in schemas:
                date_fields = self.helper.get_date_fields(
                    schemas[collection_name]["$jsonSchema"]
                )
                documents = [
                    self.helper.convert_dates_by_schema(doc, date_fields)
                    for doc in documents
                ]
                if documents:
                    self.db[collection_name].insert_many(documents)
                    print(
                        f"Seeded {len(documents)} documents into '{collection_name}' collection."
                    )
            else:
                print(
                    f"Warning: Data for '{collection_name}' is not a list or schema missing, skipping."
                )

    ## Part 3 Basic CRUD operations
    def insert_student(self, data):
        """Insert a new student document into the users collection."""
        try:
            # Ensure role is a student
            data["role"] = "student"
            result = self.users_col.insert_one(data)
            return result
        except Exception as e:
            print(f"Unexpected error inserting student: {e}")
        return None

    def insert_course(self, data):
        """Insert a new course document into the courses collection."""
        try:
            result = self.courses_col.insert_one(data)
            return result.inserted_id
        except Exception as e:
            print(f"Unexpected error inserting course: {e}")
        return None

    def register_student(self, student_id, course_id):
        """Register a student to a course (create an enrollment)."""
        enrollment = {
            "enrollmentId": f"e{self.enrollments_col.count_documents({}) + 1}",
            "studentId": student_id,
            "courseId": course_id,
            "enrollmentDate": self.helper.faker.date_time(),
            "progress": 0.0,
            "completed": False,
            "certificateIssued": False,
        }
        try:
            result = self.enrollments_col.insert_one(enrollment)
            return result.inserted_id
        except Exception as e:
            print(f"Unexpected error registering student: {e}")
        return None

    def insert_lesson(self, data):
        """Add a lesson to a course (insert into lessons collection)."""
        try:
            result = self.lessons_col.insert_one(data)
            return result
        except Exception as e:
            print(f"Unexpected error adding lesson: {e}")
        return None

    def get_active_students(self):
        """Find all active students"""
        try:
            students = list(self.users_col.find({"role": "student", "isActive": True}))
            return students
        except Exception as e:
            print(f"Error fetching active students: {e}")
            return []

    def get_course_details(self):
        """Retrieve course details with instructor information"""
        try:
            pipeline = [
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "instructorId",
                        "foreignField": "userId",
                        "as": "instructor",
                    }
                },
                {"$unwind": "$instructor"},
            ]
            courses = list(self.courses_col.aggregate(pipeline))
            return courses
        except Exception as e:
            print(f"Error fetching course details: {e}")
            return []

    def get_courses_by_category(self, category):
        """Get all courses in a specific category"""
        try:
            courses = list(self.courses_col.find({"category": category}))
            return courses
        except Exception as e:
            print(f"Error fetching courses by category: {e}")
            return []

    def get_student_enrolled_to_course(self, course_id):
        """Find students enrolled in a particular course"""
        try:
            enrollments = self.enrollments_col.find({"courseId": course_id})
            student_ids = [enr["studentId"] for enr in enrollments]
            students = list(self.users_col.find({"userId": {"$in": student_ids}}))
            return students
        except Exception as e:
            print(f"Error fetching students enrolled to course: {e}")
            return []

    def search_courses_by_title(self, title):
        """Search courses by title (case-insensitive, partial match)"""
        try:
            courses = list(
                self.courses_col.find({"title": {"$regex": title, "$options": "i"}})
            )
            return courses
        except Exception as e:
            print(f"Error searching courses by title: {e}")
            return []