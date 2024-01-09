# quiz.py
# jfb 29-DEC-2022 Based on a Real Python tutorial at https://realpython.com/python-quiz-application/
#
import pathlib
import random
from string import ascii_lowercase
import sys
import atexit # For the @atexit.register decorator. Does nothing unless you use 'exit'

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

# Put your question file name here
QFILENAME = "ALLMCQ.txt"
#QFILENAME = "ALLPRACTICEMCQ.txt"
QUESTIONS_PATH = pathlib.Path(__file__).parent / QFILENAME
# Put the number of questions for a quiz here
NUM_QUESTIONS_PER_QUIZ = 8
# Put the ID for your right answers here
CORRECTANSWERS = "rightanswer"
# Put the ID for your wrong answers here
WRONGANSWERS = "wronganswer"
# Put your introductory statement here
INTRODUCTION = "Which lecture do you want to be quizzed about?"

@atexit.register
def goodbye(): # For a message when exiting the program
    print("Bye bye!")


def run_quiz():
    questions = prepare_questions(
        QUESTIONS_PATH, num_questions=NUM_QUESTIONS_PER_QUIZ
    )

    num_correct = 0
    for num, question in enumerate(questions, start=1):
        print(f"\nQuestion {num}:")
        num_correct += ask_question(question)

    print(f"\nYou got {num_correct} correct out of {NUM_QUESTIONS_PER_QUIZ} questions")
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
        print("⭐ Correct! ⭐")
    else:
        is_or_are = " is" if len(correct_answers) == 1 else "s are"
        print("\n- ".join([f"No, the answer{is_or_are}:"] + correct_answers))

    if "explanation" in question:
        print(f"\nEXPLANATION:\n{question['explanation']}")

    return 1 if correct else 0


def get_answers(question, alternatives, num_choices=1, hint=None):
    print(f"{question}")
    labeled_alternatives = dict(zip(ascii_lowercase, alternatives))
    if hint:
        labeled_alternatives["?"] = "Hint"

    for label, alternative in labeled_alternatives.items():
        print(f"  {label}) {alternative}")

    while True:
        plural_s = "" if num_choices == 1 else f"s (choose {num_choices})"
        answer = input(f"\nChoice{plural_s}? ")
        answers = set(answer.replace(",", " ").split())

        # Handle hints
        if hint and "?" in answers:
            print(f"\nHINT: {hint}")
            continue

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
