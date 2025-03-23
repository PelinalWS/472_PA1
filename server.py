import socket
import random
import pandas as pd

def handle_request(connection, address, real_temp):
    #This method should process the client's guess
    #and respond with the appropriate message based on the guess accuracy
    attempts = 0
    while attempts < 3:
        guess = connection.recv(1024).decode()
        if guess.upper() == "END":
            connection.send("Server shutting down.".encode())
            connection.close()
            return "TERMINATE"  # Signal to terminate the server
        try:
            guess = float(guess)
            ten_percent = real_temp * 0.1
            five_percent = real_temp * 0.05

            if abs(guess - real_temp) <= five_percent:
                connection.send("Correct!".encode())
                connection.close()
                break
            elif abs(guess - real_temp) <= ten_percent:
                connection.send("Correct!".encode())
                connection.close()
                break
            attempts += 1
            if attempts >= 3:
                message = f"Temperature was {real_temp}"
                connection.send(message.encode())
                break
            hint = ""
            if guess > real_temp:
                hint = "Lower"
            else:
                hint = "Higher"
            connection.send(hint.encode())

        except ValueError:
            connection.send("Invalid input.".encode())

    connection.close()
    print(f"Connection from {address} closed\n")

def serve_forever():
    #In this method, load the weather data, randomly select a city,
    #and wait for the client to guess the temperature of the chosen city
    
    weather_data = pd.read_excel("./weathers.xlsx")
    cities = weather_data.City.tolist()
    temperatures = weather_data.Temp.tolist()

    HOST = "localhost" #'127.0.0.1'
    PORT = 8888

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"Server listening on HOST: {HOST}, PORT: {PORT}")
    while True:
        connection, address = server.accept()
        print(f"Connection from {address} established\n")
        
        #Randomly select a city and its temperature
        city = random.choice(cities)
        real_temp = temperatures[cities.index(city)]
                
        #Send city name to the client
        connection.send(f"Predict the temperature in {city}:".encode())
        
        result = handle_request(connection, address, real_temp)
        
        if result == "TERMINATE":
            break  # Exit the loop to terminate the server
    server.close()  # Close the server socket

if __name__ == '__main__':
    serve_forever()
