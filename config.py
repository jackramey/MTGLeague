import os

basedir = os.path.abspath(os.path.dirname(__file__))

#SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/mtgleague.db'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
