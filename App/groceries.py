from .db import get_db
from flask import render_template, Blueprint, request, redirect, url_for, g, jsonify, flash, abort, Response   
from App.auth import login_required

bp = Blueprint('groceries', __name__, url_prefix='/groceries')

@bp.route('', methods=['GET'])
@login_required
def display():

    groc = get_db().execute("SELECT groceries FROM users WHERE id=?",
                    (g.user['id'], )
                    ).fetchone()['groceries'].split(',')
    if groc[0] == '':
        groc = ''

    return render_template('tools/groceries.html', groceries=groc)

@bp.route('/add', methods=['POST'])
@login_required
def add():
    db = get_db()
    error = None
    new_item = request.form.get('new')
    groceries = db.execute(
            "SELECT groceries FROM users WHERE id=?",
            (g.user['id'], )
            ).fetchone()['groceries']

    if not new_item:
        error = 'Empty value entered'
    elif new_item in groceries:
        error = 'The item is already included'
    
    if error is None:
        if groceries:
            groceries += f",{new_item}"
        else:
            groceries += f"{new_item}"
        db.execute(
            'UPDATE users SET groceries=? WHERE id=?',
            [groceries, g.user['id']]
        )
        db.commit()
        return redirect(url_for('groceries.display'))
    else:
        abort(Response(error))


@bp.route('/append', methods=('POST', ))
@login_required
def append():
    groc = request.get_json()
    db = get_db()
    groceries = db.execute("SELECT groceries FROM users WHERE id=?",
                          (g.user['id'], )
                          ).fetchone()['groceries']
    
    if not groceries:
        groceries = ','.join(groc)
    else:
        groceries = groceries + ',' + ','.join(groc)

    get_db().execute("UPDATE users SET groceries=? WHERE id=?",
                    (groceries, g.user['id']))
    db.commit()
    return jsonify(groceries.split(','))

@bp.route('/remove', methods=['POST'])
@login_required
def remove():
    db = get_db()
    groceries = db.execute("SELECT groceries FROM users WHERE id=?",
                          (g.user['id'], )
                          ).fetchone()['groceries'].split(',')
    remove_item = request.form.get('remove')
    if remove_item not in groceries:
        abort(Response('No such item in the list'))
    else:
        groceries.remove(remove_item)
        db.execute(
            'UPDATE users SET groceries=? WHERE id=?',
            [','.join(groceries), g.user['id']])
        db.commit()
        return redirect(url_for('groceries.display'))
    

@bp.route('/empty', methods=('POST', ))
@login_required
def empty():
    db = get_db()
    db.execute("UPDATE users SET groceries='' WHERE id=?",
              [g.user['id']])
    db.commit()
    return redirect(url_for('groceries.display'))
