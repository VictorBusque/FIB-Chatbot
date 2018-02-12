from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.channels.telegram import TelegramInput
from rasa_core.interpreter import RegexInterpreter
from rasa_core.interpreter import RasaNLUInterpreter

from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Interpreter

def run_fib_query(serve_forever=True):
    interpreter = RasaNLUInterpreter("./models/projects/default/default/model_20180201-142832")
    agent = Agent.load("models/dialogue",
                       interpreter=interpreter)

    if serve_forever:
        agent.handle_channel(TelegramInput())
    return agent


if __name__ == '__main__':
    #utils.configure_colored_logging(loglevel="INFO")
    run_fib_query()
