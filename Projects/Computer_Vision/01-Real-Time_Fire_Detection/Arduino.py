import serial

class ArduinoController:
    def __init__(self, port='COM3', baud_rate=9600):
        """Initialize the Arduino controller with COM port and baud rate."""
        self.port = port
        self.baud_rate = baud_rate
        self.connection = self.connect()

    def connect(self):
        """Establish a connection to the Arduino."""
        try:
            return serial.Serial(self.port, self.baud_rate, timeout=1)
        except serial.SerialException as e:
            print(f"Error connecting to Arduino: {e}")
            return None

    def send_data(self, data):
        """Send data to the Arduino."""
        if self.connection:
            try:
                self.connection.write((data + '\n').encode())
                print(f"Sent: {data}")
            except Exception as e:
                print(f"Error sending data: {e}")

    def receive_data(self):
        """Receive data from the Arduino."""
        if self.connection:
            try:
                if self.connection.in_waiting > 0:
                    return self.connection.readline().decode().strip()
            except Exception as e:
                print(f"Error receiving data: {e}")
        return None

    def close(self):
        """Close the connection to the Arduino."""
        if self.connection:
            self.connection.close()
            print("Connection closed.")