import socket
import threading

from LED import LED
from settings import *
import led_commands

led_thing: LED

UTF_8 = "utf-8"

STATUS_OK = "OK"
STATUS_FAILED = "FAILED"


def create_led_thing() -> None:
    global led_thing
    led_thing = LED()


def _start_server():
    # create LED
    create_led_thing()

    print("Server start")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen(MAX_SERVER_CONNECTIONS)

    print(f"Listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        connection, client_addr = sock.accept()
        print(f"--Accepted connection from: {client_addr[0]}:{client_addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(connection, client_addr))
        client_handler.start()


def handle_client(connection, client_addr):
    try:
        request = connection.recv(RESV_SIZE)

        print(f"--from({client_addr[0]}:{client_addr[1]}): {request.decode(UTF_8)}")

        request_string: str = request.decode(UTF_8)
        c_result = command_executor(request_string, connection)

        connection.send(f"{c_result}\n".encode(UTF_8))

    finally:
        connection.close()


def command_executor(request_string: str, connection) -> str:

    if request_string.endswith("\n"):
        request_string = request_string[:-1]
    else:
        if len(request_string) == 0:
            pass
        else:
            # TODO: do something with this?
            print("Request not ends with '\\n'")
            return STATUS_FAILED

    request_split = request_string.split(" ")
    request_command = request_split[0]

    match request_command:
        case led_commands.SET_LED_STATE:
            if len(request_split) == 2:
                if led_thing.set_state(request_split[1]):
                    return STATUS_OK
                else:
                    return STATUS_FAILED
            else:
                print(f"Incorrect request: {request_string}")
                return STATUS_FAILED

        case led_commands.GET_LED_STATE:
            if len(request_split) == 1:
                return f"{STATUS_OK} {led_thing.get_state()}"
            else:
                print(f"Incorrect request: {request_string}\nMaybe you mean: {request_command}")
                return STATUS_FAILED

        case led_commands.SET_LED_COLOR:
            if len(request_split) == 2:
                if led_thing.set_color(request_split[1]):
                    return STATUS_OK
                else:
                    return STATUS_FAILED
            else:
                print(f"Incorrect request: {request_string}")
                return STATUS_FAILED

        case led_commands.GET_LED_COLOR:
            if len(request_split) == 1:
                return f"{STATUS_OK} {led_thing.get_color()}"
            else:
                print(f"Incorrect request: {request_string}\nMaybe you mean: {request_command}")
                return STATUS_FAILED

        case led_commands.SET_LED_RATE:
            if len(request_split) == 2:
                # TODO: обработка на отправку int
                if led_thing.set_rate(int(request_split[1])):
                    return STATUS_OK
                else:
                    return STATUS_FAILED
            else:
                print(f"Incorrect request: {request_string}")
                return STATUS_FAILED

        case led_commands.GET_LED_RATE:
            if len(request_split) == 1:
                return f"{STATUS_OK} {led_thing.get_rate()}"
            else:
                print(f"Incorrect request: {request_string}\nMaybe you mean: {request_command}")
                return STATUS_FAILED

        case led_commands.STOP_CONNECTION_COMMAND:
            print("Close connection")
            connection.close()
        case _:
            print(f"Undefined command: {request_command}\nFull request message: {request_string}")
            return STATUS_FAILED


if __name__ == '__main__':
    _start_server()
