from flask import (
  Blueprint, flash, g, redirect,
  render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_requred
from app.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
  db = get_db()
  posts = db.execute('''
    select p.id, title, body, created, author_id, username
    from post p join user u on p.author_id = u.id
    order by created desc'''
  ).fetchall()
  return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
def create():
  if request.method == 'POST':
    title = request.form['title']
    body = request.form['body']
    error = None
    if not title:
      error = 'Titleを入力してください'
    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute('''
        insert into post(title, body, author_id)
        values (?, ?, ?)''',
        (title, body, g.user['id'])
      )
      db.commit()
      return redirect(url_for('blog.index'))
  return render_template('blog/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_requred
def update(id):
  post = get_post(id)

  if request.method == 'POST':
    title = request.form['title']
    body = request.form['body']
    error = None
    
    if not title:
      error = 'Titleを入力してください'
    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute('''
        update post set title = ?, body = ?
        where id = ?''',
        (title, body, id)
      )
      db.commit()
      return redirect(url_for('blog.index'))
  return render_template('blog/update.html', post=post)

def get_post(id, check_author=True):
  post = get_db().execute('''
    select p.id, title, body, created, author_id, username
    from post p join user u on p.author_id = u.id
    where p.id = ?''',
    (id,)
  ).fetchone()
  
  if post is None:
    abort(404, f"ID: {id}の投稿は存在しません")
  if check_author and post['author_id'] != g.user['id'] :
    abort(403)
  
  return post