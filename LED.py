class LED:

    STATE_ON  = "on"
    STATE_OFF = "off"

    COLOR_RED   = "red"
    COLOR_GREEN = "green"
    COLOR_BLUE  = "blue"

    def __init__(self):
        self._state = self.STATE_OFF
        self._color = self.COLOR_BLUE
        self._rate  = 0

    def get_state(self) -> str:
        return self._state

    def set_state(self, new_state) -> bool:
        if new_state in (self.STATE_OFF, self.STATE_ON):
            self._state = new_state
            return True
        else:
            return False

    def get_color(self) -> str:
        return self._color

    def set_color(self, color: str) -> bool:
        if color.lower() in (self.COLOR_RED, self.COLOR_GREEN, self.COLOR_BLUE):
            self._color = color.lower()
            return True
        else:
            return False

    def get_rate(self) -> int:
        return self._rate

    def set_rate(self, new_rate: int) -> bool:
        if 0 <= new_rate <= 5:
            self._rate = int(new_rate)
            return True
        else:
            return False
