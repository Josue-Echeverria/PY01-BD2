from kafka import KafkaConsumer
from db_mongo import MongoDB

def consumer(broker1, topic):
    """
    Genera la conexion para que el cliente pueda ver todos los mensajes en el topic
    
    Parameters:
        broker1 (str) : Broker del que desea ver los mensajes
        topic (str) : Topic del que desea ver los mensajes
    Returns:
        result (): Mensajes en el topic en la consola 
    
    """
    # Se crea la conexion al broker como consumer
    c = KafkaConsumer(topic, bootstrap_servers=broker1)

    # Se muestran los mensajes anteriores
    past_messages = MongoDB().get_past_logs(topic)
    for message in past_messages:
        print(message["author"]+ " : "+ message["message"])

    while True:
        try:
            for msg in c: # Si hay mensajes
                value = msg[6].decode() # Se decodifica la informacion
                print(value)

        # Si el cliente presiona [Ctrl + c]
        except KeyboardInterrupt:
            c.close() # Se cierra la conexion con el broker
            break