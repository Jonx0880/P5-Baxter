#!/usr/bin/env python

import SocketServer

import rospy
import sys
sys.path.append('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter')

import vision

try:
	print'trying'
	rospy.init_node('action_client')
except rospy.ROSInterruptException as e:
	print 'something went wrong with: ', e 
	print'except'

import Phone

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.
 
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
 
    def handle(self):
	print'handle'
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
	vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/face.png')
	Phone.helloBaxter(self.data)
	
        # just send back the same data, but upper-cased
        self.request.sendall(self.data)
 
if __name__ == "__main__":
    HOST, PORT = "172.20.66.32", 50007
    
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
 
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
server.serve_forever()