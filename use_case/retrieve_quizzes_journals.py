# Description: retrieve every single journal and quiz in database. combines other functions:
# first uses retrieve journal and quiz list for id list, then individually retrieves each via id.
# Created by Emilia on 2026-01-31
from . import retrieve_journal_list
from . import retrieve_quiz_list

def retrieve_all_quizzes_and_journals():
    journal_list = retrieve_journal_list.retrieve_journal_list()
    quiz_list = retrieve_quiz_list.retrieve_quiz_list()
