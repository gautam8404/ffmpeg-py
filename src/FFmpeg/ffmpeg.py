from .ffmpegCommandBuilder import FFmpegCommandBuilder
import subprocess
from time import sleep


class FFmpeg(FFmpegCommandBuilder):
    def __init__(self, ffmpegPath="ffmpeg"):
        super().__init__(ffmpegPath)

    def _streamOutput(self, process):
        go = process.poll() is None
        for line in process.stdout:
            print(line, end="", flush=True)
        return go

    def execute(self, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False):
        command = super().build()
        strCommand = " ".join(command)

        print("starting ffmpeg with command: " + strCommand)
        try:
            process = subprocess.Popen(command, stdout=stdout, stderr=stderr, universal_newlines=True, shell=shell)
            while self._streamOutput(process):
                sleep(0.1)
            stdout, stderr = process.communicate()

        except FileNotFoundError:
            raise FFmpegException("File not found")
        except subprocess.CalledProcessError as e:
            raise FFmpegException(e.stderr.decode("utf-8"))
        except Exception as e:
            raise FFmpegException(e)

        if stderr:
            raise FFmpegException(stderr)
        return process.returncode, stdout, stderr


class FFmpegException(Exception):
    pass
