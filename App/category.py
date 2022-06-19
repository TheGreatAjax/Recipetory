from .db import get_db
from flask import render_template, Blueprint, request, redirect, url_for, flash, g
from App.auth import login_required
from werkzeug.exceptions import abort

bp = Blueprint('category', __name__, url_prefix='/categories')

# Get category from database by id
def get_category(id):
    category = get_db().execute("SELECT * FROM categories WHERE id=?", 
                             (id, )
                    ).fetchone()
    
    if category is None:
        abort(404, "Category not found")

    return category

# Get the categories page which presents all categories of the user
@bp.route('/my_categories')
@login_required
def my_categories():
    db = get_db()

    db_query = "SELECT * FROM categories WHERE user_id = ?"
    params = [g.user['id']]

    # Check the search query
    search_query = request.args.get('q', type=str)
    if search_query:
        db_query += "AND title LIKE ?"
        params.append('%'+search_query+'%')
    else:
        search_query = ""

    categories = db.execute(db_query, params).fetchall()
    return render_template('categories/my_categories.html',
                            categories=categories,
                            query=search_query)

# Display a category
@bp.route('/<int:id>', methods=['GET'])
@login_required
def display(id):
    return redirect(url_for('recipe.my_recipes', category=id))

# Create a new category
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        # Fetch the name and description and create the category

        category_name = request.form.get('name')
        category_description = request.form.get('description')

        error = None
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute("INSERT INTO categories"
                    "(name, description, user_id) VALUES (?, ?, ?)",
                    (category_name, category_description, g.user['id']))
        except db.IntegrityError:
            error = 'Category with such name already exists'
        else:
            db.commit()

            cat_id = cur.lastrowid # The ID of newly created category

            # Link each selected recipe to the category
            included_recipes = request.form.getlist('recipe[]')
            for recipe_id in included_recipes:
                cur.execute("UPDATE recipes SET "
                                "category_id = ? WHERE id = ?",
                                (cat_id, recipe_id)) 
            db.commit()

            return redirect(url_for('category.display', id=cat_id))

        flash(error)

    # Select recipes which don't belong to any category yet
    recipes = get_db().execute("SELECT * FROM recipes WHERE user_id = ? AND category_id is NULL", 
                                (g.user['id'],)).fetchall()
    
    return render_template('categories/create.html', recipes=recipes)

# Create a new category
@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):

    if request.method == 'POST':
        # Fetch the name and description and create the category
        category_name = request.form['name']
        category_description = request.form['description']

        db = get_db()
        cur = db.cursor()
        cur.execute("UPDATE categories SET name=?, description=? WHERE id=?",
                    (category_name, category_description, id))
        
        db.commit()

        # Unlink all unchecked recipes from the category
        excluded_recipes = request.form.getlist('excluded_recipes[]')
        for recipe_id in excluded_recipes:
            cur.execute("UPDATE recipes SET category_id = null WHERE id=?",
                        (recipe_id, ))

        # Link newly selected recipes to the category
        free_recipes = request.form.getlist('free_recipes[]')
        for recipe_id in free_recipes:
            cur.execute("UPDATE recipes SET "
                             "category_id = ? WHERE id = ?",
                             (id, recipe_id)) 
        db.commit()
        return redirect(url_for('category.display', id=id))

    
    category = get_category(id)
    # Recipes which belong to the category
    included_recipes = get_db().execute("SELECT * FROM recipes WHERE user_id = ? AND category_id = ?", 
                                (g.user['id'], id)).fetchall()

    # Recipes which do not belong to any category
    free_recipes = get_db().execute("SELECT * FROM recipes WHERE user_id = ? AND category_id is NULL", 
                                (g.user['id'],)).fetchall()
    return render_template('categories/edit.html',
                             category=category,
                             included_recipes=included_recipes,
                            free_recipes=free_recipes)

# Delete a category
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()

    recipes = db.execute("SELECT * FROM recipes WHERE category_id=?",
                        (id,)).fetchall()
    for recipe in recipes:
        db.execute("UPDATE recipes SET category_id = null WHERE id=?",
                  (recipe['id'], ))

    db.execute("DELETE FROM categories WHERE id = ?", (id, ))
    db.commit()
    return redirect(url_for('category.my_categories'))