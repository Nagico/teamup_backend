import random


class Hosts:
    def __init__(self):
        self._hosts = []

    def get_hosts(self) -> list:
        return self._hosts

    def set_hosts(self, hosts: list) -> None:
        self._hosts = hosts

    def get_random_host(self) -> str | None:
        if len(self._hosts) == 0:
            return None
        return random.choice(self._hosts)

    def get_random_host_except(self, host: str) -> str | None:
        if len(self._hosts) == 0:
            return None
        if len(self._hosts) == 1:
            return self._hosts[0]
        return random.choice([h for h in self._hosts if h != host])


hosts = Hosts()
