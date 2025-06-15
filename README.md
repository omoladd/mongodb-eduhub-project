# EduHub MongoDB Project

## What the Project Is

EduHub is a sample educational platform backend built with MongoDB. It demonstrates how to model, seed, and query a learning management system (LMS) database, including students, instructors, courses, lessons, assignments, enrollments, and submissions. The project includes schema validation, realistic sample data.

---

## Prerequisites

- Python 3.8+
- [MongoDB Community Server](https://www.mongodb.com/try/download/community) (running locally on default port)
- All Python dependencies listed in `requirements.txt`

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Running the Project

1. **Start MongoDB**  
   Make sure your MongoDB server is running locally.

2. **Seed the Database**  
   Run the notebook to create collections, apply schema validation, and seed sample data

---

## Collections and Schema Overview

### 1. `users`

| Field      | Type   | Description                        |
| ---------- | ------ | ---------------------------------- |
| userId     | string | Unique user identifier             |
| email      | string | Unique email address               |
| firstName  | string | First name                         |
| lastName   | string | Last name                          |
| role       | string | `student` or `instructor`          |
| dateJoined | date   | Date the user joined               |
| profile    | object | Contains `bio`, `avatar`, `skills` |
| isActive   | bool   | Whether the user is active         |

**Indexes:**  
| Field | Type | Description |
|----------|---------|---------------------|
| email | unique | Unique index |
| lastName | | For search |

---

### 2. `courses`

| Field        | Type   | Description                            |
| ------------ | ------ | -------------------------------------- |
| courseId     | string | Unique course identifier               |
| title        | string | Course title                           |
| description  | string | Course description                     |
| instructorId | string | Reference to users                     |
| category     | string | Course category                        |
| level        | string | `beginner`, `intermediate`, `advanced` |
| duration     | number | Duration in hours or units             |
| price        | number | Course price                           |
| tags         | array  | List of tags                           |
| createdAt    | date   | Creation date                          |
| updatedAt    | date   | Last update date                       |
| isPublished  | bool   | Whether the course is published        |
| rating       | number | Course rating (1-5)                    |

**Indexes:**  
| Field | Type | Description |
|----------|---------|---------------------|
| title | text | Text index |
| category | | Category index |

---

### 3. `lessons`

| Field     | Type   | Description                       |
| --------- | ------ | --------------------------------- |
| lessonId  | string | Unique lesson identifier          |
| courseId  | string | Reference to courses              |
| title     | string | Lesson title                      |
| content   | string | Lesson content                    |
| order     | number | Order of the lesson in the course |
| resources | array  | List of resources                 |
| duration  | number | Duration of the lesson            |
| createdAt | date   | Creation date                     |
| updatedAt | date   | Last update date                  |

---

### 4. `assignments`

| Field        | Type   | Description                  |
| ------------ | ------ | ---------------------------- |
| assignmentId | string | Unique assignment identifier |
| courseId     | string | Reference to courses         |
| lessonId     | string | Reference to lessons         |
| title        | string | Assignment title             |
| instructions | string | Assignment instructions      |
| dueDate      | date   | Due date                     |
| maxScore     | number | Maximum score                |
| createdAt    | date   | Creation date                |
| updatedAt    | date   | Last update date             |

**Indexes:**  
| Field | Description |
|---------|--------------|
| dueDate | Due date index|

---

### 5. `enrollments`

| Field             | Type   | Description                   |
| ----------------- | ------ | ----------------------------- |
| enrollmentId      | string | Unique enrollment identifier  |
| studentId         | string | Reference to users            |
| courseId          | string | Reference to courses          |
| enrollmentDate    | date   | Date of enrollment            |
| progress          | number | Progress (0.0-1.0)            |
| completed         | bool   | Whether course is completed   |
| certificateIssued | bool   | Whether certificate is issued |

**Indexes:**  
| Field | Description |
|-----------|--------------------|
| studentId | Student index |
| courseId | Course index |

---

### 6. `submissions`

| Field          | Type   | Description                  |
| -------------- | ------ | ---------------------------- |
| submissionId   | string | Unique submission identifier |
| assignmentId   | string | Reference to assignments     |
| studentId      | string | Reference to users           |
| submissionDate | date   | Date of submission           |
| content        | string | Submission content           |
| grade          | number | Grade received               |
| feedback       | string | Feedback from grader         |
| gradedBy       | string | Reference to users (grader)  |
| gradedAt       | date   | Date graded                  |

---