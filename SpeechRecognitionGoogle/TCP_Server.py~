#!/usr/bin/env python

import SocketServer
import rospy
rospy.init_node('tcp_server')
import Phone



class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.
 
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    print '2'
    def handle(self):
        # self.request is the TCP socket connected to the client
	print'3'
        self.data = self.request.recv(1024).strip()
	print'4'
        print "{} wrote:".format(self.client_address[0])
        print self.data
	Phone.helloBaxter(self.data)
	print'5'
        # just send back the same data, but upper-cased
        self.request.sendall(self.data)
 
if __name__ == "__main__":
    HOST, PORT = "172.20.66.58", 50007
    print'1'
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
 
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C

    server.serve_forever()
