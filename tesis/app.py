from flask import Flask, render_template, request, flash, redirect, session, url_for
from forms import RegistroForm
from flask.ext.mail import Message, Mail 
from models import Base, Administrador, Categoria, Dato
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
from flask import session, url_for, redirect
import xlrd
import urllib2
from sqlalchemy import exists

SECRET_KEY = '\x84\xed\xca\xe36\x8d\x17\xd4\xb3X\xfd1\xdfJx\xc6\xe9\xcf\x00\xdf\x9e \xa9l'

SQLALCHEMY_DATABASE_URI = 'mysql://root:julian@localhost/db'

app = Flask(__name__)
app.config.from_object(__name__) 

db = SQLAlchemy(app)
db.Model = Base


@app.route('/')
def home():
    cat = db.session.query(Categoria).filter_by(unidad='Nacional')
    cat2 = db.session.query(Categoria).filter_by(unidad='Internacional')    
    return render_template('home.html', cat=cat, cat2=cat2)


@app.route('/SocialesNacional')
def soc_nac():
    cons = db.session.query(Dato).filter_by(unidad='Los Rios').order_by(Dato.fecha).offset(8)
    cons2 = db.session.query(Dato).filter_by(unidad='La Araucania').order_by(Dato.fecha).offset(8)
    cons3 = db.session.query(Dato).filter_by(unidad='Los Lagos').order_by(Dato.fecha).offset(8)
    return render_template('social_nac.html', cons=cons, cons2=cons2, cons3=cons3)

@app.route('/EconomicasNacional')
def eco_nac():
    return render_template('economica_nac.html')

@app.route('/ProductivasNacional')
def pro_nac():
    return render_template('productiva_nac.html')

@app.route('/SectorialesNacional')
def sec_nac():
    return render_template('sectorial_nac.html')

@app.route('/SocialesInternacional')
def soc_int():
    return render_template('social_int.html')

@app.route('/EconomicasInternacional')
def eco_int():
    return render_template('economica_int.html')

@app.route('/ProductivasInternacional')
def pro_int():
    return render_template('productiva_int.html')

@app.route('/SectorialesInternacional')
def sec_int():
    return render_template('sectorial_int.html')

@app.route('/VariablesSociales')
def var_socn():
    return render_template('var_socialn.html')

@app.route('/DemografiaNacional')
def demo_nac():
    cons = db.session.query(Dato).order_by(Dato.unidad, Dato.fecha)
    return render_template('demografia_n.html', cons=cons)

@app.route('/PobrezaNacional')
def pobr_nac():
    return render_template('pobreza_n.html')

@app.route('/AccesosNacional')
def accs_nac():
    return render_template('Accesos_n.html')

if __name__ == '__main__':
    app.run(debug=True)
