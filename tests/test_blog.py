import pytest
from app.db import get_db

def test_index(client, auth):
  response = client.get('/')
  assert "ログイン" in response.get_data(as_text=True)
  assert "新規登録" in response.get_data(as_text=True)
  auth.login()
  response = client.get('/')
  assert "ログアウト" in response.get_data(as_text=True)
  assert b"test title" in response.data
  assert b"by test on 2018-01-01" in response.data
  assert b"test\nbody" in response.data
  assert b'href="/1/update"' in response.data

@pytest.mark.parametrize('path', (
  '/create',
  '/1/update',
  '/1/delete',
))
def test_login_required(client, path):
  response = client.post(path)
  assert response.headers["Location"] == "/auth/login"

def test_author_required(app, client, auth):
  # 投稿した作者を別の作者に変える
  with app.app_context():
    db = get_db()
    db.execute('update post set author_id = 2 where id = 1')
    db.commit()
  
  auth.login()
  # 現在のユーザは他人の投稿を修正できない
  assert client.post('/1/update').status_code == 403
  assert client.post('/1/delete').status_code == 403
  # 現在のユーザは「編集」のリンクが見えない
  assert b'href="/1/update"' not in client.get('/').data

@pytest.mark.parametrize('path', (
  '/2/update',
  '/2/delete',
))
def test_exists_required(client, auth, path):
  auth.login()
  assert client.post(path).status_code == 404

def test_crete(client, auth, app):
  auth.login()
  assert client.get('/create').status_code == 200
  client.post(
    '/create',
    data = { 'title': 'created', 'body': '' }
  )
  with app.app_context():
    db = get_db()
    count = db.execute('select count(id) from post').fetchone()[0]
    assert count == 2

def test_update(client, auth, app):
  auth.login()
  assert client.get('/1/update').status_code == 200
  client.post(
    '/1/update',
    data = { 'title': 'updated', 'body': '' }
  )
  with app.app_context():
    db = get_db()
    post = db.execute('select * from post where id = 1').fetchone()
    assert post['title'] == 'updated'

@pytest.mark.parametrize('path', (
  '/create',
  '/1/update',
))
def test_create_update_validate(client, auth, path):
  auth.login()
  response = client.post(path, data = {'title': '', 'body': ''})
  assert 'Titleを入力してください' in response.get_data(as_text=True)

def test_delete(client, auth, app):
  auth.login()
  response = client.post('/1/delete')
  assert response.headers["Location"] == "/"
  with app.app_context():
    db = get_db()
    post = db.execute('select * from post where id = 1').fetchone()
    assert post is None
