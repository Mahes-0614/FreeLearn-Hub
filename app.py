import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

from database import get_db, create_tables


# =========================================
# FLASK APPLICATION
# =========================================

app = Flask(__name__)

app.secret_key = "freelearn_secret_key"

# Create database tables when Flask starts
create_tables()


# =========================================
# IMAGE UPLOAD SETTINGS
# =========================================

app.config["UPLOAD_FOLDER"] = "static/uploads"

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)


# =========================================
# HOME
# =========================================

@app.route("/")
def home():

    db = get_db()

    courses = db.execute("""
        SELECT *
        FROM courses
        LIMIT 6
    """).fetchall()

    db.close()

    return render_template(
        "index.html",
        courses=courses
    )


# =========================================
# ALL COURSES
# =========================================

@app.route("/courses")
def courses():

    search = request.args.get(
        "search",
        ""
    )

    category = request.args.get(
        "category",
        ""
    )

    provider = request.args.get(
        "provider",
        ""
    )

    certificate = request.args.get(
        "certificate",
        ""
    )

    db = get_db()

    query = """
        SELECT *
        FROM courses
        WHERE 1=1
    """

    params = []


    # ---------------------------------
    # SEARCH
    # ---------------------------------

    if search:

        query += """
            AND (
                name LIKE ?
                OR category LIKE ?
                OR provider LIKE ?
            )
        """

        value = "%" + search + "%"

        params.extend([
            value,
            value,
            value
        ])


    # ---------------------------------
    # CATEGORY FILTER
    # ---------------------------------

    if category:

        query += """
            AND category = ?
        """

        params.append(category)


    # ---------------------------------
    # PROVIDER FILTER
    # ---------------------------------

    if provider:

        query += """
            AND provider = ?
        """

        params.append(provider)


    # ---------------------------------
    # CERTIFICATE FILTER
    # ---------------------------------

    if certificate == "yes":

        query += """
            AND certificate = 1
        """


    # ---------------------------------
    # GET COURSES
    # ---------------------------------

    courses = db.execute(
        query,
        params
    ).fetchall()


    # ---------------------------------
    # GET CATEGORIES
    # ---------------------------------

    categories = db.execute("""
        SELECT DISTINCT category
        FROM courses
        ORDER BY category
    """).fetchall()


    # ---------------------------------
    # GET PROVIDERS
    # ---------------------------------

    providers = db.execute("""
        SELECT DISTINCT provider
        FROM courses
        ORDER BY provider
    """).fetchall()


    db.close()


    return render_template(
        "courses.html",
        courses=courses,
        categories=categories,
        providers=providers
    )


# =========================================
# COURSE DETAILS
# =========================================

@app.route(
    "/course/<int:course_id>"
)
def course_details(course_id):

    db = get_db()

    course = db.execute("""
        SELECT *
        FROM courses
        WHERE id = ?
    """, (
        course_id,
    )).fetchone()

    db.close()


    if course is None:

        return "Course not found"


    return render_template(
        "course_details.html",
        course=course
    )


# =========================================
# REGISTER
# =========================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        password = request.form["password"]


        hashed_password = generate_password_hash(
            password
        )


        db = get_db()


        try:

            db.execute("""
                INSERT INTO users
                (
                    name,
                    email,
                    password
                )
                VALUES (?, ?, ?)
            """, (
                name,
                email,
                hashed_password
            ))


            db.commit()


            flash(
                "Registration successful!",
                "success"
            )


            return redirect(
                url_for("login")
            )


        except Exception:

            flash(
                "Email already exists!",
                "danger"
            )


        finally:

            db.close()


    return render_template(
        "register.html"
    )


# =========================================
# LOGIN
# =========================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]


        db = get_db()


        user = db.execute("""
            SELECT *
            FROM users
            WHERE email = ?
        """, (
            email,
        )).fetchone()


        db.close()


        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]

            session["user_name"] = user["name"]

            session["is_admin"] = user["is_admin"]


            # ---------------------------------
            # ADMIN LOGIN
            # ---------------------------------

            if user["is_admin"] == 1:

                return redirect(
                    url_for("admin_dashboard")
                )


            # ---------------------------------
            # NORMAL USER LOGIN
            # ---------------------------------

            return redirect(
                url_for("dashboard")
            )


        flash(
            "Invalid email or password!",
            "danger"
        )


    return render_template(
        "login.html"
    )


# =========================================
# LOGOUT
# =========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# =========================================
# SAVE COURSE
# =========================================

@app.route(
    "/save/<int:course_id>"
)
def save_course(course_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    db = get_db()


    existing = db.execute("""
        SELECT *
        FROM saved_courses
        WHERE user_id = ?
        AND course_id = ?
    """, (
        session["user_id"],
        course_id
    )).fetchone()


    if not existing:

        db.execute("""
            INSERT INTO saved_courses
            (
                user_id,
                course_id
            )
            VALUES (?, ?)
        """, (
            session["user_id"],
            course_id
        ))

        db.commit()


    db.close()


    return redirect(
        url_for(
            "course_details",
            course_id=course_id
        )
    )


# =========================================
# USER DASHBOARD
# =========================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    db = get_db()


    saved_courses = db.execute("""
        SELECT courses.*
        FROM courses
        JOIN saved_courses
        ON courses.id = saved_courses.course_id
        WHERE saved_courses.user_id = ?
    """, (
        session["user_id"],
    )).fetchall()


    db.close()


    return render_template(
        "dashboard.html",
        courses=saved_courses
    )


# =========================================
# MAKE ADMIN
# =========================================

@app.route("/make-admin")
def make_admin():

    ADMIN_EMAIL = "maheswariloganathan06@gmail.com"


    db = get_db()


    user = db.execute("""
        SELECT *
        FROM users
        WHERE email = ?
    """, (
        ADMIN_EMAIL,
    )).fetchone()


    if user is None:

        db.close()

        return """
        User not found.
        Please register this email first.
        """


    db.execute("""
        UPDATE users
        SET is_admin = 1
        WHERE email = ?
    """, (
        ADMIN_EMAIL,
    ))


    db.commit()

    db.close()


    return """
    Admin account created successfully!
    """


# =========================================
# ADMIN CHECK
# =========================================

def admin_required():

    if "user_id" not in session:

        return False


    if session.get("is_admin") != 1:

        return False


    return True


# =========================================
# ADMIN DASHBOARD
# =========================================

@app.route("/admin")
def admin_dashboard():

    if not admin_required():

        return redirect(
            url_for("login")
        )


    db = get_db()


    courses = db.execute("""
        SELECT *
        FROM courses
        ORDER BY id DESC
    """).fetchall()


    users = db.execute("""
        SELECT *
        FROM users
        ORDER BY id DESC
    """).fetchall()


    db.close()


    return render_template(
        "admin.html",
        courses=courses,
        users=users
    )


# =========================================
# ADD COURSE - ADMIN
# =========================================

@app.route(
    "/admin/add-course",
    methods=["GET", "POST"]
)
def add_course():

    if not admin_required():

        return redirect(
            url_for("login")
        )


    # ---------------------------------
    # POST
    # ---------------------------------

    if request.method == "POST":

        name = request.form["name"]

        provider = request.form["provider"]

        category = request.form["category"]

        description = request.form["description"]

        duration = request.form["duration"]

        level = request.form["level"]

        certificate = request.form.get(
            "certificate",
            0
        )

        link = request.form["link"]


        # ---------------------------------
        # IMAGE UPLOAD
        # ---------------------------------

        image = request.files.get(
            "image"
        )


        image_filename = None


        if image and image.filename:

            image_filename = secure_filename(
                image.filename
            )


            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    image_filename
                )
            )


        # ---------------------------------
        # SAVE COURSE TO DATABASE
        # ---------------------------------

        db = get_db()


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
                link,
                image
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            provider,
            category,
            description,
            duration,
            level,
            int(certificate),
            1,
            link,
            image_filename
        ))


        db.commit()

        db.close()


        flash(
            "Course added successfully!",
            "success"
        )


        return redirect(
            url_for("admin_dashboard")
        )


    # ---------------------------------
    # ADD COURSE PAGE
    # ---------------------------------

    return render_template(
        "add_course.html"
    )


# =========================================
# DELETE COURSE - ADMIN
# =========================================

@app.route(
    "/admin/delete-course/<int:course_id>"
)
def delete_course(course_id):

    if not admin_required():

        return redirect(
            url_for("login")
        )


    db = get_db()


    # ---------------------------------
    # DELETE SAVED COURSE RECORDS
    # ---------------------------------

    db.execute("""
        DELETE FROM saved_courses
        WHERE course_id = ?
    """, (
        course_id,
    ))


    # ---------------------------------
    # DELETE COURSE
    # ---------------------------------

    db.execute("""
        DELETE FROM courses
        WHERE id = ?
    """, (
        course_id,
    ))


    db.commit()

    db.close()


    flash(
        "Course deleted successfully!",
        "success"
    )


    return redirect(
        url_for("admin_dashboard")
    )


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )