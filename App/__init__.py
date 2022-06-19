from flask import Flask, render_template, g, redirect, url_for
from . import db, auth, recipe, category, groceries, planning, menus 
import os

# APPLICATION FACTORY
# https://flask.palletsprojects.com/en/2.1.x/tutorial/factory/
def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        #DEV = 'development',
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/Main')
    def Main():
        return render_template('Main.html')

    @app.route('/')
    def index():
        if not g.user:
            return redirect('/Main')
        else:
            return redirect(url_for('recipe.my_recipes'))

    
    db.init_app(app)

    # Blueprints
    for bp in [auth.bp, recipe.bp, category.bp, groceries.bp, planning.bp, menus.bp]:
        app.register_blueprint(bp)
   
    
    return app

