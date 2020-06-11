from umqtt.simple import MQTTClient
import time, network
from machine import Pin

aws_endpoint = 'a24e0i570zhegg.iot.us-east-2.amazonaws.com'

ssl_params = {'keyfile': "/flash/cert/aws.key",
              'certfile': "/flash/cert/aws.crt",
              'ca_certs': "/flash/cert/aws.ca"}
msgs_received = 0
conn = network.Cellular()

dio10 = Pin("P0", Pin.OUT, value=0)

while not conn.isconnected():
    print("waiting for network connection...")
    time.sleep(4)
print("network connected")

def sub_cb(topic, msg):
    global msgs_received
    msgs_received += 1
    print(topic, msg)
    dio10.toggle()

def publish_test(client_id="clientId", ssl_p=ssl_params):
    # "clientId" should be unique for each device connected
    c = MQTTClient(client_id, aws_endpoint, ssl=True, ssl_params=ssl_p)
    print("connecting...")
    c.connect()
    print("connected")
    c.set_callback(sub_cb)
    c.subscribe("sample/xbee")
    # topic: "sample/xbee"
    # message: {message: AWS Samples are cool!}
    print("publishing message...")
    c.publish("sample/xbee", '{"message": "Yay from Robert\'s Xbee"}')
    print("published")

    global msgs_received
    msgs_received = 0
    while msgs_received < 5:
        c.check_msg()
        time.sleep(5)

    time.sleep(1)
    c.disconnect()
    print("DONE")

publish_test()
