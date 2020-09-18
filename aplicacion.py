import aiml
from flask import Flask, request
from pymessenger.bot import Bot
import os

kernel = aiml.Kernel()
kernel.learn("hola.xml")
kernel.respond("cargar aiml b")

app = Flask(__name__)
TokenDeAcceso = os.environ['TokenDeAcceso']
TokenDeVerificacion = os.environ['TokenDeVerificacion'] 
bot = Bot(TokenDeAcceso)
 
@app.route("/", methods=['GET', 'POST'])
def recibirMensaje():
    if request.method == 'GET':
        tokenDeEnvio = request.args.get("hub.verify_token")
        return tokenFacebook(tokenDeEnvio)
    
    else:
       output = request.get_json()
       for event in output['entry']:
          mensajeria = event['messaging']
          for mensaje in mensajeria:
            if mensaje.get('message'):
                remitenteID = mensaje['sender']['id']
                if mensaje['message'].get('text'):
                    mensaje = mensaje['message'].get('text')
                    respuestatext = obtenerMensajeBot(mensaje)
                    enviarMensaje(remitenteID, respuestatext)

    return "Mensaje Procesado"


def tokenFacebook(tokenDeEnvio):
    if tokenDeEnvio == TokenDeVerificacion:
        return request.args.get("hub.challenge")
    return 'Token de Verificacion Invalido'

def obtenerMensajeBot(mensaje1):
    print (mensaje1)
    return kernel.respond(mensaje1)

def enviarMensaje(remitenteID, respuesta):
    bot.send_text_message(remitenteID, respuesta)
    return "Mensaje enviado con exito"

if __name__ == "__main__":
    app.run()
