from django.db import models
from django.db.models.fields.related import OneToOneField
from django.contrib.auth.models import User
import random


class Pregunta(models.Model):
    texto = models.TextField(verbose_name='Contenido de la pregunta')
    max_puntaje = models.IntegerField(verbose_name='Puntaje máximo', default=3)

    def __str__(self):
        return self.texto


class Respuesta(models.Model):
    # Cantidad máxima y mínima de opciones/respuestas por pregunta
    MAX = 4
    MIN = 4
    pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
    correcta = models.BooleanField(verbose_name='¿Es la respuesta correcta?', default=False, null=False)
    texto = models.TextField(verbose_name='Contenido de la respuesta')

    def __str__(self):
        return self.texto


class QuizUsuario(models.Model):
    # Cascade para que cuando se elimine un usuario, se eliminen las preguntas respondidas y otras asociaciones del mismo
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    puntaje_total = models.IntegerField(verbose_name='Puntaje Total', default=0)

    def crear_intentos(self, pregunta):
        intento = PreguntasRespondidas(pregunta=pregunta, quizUser=self)
        intento.save()

    def obtener_nuevas_preguntas(self):
        respondidas = PreguntasRespondidas.objects.filter(quizUser=self).values_list('pregunta__pk', flat=True)
        preguntas_restantes = Pregunta.objects.exclude(pk__in=respondidas)
        if not preguntas_restantes.exists():
            return None
        return random.choice()
    
    # Respuesta Seleccionada es de la clase Respuesta de este mismo archivo (models)
    def validar_intento(self, pregunta_respondida, respuesta_seleccionada):
        if pregunta_respondida.pregunta_id != respuesta_seleccionada.pregunta_id:
            return
        
        pregunta_respondida.respuesta_seleccionada = respuesta_seleccionada
        if respuesta_seleccionada.correcta is True:
            pregunta_respondida.correcta = True
            pregunta_respondida.puntaje_obtenido = respuesta_seleccionada.pregunta.puntaje
        
        pregunta_respondida.save()


class PreguntasRespondidas(models.Model):
    quizUser = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE, related_name='intentos')
    correcta = models.BooleanField(verbose_name='¿Es la respuesta correcta?', default=False, null=False)
    puntaje = models.IntegerField(verbose_name='Puntaje obtenido', default=0)