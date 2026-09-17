from database import get_db


courses = [

    # -----------------------------
    # ALISON
    # -----------------------------

    (
        "Python for Beginners",
        "Alison",
        "Python",
        "Learn the basics of Python programming.",
        "10 Hours",
        "Beginner",
        0,
        1,
        "https://alison.com/course/python-for-beginners"
    ),

    (
        "Introduction to Python",
        "Alison",
        "Python",
        "Learn Python programming, variables, operators, loops and functions.",
        "3-4 Hours",
        "Beginner",
        0,
        1,
        "https://alison.com/course/introduction-to-python"
    ),

    (
        "Python for Data Science",
        "Alison",
        "Data Science",
        "Learn Python, NumPy and Pandas for data science.",
        "10+ Hours",
        "Intermediate",
        0,
        1,
        "https://alison.com/course/python-for-data-science-from-the-basics-to-advanced"
    ),

    (
        "Diploma in Python Programming",
        "Alison",
        "Python",
        "Develop programming skills using Python.",
        "10-15 Hours",
        "Beginner",
        0,
        1,
        "https://alison.com/course/diploma-in-python-programming-revised"
    ),

    (
        "Programming Using Python",
        "Alison",
        "Python",
        "Learn Python programming and improve coding skills.",
        "3-4 Hours",
        "Beginner",
        0,
        1,
        "https://alison.com/course/programming-using-python"
    ),


    # -----------------------------
    # TCS iON
    # -----------------------------

    (
        "TCS iON Career Edge - IT Primer",
        "TCS iON",
        "Technology",
        "Learn IT fundamentals, programming basics, UI/UX and workplace technology.",
        "15 Days",
        "Beginner",
        1,
        1,
        "https://www.tcsion.com/courses/career-edge-it-course/"
    ),

    (
        "TCS iON Career Edge - Interview and Job Readiness",
        "TCS iON",
        "Career Skills",
        "Learn interview preparation, resume creation, soft skills and business etiquette.",
        "15 Days",
        "Beginner",
        1,
        1,
        "https://www.tcsion.com/courses/career-edge-interview-and-job-readiness/"
    ),

    (
        "YUVA AI for All",
        "TCS iON",
        "Artificial Intelligence",
        "Learn AI fundamentals, applications, AI models and responsible AI.",
        "4-5 Hours",
        "Beginner",
        1,
        1,
        "https://www.tcsion.com/courses/yuva-ai/"
    ),

    (
        "Communication Skills",
        "TCS iON",
        "Soft Skills",
        "Improve verbal and non-verbal communication skills.",
        "2 Hours",
        "Beginner",
        1,
        1,
        "https://www.tcsion.com/courses/interview-and-job-prep/introduction-to-soft-skills/"
    ),


    # -----------------------------
    # IBM SKILLSBUILD
    # -----------------------------

    (
        "AI Fundamentals",
        "IBM SkillsBuild",
        "Artificial Intelligence",
        "Learn AI concepts, machine learning, neural networks and deep learning.",
        "10+ Hours",
        "Intermediate",
        1,
        1,
        "https://skillsbuild.org/learning-catalog/university-catalog?topic=ai"
    ),

    (
        "AI Literacy",
        "IBM SkillsBuild",
        "Artificial Intelligence",
        "Learn AI concepts, applications, benefits, risks and AI ethics.",
        "4 Hours",
        "Beginner",
        1,
        1,
        "https://skillsbuild.org/learning-catalog/university-catalog?topic=ai"
    ),

    (
        "Data Literacy",
        "IBM SkillsBuild",
        "Data Science",
        "Learn data concepts, data analysis, charts and data quality.",
        "1-3 Hours",
        "Beginner",
        1,
        1,
        "https://skillsbuild.org/learning-catalog/university-catalog?topic=data"
    ),

    (
        "Data Fundamentals",
        "IBM SkillsBuild",
        "Data Science",
        "Learn data science concepts, data cleaning and visualization.",
        "3-10 Hours",
        "Intermediate",
        1,
        1,
        "https://skillsbuild.org/learning-catalog/university-catalog?topic=data"
    ),

    (
        "Cybersecurity",
        "IBM SkillsBuild",
        "Cyber Security",
        "Learn cybersecurity fundamentals, network security and incident response.",
        "6 Hours",
        "Beginner",
        1,
        1,
        "https://test.skillsbuild.org/adult-learners/explore-learning/cybersecurity-analyst"
    )
]


# --------------------------------
# ADD COURSES
# --------------------------------

db = get_db()

for course in courses:

    db.execute("""
        INSERT INTO courses
        (
            name,
            provider,
            category,
            description,
            duration,
            level,
            certificate,
            free,
            link
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, course)


db.commit()
db.close()


print("Real courses added successfully!")
print("Total courses added:", len(courses))