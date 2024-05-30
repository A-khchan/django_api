import json 
from channels.generic.websocket import WebsocketConsumer 
from asgiref.sync import async_to_sync  
import uuid

class Counter(WebsocketConsumer): 

    def connect(self): 
        # global count
        print("Connect")

        self.accept()
        async_to_sync(self.channel_layer.group_add)("ride", self.channel_name)
        id = str(uuid.uuid4())

        # Convert dict to JSON before send.
        # This JSON is accessible by event.data on client onMessage method
        self.send(json.dumps({
            'message': 'assignId',
            'id': id
        }))
          
    def ride_message(self, event):
        # event is assumed to be a dict
        print("event: ", event)

        # Convert dict to JSON before send
        self.send(json.dumps(event['data']))

    def disconnect(self, close_code): 
        print("Disconnect")
        # pass dict to ride_message
        async_to_sync(self.channel_layer.group_send)("ride", {
            'type': 'ride.message',
            'data': {
                'message': 'leave'
            } 
        })
        async_to_sync(self.channel_layer.group_discard(
            "ride",
            self.channel_name
        ))
        self.close()    
  
    def receive(self, text_data): 
        # Client has to send str to this websocket server
        # print("consumers.py, receive is called, with text_data: ", text_data)
        
        # Convert JSON data to dict
        dictObj = json.loads(text_data)

        print("**** text_data is type of: ", type(text_data))
        print("**** text_data is: ", text_data)
        print("**** dictObj is type of: ", type(dictObj))
        print("**** dictObj is: ", dictObj)

        request = dictObj["request"]

        if (request == 'boardcast'):
            async_to_sync(self.channel_layer.group_send)("ride", {
                'type': 'ride.message',
                'data': dictObj
            })
