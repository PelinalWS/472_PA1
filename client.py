import socket

HOST = "localhost"
PORT = 8888


def main():
    #Connect to the server, receive the city information
    #prompt the user for a temperature prediction and send it to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8888))

    message = client.recv(1024).decode()
    print(message)

    while True:
        guess = input("Enter your guess (or type 'END' to quit): ")
        client.sendall(guess.encode())
        if guess.upper() == "END":
            break
        response = client.recv(1024).decode()

        responses = {
            "Correct!": lambda: print("Congratulations! You guessed the correct temperature."),
            "Lower": lambda: print("Try a lower temperature"),
            "Higher": lambda: print("Try a higher temperature"),
            "Invalid input.": lambda: print("Invalid input. Please enter a number."),
        }

        if response.startswith("Temperature was"):
            print(response)
            break
        elif response == "Connection closed":
            print("Connection closed")
            break
        elif response in responses:
            responses[response]()
            if response == "Correct!":
                break
    client.close()

if __name__ == '__main__':
    main()

