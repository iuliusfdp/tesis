from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, PasswordField
from wtforms import DateTimeField, BooleanField
from models import Administrador

class RegistroForm(Form):      
    usuario = TextField("Usuario",  [validators.Required("Introduzca su nombre de usuario.")])
    password = PasswordField('Contrasena', [validators.Required("Introduzca una contrasena")])
    enviar = SubmitField("Entrar")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self, db):
        if not Form.validate(self):
            return False
        user = db.session.query(User).filter_by(usuario = self.usuario.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            return False  
