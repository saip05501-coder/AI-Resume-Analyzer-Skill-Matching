JOB_ROLES = {

    "Data Scientist": {
        "must_have_skills": [
            "python",
            "machine learning",
            "statistics",
            "pandas",
            "data analysis"
        ],
        "optional_skills": [
            "numpy",
            "sql",
            "deep learning",
            "tensorflow",
            "scikit learn"
        ]
    },

    "Web Developer": {
        "must_have_skills": [
            "html",
            "css",
            "javascript",
            "web development"
        ],
        "optional_skills": [
            "react",
            "node",
            "django",
            "bootstrap"
        ]
    },

    "Java Developer": {
        "must_have_skills": [
            "java",
            "oops",
            "spring",
            "data structures"
        ],
        "optional_skills": [
            "hibernate",
            "sql",
            "microservices",
            "rest api"
        ]
    },

    "AI Engineer": {
        "must_have_skills": [
            "python",
            "machine learning",
            "deep learning",
            "neural networks"
        ],
        "optional_skills": [
            "tensorflow",
            "pytorch",
            "nlp",
            "computer vision"
        ]
    },

    "Backend Developer": {
        "must_have_skills": [
            "python",
            "django",
            "rest api",
            "sql",
            "backend development"
        ],
        "optional_skills": [
            "flask",
            "postgresql",
            "docker",
            "redis"
        ]
    },

    "Frontend Developer": {
        "must_have_skills": [
            "html",
            "css",
            "javascript",
            "react"
        ],
        "optional_skills": [
            "redux",
            "typescript",
            "bootstrap",
            "webpack"
        ]
    },

    "Full Stack Developer": {
        "must_have_skills": [
            "html",
            "css",
            "javascript",
            "python",
            "django"
        ],
        "optional_skills": [
            "react",
            "node",
            "mongodb",
            "docker"
        ]
    },

    "DevOps Engineer": {
        "must_have_skills": [
            "linux",
            "docker",
            "aws",
            "ci cd"
        ],
        "optional_skills": [
            "kubernetes",
            "terraform",
            "jenkins",
            "ansible"
        ]
    },

    "Data Analyst": {
        "must_have_skills": [
            "python",
            "sql",
            "excel",
            "data analysis"
        ],
        "optional_skills": [
            "power bi",
            "tableau",
            "pandas",
            "statistics"
        ]
    },

    "Mobile App Developer": {
        "must_have_skills": [
            "android",
            "java",
            "kotlin",
            "mobile development"
        ],
        "optional_skills": [
            "flutter",
            "react native",
            "firebase",
            "ios"
        ]
    }
}


ALL_SKILLS = sorted(set([
    # Programming
    "python", "java", "c++", "javascript", "sql",

    # Data
    "machine learning", "deep learning", "statistics",
    "pandas", "numpy", "tensorflow",

    # Web
    "html", "css", "react", "node", "django", "flask",

    # Backend
    "spring", "hibernate", "microservices",

    # Tools
    "git", "docker", "aws", "linux"
]))
