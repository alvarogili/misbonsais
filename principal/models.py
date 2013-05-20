#encoding:utf-8 <- Esta línea permite usar tíldes y caracteres especiales 
from django.db import models #<- Clase con la descripción de modelos
from django.contrib.auth.models import User #<- Llama al modelo usuario

class Bonsai(models.Model):
	"""
		Class that represents a bonsái
	"""
	#nombre comun o regional de la planta
	common_name = models.CharField(max_length=100)
	#nombre botasnico o latin
	botanical_name = models.CharField(max_length=100, blank=True)
	#sobrenombre
	byname = models.CharField(max_length=100, blank=True)
	#Fecha de nacimiento o adquisicion
	birth_date = models.DateField()
	#estilo
	style = models.CharField(max_length=100, blank=True)	
	#ruta de la imagen
	imagePath = models.URLField(max_length=400, blank=True)
	#Enlace al modelo Usuario que Django ya tiene construido
	usuario = models.ForeignKey(User)

	def __unicode__(self):
		return unicode(self.id)
		

class Labor(models.Model):
	"""
		Class that represents a task in a bonsái
	"""
	#Fecha de la Labor
	date = models.DateField()
	#Descripción de la labor
	description = models.TextField(max_length=500, blank=True)
	#bonsái al que se le aplicó la Labor
	bonsai = models.ForeignKey(Bonsai)
	#tipo de labor
	task_type_of_labor = (
		(0, 'Poda aérea'),
		(1, 'Pinzado'),
		(2, 'Poda de raíces'),
		(3, 'Transplante'),
		(4, 'Abonado'),
		(5, 'Afección/Enfermedad'),
		(6, 'Tratamiento de enfermedad'),
		(7, 'Enraizado sobre piedra'),		
		(8, 'Otra'),
		(9, 'Defoliado'),
		(10, 'Cambio de mantillo'),
		(11, 'Alambrado')		
	)
	task_type = models.IntegerField(choices=task_type_of_labor)

class EMail(models.Model):
	"""
		Class that represents an email to send when the user lost the password
	"""
	email = models.EmailField()