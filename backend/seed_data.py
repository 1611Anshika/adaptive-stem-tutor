from app.database import SessionLocal
from app.models import Topic, Question


db = SessionLocal()


# ------------------------------------------------
# TOPICS
# ------------------------------------------------

topic_names = [
    ("Algebra", "Mathematics"),
    ("Geometry", "Mathematics"),
    ("Probability", "Mathematics"),
    ("Statistics", "Mathematics"),
]


for name, subject in topic_names:

    existing = db.query(Topic).filter(
        Topic.name == name
    ).first()

    if not existing:

        db.add(
            Topic(
                name=name,
                subject=subject
            )
        )


db.commit()


algebra = db.query(Topic).filter(
    Topic.name == "Algebra"
).first()

geometry = db.query(Topic).filter(
    Topic.name == "Geometry"
).first()

probability = db.query(Topic).filter(
    Topic.name == "Probability"
).first()

statistics = db.query(Topic).filter(
    Topic.name == "Statistics"
).first()


# ------------------------------------------------
# QUESTIONS
# ------------------------------------------------

questions = [

    # ==============================
    # ALGEBRA - EASY
    # ==============================

    Question(
        question_text="What is the value of x in 2x + 4 = 10?",
        option_a="2",
        option_b="3",
        option_c="4",
        option_d="5",
        correct_answer="B",
        difficulty="easy",
        topic_id=algebra.id,
        explanation="2x + 4 = 10, so 2x = 6 and x = 3."
    ),

    Question(
        question_text="If x + 5 = 12, what is x?",
        option_a="5",
        option_b="6",
        option_c="7",
        option_d="8",
        correct_answer="C",
        difficulty="easy",
        topic_id=algebra.id,
        explanation="x = 12 - 5 = 7."
    ),

    # ==============================
    # ALGEBRA - MEDIUM
    # ==============================

    Question(
        question_text="What is the value of x in 3x - 7 = 14?",
        option_a="5",
        option_b="6",
        option_c="7",
        option_d="8",
        correct_answer="C",
        difficulty="medium",
        topic_id=algebra.id,
        explanation="3x - 7 = 14, therefore 3x = 21 and x = 7."
    ),

    Question(
        question_text="Solve: 2(x + 3) = 14.",
        option_a="3",
        option_b="4",
        option_c="5",
        option_d="7",
        correct_answer="B",
        difficulty="medium",
        topic_id=algebra.id,
        explanation="2x + 6 = 14, so 2x = 8 and x = 4."
    ),

    # ==============================
    # ALGEBRA - HARD
    # ==============================

    Question(
        question_text="What are the roots of x² - 5x + 6 = 0?",
        option_a="1 and 6",
        option_b="2 and 3",
        option_c="-2 and -3",
        option_d="3 and 5",
        correct_answer="B",
        difficulty="hard",
        topic_id=algebra.id,
        explanation="x² - 5x + 6 = (x - 2)(x - 3)."
    ),

    Question(
        question_text="If 2x² - 8 = 0, what is the positive value of x?",
        option_a="1",
        option_b="2",
        option_c="4",
        option_d="8",
        correct_answer="B",
        difficulty="hard",
        topic_id=algebra.id,
        explanation="2x² = 8, x² = 4, so positive x = 2."
    ),


    # ==============================
    # GEOMETRY - EASY
    # ==============================

    Question(
        question_text="How many degrees are there in a triangle?",
        option_a="90°",
        option_b="180°",
        option_c="270°",
        option_d="360°",
        correct_answer="B",
        difficulty="easy",
        topic_id=geometry.id,
        explanation="The sum of angles in a triangle is 180°."
    ),

    Question(
        question_text="How many sides does a hexagon have?",
        option_a="5",
        option_b="6",
        option_c="7",
        option_d="8",
        correct_answer="B",
        difficulty="easy",
        topic_id=geometry.id,
        explanation="A hexagon has six sides."
    ),

    # ==============================
    # GEOMETRY - MEDIUM
    # ==============================

    Question(
        question_text="What is the area of a rectangle with length 8 cm and width 5 cm?",
        option_a="13 cm²",
        option_b="26 cm²",
        option_c="40 cm²",
        option_d="80 cm²",
        correct_answer="C",
        difficulty="medium",
        topic_id=geometry.id,
        explanation="Area = length × width = 8 × 5 = 40 cm²."
    ),

    Question(
        question_text="A square has a side of 9 cm. What is its area?",
        option_a="18 cm²",
        option_b="36 cm²",
        option_c="72 cm²",
        option_d="81 cm²",
        correct_answer="D",
        difficulty="medium",
        topic_id=geometry.id,
        explanation="Area = side² = 9² = 81 cm²."
    ),

    # ==============================
    # GEOMETRY - HARD
    # ==============================

    Question(
        question_text="What is the hypotenuse of a right triangle with sides 6 cm and 8 cm?",
        option_a="9 cm",
        option_b="10 cm",
        option_c="12 cm",
        option_d="14 cm",
        correct_answer="B",
        difficulty="hard",
        topic_id=geometry.id,
        explanation="Using Pythagoras: √(6² + 8²) = √100 = 10."
    ),

    Question(
        question_text="What is the area of a circle with radius 7 cm? Use π = 22/7.",
        option_a="44 cm²",
        option_b="154 cm²",
        option_c="308 cm²",
        option_d="616 cm²",
        correct_answer="B",
        difficulty="hard",
        topic_id=geometry.id,
        explanation="Area = πr² = 22/7 × 49 = 154 cm²."
    ),


    # ==============================
    # PROBABILITY - EASY
    # ==============================

    Question(
        question_text="What is the probability of getting heads when tossing a fair coin?",
        option_a="0",
        option_b="1/4",
        option_c="1/2",
        option_d="1",
        correct_answer="C",
        difficulty="easy",
        topic_id=probability.id,
        explanation="A fair coin has two equally likely outcomes."
    ),

    Question(
        question_text="How many possible outcomes are there when rolling a standard die?",
        option_a="4",
        option_b="5",
        option_c="6",
        option_d="8",
        correct_answer="C",
        difficulty="easy",
        topic_id=probability.id,
        explanation="A standard die has six faces."
    ),

    # ==============================
    # PROBABILITY - MEDIUM
    # ==============================

    Question(
        question_text="A die is rolled once. What is the probability of getting a 6?",
        option_a="1/2",
        option_b="1/3",
        option_c="1/6",
        option_d="1/12",
        correct_answer="C",
        difficulty="medium",
        topic_id=probability.id,
        explanation="There is one favorable outcome among six possible outcomes."
    ),

    Question(
        question_text="What is the probability of drawing a red card from a standard deck of 52 cards?",
        option_a="1/4",
        option_b="1/2",
        option_c="13/52",
        option_d="3/4",
        correct_answer="B",
        difficulty="medium",
        topic_id=probability.id,
        explanation="There are 26 red cards out of 52 cards."
    ),

    # ==============================
    # PROBABILITY - HARD
    # ==============================

    Question(
        question_text="Two coins are tossed. What is the probability of getting exactly one head?",
        option_a="1/4",
        option_b="1/2",
        option_c="3/4",
        option_d="1",
        correct_answer="B",
        difficulty="hard",
        topic_id=probability.id,
        explanation="Possible outcomes are HH, HT, TH, TT. Two have exactly one head."
    ),

    Question(
        question_text="A bag contains 3 red and 2 blue balls. What is the probability of drawing a red ball?",
        option_a="2/5",
        option_b="3/5",
        option_c="1/2",
        option_d="4/5",
        correct_answer="B",
        difficulty="hard",
        topic_id=probability.id,
        explanation="There are 3 red balls out of 5 total balls."
    ),


    # ==============================
    # STATISTICS - EASY
    # ==============================

    Question(
        question_text="What is the mean of 2, 4 and 6?",
        option_a="3",
        option_b="4",
        option_c="5",
        option_d="6",
        correct_answer="B",
        difficulty="easy",
        topic_id=statistics.id,
        explanation="Mean = (2 + 4 + 6) / 3 = 4."
    ),

    Question(
        question_text="What is the mode of 2, 3, 3, 4, 5?",
        option_a="2",
        option_b="3",
        option_c="4",
        option_d="5",
        correct_answer="B",
        difficulty="easy",
        topic_id=statistics.id,
        explanation="3 occurs most frequently."
    ),

    # ==============================
    # STATISTICS - MEDIUM
    # ==============================

    Question(
        question_text="What is the median of 3, 7, 9, 12 and 15?",
        option_a="7",
        option_b="9",
        option_c="12",
        option_d="15",
        correct_answer="B",
        difficulty="medium",
        topic_id=statistics.id,
        explanation="The middle value is 9."
    ),

    Question(
        question_text="What is the range of 5, 8, 12, 15 and 20?",
        option_a="10",
        option_b="12",
        option_c="15",
        option_d="20",
        correct_answer="C",
        difficulty="medium",
        topic_id=statistics.id,
        explanation="Range = maximum - minimum = 20 - 5 = 15."
    ),

    # ==============================
    # STATISTICS - HARD
    # ==============================

    Question(
        question_text="What is the mean of 5, 10, 15, 20 and 25?",
        option_a="10",
        option_b="12",
        option_c="15",
        option_d="20",
        correct_answer="C",
        difficulty="hard",
        topic_id=statistics.id,
        explanation="Mean = 75 / 5 = 15."
    ),

    Question(
        question_text="If the mean of five numbers is 20, what is their total?",
        option_a="25",
        option_b="50",
        option_c="100",
        option_d="125",
        correct_answer="C",
        difficulty="hard",
        topic_id=statistics.id,
        explanation="Total = mean × number of values = 20 × 5 = 100."
    )
]


# ------------------------------------------------
# INSERT QUESTIONS
# ------------------------------------------------

for question in questions:

    existing = db.query(Question).filter(
        Question.question_text == question.question_text
    ).first()

    if not existing:
        db.add(question)


db.commit()
db.close()

print("Expanded STEM question bank seeded successfully!")