from Fibot.chats import Chats
from Fibot.api.api_raco import API_raco
from Fibot.Data.data_types.exam import Exam_schedule
from Fibot.Data.data_types.practical_work import Practical_schedule
from pprint import pprint

c = Chats()
c.load()
a = API_raco()
a_t = c.get_chat('349611162')['access_token']
user_lang = c.get_chat('349611162')['language']
exams = list(a.get_exams_user(a_t))
e_e = Exam_schedule(exams, user_lang)

pprint(list(e_e.get_closest_exams(range = 50)))

pracs = list(a.get_practiques(a_t))
p_e = Practical_schedule(pracs, user_lang)

pprint(list(p_e.get_closest_pracs(range = 50)))
