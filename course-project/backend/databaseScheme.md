# Database Schema Report: `cs125`
Generated on: 2026-02-11

## Collections Overview

### Collection: `courses`
- **Document Count**: 73
- **Schema (Sample Structure)**:
  ```json
{
    "_id": "698971253bdecb38dd2d47e6",
    "id": "I&CSCI163",
    "title": "Mobile and Ubiquitous Games",
    "description": "Design and technolfogy of mobile games, including mixed reality gaming, urban games, and locative media. Case studies of significant systems. Uses and limitations of location-based technologies. Infrastructures and their relationships to gameplay and design.",
    "prerequisiteTree": {
        "AND": [
            {
                "OR": [
                    {
                        "courseId": "I&CSCI61",
                        "minGrade": "D-"
                    },
                    {
                        "courseId": "GDIM25",
                        "minGrade": "D-"
                    }
                ]
            },
            {
                "OR": [
                    {
                        "courseId": "GDIM31",
                        "minGrade": "D-"
                    },
                    {
                        "courseId": "I&CSCI10",
                        "minGrade": "D-"
                    },
                    {
                        "courseId": "I&CSCI31",
                        "minGrade": "D-"
                    },
                    {
                        "courseId": "I&CSCIH32",
                        "minGrade": "D-"
                    }
                ]
            }
        ]
    },
    "dependencies": [
        {
            "courseId": "COMPSCI113",
            "title": "Computer Game Development"
        }
    ],
    "keywords": [
        "Game Development"
    ]
}
  ```
- **Field Types (Detected)**:
  - `_id`: ObjectId
  - `id`: str
  - `title`: str
  - `description`: str
  - `prerequisiteTree`: dict
  - `dependencies`: list
  - `keywords`: list

### Collection: `keywords`
- **Document Count**: 15
- **Schema (Sample Structure)**:
  ```json
{
    "_id": "698971908a7164da4cc9af94",
    "keyword": "Graphics & Visualization",
    "description": "Computer graphics, image processing, computer vision, and visual rendering",
    "courses": [
        {
            "id": "COMPSCI111",
            "title": "Digital Image Processing"
        },
        {
            "id": "COMPSCI112",
            "title": "Computer Graphics"
        },
        {
            "id": "COMPSCI114",
            "title": "Projects in Advanced 3D Computer Graphics"
        },
        {
            "id": "COMPSCI116",
            "title": "Computational Photography and Vision"
        },
        {
            "id": "COMPSCI117",
            "title": "Project in Computer Vision"
        },
        {
            "id": "COMPSCI118",
            "title": "Introduction to Virtual Reality"
        },
        {
            "id": "I&CSCI33",
            "title": "Intermediate Programming"
        },
        {
            "id": "I&CSCI46",
            "title": "Data Structure Implementation and Analysis"
        },
        {
            "id": "I&CSCI6D",
            "title": "Discrete Mathematics for Computer Science"
        },
        {
            "id": "I&CSCI6N",
            "title": "Computational Linear Algebra"
        }
    ]
}
  ```
- **Field Types (Detected)**:
  - `_id`: ObjectId
  - `keyword`: str
  - `description`: str
  - `courses`: list

### Collection: `specializations`
- **Document Count**: 0
- *Collection is empty.*

### Collection: `users`
- **Document Count**: 2
- **Schema (Sample Structure)**:
  ```json
{
    "_id": "698a9685eb38f3cb7cca7bdd",
    "username": "testuser",
    "password": "123",
    "quartersLeft": 3,
    "specialization": "None",
    "coursesLeft": 6
}
  ```
- **Field Types (Detected)**:
  - `_id`: ObjectId
  - `username`: str
  - `password`: str
  - `quartersLeft`: int
  - `specialization`: str
  - `coursesLeft`: int