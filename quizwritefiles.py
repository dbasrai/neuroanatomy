# quiz.py
# jfb 9-JAN-2023 Based on a Real Python tutorial at https://realpython.com/python-quiz-application/
#
import pathlib
import random
from string import ascii_lowercase
import time
import sys
import atexit # For the @atexit.register decorator. Does nothing unless you use 'exit'

# Put your question pool file name here
QFILENAME = "ALLPRACTICEMCQ.txt"

# Quiz and answer filenames here
OUTFN1 = 'tempQ.txt'
OUTFN2 = 'tempA.txt'


try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

OUTFN = input("Enter name, without extension, of output files: ") or "temp"
OUTFN1 = OUTFN+"Q.txt"
OUTFN2 = OUTFN+"A.txt"

f1 = open(OUTFN1, "w")
#f1.write(f"FILE: {OUTFN1}\n")
f2 = open(OUTFN2, "w")
#f2.write(f"FILE: {OUTFN2}\n")

QUESTIONS_PATH = pathlib.Path(__file__).parent / QFILENAME

# Put the number of questions for a quiz here
NUM_QUESTIONS_PER_QUIZ = 25
# Put the ID for your right answers here
CORRECTANSWERS = "rightanswer"
# Put the ID for your wrong answers here
WRONGANSWERS = "wronganswer"
# Put your introductory statement here
#INTRODUCTION = "Which lecture do you want to be quizzed about?"
INTRODUCTION = " "
lecturename = "1"

@atexit.register

def goodbye(): # For a message when exiting the program
    time.sleep(.1) # Give it time to print to shell window
    f1.close()
    f2.close()
    time.sleep(.1) # Give it time to print to shell window
    print("\nBye bye!")


def run_quiz():
    global lecturename
    questions = prepare_questions(
        QUESTIONS_PATH, num_questions=NUM_QUESTIONS_PER_QUIZ
    )

    num_correct = 0
    for num, question in enumerate(questions, start=1):
        if question !=INTRODUCTION:
            print(f"\n\nLecture {lecturename}\nQuestion {num}:")
            f1.write(f"\n\nLecture {lecturename}\nQuestion {num}: ")
            f2.write(f"\n\nLecture {lecturename}\nQuestion {num}: ")
        num_correct += ask_question(question)

#    print(f"\nYou got {num_correct} correct out of {NUM_QUESTIONS_PER_QUIZ} questions")
    f1.close()
    f2.close()
    sys.exit()

def prepare_questions(path, num_questions):
    topic_info = tomllib.loads(path.read_text())
    topics = {
        topic["label"]: topic["questions"] for topic in topic_info.values()
    }
    topic_label = get_answers(
        question=INTRODUCTION,
        alternatives=sorted(topics),
    )[0]

    questions = topics[topic_label]
    num_questions = min(num_questions, len(questions))
    return random.sample(questions, k=num_questions)


def ask_question(question):
    correct_answers = question[CORRECTANSWERS]
    alternatives = question[CORRECTANSWERS] + question[WRONGANSWERS]
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))

    answers = get_answers(
        question=question["question"],
        alternatives=ordered_alternatives,
        num_choices=len(correct_answers),
        hint=question.get("hint"),
    )
    if correct := (set(answers) == set(correct_answers)):
#        print("⭐ Correct! ⭐")
        time.sleep(.001)
    else:
        is_or_are = " is" if len(correct_answers) == 1 else "s are"
#        print("\n- ".join([f"No, the answer{is_or_are}:"] + correct_answers))
    if "hint" in question:
#        print(f"\nEXPLANATION:\n{question['explanation']}")
        f2.write(f"\nHINT:\n{question['hint']}")
    if "explanation" in question:
#        print(f"\nEXPLANATION:\n{question['explanation']}")
        f2.write(f"\nEXPLANATION:\n{question['explanation']}")
    f2.write(f"\nANSWER: {correct_answers}\n")

    return 1 if correct else 0


def get_answers(question, alternatives, num_choices=1, hint=None):
    global lecturename
    print(f"{question}")
    f1.write(f"{question}")
    f2.write(f"{question}")
    labeled_alternatives = dict(zip(ascii_lowercase, alternatives))
#     if hint:
#         labeled_alternatives["?"] = "Hint"

    for label, alternative in labeled_alternatives.items():
#        print(f"  {label}) {alternative}")
        print(f"  {label}) {alternative}")
        # Don't write topic choices to quiz file
        if question !=INTRODUCTION:
            f1.write(f"\n  {label}) {alternative}")
            f2.write(f"\n  {label}) {alternative}")

    while True:
        plural_s = "" if num_choices == 1 else f"s (choose {num_choices})"
        if question == INTRODUCTION:
            answer = input(f"\nChoice{plural_s}? ")
            lecturename = (str(labeled_alternatives[answer]))
            print(lecturename)
        else:
            answer = "a"
        
#        answer = "a"
        answers = set(answer.replace(",", " ").split())

#         # Handle hints
#         if hint and "?" in answers:
#             print(f"\nHINT: {hint}")
#             continue
# 
#         # Handle hints
#         if hint and "?" in answers:
#             print(f"\nHINT: {hint}")
#             continue

        # Handle invalid answers
        if len(answers) != num_choices:
            plural_s = "" if num_choices == 1 else "s, separated by comma"
            print(f"Please answer {num_choices} alternative{plural_s}")
            continue

        if any(
            (invalid := answer) not in labeled_alternatives
            for answer in answers
        ):
            print(
                f"{invalid!r} is not a valid choice. "  # noqa
                f"Please use {', '.join(labeled_alternatives)}"
            )
            continue

        return [labeled_alternatives[answer] for answer in answers]


if __name__ == "__main__":
    run_quiz()
