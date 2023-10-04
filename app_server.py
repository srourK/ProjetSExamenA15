from flask import Flask, request, render_template, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(app)
app.secret_key = '123//'


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_projet = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    projects = Project.query.all()

    if request.method == 'POST':
        code_projet = request.form['code_projet']
        description = request.form['description']

        try:
            new_project = Project(code_projet=code_projet, description=description)
            db.session.add(new_project)
            db.session.commit()
            message = 'Projet ajouté avec succès.'
        except IntegrityError:
            db.session.rollback()
            message = 'Erreur : Le code du projet existe déjà.'

    return render_template('index.html', message=message, projects=projects)


@app.route('/recherche_projet', methods=['GET', 'POST'])
def recherche_projet():
    projects = Project.query.all()


    project = None
    if request.method == 'POST':
        code_projet = request.form['search_code_projet']
        project = Project.query.filter_by(code_projet=code_projet).first()

        if not project:
            flash('Projet non trouvé.', 'error')

    return render_template('recherche_projet.html', project=project, projects=projects)


#delete
@app.route('/delete_project/<int:project_id>', methods=['GET'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    try:
        db.session.delete(project)
        db.session.commit()
        flash('Projet supprimé avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(str(e), 'error')
    return redirect(url_for('recherche_projet'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
