## search_teacher_mail_complete
* ask_teacher_mail{"teacher_name": "Javier", "teacher_surname": "Bejar"}
  - action_show_teacher_mail

## search_teacher_mail_incomplete
* ask_teacher_mail{"teacher_surname": "Bejar"}
  - utter_ask_teacher_name
* inform{"teacher_name": "Javier"}
  - action_show_teacher_mail

## search_teacher_desk
* ask_teacher_desk{"teacher_name": "Javier", "teacher_surname": "Bejar"}
  - action_show_teacher_desk

## search_teacher_desk_incomplete
* ask_teacher_desk{"teacher_name": "Pere"}
  - utter_ask_teacher_surname
* inform{"teacher_name": "Barlet"}
  - action_show_teacher_desk

## search_free_spots_complete
* ask_free_spots{"subject_acronym": "CAIM"}
  - action_show_subject_free_spots

## search_free_spots_incomplete
* ask_free_spots
  - utter_ask_subject_acronym
* inform{"subject_acronym": "WSE"}
  - action_show_subject_free_spots

## search_subject_classroom_complet
* ask_subject_classroom{"subject_acronym": "APA"}
  - action_show_subject_classroom

## search_subject_schedule_complet
* ask_subject_schedule{"subject_acronym": "PAE"}
  - action_show_subject_schedule
