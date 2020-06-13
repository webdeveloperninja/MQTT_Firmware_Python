from umqtt.simple import MQTTClient
import time, network


def connect(client_id):
    conn = network.Cellular()

    aws_endpoint = 'a24e0i570zhegg.iot.us-east-2.amazonaws.com'

    ssl_params = {'keyfile': "/flash/cert/aws.key",
                  'certfile': "/flash/cert/aws.crt",
                  'ca_certs': "/flash/cert/aws.ca"}

    while not conn.isconnected():
        print("waiting for network connection...")
        time.sleep(4)

    c = MQTTClient(client_id, aws_endpoint, ssl=True, ssl_params=ssl_params)
    c.connect()
    return c
