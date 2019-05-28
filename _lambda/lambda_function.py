# -*- coding: utf-8 -*-

import logging
import json
import random
import math
import re

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name, viewport
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective, ExecuteCommandsDirective, SpeakItemCommand,
    AutoPageCommand, HighlightMode)

from typing import Dict, Any


SKILL_NAME = "Operaciones Básicas"
WELCOME_MESSAGE = ("<speak>Bienvenido a la Skill de Operaciones Básicas, aquí podrás aprender y practicar las tablas de multiplicar, sumas, restas y divisiones. <break time=\"500ms\"/> Si necesitas ayuda, solo dí: 'Ayuda'. ¿Qué deseas realizar? </speak>")
HELP_MESSAGE = ('''<speak> 
    <p>Si deseas una tabla de multiplicar, puedes pedirme: <s>"Alexa, abre operaciones básicas y dime la tabla del 2"<break time=\"500ms\"/> </s> </p> 
    <p>Si deseas una tabla en específico, puedes preguntarme: <s>"¿Cuál es la tabla del ...?"<break time=\"500ms\"/> </s> </p> 
    <p>Si deseas practicar, puedes decirme: <s>"Quiero practicar"<break time=\"500ms\"/> </s> </p> 
    ¿Qué deseas realizar?
    </speak>''')
HELP_REPROMPT = (HELP_MESSAGE)
STOP_MESSAGE = "Gracias por usar esta skill. ¡Adiós! "
EXCEPTION_MESSAGE = "No entendí muy bien, ¿Qué deseas realizar?"

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def apl_img_title_text(title, text):
    return {
    "json" :"apl_img_title_text.json",
                    "datasources" : {
                    "bodyTemplate1Data": {
                        "type": "object",
                        "objectId": "bt1Sample",
                        "backgroundImage": {
                            "contentDescription": None,
                            "smallSourceUrl": None,
                            "largeSourceUrl": None,
                            "sources": [
                                {
                                    "url": "https://observatoriotecnologico.org.mx/assets/img/alexa/calculo.jpg",
                                    "size": "small",
                                    "widthPixels": 0,
                                    "heightPixels": 0
                                },
                                {
                                    "url": "https://observatoriotecnologico.org.mx/assets/img/alexa/calculo.jpg",
                                    "size": "large",
                                    "widthPixels": 0,
                                    "heightPixels": 0
                                }
                            ]
                        },
                        "title": title,
                        "textContent": {
                            "primaryText": {
                                "type": "PlainText",
                                "text": text
                            }
                        },
                        "logoUrl": "https://observatoriotecnologico.org.mx/assets/img/alexa/calculo_icon.png"
                    }
                }
            }

def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)

# Built-in Intent Handlers
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequest")


        speech = WELCOME_MESSAGE

        apl = apl_img_title_text("Bienvenido", re.sub('<[^<]+>', "",WELCOME_MESSAGE))
        
        if viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_LARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_MEDIUM or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_ROUND_SMALL or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.TV_LANDSCAPE_XLARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.MOBILE_LANDSCAPE_SMALL:
            handler_input.response_builder.speak(speech).add_directive(
                RenderDocumentDirective(document=_load_apl_document(apl["json"]),datasources=apl["datasources"])
            ).set_should_end_session(False)
        else:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).set_card(SimpleCard(SKILL_NAME, re.sub('<[^<]+>', "",speech))).set_should_end_session(False)
        #handler_input.response_builder.speak(speech).ask(speech).set_card(
        #    SimpleCard(SKILL_NAME, speech))
        return handler_input.response_builder.response




class TablaIntentHandler(AbstractRequestHandler):
    """Handler for Device Information Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("TablaIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("Tabla Intent")

        speech = "No entendí muy bien"+ ". ¿Qué más deseas realizar?"
    
        session_attributes = {}
        card_title = SKILL_NAME
        card_content = "No entendí muy bien"
        
        
        slots = handler_input.request_envelope.request.intent.slots
        
        try:
            numero = int(slots["numero"].value)
        except:
            numero = 1
        
        
        card_content = ""
        speech =  ""
        #MULTIPLICACION
        for i in range(0, 10+1):    
            card_content = card_content + ( "{} x {} = {} <br>".format(numero, i, numero*i))
            speech = speech + ("{} por {} es <break time=\"200ms\"/> {}. ".format(numero, i, numero*i))
            
            
        speech = speech + ". ¿Qué más deseas realizar?"
        
            
        apl = apl_img_title_text(card_title, card_content)
        
        if viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_ROUND_SMALL:
            
            apl = apl_img_title_text(card_title, "La tabla del "+str(numero))
            
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).add_directive(
            RenderDocumentDirective(document=_load_apl_document(apl["json"]),datasources=apl["datasources"])
            ).set_should_end_session(False)
        elif viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_LARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_MEDIUM or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_ROUND_SMALL or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.TV_LANDSCAPE_XLARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.MOBILE_LANDSCAPE_SMALL:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).add_directive(
            RenderDocumentDirective(document=_load_apl_document(apl["json"]),datasources=apl["datasources"])
            ).set_should_end_session(False)
        else:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).set_card(SimpleCard(SKILL_NAME, re.sub('<[^<]+>', "",speech))).set_should_end_session(False)
            
        

        return handler_input.response_builder.response
   
   
class MultiplicaIntentHandler(AbstractRequestHandler):
    """Handler for Device Information Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("MultiplicaIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("Multiplica Intent")

        speech = "No entendí muy bien"+ ". ¿Qué más deseas realizar?"
    
        session_attributes = {}
        card_title = SKILL_NAME
        card_content = "No entendí muy bien"
        
        
        #num1 = random.randint(0,10)
        #num2 = random.randint(0,10)
        slots = handler_input.request_envelope.request.intent.slots
        
        try:
            num1 = int(slots["numero_uno"].value)
            num2 = int(slots["numero_dos"].value)
            op = int(slots["operacion"].resolutions.resolutions_per_authority[0].values[0].value.id)
        except:
            num1 = 1
            num2 = 1
            op = 0
        
        if op == 0:
            card_content = "{} x {} = {} ".format(num1, num2, num1*num2)
            speech = "{} por {} es igual a {}. ¿Qué más deseas realizar?".format(num1, num2, num1*num2)
        elif op ==  1:
            card_content = "{} + {} = {} ".format(num1, num2, num1+num2)
            speech = "{} más {} es igual a {}. ¿Qué más deseas realizar?".format(num1, num2, num1+num2)
        elif op == 2:
            card_content = "{} - {} = {} ".format(num1, num2, num1-num2)
            speech = "{} menos {} es igual a {}. ¿Qué más deseas realizar?".format(num1, num2, num1-num2)
        elif op == 3:
            card_content = "{} / {} = {} ".format(num1, num2, num1+num2)
            speech = "{} entre {} es igual a {}. ¿Qué más deseas realizar?".format(num1, num2, num1/num2)
            
    
        
            
        apl = apl_img_title_text(card_title, card_content)
        
        if viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_LARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_MEDIUM or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_ROUND_SMALL or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.TV_LANDSCAPE_XLARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.MOBILE_LANDSCAPE_SMALL:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).add_directive(
            RenderDocumentDirective(document=_load_apl_document(apl["json"]),datasources=apl["datasources"])
            ).set_should_end_session(False)
        else:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).set_card(SimpleCard(SKILL_NAME, re.sub('<[^<]+>', "",speech))).set_should_end_session(False)
            
        

        return handler_input.response_builder.response
        
 


class RespuestaIntentHandler(AbstractRequestHandler):
    """Handler for Device Information Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("RespuestaIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("Respuesta Intent")

        speech = "No entendí muy bien"+ ". ¿Qué deseas realizar?"
            
        card_title = SKILL_NAME
        card_content = "No entendí muy bien"
        correcto = False
        
        
        try:
        
            #attr = handler_input.attributes_manager.persistent_attributes
            session_attr = handler_input.attributes_manager.session_attributes
            
            nivel = session_attr['nivel']
            contador = session_attr['contador']
            respuesta = session_attr['respuesta']
            
            slots = handler_input.request_envelope.request.intent.slots
            try:
                respuesta_usuario = int(slots["numero"].value)
            except:
                respuesta_usuario = 0
            session_attr['nivel'] = nivel
        except:
            contador = -1
        
        if int(respuesta_usuario) == int(session_attr['respuesta']):
            correcto = True
            session_attr['correctas'] = session_attr['correctas'] +1
        
        if correcto:
            tu_respuesta = "¡Correcto!. ".format(respuesta_usuario , session_attr['respuesta'])
        else:
            tu_respuesta = "Incorrecto, la respuesta correcta de {} {} {} es {} . ".format(session_attr['num1'],session_attr['op'],session_attr['num2'],session_attr['respuesta'])
        
        if nivel == 1:
            max_num = 10
        elif nivel == 2:
            max_num = 20
        elif nivel == 3:
            max_num = 50
            
        num1 = random.randint(0,max_num)
        num2 = random.randint(0,max_num)
        
        if contador <= 2:
            card_content = "{} + {} = ? ".format(num1, num2)
            speech = "¿cuánto es {} más {}? .".format(num1, num2)
            
            session_attr['op'] = "más"
            session_attr['respuesta'] = int(num1+num2)
        elif contador <= 5:
            if num1 < num2:
                num1 = num2 + random.randint(0,2)
            if num1 > max_num:
                num1 = max_num
            card_content = "{} - {} = ? ".format(num1, num2)
            speech = "¿cuánto es {} menos {} ? .".format(num1, num2)
            
            session_attr['op'] = "menos"
            session_attr['respuesta'] = int(num1-num2)
        elif contador <= 8:
            card_content = "{} x {} = ? ".format(num1, num2)
            speech = "¿cuánto es {} por {} ? .".format(num1, num2)
            
            session_attr['op'] = "por"
            session_attr['respuesta'] = int(num1*num2)
        else:
            while True:
                num1 = random.randint(1,max_num)
                num2 = random.randint(2,max_num)
                if num1 % num2 == 0 and num1 != num2:
                    break
            card_content = "{} / {} = ? ".format(num1, num2, num1/num2)
            speech = "¿cuánto es {} entre {} ? .".format(num1, num2)
            
            session_attr['op'] = "entre"
            session_attr['respuesta'] = int(num1/num2)
            
        session_attr['num1'] = num1
        session_attr['num2'] = num2
        
        speech = tu_respuesta +" Siguiente: "+ speech
        card_content = tu_respuesta +"<br><br>Siguiente: "+ card_content
        
        
        if contador == 10:
            session_attr['contador'] = 0
            
            if int(session_attr['correctas']) == 10:
                calif = "¡Excelente!"
            elif int(session_attr['correctas']) > 7:
                calif = "¡Muy bien!"
            elif int(session_attr['correctas']) > 5:
                calif = "¡Bien, sigue practicando!"
            else:
                calif = "¡Necesitas practicar más!"
                
            speech = tu_respuesta +"Tu calificación es de {} de {}, {}. ¿Qué más deseas realizar?".format( int(session_attr['correctas']),contador, calif)
            card_content = "Tu calificación es de {} de {}".format( int(session_attr['correctas']),contador)
        else:
            session_attr['contador'] = contador +1
            
        apl = apl_img_title_text(card_title, card_content)
        
        if viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_LARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_MEDIUM or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_ROUND_SMALL or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.TV_LANDSCAPE_XLARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.MOBILE_LANDSCAPE_SMALL:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).add_directive(
            RenderDocumentDirective(document=_load_apl_document(apl["json"]),datasources=apl["datasources"])
            ).set_should_end_session(False)
        else:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).set_card(SimpleCard(SKILL_NAME, re.sub('<[^<]+>', "",speech))).set_should_end_session(False)
            
        

        return handler_input.response_builder.response
        

class PracticarIntentHandler(AbstractRequestHandler):
    """Handler for Device Information Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PracticarIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("Practicar Intent")

        speech = "No entendí muy bien"+ ". ¿Qué más deseas realizar?"
            
        card_title = SKILL_NAME
        card_content = "No entendí muy bien"
        
        nivel = 1
        
        
    
        #attr = handler_input.attributes_manager.persistent_attributes
        session_attr = handler_input.attributes_manager.session_attributes
        
        session_attr['nivel'] = 1
        session_attr['correctas'] = 0
        session_attr['contador'] = 1
        
        slots = handler_input.request_envelope.request.intent.slots
        try:
            nivel = int(slots["practica"].resolutions.resolutions_per_authority[0].values[0].value.id)
            session_attr['nivel'] = nivel
            #if 'contador' in session_attr:
            #    contador = session_attr['contador']
        except:
            nivel = 1
            
        
        if nivel == 1:
            max_num = 10
        elif nivel == 2:
            max_num = 20
        elif nivel == 3:
            max_num = 50
            
        num1 = random.randint(0,max_num)
        num2 = random.randint(0,max_num)
        
        
        card_content = "{} + {} = ? ".format(num1, num2)
        speech = "Modo de práctica de 10 preguntas: ¿cuánto es {} más {} ? .".format(num1, num2)
        
        session_attr['op'] = "más"
        session_attr['respuesta'] = int(num1+num2)
            
        session_attr['num1'] = num1
        session_attr['num2'] = num2
        
            
        #session_attr['contador'] = contador +1
        apl = apl_img_title_text(card_title, card_content)
        
        if viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_LARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_MEDIUM or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_ROUND_SMALL or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.TV_LANDSCAPE_XLARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.MOBILE_LANDSCAPE_SMALL:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).add_directive(
            RenderDocumentDirective(document=_load_apl_document(apl["json"]),datasources=apl["datasources"])
            ).set_should_end_session(False)
        else:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).set_card(SimpleCard(SKILL_NAME, re.sub('<[^<]+>', "",speech))).set_should_end_session(False)
            
        

        return handler_input.response_builder.response
   
   
class AleatorioIntentHandler(AbstractRequestHandler):
    """Handler for Device Information Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AleatorioIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("Aleatiorio")

        speech = "Muy Bien, ¿Qué modo de practica deseas?: Fácil, Normal o Avanzado "
    
        session_attributes = {}
        card_title = SKILL_NAME
        card_content = "¿Qué modo de practica deseas?: Fácil, Normal o Avanzado"
        
        

        #session_attr['contador'] = contador +1
        apl = apl_img_title_text(card_title, card_content)
        
        if viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_LARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_MEDIUM or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_ROUND_SMALL or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.TV_LANDSCAPE_XLARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.MOBILE_LANDSCAPE_SMALL:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).add_directive(
            RenderDocumentDirective(document=_load_apl_document(apl["json"]),datasources=apl["datasources"])
            ).set_should_end_session(False)
        else:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).set_card(SimpleCard(SKILL_NAME, re.sub('<[^<]+>', "",speech))).set_should_end_session(False)
            
        

        return handler_input.response_builder.response
   
        
        
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ( is_intent_name("AMAZON.HelpIntent")(handler_input) or
                is_intent_name("AyudaIntent")(handler_input) )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, re.sub('<[^<]+>', "",HELP_MESSAGE)))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input) or
                is_intent_name("SalirIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE).set_should_end_session(True)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(LaunchRequestHandler())



sb.add_request_handler(RespuestaIntentHandler())
sb.add_request_handler(PracticarIntentHandler())
sb.add_request_handler(TablaIntentHandler())
sb.add_request_handler(AleatorioIntentHandler())
sb.add_request_handler(MultiplicaIntentHandler())
#sb.add_request_handler(TopicoAleatorioIntentHandler())
#sb.add_request_handler(SalirIntentHandler())



sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
# sb.add_global_request_interceptor(RequestLogger())
# sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
