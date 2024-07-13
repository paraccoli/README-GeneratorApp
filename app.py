import os
from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from flask_babel import Babel, get_locale
from claude_api import generate_readme
from config import Config
import markdown
from models import db, Project

os.environ['FLASK_ENV'] = 'development'

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
babel = Babel(app)

def get_locale():
    if 'language' in session:
        return session['language']
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())

babel.init_app(app, locale_selector=get_locale)

@app.context_processor
def inject_conf_var():
    return dict(
        LANGUAGES=app.config['LANGUAGES'],
        get_locale=get_locale
    )

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    project_name = data['projectName']
    project_description = data['projectDescription']
    project_features = data['projectFeatures'].split(',')

    readme = generate_readme(project_name, project_description, project_features)

    return jsonify({'readme': readme})

@app.route('/projects', methods=['GET'])
def list_projects():
    projects = Project.query.order_by(Project.updated_at.desc()).all()
    return render_template('projects.html', projects=projects)

@app.route('/project/<int:project_id>', methods=['GET'])
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('edit_project.html', project=project)

@app.route('/save_project', methods=['POST'])
def save_project():
    data = request.json
    project_id = data.get('id')
    
    if project_id:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
    else:
        project = Project()
    
    project.name = data['name']
    project.description = data['description']
    project.features = data['features']
    project.readme = data['readme']
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify(project.to_dict()), 200

@app.route('/update_readme', methods=['POST'])
def update_readme():
    data = request.json
    project_id = data['id']
    new_readme = data['readme']
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    project.readme = new_readme
    db.session.commit()
    
    return jsonify({'message': 'README updated successfully'}), 200

@app.route('/change_language/<language>')
def change_language(language):
    session['language'] = language
    return redirect(request.referrer)

@app.route('/render_markdown', methods=['POST'])
def render_markdown():
    data = request.json
    md = markdown.markdown(data['markdown'])
    return md

@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash(_('Project deleted successfully'), 'success')
    return redirect(url_for('list_projects'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
