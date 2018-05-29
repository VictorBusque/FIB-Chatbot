## Generated Story teacher mail 1
* ask_teacher_mail{"teacher_name": "Javier bejar"}
  - Action_show_teacher_mail
  - Action_slot_reset

## Generated Story teacher mail 2
* ask_teacher_mail{"teacher_name": "joan climent"}
  - Action_show_teacher_mail
  - Action_slot_reset

## Generated Story teacher mail 3
* ask_teacher_mail{"teacher_name": "Javier vazquez"}
  - Action_show_teacher_mail
  - Action_slot_reset

## Generated Story teacher mail 4
* ask_teacher_mail{"teacher_name": "luis antonio belanche"}
  - Action_show_teacher_mail
  - Action_slot_reset

## Generated Story teacher mail 5
* ask_teacher_mail{"teacher_name": "carlos"}
   - Action_show_teacher_mail

## Generated Story teacher mail 6
* ask_teacher_mail{"teacher_name": "jordi turmo"}
   - slot{"teacher_name": "jordi turmo"}
   - Action_show_teacher_mail
   - Action_slot_reset

## Generated Story teacher mail 7
* ask_teacher_mail{"teacher_name": "roberto niehhuehuis"}
   - slot{"teacher_name": "roberto niehhuehuis"}
   - Action_show_teacher_mail
   - Action_slot_reset



## Generated Story subject schedule 1
* ask_subject_schedule{"subject_acronym": "APA"}
    - Action_show_subject_schedule
    - Action_slot_reset

## Generated Story subject schedule 2
* ask_subject_schedule{"subject_acronym": "apc"}
  - Action_show_subject_schedule
  - Action_slot_reset

## Generated Story subject schedule 3
* ask_subject_schedule{"subject_acronym": "wse"}
  - Action_show_subject_schedule
  - Action_slot_reset

## Generated Story subject schedule 4
* ask_subject_schedule{"subject_acronym": "IES"}
  - Action_show_subject_schedule
  - Action_slot_reset

## Generated Story subject schedule 5
* ask_subject_schedule{"subject_acronym": "asw"}
  - Action_show_subject_schedule
  - Action_slot_reset



## Generated Story subject classroom 1
* ask_subject_classroom{"subject_acronym": "APA"}
  - Action_show_subject_classroom
  - Action_slot_reset

## Generated Story subject classroom 2
* ask_subject_classroom{"subject_acronym": "apc"}
  - Action_show_subject_classroom
  - Action_slot_reset

## Generated Story subject classroom 3
* ask_subject_classroom{"subject_acronym": "wse"}
  - Action_show_subject_classroom
  - Action_slot_reset

## Generated Story subject classroom 4
* ask_subject_classroom{"subject_acronym": "IES"}
  - Action_show_subject_classroom
  - Action_slot_reset

## Generated Story subject classroom 5
* ask_subject_classroom{"subject_acronym": "asw"}
  - Action_show_subject_classroom
  - Action_slot_reset



## Generated Story teacher office 1
* ask_teacher_office{"teacher_name": "Jesus Alonso"}
   - Action_show_teacher_office
   - Action_slot_reset

## Generated Story teacher office 2
* ask_teacher_office{"teacher_name": "maria carme"}
    - Action_show_teacher_office
    - Action_slot_reset

## Generated Story teacher office 2
* ask_teacher_office{"teacher_name": "alvarez"}
    - Action_show_teacher_office
    - Action_slot_reset

## Generated Story teacher office 4
* ask_teacher_office{"teacher_name": "josep carmona"}
- Action_show_teacher_office
- Action_slot_reset

## Generated Story teacher office 5
* ask_teacher_office{"teacher_name": "nieuhenwuis"}
    - Action_show_teacher_office
    - Action_slot_reset



## Generated Story free spots 1
* ask_free_spots{"subject_acronym": "M2"}
   - Action_show_subject_free_spots
   - Action_slot_reset

## Generated Story free spots 2
* ask_free_spots{"subject_acronym": "XC"}
   - Action_show_subject_free_spots
   - Action_slot_reset

## Generated Story free spots 3
* ask_free_spots{"subject_acronym": "ac"}
   - Action_show_subject_free_spots
   - Action_slot_reset

## Generated Story free spots  4
* ask_free_spots{"subject_acronym": "vc"}
   - slot{"subject_acronym": "vc"}
   - Action_show_subject_free_spots
   - Action_slot_reset

## Generated Story free spots  5
* ask_free_spots{"subject_acronym": "VJ"}
  - slot{"subject_acronym": "VJ"}
  - Action_show_subject_free_spots
  - Action_slot_reset



## Generated Story free spots group 1
* ask_free_spots{"subject_acronym": "VJ", "group": "22"}
   - Action_show_subject_free_spots
   - Action_slot_reset

## Generated Story free spots group 2
* ask_free_spots{"subject_acronym": "IA", "group": "14"}
   - Action_show_subject_free_spots
   - Action_slot_reset

## Generated Story free spots group 3
* ask_free_spots{"subject_acronym": "pro1", "group": "12"}
   - Action_show_subject_free_spots
   - Action_slot_reset

## Generated Story free spots group  4
* ask_free_spots{"subject_acronym": "eda", "group": "33"}
   - Action_show_subject_free_spots
   - Action_slot_reset

## Generated Story free spots group  5
* ask_free_spots{"subject_acronym": "pes", "group": "41"}
  - Action_show_subject_free_spots
  - Action_slot_reset



## Generated Story subject teacher mail 1
* ask_subject_teacher_mail{"subject_acronym": "prop"}
    - slot{"subject_acronym": "prop"}
    - Action_show_subject_teachers_mails
    - slot{"matches": true}
* inform{"teacher_name": "javier bejar"}
    - Action_show_teacher_mail
    - Action_slot_reset

## Generated Story subject teacher mail 2
* ask_subject_teacher_mail{"subject_acronym": "ac"}
    - slot{"subject_acronym": "ac"}
    - Action_show_subject_teachers_mails
    - Action_slot_reset

## Generated Story subject teacher mail 2
* ask_subject_teacher_mail{"subject_acronym": "prop"}
    - slot{"subject_acronym": "prop"}
    - Action_show_subject_teachers_mails
    - slot{"matches": true}
* inform{"teacher_name": "jordi delgado"}
    - Action_show_teacher_mail
    - Action_slot_reset

## Generated Story subject teacher mail 4
* ask_subject_teacher_mail{"subject_acronym": "IES"}
    - slot{"subject_acronym": "IES"}
    - Action_show_subject_teachers_mails
    - Action_slot_reset

## Generated Story subject teacher name 5
* ask_subject_teacher_mail{"subject_acronym": "LP"}
    - slot{"subject_acronym": "LP"}
    - Action_show_subject_teachers_mails
    - Action_slot_reset



## Generated Story subject teacher office 1
* ask_subject_teacher_office{"subject_acronym": "pro1"}
    - slot{"subject_acronym": "pro1"}
    - Action_show_subject_teachers_offices
    - Action_slot_reset

## Generated Story subject teacher office 2
* ask_subject_teacher_office{"subject_acronym": "prop"}
    - slot{"subject_acronym": "prop"}
    - Action_show_subject_teachers_offices
    - slot{"matches": true}
* inform{"teacher_name": "jordi delgado"}
    - Action_show_teacher_office
    - Action_slot_reset

## Generated Story subject teacher office 3
* ask_subject_teacher_office{"subject_acronym": "asw"}
  - slot{"subject_acronym": "asw"}
  - Action_show_subject_teachers_offices
  - Action_slot_reset

## Generated Story subject teacher office 4
* ask_subject_teacher_office{"subject_acronym": "pro1"}
    - slot{"subject_acronym": "pro1"}
    - Action_show_subject_teachers_offices
    - slot{"matches": true}
* inform{"teacher_name": "josep carmona"}
    - Action_show_teacher_office
    - Action_slot_reset

## Generated Story subject teacher office 5
* ask_subject_teacher_office{"subject_acronym": "IA"}
    - slot{"subject_acronym": "IA"}
    - Action_show_subject_teachers_offices
    - Action_slot_reset



## Generated Story subject teacher name 1
* ask_subject_teacher_name{"subject_acronym": "asw"}
    - slot{"subject_acronym": "prop"}
    - Action_show_subject_teachers_names
    - Action_slot_reset

## Generated Story subject teacher name 2
* ask_subject_teacher_name{"subject_acronym": "AC"}
    - slot{"subject_acronym": "ac"}
    - Action_show_subject_teachers_names
    - Action_slot_reset

## Generated Story subject teacher name 3
* ask_subject_teacher_name{"subject_acronym": "IM"}
    - slot{"subject_acronym": "prop"}
    - Action_show_subject_teachers_names
    - Action_slot_reset

## Generated Story subject teacher name 4
* ask_subject_teacher_name{"subject_acronym": "as"}
    - slot{"subject_acronym": "ac"}
    - Action_show_subject_teachers_names
    - Action_slot_reset

## Generated Story subject teacher name 5
* ask_subject_teacher_name{"subject_acronym": "tc"}
    - slot{"subject_acronym": "prop"}
    - Action_show_subject_teachers_names
    - Action_slot_reset


## Generated Story next class 1
* ask_next_class
    - Action_show_next_class

## Generated Story next class 2
* ask_next_class
    - Action_show_next_class

## Generated Story next class 3
* ask_next_class
    - Action_show_next_class



## Generated Story exams 1
* ask_exams
    - Action_show_next_exams

## Generated Story exams 2
* ask_exams
    - Action_show_next_exams

## Generated Story exams 3
* ask_exams
    - Action_show_next_exams



## Generated Story exams subj 1
* ask_exams{"subject_acronym": "m1"}
    - Action_show_next_exams
    - Action_slot_reset

## Generated Story exams subj 2
* ask_exams{"subject_acronym": "as"}
    - Action_show_next_exams
    - Action_slot_reset

## Generated Story exams subj 3
* ask_exams{"subject_acronym": "pes"}
    - Action_show_next_exams
    - Action_slot_reset



## Generated Story pracs 1
* ask_pracs
    - Action_show_next_pracs

## Generated Story pracs 2
* ask_pracs
    - Action_show_next_pracs

## Generated Story pracs 3
* ask_pracs
    - Action_show_next_pracs


## Generated Story pracs subj 1
* ask_pracs{"subject_acronym": "m2"}
    - Action_show_next_pracs
    - Action_slot_reset

## Generated Story pracs subj 2
* ask_pracs{"subject_acronym": "pds"}
    - Action_show_next_pracs
    - Action_slot_reset

## Generated Story pracs subj 3
* ask_pracs{"subject_acronym": "fdm"}
    - Action_show_next_pracs
    - Action_slot_reset
