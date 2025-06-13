import random
import dateutil.parser
from faker import Faker
from bson import ObjectId


class Helper:
    def __init__(self):
        self.faker = Faker()
        self.roles = ["student", "instructor"]

        self.skills = [
            "Python",
            "SQL",
            "Data Engineering",
            "ETL",
            "JavaScript",
            "APIs",
            "Kubernetes",
            "Machine Learning",
            "MongoDB",
            "Cloud Computing",
        ]
        self.levels = ["beginner", "intermediate", "advanced"]

    # make mock data
    def make_user(self, user_id):
        return {
            "_id": ObjectId(),
            "userId": user_id,
            "email": self.faker.email(),
            "firstName": self.faker.first_name(),
            "lastName": self.faker.last_name(),
            "role": random.choice(self.roles),
            "dateJoined": self.faker.date_time_between(
                start_date="-2y", end_date="now"
            ),
            "profile": {
                "bio": self.faker.sentence(),
                "avatar": self.faker.image_url(),
                "skills": random.sample(self.skills, k=3),
            },
            "is_active": random.choice([True, False]),
        }

    def make_course(self, course_id, instructor_id):
        return {
            "courseId": course_id,
            "title": self.faker.sentence(),
            "description": " ".join(self.faker.sentences(nb=3)),
            "instructorId": instructor_id,
            "category": random.choice(self.skills),
            "level": random.choice(self.levels),
            "duration": self.faker.random_int(min=10, max=99),
            "price": self.faker.random_int(min=1000, max=10000),
            "tags": random.sample(self.skills, k=2),
            "createdAt": self.faker.date_time_between(start_date="-3y", end_date="-2y"),
            "updatedAt": self.faker.date_time_between(start_date="-1y", end_date="now"),
            "isPublished": random.choice([True, False]),
        }

    def make_lesson(self, lesson_id, course_id):
        return {
            "lessonId": lesson_id,
            "courseId": course_id,
            "title": self.faker.sentence(),
            "content": " ".join(self.faker.sentences(nb=5)),
            "order": self.faker.random_int(min=0, max=99),
            "resources": ["intro.pdf"],
            "duration": 30,
            "createdAt": self.faker.date_time_between(start_date="-3y", end_date="-2y"),
            "updatedAt": self.faker.date_time_between(start_date="-1y", end_date="now"),
        }

    def get_date_fields(self, schema):
        """Extract all property names with bsonType 'date' from a schema dict."""
        date_fields = set()

        def extract_dates(properties, prefix=""):
            for k, v in properties.items():
                if isinstance(v, dict):
                    if v.get("bsonType") == "date":
                        date_fields.add(prefix + k)
                    # Check nested properties (e.g., profile)
                    if "properties" in v:
                        extract_dates(v["properties"], prefix + k + ".")

        extract_dates(schema.get("properties", {}))
        return date_fields

    def convert_dates_by_schema(self, obj, date_fields, prefix=""):
        """Convert only fields listed in date_fields to datetime."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                full_key = prefix + k
                if full_key in date_fields and isinstance(v, str):
                    try:
                        obj[k] = dateutil.parser.isoparse(v)
                    except Exception:
                        pass
                elif isinstance(v, dict):
                    obj[k] = self.convert_dates_by_schema(
                        v, date_fields, prefix=full_key + "."
                    )
                elif isinstance(v, list):
                    obj[k] = [
                        (
                            self.convert_dates_by_schema(
                                item, date_fields, prefix=full_key + "."
                            )
                            if isinstance(item, dict)
                            else item
                        )
                        for item in v
                    ]
        return obj