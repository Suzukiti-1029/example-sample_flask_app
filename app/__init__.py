import os
from flask import Flask

def create_app(test_config=None):
  # アプリの作成・設定
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY='256133', #TODO 本番はランダムな値に変更
    DATABASE=os.path.join(app.instance_path, 'app.mysql'), #TODO データベース設定
  )
  
  if test_config is None:
    # テスト設定が渡されてない場合、インスタンスの設定が存在すれば、それを読み込む
    app.config.from_pyfile('config.py', silent=True)
  else:
    # テスト設定が渡された場合、それを読み込む
    app.config.from_mapping(test_config)
  
  # インスタンスのフォルダが存在することを確認する
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass
  
  # Helloと返すだけの単純なページ
  @app.route('/hello')
  def hello():
    return 'Hello, World!'
  
  return app
