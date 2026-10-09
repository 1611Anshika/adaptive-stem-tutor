
from app.database import SessionLocal
from app.models import Topic, Question


QUESTION_BANK = {
    "Physics": {
        "Motion": [
            ("What is the SI unit of speed?", "m/s", "kg", "N", "J", "A", "easy", "Speed is distance travelled per unit time, measured in metres per second."),
            ("A car travels 100 m in 20 s. What is its average speed?", "5 m/s", "20 m/s", "80 m/s", "2000 m/s", "A", "medium", "Average speed = distance / time = 100 / 20 = 5 m/s."),
        ],
        "Force and Laws of Motion": [
            ("What is the SI unit of force?", "Newton", "Joule", "Watt", "Pascal", "A", "easy", "Force is measured in newtons (N)."),
            ("What force is needed to accelerate a 2 kg object at 3 m/s²?", "6 N", "1.5 N", "5 N", "9 N", "A", "medium", "Newton's second law gives F = ma = 2 × 3 = 6 N."),
        ],
        "Work, Energy and Power": [
            ("What is the SI unit of work?", "Joule", "Newton", "Watt", "Metre", "A", "easy", "Work is measured in joules."),
            ("A 10 N force moves an object 3 m in its direction. How much work is done?", "30 J", "13 J", "7 J", "3.3 J", "A", "medium", "Work = force × displacement = 10 × 3 = 30 J."),
        ],
        "Electricity": [
            ("What is the SI unit of electric current?", "Ampere", "Volt", "Ohm", "Watt", "A", "easy", "Electric current is measured in amperes."),
            ("A 6 Ω resistor is connected to a 12 V supply. What current flows?", "2 A", "0.5 A", "6 A", "72 A", "A", "medium", "Ohm's law gives I = V/R = 12/6 = 2 A."),
        ],
        "Waves and Optics": [
            ("Which type of wave can travel through a vacuum?", "Light wave", "Sound wave", "Water wave", "Seismic wave", "A", "easy", "Light is an electromagnetic wave and does not require a material medium."),
            ("A wave has frequency 5 Hz and wavelength 2 m. What is its speed?", "10 m/s", "2.5 m/s", "7 m/s", "0.4 m/s", "A", "medium", "Wave speed = frequency × wavelength = 5 × 2 = 10 m/s."),
        ],
    },
    "Chemistry": {
        "Atomic Structure": [
            ("Which particle has a negative electric charge?", "Electron", "Proton", "Neutron", "Nucleus", "A", "easy", "Electrons carry a negative charge."),
            ("The atomic number of an element equals its number of what?", "Protons", "Neutrons", "Electron shells", "Isotopes", "A", "medium", "Atomic number is defined as the number of protons in the nucleus."),
        ],
        "Periodic Table": [
            ("Which element has the chemical symbol O?", "Oxygen", "Gold", "Osmium", "Iron", "A", "easy", "O is the chemical symbol for oxygen."),
            ("Elements in the same group generally have the same number of what?", "Valence electrons", "Neutrons", "Electron shells", "Isotopes", "A", "medium", "For main-group elements, members of a group generally share the same number of valence electrons."),
        ],
        "Chemical Reactions": [
            ("What is formed when an acid reacts with a base?", "Salt and water", "Only oxygen", "Only hydrogen", "Carbon", "A", "easy", "A typical acid-base neutralization produces salt and water."),
            ("What is the balanced equation for hydrogen reacting with oxygen to form water?", "2H2 + O2 → 2H2O", "H2 + O2 → H2O", "H2 + 2O2 → H2O", "2H2 + 2O2 → H2O", "A", "medium", "The balanced equation has four hydrogen atoms and two oxygen atoms on both sides."),
        ],
        "Acids and Bases": [
            ("What is the pH of a neutral solution at 25°C?", "7", "0", "1", "14", "A", "easy", "At 25°C, a neutral aqueous solution has pH 7."),
            ("Which substance is commonly used to test for acids and bases?", "Litmus paper", "Copper wire", "Sand", "Sugar", "A", "medium", "Litmus paper changes colour in acidic and basic solutions."),
        ],
        "Chemical Bonding": [
            ("Which bond involves the sharing of electron pairs?", "Covalent bond", "Ionic bond", "Metallic bond", "Hydrogen bond", "A", "easy", "Covalent bonds form when atoms share electron pairs."),
            ("What is the usual charge on a sodium ion, Na⁺?", "+1", "-1", "+2", "0", "A", "medium", "Sodium typically loses one electron and forms a +1 ion."),
        ],
    },
    "Biology": {
        "Cell Biology": [
            ("Which structure is often called the powerhouse of the cell?", "Mitochondrion", "Ribosome", "Nucleus", "Golgi apparatus", "A", "easy", "Mitochondria produce much of the cell's usable energy through cellular respiration."),
            ("Which structure controls the movement of substances into and out of a cell?", "Cell membrane", "Cell wall only", "Nucleolus", "Chromosome", "A", "medium", "The cell membrane regulates the movement of substances into and out of the cell."),
        ],
        "Human Biology": [
            ("Which organ pumps blood around the human body?", "Heart", "Liver", "Lung", "Kidney", "A", "easy", "The heart pumps blood through the circulatory system."),
            ("Which blood cells primarily transport oxygen?", "Red blood cells", "White blood cells", "Platelets", "Plasma cells", "A", "medium", "Red blood cells contain haemoglobin, which carries oxygen."),
        ],
        "Genetics": [
            ("What molecule carries hereditary information in most organisms?", "DNA", "Starch", "Water", "Fat", "A", "easy", "DNA stores genetic information in most organisms."),
            ("Different versions of the same gene are called what?", "Alleles", "Tissues", "Organs", "Enzymes", "A", "medium", "Alleles are alternative forms of a gene."),
        ],
        "Plant Biology": [
            ("Which pigment absorbs light for photosynthesis?", "Chlorophyll", "Haemoglobin", "Melanin", "Keratin", "A", "easy", "Chlorophyll absorbs light energy used in photosynthesis."),
            ("Which plant tissue transports water from roots to other parts?", "Xylem", "Phloem", "Epidermis", "Cortex only", "A", "medium", "Xylem transports water and dissolved minerals through the plant."),
        ],
        "Ecology": [
            ("What do we call organisms that make their own food?", "Producers", "Consumers", "Decomposers", "Predators", "A", "easy", "Producers, such as green plants, make organic food using energy sources such as sunlight."),
            ("What is the main source of energy for most ecosystems?", "The Sun", "The Moon", "Soil minerals", "Wind alone", "A", "medium", "Sunlight supplies the energy captured by producers in most ecosystems."),
        ],
    },
    "Computer Science": {
        "Programming Fundamentals": [
            ("Which data type commonly stores True or False?", "Boolean", "Integer", "String", "Float", "A", "easy", "A Boolean represents a true-or-false value."),
            ("What is the value of 7 // 2 in Python?", "3", "3.5", "4", "2", "A", "medium", "Python's // operator performs floor division; 7 // 2 evaluates to 3."),
        ],
        "Data Structures": [
            ("Which data structure follows LIFO order?", "Stack", "Queue", "Tree", "Graph", "A", "easy", "A stack follows Last In, First Out."),
            ("Which data structure typically follows FIFO order?", "Queue", "Stack", "Heap", "Binary search tree", "A", "medium", "A queue processes items in First In, First Out order."),
        ],
        "Algorithms": [
            ("What is the time complexity of linear search in the worst case?", "O(n)", "O(1)", "O(log n)", "O(n²)", "A", "easy", "Linear search may inspect every element, so its worst-case time is O(n)."),
            ("What condition is required for standard binary search on an array?", "The array must be sorted", "The array must contain only even numbers", "The array must have unique values", "The array must have length two", "A", "medium", "Binary search relies on sorted order to eliminate half of the remaining search space."),
        ],
        "Database Management": [
            ("What does SQL stand for?", "Structured Query Language", "Simple Question Language", "System Quality Logic", "Sequential Query List", "A", "easy", "SQL stands for Structured Query Language."),
            ("Which SQL command retrieves records from a table?", "SELECT", "DELETE", "DROP", "UPDATE", "A", "medium", "SELECT retrieves data from one or more database tables."),
        ],
        "Computer Networks": [
            ("What does IP stand for in networking?", "Internet Protocol", "Internal Program", "Integrated Process", "Input Port", "A", "easy", "IP stands for Internet Protocol."),
            ("Which device forwards packets between different networks?", "Router", "Keyboard", "Monitor", "Printer", "A", "medium", "Routers forward packets between networks using network-layer information."),
        ],
    },
}


def seed_questions():
    db = SessionLocal()

    try:
        added = 0
        skipped = 0

        for subject, topics in QUESTION_BANK.items():
            for topic_name, questions in topics.items():
                topic = db.query(Topic).filter(
                    Topic.subject == subject,
                    Topic.name == topic_name,
                ).first()

                if not topic:
                    print(f"Skipping missing topic: {subject} / {topic_name}")
                    continue

                for item in questions:
                    (
                        text, a, b, c, d,
                        correct, difficulty, explanation
                    ) = item

                    existing = db.query(Question).filter(
                        Question.topic_id == topic.id,
                        Question.question_text == text,
                    ).first()

                    if existing:
                        skipped += 1
                        continue

                    db.add(
                        Question(
                            question_text=text,
                            option_a=a,
                            option_b=b,
                            option_c=c,
                            option_d=d,
                            correct_answer=correct,
                            difficulty=difficulty,
                            topic_id=topic.id,
                            explanation=explanation,
                        )
                    )
                    added += 1

        db.commit()
        print(f"Added {added} questions; skipped {skipped} existing questions.")

        for subject in QUESTION_BANK:
            count = (
                db.query(Question)
                .join(Topic)
                .filter(Topic.subject == subject)
                .count()
            )
            print(f"{subject}: {count} questions")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_questions()