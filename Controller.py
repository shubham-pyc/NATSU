#imports
import bluetooth
'''--------------------------------------------X--------------------------------------------'''
class Controller:
    def __init__(self):
        # hardware address of HC-05 bluetooth module used in arduino
        self.address = "20:15:03:31:69:41"
        self.send = None
        # flag bit which specifies if the communication is established
        self.connected = True
        # protocol used RFCOMM
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        try:
            self.socket.connect((self.address,1))
        except:
            #if any exception occurred set the connection flag bit to false
            self.connected = False

    #method to find the available devices
    def search(self):
        nearby = bluetooth.discover_devices()
        if len(nearby) ==0:
            print('no devices found')
        else:
            for temp in nearby:
                if temp == self.address:
                    self.connected  = True
                else:
                    print 'the bot not found'
    #method to send the signal to the robot to turn left
    def turnLeft(self):
        if self.connected ==True:
            self.socket.send('3')
    # method to send the signal to the robot to turn right
    def turnRight(self):
        if self.connected == True:
            self.socket.send('4')

    # method to send the signal to the robot to go forward
    def forward(self):
        if self.connected == True:
            self.socket.send('1')

    # method to send the signal to the robot to go reverse
    def backward(self):
        if self.connected == True:
            self.socket.send('2')

    # method to send the signal to the robot to stop
    def stop(self):
        if self.connected == True:
            self.socket.send('0')




