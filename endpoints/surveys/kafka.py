from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import time
from db_mongo import MongoDB
import os


KAFKA1 = os.getenv('KAFKA_BROKER1')

class kafka:
    def __init__(self):
        self.host_port = KAFKA1
        self.producer = KafkaProducer(bootstrap_servers=KAFKA1)

    def connect_user(self, user, id_survey):
        """
        Registra la conexion de un usuario al modo edicion de un survey en kafka

        Parameters:
            client_name (str) : El nombre del cliente que esta enviando el mensaje
            broker1 (str) : Al broker que lo esta enviando
            id_survey (str) : El id_survey al que se esta conectando
        Returns:
            result (): Datos registrados en el topic y la base de datos 
        
        """
        msg = user + " se ha conectado"
        self.producer.send(topic=str(id_survey), value=msg.encode(encoding='utf8'))
        

    def disconnect_user(self, user, id_survey):
        """
        Registra la conexion de un usuario al modo edicion de un survey en kafka

        Parameters:
            user (str) : El nombre del cliente que esta enviando el mensaje
            broker1 (str) : Al broker que lo esta enviando
            id_survey (str) : El id_survey al que se esta conectando
        Returns:
            result (): Datos registrados en el topic y la base de datos 
        
        """
        msg = user + " se ha desconectado"
        self.producer.send(topic=str(id_survey), value=msg.encode(encoding='utf8'))


    def stop_edition(self, id_survey):
        """
        Envia el mensaje que se el modo edicion del survey a parado

        Parameters:
            broker1 (str) : Al broker que lo esta enviando
            id_survey (str) : El id_survey que estaria parando
        Returns:
            result (): Datos registrados en el topic y la base de datos 
        
        """
        msg = "El modo edicion edicion del survey ha terminado, ningun usuario podra editar el survey"
        self.producer.send(topic=str(id_survey), value=msg.encode(encoding='utf8'))


    def update_question(self, user, id_survey, id_question, before, after):
        """
        Envia el mensaje que un usuario ha realizado un cambio en una pregunta en el survey

        Parameters:
            user (str) : El nombre del cliente que esta enviando el cambio
            broker1 (str) : Al broker que lo esta enviando
            id_survey (str) : El id_survey que estaria parando
        Returns:
            result (): Datos registrados en el topic y la base de datos 
        
        """
        msg = f"El usuario { user } ha realizado el cambio en la pregunta { id_question }\n{str(before)}\n{str(after)}"
    
        
        self.producer.send(topic=str(id_survey), value=msg.encode(encoding='utf8'))



    def get_notifications(self, id_survey):
        consumer = KafkaConsumer(bootstrap_servers=self.host_port, group_id='0')
        notifications = []
        topic_partition = TopicPartition(str(id_survey), 0)
        
        # El tiempo hace 30 segundos
        timestamp = int(time.time() * 1000) - 30000
        offsets = consumer.offsets_for_times({topic_partition: timestamp})
        last_notification = 0
        # Si hay offsets de hace 30 segundos
        if offsets[topic_partition] is not None:
            consumer.assign([topic_partition])
            consumer.seek_to_end(topic_partition)
            # El offset de la ultima notificacion que llego en los 30 segundos
            last_notification = consumer.position(topic_partition) - 1
            consumer.seek(topic_partition, offsets[topic_partition].offset)
            for notification in consumer:
                notifications.append(notification.value.decode())
                if(notification.offset == last_notification):
                    break
        else:
            notifications.append('No notifications in the last 30 seconds')
        return notifications



