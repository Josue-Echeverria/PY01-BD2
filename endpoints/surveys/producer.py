from kafka import KafkaProducer
import time
from db_mongo import MongoDB


def producer(client_name, broker1, topic): 
    """
    Genera la entrada para que el cliente pueda ingresar un mensaje
    Cuando el cliente lo digita, la funcion lo envia y vuelve a generar la entrada
    
    Parameters:
        client_name (str) : El nombre del cliente que esta conectado
        broker1 (str) : Broker al que desea enviar mensajes
        topic (str) : Topic al que desea enviar mensajes
    """
    while True:
        # Espera hasta que el cliente especifique el mensaje que desea enviar
        data = input(client_name + " : ")

        # Si el mensaje es /exit 
        if (data == "/exit"):
            break
        # Si el mensaje es cualquier string que no sea /exit 
        else:
            send_data(client_name, broker1, topic, data)
            time.sleep(2) 
    

def send_data(client_name, broker1, in_topic, msg):
    """
    Envia un mensaje a un topic de un broker especifico registrando tambien el mensaje en la base de datos

    Parameters:
        client_name (str) : El nombre del cliente que esta enviando el mensaje
        broker1 (str) : Al broker que lo esta enviando
        in_topic (str) : El topic al que lo esta enviando 
        msg (str) : Mensaje que el cliente esta enviando 
    Returns:
        result (): Datos registrados en el topic y la base de datos 
    
    """
    # Guarda el log en la base de datos
    MongoDB().register_log(in_topic, client_name, msg)
    
    # Crea la conexion como un producer
    p = KafkaProducer(bootstrap_servers=broker1)
    formated_msg = client_name + " : " + msg

    # Envia el mensaje al topic del broker
    p.send(topic=in_topic, value=formated_msg.encode(encoding='utf8'))
    p.close()
    

def connect_user(user, broker1, survey_id):
    """
    Registra la conexion de un usuario al modo edicion de un survey

    Parameters:
        client_name (str) : El nombre del cliente que esta enviando el mensaje
        broker1 (str) : Al broker que lo esta enviando
        survey_id (str) : El survey_id al que se esta conectando
    Returns:
        result (): Datos registrados en el topic y la base de datos 
    
    """
    # Guarda el log en la base de datos
    MongoDB().register_user_connection(survey_id, user)
    
    # Crea la conexion como un producer
    p = KafkaProducer(bootstrap_servers=broker1)

    msg = user + " se ha conectado"

    # Envia el mensaje al topic del broker
    p.send(topic=survey_id, value=msg.encode(encoding='utf8'))
    p.close()
    


