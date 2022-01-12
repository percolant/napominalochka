from setuptools import setup, find_packages

setup(
  name='NapominalOchka',
  version='0.0.1',
  description='NapominalOchka',
  py_modules=['napominalochka.napominalochka', 'napominalochka.api'],
  packages=find_packages(include=['src', 'src.*']),
  package_dir={'': 'src'},
  install_requires=[
    'python-telegram-bot'
  ],
  entry_points={
    'console_scripts': [
        'napominalochka=napominalochka.napominalochka:main',
    ],
  }
)
