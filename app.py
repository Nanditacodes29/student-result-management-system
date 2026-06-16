from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    student_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM marks")
    marks_count = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        student_count=student_count,
        marks_count=marks_count
    )


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():

    if request.method == 'POST':

        name = request.form['name']
        rollno = request.form['rollno']
        department = request.form['department']

        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students (name, rollno, department) VALUES (?, ?, ?)",
            (name, rollno, department)
        )

        conn.commit()
        conn.close()

        return "Student Added Successfully!"

    return render_template('add_student.html')
@app.route('/view_students')
def view_students():

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return render_template(
        'view_students.html',
        students=students
    )
@app.route('/marks_entry', methods=['GET', 'POST'])
def marks_entry():

    if request.method == 'POST':

        rollno = request.form['rollno']
        maths = request.form['maths']
        physics = request.form['physics']
        chemistry = request.form['chemistry']

        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO marks
            (rollno, maths, physics, chemistry)
            VALUES (?, ?, ?, ?)
            ''',
            (rollno, maths, physics, chemistry)
        )

        conn.commit()
        conn.close()

        return "Marks Saved Successfully!"

    return render_template('marks_entry.html')

@app.route('/results')
def results():

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT rollno, maths, physics, chemistry FROM marks"
    )

    rows = cursor.fetchall()

    conn.close()

    results = []

    for row in rows:

        rollno = row[0]
        maths = row[1]
        physics = row[2]
        chemistry = row[3]

        total = maths + physics + chemistry
        average = total / 3

        if average >= 90:
            grade = 'A'

        elif average >= 80:
            grade = 'B'

        elif average >= 70:
            grade = 'C'

        elif average >= 60:
            grade = 'D'

        else:
            grade = 'F'

        results.append({
            'rollno': rollno,
            'total': total,
            'average': round(average, 2),
            'grade': grade
        })

    return render_template(
        'results.html',
        results=results
    )

if __name__ == '__main__':
    app.run(debug=True)