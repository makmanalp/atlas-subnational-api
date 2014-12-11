from colombia import create_app, models
import factories
from flask.ext.script import Manager, Shell

import random

app = create_app()
manager = Manager(app)


def _make_context():
        return dict(app=app, db=models.db, models=models, factories=factories)

manager.add_command("shell", Shell(make_context=_make_context))


@manager.option("-n", help="Number of dummy things")
def dummy(n=10):
    """Generate dummy data."""
    if not app.debug:
        raise Exception("Unsafe to generate dummy data while not in DEBUG.")

    # Generate a set of products and departments.
    departments = []
    for x in range(0, 10):
        departments.append(factories.Department())

    products = []
    for x in range(0, 20):
        products.append(factories.HSProduct())

    # Generate what products exist in which departments and by how much
    for d in departments:
        if random.random() < 0.2:
            # This place focuses on a few products
            for x in range(4):
                factories.DepartmentProductYear(
                    department=d,
                    product=random.choice(products),
                    year=2008
                )
        else:
            # This place is a diverse economy
            for x in range(20):
                factories.DepartmentProductYear(
                    department=d,
                    product=random.choice(products),
                    year=2008
                )

    # Permute data for the following years according to this year.
    for d in departments:
        dpys = models.DepartmentProductYear\
            .query.filter_by(department=d).all()
        for year in range(2009, 2013):
            if random.random() < 0.1:
                delta = random.random() - 0.5
            else:
                delta = 5 * (random.random() - 0.5)

            for dpy in dpys:
                factories.DepartmentProductYear(
                    department=dpy.department,
                    product=dpy.product,
                    year=year,
                    import_value=dpy.import_value * delta,
                    export_value=dpy.export_value * delta
                )

    models.db.session.commit()


if __name__ == "__main__":
    manager.run()
