import os
import shlex
import subprocess

from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.utils import autoreload
from loguru import logger

from server.settings import config


class Command(BaseCommand):
    help = "Run celery components"

    work_dir = os.getcwd()
    conda_env_name = None
    conda_activate_command = None
    conda_deactivate_command = None

    options = None

    beat_thread = None
    worker_thread = None
    flower_thread = None

    def __init__(
        self, stdout=None, stderr=None, no_color=False, force_color=False
    ):
        super().__init__(stdout, stderr, no_color, force_color)

    def add_arguments(self, parser):
        parser.add_argument(
            "--beat",
            action="store_true",
            dest="beat_enabled",
            default=False,
            help="Enable celery beat",
        )

        parser.add_argument(
            "--worker",
            action="store_true",
            dest="worker_enabled",
            default=False,
            help="Enable celery worker",
        )

        parser.add_argument(
            "--flower",
            action="store_true",
            dest="flower_enabled",
            default=False,
            help="Enable celery flower",
        )

        parser.add_argument(
            "--loglevel",
            action="store",
            dest="loglevel",
            default="INFO",
            help="Set celery log level",
        )

        parser.add_argument(
            "--broker",
            action="store",
            dest="broker",
            default=config("CELERY_BROKER_URL", None),
            help="Set celery broker",
        )

    def check_arguments(self, options):
        if (
            not options["beat_enabled"]
            and not options["worker_enabled"]
            and not options["flower_enabled"]
        ):
            raise CommandError(
                "You must enable at least one of the celery components: --beat, --worker, --flower"
            )

        if options["broker"] is None:
            raise CommandError(
                "You must set a broker for celery: --broker, or define "
                "CELERY_BROKER_URL in your .env file"
            )

        self.options = options

    def prepare_env(self):
        # detect conda
        self.conda_env_name = os.environ.get("CONDA_DEFAULT_ENV", None)
        if self.conda_env_name is not None:
            logger.info("Conda env name: {}", self.conda_env_name)
            self.conda_activate_command = (
                f"conda activate {self.conda_env_name}"
            )
            self.conda_deactivate_command = "conda deactivate"

    def run_command(self, command):
        if self.conda_env_name is not None:
            command = f"{self.conda_activate_command} && {command}"

        logger.debug("Running command: {}", command)

        return subprocess.Popen(
            shlex.split(command), shell=True, cwd=self.work_dir, env=os.environ
        )

    def run_celery_beat(self):
        logger.info("Running celery beat...")
        self.beat_thread = self.run_command(
            f'celery -A server -b {self.options["broker"]} beat -l {self.options["loglevel"]}'
        )

    def run_celery_worker(self):
        logger.info("Running celery worker...")
        self.worker_thread = self.run_command(
            f'celery -A server -b {self.options["broker"]} worker -l {self.options["loglevel"]} -P solo'
        )

    def run_celery_flower(self):
        logger.info("Running celery flower...")
        self.flower_thread = self.run_command(
            f'celery -A server -b {self.options["broker"]} flower -l {self.options["loglevel"]}'
        )

    def start(self):
        if self.options["beat_enabled"]:
            self.run_celery_beat()

        if self.options["worker_enabled"]:
            self.run_celery_worker()

        if self.options["flower_enabled"]:
            self.run_celery_flower()

    def stop(self):
        if self.beat_thread is not None:
            logger.info("Stopping celery beat...")
            self.beat_thread.send_signal(0)
            self.beat_thread.wait()
            self.beat_thread = None

        if self.worker_thread is not None:
            logger.info("Stopping celery worker...")
            self.worker_thread.send_signal(0)
            self.worker_thread.wait()
            self.worker_thread = None

        if self.flower_thread is not None:
            logger.info("Stopping celery flower...")
            self.flower_thread.send_signal(0)
            self.flower_thread.wait()
            self.flower_thread = None

        if os.name == "nt":
            os.system("taskkill /im celery.exe /f")
        else:
            os.system("pkill celery")

    def run(self):
        self.stop()
        self.start()
        while True:
            if self.beat_thread is not None:
                self.beat_thread.wait()

            if self.worker_thread is not None:
                self.worker_thread.wait()

            if self.flower_thread is not None:
                self.flower_thread.wait()
            self.start()

    @staticmethod
    def tasks_watchdog(sender, **kwargs):
        sender.watch_dir(settings.BASE_DIR, "**/*tasks.py")

    def handle(self, *args, **options):
        self.check_arguments(options)
        self.prepare_env()

        autoreload.autoreload_started.connect(self.tasks_watchdog)
        autoreload.run_with_reloader(self.run)
