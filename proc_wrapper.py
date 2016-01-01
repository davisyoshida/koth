import asyncio


class IOProcess(object):
    """
    Simple wrapper for ease of interaction with program stdout and stdin

    Attributes:
        arglist: argv for the command (e.g. ['ls', '-l'])
        setup: Bytes to send to the process one time after it has been started
        timeout: Time, in seconds, to wait for responses from the process
    """

    def __init__(self, arglist, setup, timeout=10):
        self.arglist = arglist
        self.loop = asyncio.get_event_loop()
        self.setup = setup
        self.timeout = timeout

    @asyncio.coroutine
    def _start_co(self):
        create = asyncio.create_subprocess_exec(*self.arglist, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE)
        self.proc = yield from create
        for s in self.setup:
            self.proc.stdin.write(s)

    def start(self):
        self.loop.run_until_complete(self._start_co())

    @asyncio.coroutine
    def _send_co(self, bytes_in):
        print("Sending")
        self.proc.stdin.write(bytes_in)
        try:
            print("Getting stdout")
            res = yield from self.proc.stdout.readline()
        except asyncio.CancelledError:
            self.proc.kill()
            res = None

        return res

    @asyncio.coroutine
    def _timed_send(self, bytes_in):
        try:
            print("Waiting")
            result = yield from asyncio.wait_for(self._send_co(bytes_in), loop=self.loop, timeout=3)
        except asyncio.TimeoutError:
            result = None
            yield from self.proc.wait()

        return result

    def send(self, bytes_in):
        return self.loop.run_until_complete(self._timed_send(bytes_in))

    def end(self):
        if not self.proc.returncode:
            self.proc.kill()

    def send_str(self, s):
        """
        Send a string to the process via stdin, and wait <timeout> seconds for the response.
        Args:
            s: The string to send. It should have no newlines.

        Returns:
            The string that the process printed, or None if the time limit was exceeded.
        """
        ...
