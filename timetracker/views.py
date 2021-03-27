from flask import Blueprint, render_template, request
import sqlite3

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print('<h1> Good </h1>')
    return render_template('home.html')


@views.route('/hours', methods=['GET', 'POST'])
def hours():
    connection = sqlite3.connect(r'timetracker\time_tracker.db')
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()

    if request.method == 'POST':
        amount = request.form['amount']
        project_shortcut = request.form['shortcut']
        if request.form['work-date']:
            work_date = request.form['work-date']

            cur.execute('INSERT INTO hours (amount, work_date, '
                        'project_shortcut) VALUES (?, ?, ?)', [amount,
                                                               work_date, project_shortcut])
        else:
            cur.execute('INSERT INTO hours (amount, project_shortcut) VALUES (?, ?)',
                        [amount, project_shortcut])

    c = cur.execute('select * from hours order by work_date desc')
    results = c.fetchall()
    connection.commit()
    connection.close()

    return render_template('hours.html', results=results)


@views.route('/projects', methods=['GET', 'POST'])
def projects():
    connection = sqlite3.connect(r'timetracker\time_tracker.db')
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        shortcut = request.form['shortcut']

        cur.execute('INSERT INTO projects (name, shortcut) VALUES (?, ?)', \
                    [name, shortcut])

    c = cur.execute('SELECT p.id, p.name, p.shortcut, SUM(h.amount) as sum '
                    'FROM projects p '
                    'JOIN hours h ON p.shortcut = h.project_shortcut '
                    'GROUP BY p.id ')
    results = c.fetchall()
    connection.commit()
    connection.close()

    return render_template('projects.html', results=results)