from threading import Thread
from time import sleep

import dns.resolver
from loguru import logger


class FindHostAsync(Thread):
    HOST = "baidu.com"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flag = True
        self.interval = 30

    def __enter__(self):
        self.daemon = True
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def run(self) -> None:
        """
        线程开始
        :return:
        """
        self.flag = True
        while self.flag:
            self.find_host()
            sleep(self.interval)

    def stop(self) -> None:
        """
        强制结束线程
        :return:
        """
        self.flag = False
        self.join()

    def find_host(self):
        from . import hosts

        new_hosts = []

        for host in dns.resolver.resolve(
            FindHostAsync.HOST, "A", raise_on_no_answer=False
        ):
            ip = host.address
            if self.check_health(ip):
                new_hosts.append(ip)
            else:
                logger.warning(f"Host {ip} is not healthy")

        hosts.set_hosts(new_hosts)
        logger.info(f"Found hosts: {new_hosts}")

    def check_health(self, ip: str) -> bool:
        return True
