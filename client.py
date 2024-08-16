import socket

import led_commands
from settings import *

UTF_8 = "utf-8"


def _start_client():
    print("Client start")
    _print_menu()

    while True:
        print("="*42)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((SERVER_IP, SERVER_PORT))
            print(f"Connected to:{SERVER_IP}: {SERVER_PORT}")
            menu_choice: int = _int_input("-->")

            match menu_choice:
                case 1:
                    _in = _int_input("set-led-state\n1:on 2:off\n-->")
                    if int(_in) in (1, 2):
                        _state = ("0", "on", "off")
                        client.sendall(f"{led_commands.SET_LED_STATE} {_state[_in]}\n".encode(UTF_8))
                    else:
                        print("Wrong value")
                        _print_menu()
                        continue

                case 2:
                    client.sendall(f"{led_commands.GET_LED_STATE}\n".encode(UTF_8))

                case 3:
                    _in = _int_input("set-led-color\n1:RED 2:GREEN 3:BLUE\n-->")
                    if int(_in) in (1, 2, 3):
                        _color = ("0", "RED", "GREEN", "BLUE")
                        client.sendall(f"{led_commands.SET_LED_COLOR} {_color[_in]}\n".encode(UTF_8))
                    else:
                        print("Wrong value")
                        _print_menu()
                        continue

                case 4:
                    client.sendall(f"{led_commands.GET_LED_COLOR}\n".encode(UTF_8))

                case 5:
                    _in = _int_input("set-led-rate 0..5\n-->")
                    if int(_in) in range(6):
                        client.sendall(f"{led_commands.SET_LED_RATE} {_in}\n".encode(UTF_8))
                    else:
                        print("Wrong value")
                        _print_menu()
                        continue

                case 6:
                    client.sendall(f"{led_commands.GET_LED_RATE}\n".encode(UTF_8))
                case 7:
                    _in = input("command-->")
                    if not _in.endswith("\n"):
                        _in = _in + "\n"
                    client.sendall(_in.encode(UTF_8))
                case 8:
                    break
                case _:
                    _print_menu()
                    continue

            response = client.recv(RESV_SIZE)
            print(f"[r]: {response.decode(UTF_8)}")
            client.close()


def _print_menu() -> None:
    print(f"""Requests-list:
    1: {led_commands.SET_LED_STATE} [on/off]
    2: {led_commands.GET_LED_STATE}
    3: {led_commands.SET_LED_COLOR} [red/green/blue]
    4: {led_commands.GET_LED_COLOR}
    5: {led_commands.SET_LED_RATE} [0..5]
    6: {led_commands.GET_LED_RATE}
    7: custom-command
    8: close-client
    """)


def _int_input(message: str) -> int:
    _input = input(message)
    try:
        return int(_input)
    except ValueError:
        print("Wrong value")
        return -1


if __name__ == '__main__':
    _start_client()
