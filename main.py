import time
from connection import connect
from machine import Pin

msgs_received = 0

dio10 = Pin("P0", Pin.OUT, value=0)

print("network connected")

client_id = "oasidfjoasidfjasdf"
c = connect(client_id)


def sub_cb(topic, msg):
    global msgs_received
    msgs_received += 1
    print(topic, msg)
    dio10.toggle()


def subscribe():
    c.set_callback(sub_cb)
    c.subscribe("sample/xbee")

    global msgs_received

    msgs_received = 0
    while msgs_received < 5:
        c.check_msg()
        time.sleep(5)
    time.sleep(1)
    c.disconnect()
    print("DONE")


def publish_test():
    c.publish("sample/xbee", '{"message": "Yay from Robert\'s Xbee"}')


publish_test()
subscribe()
