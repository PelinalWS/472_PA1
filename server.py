import socket
import random
import pandas as pd

def handle_request(connection, address, real_temp):
    #This method should process the client's guess
    #and respond with the appropriate message based on the guess accuracy
    attempts = 0
    # The accepted margin of error is calculated to refrain from calculating them multiple times during the loop
    ten_percent = real_temp * 0.1
    # The attmepts count is initialized as 0 on every subsequent connection to a client
    # The while loop is used to limit the attempts to 3
    while attempts < 3:
        # The server receives the guess sent by the client
        guess = connection.recv(1024).decode()
        # If the client sends "END", which is case insensitive, the connection is severed and 
        # the handle request function will return "TERMINATE" which will terminate the server
        if guess.upper() == "END":
            connection.send("Server shutting down.".encode())
            connection.close()
            return "TERMINATE"  # Could also use a boolean value
        # The try catch block is in case the guess is not a number, which would cause an error trying to strip it as a float
        try:
            guess = float(guess)
            # If the guess is exactly correct, there is a special success message
            if abs(guess - real_temp) == 0:
                print(f"Client {address} guessed {guess}, which was the correct temperature.")
                connection.send("Exactly correct!".encode())
                break
            # If the guess is within the 10% tolerance range, the server sends a message of approval
            # The connection between server and client is severed and the while loop is broken
            elif abs(guess - real_temp) <= ten_percent:
                print(f"Client {address} guessed {guess}, which was accepted within the 10% tolerance range of {real_temp}.")
                connection.send("Correct!".encode())
                break
            # The attempts count is incremented before the hint is sent to the client
            attempts += 1
            # If the attempts reached 3, the real temperature is sent to the client
            if attempts >= 3:
                connection.send(f"Temperature was {real_temp}".encode())
                break
            # If the loop was not broken by now, the hint is sent to the client based on the guess being bigger or smaller than the real temperature
            hint = ""
            if guess > real_temp:
                hint = "Lower"
            else:
                hint = "Higher"
            connection.send(hint.encode())
        # The error is caught and handled, the loop asks for a new guess
        except ValueError:
            connection.send("Invalid input.".encode())
    # The connection is closed after the loop is broken
    connection.close()
    # Notification in the server that a connection was closed
    print(f"Connection from {address} closed\n")

def serve_forever():
    #In this method, load the weather data, randomly select a city,
    #and wait for the client to guess the temperature of the chosen city
    
    # The table is loaded, the rows are made into lists
    weather_data = pd.read_excel("./weathers.xlsx")
    cities = weather_data.City.tolist()
    temperatures = weather_data.Temp.tolist()
    # The server is initialized as localhost on port 8888 as specified on the requirements
    HOST = "localhost" #'127.0.0.1'
    PORT = 8888

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    # Affirmation that the server listening has commenced
    print(f"Server listening on HOST: {HOST}, PORT: {PORT}")
    # Since the function is supposed to "serve forever", the while loop runs indefinitely, accepting connections from clients
    while True:
        connection, address = server.accept()
        # Notification in the server that a connection with a client was established
        print(f"Connection from {address} established\n")
        
        # Randomly select a city and its temperature
        # Picks a random city for each connection by a client
        city = random.choice(cities)
        real_temp = temperatures[cities.index(city)]
                
        # Send the city name to the client, asking for a guess
        connection.send(f"Predict the temperature in {city}:".encode())
        # The guesses are handled in the handle_request function
        result = handle_request(connection, address, real_temp)
        
        if result == "TERMINATE":
            print(f"Client {address} requested to end the session.")
            break  # Exit the loop to terminate the server
    server.close()  # Close the server socket

# The running of the file calls the serve_forever function 
if __name__ == '__main__':
    serve_forever()




