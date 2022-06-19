from .db import get_db
from flask import render_template, Blueprint, request, redirect, url_for, flash, g
from App.auth import login_required
from werkzeug.exceptions import abort

bp = Blueprint('recipe', __name__, url_prefix='/recipes')

# Get recipe from database by id
def get_recipe(id):
    recipe = get_db().execute("SELECT * FROM recipes WHERE id=?", 
                             (id, )
                    ).fetchone()
    
    if recipe is None:
        abort(404, "Recipe not found")

    return recipe

# Get the my_recipes page which presents all recipes of the user
@bp.route('/my_recipes')
@login_required
def my_recipes():
    db = get_db()

    db_query = "SELECT * FROM recipes WHERE user_id = ?"
    params = [g.user['id']]

    # Check the search query
    search_query = request.args.get('q', type=str)
    if search_query:
        db_query += "AND title LIKE ?"
        params.append('%'+search_query+'%')
    else:
        search_query = ""
    
    # Check if category was selected
    category_id = request.args.get('category', type=int)
    if category_id:
        db_query += "AND category_id = ?"
        params.append(category_id)
        category = db.execute("SELECT * FROM categories WHERE id = ?",
                              (category_id, )).fetchone()
    else:
        category = None

    recipes = db.execute(db_query, params).fetchall()

    return render_template('recipes/my_recipes.html',
                            recipes=recipes,
                            query=search_query,
                            category=category)

# Display a recipe
@bp.route('/<int:id>', methods=('GET', ))
@login_required
def display(id):
    recipe = get_recipe(id)
    db = get_db()
    category = db.execute("SELECT * FROM categories WHERE id=?",
                                (recipe['category_id'], )).fetchone()
    groceries = db.execute("SELECT groceries FROM users WHERE id=?",
                                (g.user['id'], )).fetchone()
    groceries = groceries['groceries'].split(',') if groceries['groceries'] else []
    return render_template('/recipes/recipe.html', recipe=recipe, category=category, groceries=groceries)

# Create a new recipe
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        error = None
        title = request.form['title']

        if not title:
            error = "Title must not be empty"
        
        description = request.form['description']
        directions = request.form['directions']

        if not directions:
            error = "Directions must not be empty"

        category = request.form['category']
        if category == '':
            category = None

        # Ingredients and links are stored in a string, separated by ','
        ingredients = request.form.getlist('ingredient[]')
        ingredients = ','.join(ingredients)

        if not ingredients:
            error = "Ingredients list must not be empty."

        links = request.form.getlist('link[]')
        links = ','.join(links)

        notes = request.form['notes']
        servings = request.form['servings']
        prep = request.form['prep_t']
        cook = request.form['cook_t']
        total = int(prep) + int(cook)

        if error is None:
            db = get_db()
            cur = db.cursor()
            cur.execute("INSERT INTO recipes" 
                       "(title, description, ingredients,"
                       "directions, links, notes,"
                       "servings, prep_t, cook_t,"
                       "total_t, category_id,  user_id)"
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (title, description, ingredients,
                        directions, links, notes, 
                        servings, prep, cook,
                        total, category, g.user['id']))   
        
            db.commit()
            return redirect(url_for('recipe.display', id=cur.lastrowid))
            
        else:
            flash(error)
    
    categories = get_db().execute("SELECT * FROM categories WHERE user_id = ?",
                            (g.user['id'], ))
    return render_template('recipes/create.html', categories=categories)
    

# Edit a recipe
@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):

    if request.method == 'POST':
        error = None
        title = request.form.get('title')

        if not title:
            error = "Title must not be empty"
        
        description = request.form['description']
        directions = request.form['directions']

        if not directions:
            error = "Directions must not be empty"

        category = request.form['category']

        # Ingredients and links are store in a string, separated by ','
        ingredients = request.form.getlist('ingredient[]')
        ingredients = ','.join(ingredients)

        if not ingredients:
            error = "Ingredients list must not be empty."

        links = request.form.getlist('link[]')
        links = ','.join(links)

        notes = request.form['notes']
        servings = request.form['servings']
        prep = request.form['prep_t']
        cook = request.form['cook_t']
        total = int(prep) + int(cook)
      
        if error is None:
            db = get_db()
            db.execute("UPDATE recipes SET "
                    "title=?, description=?, ingredients=?, directions=?, links=?, notes=?, servings=?, prep_t=?, cook_t=?, total_t=?, category_id=?"
                    " WHERE id = ?",
                    (title, description, ingredients, directions, links, notes, servings, prep, cook, total, category, id))   
            db.commit()
            return redirect(url_for('recipe.display', id=id))
        else:
            flash(error)
    
    recipe = get_recipe(id)
    categories = get_db().execute("SELECT * FROM categories WHERE user_id=?",
                            (g.user['id'], ))
    return render_template('recipes/edit.html', recipe=recipe, categories=categories)

# Delete a recipe
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute("DELETE FROM recipes WHERE id=?", (id, ))
    db.commit()
    return redirect(url_for('recipe.my_recipes'))
