import functools
from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from src.db import get_db

bp = Blueprint('auth',__name__, url_prefix='/auth')

@bp.route('/register', methods = ('GET', 'POST'))
def register():
  if request.method == 'POST':
    userId = request.form['userId']
    password = request.form['password']
    email = request.form['email']
    db = get_db()
    error = None
    
    if not userId:
      error = 'ID is required'
    elif not password:
      error = 'Password is required'
    elif not email:
      error = 'Email is required'
      
    if error is None:
      try:
        db.execute(
          "INSERT INTO user (userId, password, email) VALUES (?,?,?)", (userId,generate_password_hash(password),email)
        )
        db.commit()
      except db.IntegrityError:
        error = f"User {userId} is already registered"
      else:
        return redirect(url_for("auth.login"))
    flash(error)
  return render_template('auth/register.html')

@bp.route('/login', methods = ('GET','POST'))
def login():
  if request.method == 'POST':
    userId = request.form['userId']
    password = request.form['password']
    db = get_db()
    error = None
    user = db.execute(
      'SELECT * FROM user WHERE userId = ?', (userId,)
    ).fetchone()
    
    if user is None:
      error = 'Incorrect ID'
    elif not check_password_hash(user['password'], password):
      error = ' Incorrect password'
      
    if error is None:
      session.clear()
      session['user_id'] = user['id']
      return redirect(url_for('main_page'))
    flash(error)
  return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')
  
  if user_id is None:
    g.user = None
  else:
    g.user = get_db().execute(
      'SELECT * FROM user WHERE id = ?',(user_id,)
    ).fetchone()
    
@bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('main_page'))

def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth.login'))
    return view(**kwargs)
  return wrapped_view


    