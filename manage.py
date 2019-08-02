# manage.py

import unittest
from flask.cli import FlaskGroup
from src import create_app, db
# from project.api.models import Product, Price
app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def recreate_db():
    """ Recreates the DataBase """
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """ Runs the tests without code coverage """
    tests = unittest.TestLoader().discover('src/test/', pattern='*_test.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        return 0
    
    return 1

@cli.command()
def seed_db():
    """Seeds the database."""
    # db.session.add(Product(name = 'Carrots'))
    # db.session.add(Product(name = 'Potatoes'))
    # db.session.commit()

if __name__ == '__main__':
    db.create_all()
    cli()
