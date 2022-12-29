from setuptools import find_packages, setup

setup(
  name='sample_flask_app',
  version='1.0.0',
  packages=find_packages(),
  include_package_data=True, # 「MANIFEST.in」ファイルが必要
  zip_safe=False,
  install_requires=[
    'flask',
  ]
)