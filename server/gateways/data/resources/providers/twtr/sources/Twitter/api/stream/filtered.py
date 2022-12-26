from multiprocessing import Process
import time
from lib.Twitter.api.endpoints.helpers.stream import read_filtered_stream
from lib.Twitter.api.stream.resources.controller import StreamController
from lib.Mongo.resources.utils import update_record
from server.lib.utils.logger import status_logger


# GAME PLAN
# finance 10 min
# cams 5-10 min
# events 10 min
# trending 5-10 min
# sports 5 min
# misc 5 min -- wordle, earthquake, severe events, random thread etc.
# earth 5 min
# stream stat report 5 min
# spaces 5 min


class FilteredStream:

    def __init__(self, database):
        # ################################################
        self.process = None
        self.stream_controller = StreamController(database)
        # ################################################
        self.run()

    def init_process(self):
        self.process = Process(
            target=read_filtered_stream,
            name="connection",
            args=(self.stream_controller.message_handler,),
        )

    def streaming(self):

        while True:

            if self.stream_controller.rules_set:
                status_logger(
                    inline=False, status_text="Rules set", green=True)
                self.process_manager(start=True)
                status_logger(
                    inline=False, status_text="STREAM STARTED", green=True)
                while self.stream_controller.up_to_date:
                    # status_logger(inline=False, status_text="streaming... \r", purple=True, inline=True)
                    self.stream_controller.monitor_global_conversation()
                else:
                    status_logger(
                        inline=False, status_text="STREAM OUT OF DATE", red=True)
                    self.stream_controller.rules_set = False
                    self.process_manager(stop=True)
                    status_logger(
                        inline=False, status_text="STREAM STOPPED", red=True)
                    time.sleep(5)
            else:
                status_logger(
                    inline=False, status_text="Finding active rules", purple=False)
                self.stream_controller.find_active_rules()

    def process_manager(self, start=False, stop=False):

        if start:
            status_logger(
                inline=False, status_text="INITIALIZING PROCESS", green=True)
            self.init_process()
            self.process.start()
            status_logger(
                inline=False, status_text="PROCESS STARTED", green=True)
            update_record(db=self.stream_controller.db,
                          table='StreamingRules', column="ResetState", data=False)
            self.stream_controller.running = True
            self.stream_controller.up_to_date = True

        if stop:
            self.process.terminate()
            status_logger(
                inline=False, status_text="PROCESS TERMINATED", green=True)
            self.stream_controller.running = False
            self.process = None

    def run(self):
        Process(target=self.streaming).start()
