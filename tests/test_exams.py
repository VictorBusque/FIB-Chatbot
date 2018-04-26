from Fibot.chats import Chats
from Fibot.api.api_raco import API_raco
from Fibot.Data.data_types.exam import Exam_schedule
from pprint import pprint
c = Chats()
c.load()
a = API_raco()
a_t = c.get_chat('461088493')['access_token']
user_lang = c.get_chat('461088493')['language']
exams = list(a.get_exams_user(a_t))
e_e = Exam_schedule(exams, 'es')

pprint(list(e_e.get_closest_exams(range = 50)))
