import socket

def main():
    #Connect to the server, receive the city information
    #prompt the user for a temperature prediction and send it to the server
    # Establish the client and connect it to the server by the same host and port
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8888))
    # The client halts until receiving a message, which is the city name with the question that is sent when a client connects
    message = client.recv(1024).decode()
    # The client console shows the message
    print(message)
    # The while loop allows for the client to guess until the server ends the connection or the client types "END"
    while True:
        guess = input("Enter your guess (or type 'END' to quit): ")
        # The guess is sent to the server
        client.send(guess.encode())
        # The "END" command is case insensitive, the while loop is broken if TRUE and the client is closed after the loop
        if guess.upper() == "END":
            break
        # The client listens for the server's response to its guess
        response = client.recv(1024).decode()
        # The list of responses without variations were put in a list of lambda functions to lessen the conditionals
        responses = {
            "Exactly correct!": lambda: print("Congratulations! You guessed the correct temperature."),
            "Correct!": lambda: print("Congratulations! You guessed the correct temperature."),
            "Lower": lambda: print("Try a lower temperature"),
            "Higher": lambda: print("Try a higher temperature"),
            "Invalid input.": lambda: print("Invalid input. Please enter a number."),
        }
        # The reresponse is shown to the client, if the guess is successful or ends in a failure, the loop is broken
        if response.startswith("Temperature was"):
            print(response)
            break
        elif response in responses:
            responses[response]()
            if response == "Correct!":
                break
    # The client is closed after the loop is broken
    client.close()
# The running of this file calls the main method by the magic method
if __name__ == '__main__':
    main()

