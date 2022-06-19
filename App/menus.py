from cmath import e
from crypt import methods
from .db import get_db
from flask import render_template, Blueprint, request, redirect, url_for, g, jsonify, flash    
from App.auth import login_required

bp = Blueprint('menus', __name__, url_prefix='/menus')

@bp.route('', methods=['GET'])
@login_required
def display():

    db = get_db()
    if request.method == 'POST':
        pass
    
    db_query = "SELECT * FROM menus WHERE user_id = ?"
    params = [g.user['id']]

    # Check the search query
    search_query = request.args.get('q', type=str)
    if search_query:
        db_query += "AND title LIKE ?"
        params.append('%'+search_query+'%')
    else:
        search_query = ""
    
    menus = db.execute(db_query, params).fetchall()

    # Send recipe titles as well, for display
    recipe_titles = dict()
    for menu in menus:
        for course in menu['recipes'].split(','):
            for recipe_id in course.split('-'):
                if recipe_id:
                    recipe_titles[recipe_id] = db.execute(
                        'SELECT title FROM recipes WHERE id=?',
                        [recipe_id]
                        ).fetchone()['title']
    
    return render_template('tools/menus.html',
                        menus=menus,
                        recipe_titles = recipe_titles,
                        query=search_query)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():

    db = get_db()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        selected_recipes = request.form.getlist('selected_recipe')
        if selected_recipes:

            # Create the array of recipes
            menu = [''] * 5
            for recipe in selected_recipes:
                course = int(recipe[0])
                menu[course] += f"{recipe[1:]}-"

            # Remove '-' in the end (if any)
            for c, course in enumerate(menu):
                if course:
                    menu[c] = course[:len(course) - 1]

            db.execute('INSERT INTO menus'
                    '(title, description, recipes, user_id)'
                    ' VALUES (?, ?, ?, ?)',
                    [title, description, ','.join(menu), g.user['id']])
            
            db.commit()
            return redirect(url_for('menus.display'))
            
        else:
            flash('Menu cannot be empty')

    recipes = get_db().execute('SELECT * FROM recipes WHERE user_id=?',
                            [g.user['id']]
                            ).fetchall()
    return render_template('tools/create_menu.html',
                            recipes=recipes)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):

    db = get_db()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        selected_recipes = request.form.getlist('selected_recipe')

        if selected_recipes:

            # Create the array of recipes
            menu = [''] * 5
            for recipe in selected_recipes:
                course = int(recipe[0])
                menu[course] += f"{recipe[1:]}-"

            # Remove '-' in the end (if any)
            for c, course in enumerate(menu):
                if course:
                    menu[c] = course[:len(course) - 1]

            db.execute('UPDATE menus SET'
                    ' title=?, description=?, recipes=?'
                    ' WHERE id=?',
                    [title, description, ','.join(menu), id])
        
            db.commit()
            return redirect(url_for('menus.display'))
            
        else:
            flash('Menu cannot be empty')

    menu = db.execute(
            'SELECT * FROM menus WHERE id=?', [id]).fetchone()

    included_recipes = []
    for course in menu['recipes'].split(','):
        included_recipes.append([db.execute(
            'SELECT * FROM recipes WHERE id=?', [int(recipe_id)]).fetchone()
            for recipe_id in course.split('-')
            if recipe_id != ''])
    
    all_recipes = db.execute('SELECT * FROM recipes WHERE user_id=?',
                            [g.user['id']]
                            ).fetchall()
    for rec in all_recipes.copy():
        for included_course in included_recipes:
            if rec in included_course:
                all_recipes.remove(rec)
                break
    
    return render_template('tools/edit_menu.html',
                            menu=menu,
                            included_recipes=included_recipes,
                            all_recipes=all_recipes)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute("DELETE FROM menus WHERE id=?", [id])
    db.commit()
    return redirect(url_for('menus.display'))
