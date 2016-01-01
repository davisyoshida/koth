import asyncio


class IOProcess(object):
    """
    Simple wrapper for ease of interaction with program stdout and stdin

    Attributes:
        arglist: argv for the command (e.g. ['ls', '-l'])
        loop: The event loop to use
        setup: Bytes to send to the process one time after it has been started
        timeout: Time, in seconds, to wait for responses from the process
    """

    def __init__(self, arglist, loop, setup, timeout=10):
        self.arglist = arglist
        self.loop = loop
        self.setup = setup
        self.timeout = timeout

    @asyncio.coroutine
    def start(self):
        create = asyncio.create_subprocess_exec(*self.arglist, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        self.proc = yield from create
        for s in self.setup:
            self.proc.stdin.write(s)

    @asyncio.coroutine
    def sender(self, bytes_in):
        self.proc.stdin.write(bytes_in)
        try:
            res = yield from self.proc.stdout.readline()
        except asyncio.CancelledError:
            self.proc.kill()
            res = None

        return res

    @asyncio.coroutine
    def send_receive(self, bytes_in):
        try:
            result = yield from asyncio.wait_for(self.sender(bytes_in), loop=self.loop, timeout=3)
        except asyncio.TimeoutError:
            result = None
            yield from self.proc.wait()

        return result

    def send_no_wait(self, bytes_in):
        self.proc.stdin.write(bytes_in)

    @asyncio.coroutine
    def end(self):
        try:
            self.proc.kill()
        except ProcessLookupError:
            pass
        yield from self.proc.wait()
