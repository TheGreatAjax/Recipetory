import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from App.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        
        if error is None:
            try:
                cur = db.cursor()
                cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                            (username, generate_password_hash(password)),
                )

                # Create the first week in the planner
                cur.execute("INSERT INTO weeks (user_id, week_n) VALUES (?, ?)",
                            (cur.lastrowid, 1))
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for('auth.login'))
            
        flash(error)
        
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute("SELECT * FROM users WHERE username = ?",
                         (username, )
                         ).fetchone()
        
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('recipe.my_recipes'))

        flash(error)
    return render_template('auth/login.html')
    
# Each page should check if the user is logged in
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id, )
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/Main')

def login_required(view):
    # Makes the wrapper function (wrapped_view) has attributes of view
    # https://docs.python.org/3/library/functools.html#functools.wraps
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user == None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    
    return wrapped_view
