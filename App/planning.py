from .db import get_db
from flask import render_template, Blueprint, request, redirect, url_for, g, jsonify, flash    
from App.auth import login_required

bp = Blueprint('planning', __name__, url_prefix='/planning')

@bp.route('', methods=('GET', 'POST'))
@login_required
def display():
    db = get_db()

    if request.method == 'POST':
        error = None
        recipe_id = request.form.get('selected_id')
        course = int(request.form.get('course'))
        week_n = request.form.get('week_n')
        day = request.form.get('day')

        if not recipe_id:
            error = 'No recipe was selected'

        if error is None:
            # Get the current plan of the day
            day_plan = db.execute("SELECT * FROM weeks WHERE user_id=? AND week_n=?",
                                (g.user['id'], week_n)
                                ).fetchone()[day].split(',')
            
            # New meal to be included in the day
            new = db.execute("SELECT * FROM recipes WHERE id=?",
                            (recipe_id, )
                            ).fetchone()['id']

            if day_plan[course] != '':
                day_plan[course] += f"-{new}"
            else:
                day_plan[course] += f"{new}"

            # Update the database and return to the planning page
            db.execute(f'UPDATE weeks SET {day}=? WHERE user_id=? AND week_n=?',
                    (','.join(day_plan), g.user['id'], week_n))
            db.commit()
            return redirect(request.url)
        else:
            flash(error)


    # Number of weeks in the user's planner
    weeks_count = db.execute('SELECT weeks_count FROM users WHERE id=?',
                           (g.user['id'], )
                           ).fetchone()['weeks_count'];
    
    # planned_recipes[week 1..3][day 1..7][course 0..4]
    planned_recipes = [[[None for c in range(5)] 
                                for d in range(7)]
                                    for w in range(weeks_count)]
    for w in range(weeks_count):

        # Get the week
        week = db.execute("SELECT * FROM weeks WHERE user_id=? AND week_n=?",
                          (g.user['id'], w + 1)).fetchone() 
        for d, day in enumerate(['Monday', 'Tuesday', 'Wednsday',
                    'Thursday', 'Friday', 'Saturday', 'Sunday']):
            
            # [No coures, Breakfast, Lunch, Dinner, Snack]
            # ['rec1-rec2-rec3', 'rec4-..-rec6, ..']
            meals = week[day].split(',')

            for course, course_meals in enumerate(meals): # 'rec1-rec2-rec3'
                # Append the list of actual recipes given their ids
                course_recipes = [db.execute(
                                'SELECT * FROM recipes WHERE id=?', [int(meal_id)]).fetchone()
                                for meal_id in course_meals.split('-')
                                if meal_id != '']
                planned_recipes[w][d][course] = course_recipes

    # Send all recipes to pick in recipe selector
    recipes = get_db().execute("SELECT * FROM recipes WHERE user_id=?",
                              (g.user['id'], )).fetchall()
    return render_template('tools/planning.html',
                            recipes=recipes,
                            planned_recipes=planned_recipes,
                            weeks_count=weeks_count)

# Add new week to the meal planner calendar
@bp.route('/add_week', methods=('POST', ))
@login_required
def add_week():
    db = get_db()
    error = None

    # Get the current number of weeks and make sure it doesn't exceed maximum
    weeks_count = db.execute("SELECT weeks_count FROM users WHERE id=?",
                            (g.user['id'], )
                            ).fetchone()['weeks_count']
    if weeks_count > 4:
        error = "Calender is of max size."
        flash(error)
        return redirect(url_for('planning.display'))

    else:
        # Create new week
        weeks_count += 1
        db.execute('UPDATE users SET weeks_count=? WHERE id=?',
                  [weeks_count, g.user['id']])
        db.execute('INSERT INTO weeks (user_id, week_n) VALUES (?, ?)',
                  [g.user['id'], weeks_count])
        db.commit()
        return redirect(url_for('planning.display'))

@bp.route('/remove_week', methods=['POST'])
@login_required
def remove_week():
    db = get_db()
    error = None

    week_n = int(request.form.get('remove_week'))

    # Get the current number of weeks and make sure it doesn't exceed maximum
    weeks_count = db.execute("SELECT weeks_count FROM users WHERE id=?",
                            (g.user['id'], )
                            ).fetchone()['weeks_count']
    if week_n > weeks_count:
        error = "The week's number exceed existing count."
    elif weeks_count == 1:
        error = 'The calendar is of min size'
    
    if error is None:
        # Remove the week
        db.execute('DELETE FROM weeks WHERE user_id=? AND week_n=?',
                  [g.user['id'], week_n])
        db.execute('UPDATE users SET weeks_count=? WHERE id=?',
                  [weeks_count - 1, g.user['id']])
        # Update the weeks' number which are higher than week_n
        for w in range(week_n + 1, weeks_count + 1):
            db.execute('UPDATE weeks SET week_n=? WHERE user_id=? AND week_n=?',
                      [w - 1, g.user['id'], w])
        db.commit()
        return redirect(url_for('planning.display'))
    else:
        flash(error)
        return redirect(url_for('planning.display'))

@bp.route('/remove_recipe', methods=['POST'])
@login_required
def remove_recipe():
    db = get_db()
    remove_info = request.get_json()   
    week_n = int(remove_info['week_n'])
    day = remove_info['day']
    course = int(remove_info['course'])
    recipe_id = remove_info['recipe_id']                  

    day_plan = db.execute('SELECT * FROM weeks WHERE user_id=? AND week_n=?',
                         [g.user['id'], week_n]
                         ).fetchone()[day].split(',')

    day_recipes = day_plan[course].split('-')
    day_recipes.remove(recipe_id)
    day_recipes = '-'.join(day_recipes)
    day_plan[course] = day_recipes
    db.execute(f'UPDATE weeks SET {day}=? WHERE user_id=? AND week_n=?',
              [','.join(day_plan), g.user['id'], week_n])

    db.commit()
    return jsonify(day_plan)