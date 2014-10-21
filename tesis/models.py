from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import xlrd
import urllib2
import wbpy
import pandas as pd
from pprint import pprint

Base = declarative_base()

class Administrador(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key = True)
    nombre = Column(String(100))
    pwdhash = Column(String(100))

    def __init__(self, nombre, password):
        self.nombre = nombre.title()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def __str__(self):
        return "{nombre}".format(nombre=self.nombre)

class Categoria(Base):
	__tablename__ = 'categoria'
	id = Column(Integer, primary_key = True)
	nombre = Column(String(100))
	unidad = Column(String(100))
	ind = Column(String(100), unique=True)
	
	def __init__(self, nombre, unidad, ind):
		self.nombre=nombre.title()
		self.unidad=unidad.title()
		self.ind=ind.upper()
	
	def __str__(self):
		return "{nombre}".format(nombre=self.nombre)

class Dato(Base):
	__tablename__='dato'
	id = Column(Integer, primary_key=True)
	variable = Column(String(100))
	unidad = Column(String(100))
	categoria = Column(String(100), ForeignKey('categoria.ind'))
	tipofecha = Column(String(100))
	fecha = Column(String(100))
	valor = Column(Integer)
    	cate = relationship(Categoria, lazy='joined', join_depth=1, viewonly=True)

	def __init__(self, variable, unidad, categoria, fecha, tipofecha, valor):
		self.variable = variable.title()
		self.categoria = categoria.upper()
		self.unidad = unidad.title()
		self.fecha = fecha.title()
		self.tipofecha = tipofecha.title()
		self.valor = valor
	
	def __str__(self):
		return "{variable} {unidad} {tipofecha} {fecha} {valor}".format(variable=self.variable, unidad=self.unidad, tipofecha=self.tipofecha, fecha=self.fecha, valor=self.valor)	


if __name__ == '__main__':
	# Para test de los modelos
	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker
	from datetime import timedelta

	engine = create_engine('mysql://root:julian@localhost/db', echo=True)

	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

	Session = sessionmaker(bind=engine)
	session = Session()

	cat=Categoria(nombre='Sociales', unidad='Nacional', ind='SONA')
	session.add(cat)

	session.add(Categoria(nombre='Economicas', unidad='Nacional', ind='ECNA'))
	session.add(Categoria(nombre='Productivas', unidad='Nacional', ind='PRNA'))
	session.add(Categoria(nombre='Sectoriales', unidad='Nacional', ind='SENA'))

	cat5=Categoria(nombre='Sociales', unidad='Internacional', ind='SOIN')
	session.add(cat5)
	session.add(Categoria(nombre='Economicas', unidad='Internacional', ind='ECIN'))
	session.add(Categoria(nombre='Productivas', unidad='Internacional', ind='PRIN'))
	session.add(Categoria(nombre='Sectoriales', unidad='Internacional', ind='SEIN'))
	session.commit()

	myfile = urllib2.urlopen("http://www.ine.cl/canales/chile_estadistico/demografia_y_vitales/proyecciones2014/proyecciones-de-poblacion-2014.xlsx")
	output = open('proyecciones-de-poblacion-2014.xlsx', 'wb')
	output.write(myfile.read())
	output.close()


	book = xlrd.open_workbook("proyecciones-de-poblacion-2014.xlsx")
	for x in range(1,14):
		sh15 = book.sheet_by_index(5)
		pob15 = sh15.cell_value(rowx=86, colx=x)
		sh1 = book.sheet_by_index(6)
		pob1 = sh1.cell_value(rowx=86, colx=x)
		sh2 = book.sheet_by_index(7)
		pob2 = sh2.cell_value(rowx=86, colx=x)
		sh3 = book.sheet_by_index(8)
		pob3 = sh3.cell_value(rowx=86, colx=x)
		sh4 = book.sheet_by_index(9)
		pob4 = sh4.cell_value(rowx=86, colx=x)
		sh5 = book.sheet_by_index(10)
		pob5 = sh5.cell_value(rowx=86, colx=x)
		shm = book.sheet_by_index(11)
		pobm = shm.cell_value(rowx=86, colx=x)
		sh6 = book.sheet_by_index(12)
		pob6 = sh6.cell_value(rowx=86, colx=x)
		sh7 = book.sheet_by_index(13)
		pob7 = sh7.cell_value(rowx=86, colx=x)
		sh8 = book.sheet_by_index(14)
		pob8 = sh8.cell_value(rowx=86, colx=x)
		sh9 = book.sheet_by_index(15)
		pob9 = sh9.cell_value(rowx=86, colx=x)
		sh14 = book.sheet_by_index(16)
		pob14 = sh14.cell_value(rowx=86, colx=x)
		sh10 = book.sheet_by_index(17)
		pob10 = sh10.cell_value(rowx=86, colx=x)
		sh11 = book.sheet_by_index(18)
		pob11 = sh11.cell_value(rowx=86, colx=x)
		sh12 = book.sheet_by_index(19)
		pob12 = sh12.cell_value(rowx=86, colx=x)
		anno=x+2001
		session.add(Dato(categoria=cat.ind, variable='Demografica', unidad='Arica y Parinacota', tipofecha='anual',fecha=str(anno), valor=int(pob15)))
		session.add(Dato(categoria=cat.ind, variable='Demografica', unidad='Tarapaca', tipofecha='anual', fecha=str(anno), valor=int(pob1)))
		session.add(Dato(categoria=cat.ind, variable='Demografica', unidad='Antofagasta', tipofecha='anual', fecha=str(anno), valor=int(pob2)))
		session.add(Dato(categoria=cat.ind, variable='Demografica', unidad='Atacama', tipofecha='anual', fecha=str(anno), valor=int(pob3)))
		session.add(Dato(categoria=cat.ind, variable='Demografica', unidad='Coquimbo', tipofecha='anual', fecha=str(anno), valor=int(pob4)))
		session.add(Dato(categoria=cat.ind, variable='Demografica', unidad='Valparaiso', tipofecha='anual', fecha=str(anno), valor=int(pob5)))
		session.add(Dato(categoria=cat.ind, variable='Demografica', unidad='Region Metropolitana', tipofecha='anual', fecha=str(anno), valor=int(pobm)))
		session.add(Dato(categoria=cat.ind, variable='Demografica', unidad="O'Higgins", tipofecha='anual', fecha=str(anno), valor=int(pob6)))
		session.add(Dato(categoria=cat.ind, variable='Demografica', unidad='Maule', tipofecha='anual', fecha=str(anno), valor=int(pob7)))
		session.add(Dato(categoria=cat.ind, variable='Demografica', unidad='Biobio', tipofecha='anual', fecha=str(anno), valor=int(pob8)))
		session.add(Dato(categoria=cat.ind, variable='Demografica', unidad='La Araucania', tipofecha='anual', fecha=str(anno), valor=int(pob9)))
		session.add(Dato(categoria=cat.ind, variable='Demografica', unidad='Los Rios', tipofecha='anual', fecha=str(anno), valor=int(pob14)))
		session.add(Dato(categoria=cat.ind, variable='Demografica', unidad='Los Lagos', tipofecha='anual', fecha=str(anno), valor=int(pob10)))
		session.add(Dato(categoria=cat.ind, variable='Demografica', unidad='Aysen', tipofecha='anual', fecha=str(anno), valor=int(pob11)))
		session.add(Dato(categoria=cat.ind, variable='Demografica', unidad='Magallanes', tipofecha='anual', fecha=str(anno), valor=int(pob12)))

	session.commit()

	api = wbpy.IndicatorAPI()
	iso_country_codes = ["AR", "BO", "BR", "CL", "CO", "EC", "GY", "PY", "PE", "SR", "UY", "VE"]
	total_population = "SP.POP.TOTL"

	dataset = api.get_dataset(total_population, iso_country_codes, date="2002:2014")
	data = dataset.as_dict()
	for x in range(2002,2014):
		session.add(Dato(categoria=cat5.ind, variable='Demografica', unidad='Argentina', tipofecha='anual', fecha=str(x), valor=int(data["AR"][str(x)])))
		session.add(Dato(categoria=cat5.ind, variable='Demografica', unidad='Bolivia', tipofecha='anual', fecha=str(x), valor=int(data["BO"][str(x)])))
		session.add(Dato(categoria=cat5.ind, variable='Demografica', unidad='Brasil', tipofecha='anual', fecha=str(x), valor=int(data["BR"][str(x)])))
		session.add(Dato(categoria=cat5.ind, variable='Demografica', unidad='Chile', tipofecha='anual', fecha=str(x), valor=int(data["CL"][str(x)])))
		session.add(Dato(categoria=cat5.ind, variable='Demografica', unidad='Colombia', tipofecha='anual', fecha=str(x), valor=int(data["CO"][str(x)])))
		session.add(Dato(categoria=cat5.ind, variable='Demografica', unidad='Ecuador', tipofecha='anual', fecha=str(x), valor=int(data["EC"][str(x)])))
		session.add(Dato(categoria=cat5.ind, variable='Demografica', unidad='Guyana', tipofecha='anual', fecha=str(x), valor=int(data["GY"][str(x)])))
		session.add(Dato(categoria=cat5.ind, variable='Demografica', unidad='Paraguay', tipofecha='anual', fecha=str(x), valor=int(data["PY"][str(x)])))
		session.add(Dato(categoria=cat5.ind, variable='Demografica', unidad='Peru', tipofecha='anual', fecha=str(x), valor=int(data["PE"][str(x)])))
		session.add(Dato(categoria=cat5.ind, variable='Demografica', unidad='Surinam', tipofecha='anual', fecha=str(x), valor=int(data["SR"][str(x)])))
		session.add(Dato(categoria=cat5.ind, variable='Demografica', unidad='Uruguay', tipofecha='anual', fecha=str(x), valor=int(data["UY"][str(x)])))
		session.add(Dato(categoria=cat5.ind, variable='Demografica', unidad='Venezuela', tipofecha='anual', fecha=str(x), valor=int(data["VE"][str(x)])))

	session.commit()
