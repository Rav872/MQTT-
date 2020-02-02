#! /usr/bin/python3

import os                             # to execute the system call
from tkinter import *                 # it's a packkage for GUI
import paho.mqtt.client as mqtt       # package for mqtt
from threading import Thread          # for multiple threading
import time


UPSTREAM_TOPIC="test/upstream"        # which subscriber will subscibe
DOWNSTREAM_TOPIC="test/downstream"    # which publisher will subscribe
QOS=0                                 # flag 
KEEPALIVE=60                          
BROKER="127.0.0.1"                    # mosquitto -p 8008 because we are using in local host
PORT=8008

Name = input("Enter Your Name: ")

window = Tk()                       # all three window are used to make GUI window
window.geometry('400x300')
window.title("%s's Chat" % Name)

lbl = Label(window, text = "WELCOME TO MY APP")
#lbl.grid(column=0, row=0)
lbl.pack(side=TOP, fill=X)

messages_frame = Frame(window)
messages_frame.pack(side=TOP, fill=X)

scrollbar = Scrollbar(window)  # To navigate through past messages.

def select_text_or_copy_text(e):
	e.widget.delete(0, 'end')

def send(event):
	payload= Name + ": " + my_msg.get()	
	time.sleep(0.5)
	client.publish(UPSTREAM_TOPIC, payload, qos=QOS, retain=False)
	msg_list.insert(END, payload)

# To Read Msg in Text Form
my_msg=StringVar()
my_msg.set("Type your message here")

btn_fr = Frame(window)
btn_fr.pack(side=TOP, fill=X)

btn = Button(btn_fr, text="send", fg="green", bg="black", width=5)
btn.bind('<Button-1>', send)
btn.pack(anchor=NE, padx=5)

msg_list = Listbox(window, height=10, width=40, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(anchor=CENTER, fill=Y, expand=True)


lbl1 = Label(messages_frame, text="Message Box", width=11)
lbl1.pack(side=LEFT, padx=0, pady=0)

entry_field = Entry(messages_frame, textvariable=my_msg, width=25)
entry_field.bind("<Return>", send)
entry_field.bind('<Delete>', select_text_or_copy_text)
entry_field.focus()
entry_field.pack(side=TOP, padx=5, fill=X, expand=True)

def on_connect(client, userdata, flags, rc):
	msg_list.insert(END, "%s : Connected Successfully" % Name)
	client.subscribe(DOWNSTREAM_TOPIC)

def on_disconnect(client, userdata, rc):
	msg_list.insert(END, "%s : Disconnected from Chat" % Name)

def on_subscribe(client, userdata, mid, granted_qos): 
	print("Successfully subscribed Userdata: %s : granted_qos: %s" % (str(userdata), str(granted_qos)))

def on_publish(client, userdata, mid):
	print("Successfully published Message %s: mid: %s" % (str(userdata), str(mid)))

def on_message(client, userdata, msg):
	msg.payload = msg.payload.decode("utf-8")
	msg_list.insert(END, msg.payload)
	print("Got Message: Topic: %s Msg: %s" % (str(msg.topic),str(msg.payload)))

def close_window():
	client.disconnect()
	window.quit()        # inbuild function

def handle_reply():
	client.loop_forever()
	

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.connect(BROKER, PORT, KEEPALIVE)   # this is an inbuild function

window.protocol("WM_DELETE_WINDOW", close_window)

receive_thread = Thread(target=handle_reply)   # it is used for forever looping 
receive_thread.start()       # variable to start the thread

window.mainloop()


#window.after(1000, connect_user)

#while True:
#	window.update_idletasks()
#	window.update()

