import sqlite3

DATABASE = "freelearn.db"


# -----------------------------------------
# DATABASE CONNECTION
# -----------------------------------------

def get_db():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# -----------------------------------------
# CREATE TABLES
# -----------------------------------------

def create_tables():

    conn = get_db()
    cursor = conn.cursor()


    # =====================================
    # USER TABLE
    # =====================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
    """)


    # =====================================
    # ADD ADMIN COLUMN
    # =====================================

    cursor.execute("""
        PRAGMA table_info(users)
    """)

    user_columns = [
        column["name"]
        for column in cursor.fetchall()
    ]

    if "is_admin" not in user_columns:

        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN is_admin INTEGER DEFAULT 0
        """)


    # =====================================
    # COURSE TABLE
    # =====================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            provider TEXT NOT NULL,

            category TEXT NOT NULL,

            description TEXT,

            duration TEXT,

            level TEXT,

            certificate INTEGER DEFAULT 0,

            free INTEGER DEFAULT 1,

            link TEXT NOT NULL

        )
    """)


    # =====================================
    # ADD IMAGE COLUMN
    # =====================================

    cursor.execute("""
        PRAGMA table_info(courses)
    """)

    course_columns = [
        column["name"]
        for column in cursor.fetchall()
    ]

    if "image" not in course_columns:

        cursor.execute("""
            ALTER TABLE courses
            ADD COLUMN image TEXT
        """)


    # =====================================
    # SAVED COURSES TABLE
    # =====================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_courses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            course_id INTEGER,

            FOREIGN KEY(user_id)
            REFERENCES users(id),

            FOREIGN KEY(course_id)
            REFERENCES courses(id)

        )
    """)


    conn.commit()


    # =====================================
    # CHECK COURSES
    # =====================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM courses
    """)

    count = cursor.fetchone()[0]


    # =====================================
    # INSERT SAMPLE COURSES
    # =====================================

    if count == 0:

        courses = [

            (
                "Python Programming for Beginners",
                "Alison",
                "Python",
                "Learn Python programming basics, variables, loops and functions.",
                "10 Hours",
                "Beginner",
                1,
                1,
                "https://alison.com/"
            ),

            (
                "Diploma in Python Programming",
                "Alison",
                "Python",
                "Learn Python programming concepts and practical programming skills.",
                "15 Hours",
                "Beginner",
                1,
                1,
                "https://alison.com/"
            ),

            (
                "Data Analytics",
                "Accenture",
                "Data Science",
                "Learn basic concepts of data analysis and data-driven decision making.",
                "6 Hours",
                "Beginner",
                1,
                1,
                "https://www.accenture.com/"
            ),

            (
                "Digital Skills",
                "Accenture",
                "Technology",
                "Learn useful digital and technology skills.",
                "5 Hours",
                "Beginner",
                1,
                1,
                "https://www.accenture.com/"
            ),

            (
                "Cyber Security Basics",
                "TATA",
                "Cyber Security",
                "Introduction to cyber security, online safety and security concepts.",
                "8 Hours",
                "Beginner",
                1,
                1,
                "https://www.tata.com/"
            ),

            (
                "Web Development Basics",
                "Google",
                "Web Development",
                "Learn HTML, CSS and basic web development concepts.",
                "12 Hours",
                "Beginner",
                1,
                1,
                "https://grow.google/"
            ),

            (
                "Artificial Intelligence Basics",
                "IBM",
                "AI & ML",
                "Introduction to Artificial Intelligence and Machine Learning.",
                "10 Hours",
                "Beginner",
                1,
                1,
                "https://www.ibm.com/"
            ),

            (
                "Machine Learning Fundamentals",
                "IBM",
                "AI & ML",
                "Learn fundamental concepts of Machine Learning.",
                "15 Hours",
                "Intermediate",
                1,
                1,
                "https://www.ibm.com/"
            ),

            (
                "SQL for Beginners",
                "Alison",
                "Database",
                "Learn SQL queries, tables and database fundamentals.",
                "8 Hours",
                "Beginner",
                1,
                1,
                "https://alison.com/"
            ),

            (
                "Database Management Basics",
                "IBM",
                "Database",
                "Learn database concepts and database management fundamentals.",
                "10 Hours",
                "Beginner",
                1,
                1,
                "https://www.ibm.com/"
            ),

            (
                "HTML Fundamentals",
                "Google",
                "Web Development",
                "Learn the basic structure of HTML web pages.",
                "5 Hours",
                "Beginner",
                1,
                1,
                "https://grow.google/"
            ),

            (
                "CSS Fundamentals",
                "Google",
                "Web Development",
                "Learn CSS styling and webpage design basics.",
                "6 Hours",
                "Beginner",
                1,
                1,
                "https://grow.google/"
            ),

            (
                "Cloud Computing Basics",
                "IBM",
                "Cloud Computing",
                "Introduction to cloud computing and cloud technologies.",
                "8 Hours",
                "Beginner",
                1,
                1,
                "https://www.ibm.com/"
            ),

            (
                "Data Science Fundamentals",
                "IBM",
                "Data Science",
                "Introduction to data science concepts and workflow.",
                "12 Hours",
                "Beginner",
                1,
                1,
                "https://www.ibm.com/"
            ),

            (
                "Statistics for Data Science",
                "Alison",
                "Data Science",
                "Learn basic statistics concepts useful for data science.",
                "10 Hours",
                "Beginner",
                1,
                1,
                "https://alison.com/"
            )

        ]


        # =====================================
        # INSERT COURSES
        # =====================================

        cursor.executemany("""
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
        """, courses)


        conn.commit()

    # =====================================
    # ADD NPTEL & SWAYAM COURSES
    # =====================================

    extra_courses = [

        (
            "Programming in Python",
            "NPTEL",
            "Python",
            "Learn Python programming concepts and problem solving.",
            "12 Weeks",
            "Beginner",
            1,
            1,
            "https://www.nptel.ac.in/courses"
        ),

        (
            "Data Science for Engineers",
            "NPTEL",
            "Data Science",
            "Learn basic concepts of data science and engineering applications.",
            "8 Weeks",
            "Beginner",
            1,
            1,
            "https://www.nptel.ac.in/courses"
        ),

        (
            "Introduction to Machine Learning",
            "NPTEL",
            "AI & ML",
            "Learn the fundamentals of machine learning.",
            "8 Weeks",
            "Intermediate",
            1,
            1,
            "https://www.nptel.ac.in/courses"
        ),

        (
            "Database Management System",
            "NPTEL",
            "Database",
            "Learn database concepts, SQL and database management.",
            "8 Weeks",
            "Beginner",
            1,
            1,
            "https://www.nptel.ac.in/courses"
        ),

        (
            "Introduction to Artificial Intelligence",
            "SWAYAM",
            "AI & ML",
            "Learn the basic concepts of Artificial Intelligence.",
            "12 Weeks",
            "Beginner",
            1,
            1,
            "https://swayam.gov.in/search_courses"
        ),

        (
            "Programming Fundamentals",
            "SWAYAM",
            "Programming",
            "Learn fundamental programming concepts and problem solving.",
            "8 Weeks",
            "Beginner",
            1,
            1,
            "https://swayam.gov.in/search_courses"
        ),

        (
            "Data Science Fundamentals",
            "SWAYAM",
            "Data Science",
            "Learn the fundamentals of data science and data analysis.",
            "12 Weeks",
            "Beginner",
            1,
            1,
            "https://swayam.gov.in/search_courses"
        ),

        (
            "Computer Science Fundamentals",
            "SWAYAM",
            "Computer Science",
            "Learn fundamental concepts of computer science.",
            "8 Weeks",
            "Beginner",
            1,
            1,
            "https://swayam.gov.in/search_courses"
        )

    ]

    for course in extra_courses:

        cursor.execute(
            "SELECT id FROM courses WHERE name = ? AND provider = ?",
            (course[0], course[1])
        )

        if cursor.fetchone() is None:

            cursor.execute("""
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

    conn.commit()
    conn.close()


# -----------------------------------------
# TEST DATABASE
# -----------------------------------------

if __name__ == "__main__":

    create_tables()

    print("Database created successfully!")

    print("Database name: freelearn.db")