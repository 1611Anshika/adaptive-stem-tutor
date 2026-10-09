"""
Supplementary question bank for Adaptive STEM Tutor.

This script ADDS questions to the existing SQLite database. It does not delete,
reset, or modify existing questions or student attempts. It is safe to run more
than once: exact duplicate question text within the same topic is skipped.

Run from the backend folder:
    python seed_expanded_questions.py
"""
from app.database import SessionLocal
from app.models import Topic, Question

# Format:
# (subject, topic, question, option_a, option_b, option_c, option_d,
#  correct_answer_letter, difficulty, explanation)
QUESTION_BANK = [
    # MATHEMATICS — Algebra
    ("Mathematics", "Algebra", "Solve: 3x + 5 = 20.", "x = 3", "x = 5", "x = 7", "x = 15", "B", "easy", "Subtract 5 to get 3x = 15, then divide by 3."),
    ("Mathematics", "Algebra", "Simplify: 4a + 3a - 2a.", "5a", "9a", "5a²", "a", "A", "easy", "Combine like terms: (4 + 3 - 2)a = 5a."),
    ("Mathematics", "Algebra", "If y = 2x - 3, find y when x = 4.", "3", "5", "8", "11", "B", "easy", "Substitute x = 4: y = 8 - 3 = 5."),
    ("Mathematics", "Algebra", "Expand: (x + 4)(x + 2).", "x² + 6x + 8", "x² + 8", "x² + 6x + 6", "x² + 2x + 8", "A", "medium", "Multiply each term: x² + 2x + 4x + 8."),
    ("Mathematics", "Algebra", "Solve the system x + y = 9 and x - y = 3.", "x=3, y=6", "x=6, y=3", "x=9, y=3", "x=4, y=5", "B", "medium", "Adding the equations gives 2x = 12, so x = 6 and y = 3."),
    ("Mathematics", "Algebra", "Factorise x² - 9x + 20.", "(x - 2)(x - 10)", "(x + 4)(x + 5)", "(x - 4)(x - 5)", "(x - 1)(x - 20)", "C", "hard", "The numbers -4 and -5 multiply to 20 and add to -9."),
    ("Mathematics", "Algebra", "If x + 1/x = 3, find x² + 1/x².", "7", "9", "11", "5", "A", "hard", "Square both sides: x² + 2 + 1/x² = 9, so the result is 7."),
    ("Mathematics", "Algebra", "For what real values of k does x² - 6x + k = 0 have equal roots?", "k = 6", "k = 9", "k = 12", "k = 18", "B", "extreme hard", "Equal roots require discriminant 36 - 4k = 0, hence k = 9."),
    # MATHEMATICS — Geometry
    ("Mathematics", "Geometry", "The sum of the interior angles of a triangle is:", "90°", "180°", "270°", "360°", "B", "easy", "The interior angles of every Euclidean triangle sum to 180°."),
    ("Mathematics", "Geometry", "A rectangle has length 8 cm and width 3 cm. Its area is:", "11 cm²", "22 cm²", "24 cm²", "48 cm²", "C", "easy", "Area = length × width = 8 × 3 = 24 cm²."),
    ("Mathematics", "Geometry", "A circle has radius 7 cm. Using π = 22/7, its circumference is:", "22 cm", "44 cm", "49 cm", "154 cm", "B", "medium", "Circumference = 2πr = 2 × 22/7 × 7 = 44 cm."),
    ("Mathematics", "Geometry", "The hypotenuse of a right triangle with legs 5 cm and 12 cm is:", "13 cm", "15 cm", "17 cm", "10 cm", "A", "medium", "By Pythagoras, c = √(25 + 144) = 13."),
    ("Mathematics", "Geometry", "The distance between (1, 2) and (4, 6) is:", "4", "5", "6", "7", "B", "hard", "Distance = √((4−1)² + (6−2)²) = √25 = 5."),
    ("Mathematics", "Geometry", "A cone has radius 3 cm and height 4 cm. Its volume is:", "12π cm³", "16π cm³", "24π cm³", "36π cm³", "A", "hard", "Volume = (1/3)πr²h = (1/3)π × 9 × 4 = 12π cm³."),
    ("Mathematics", "Geometry", "A chord is 5 cm from the centre of a circle of radius 13 cm. The chord length is:", "12 cm", "18 cm", "24 cm", "26 cm", "C", "extreme hard", "The perpendicular bisects the chord: half-length = √(13²−5²) = 12, so length = 24 cm."),
    # MATHEMATICS — Probability
    ("Mathematics", "Probability", "A fair coin is tossed once. The probability of heads is:", "0", "1/4", "1/2", "1", "C", "easy", "There is one head outcome among two equally likely outcomes."),
    ("Mathematics", "Probability", "A fair six-sided die is rolled. Probability of rolling a 6 is:", "1/2", "1/3", "1/6", "5/6", "C", "easy", "One of the six equally likely outcomes is 6."),
    ("Mathematics", "Probability", "A bag has 3 red and 2 blue balls. Probability of drawing a blue ball is:", "2/3", "2/5", "3/5", "1/5", "B", "medium", "There are 2 blue balls among 5 total balls."),
    ("Mathematics", "Probability", "Two fair coins are tossed. Probability of exactly one head is:", "1/4", "1/2", "3/4", "1", "B", "medium", "Outcomes are HH, HT, TH, TT; two of four have exactly one head."),
    ("Mathematics", "Probability", "A card is drawn from a standard 52-card deck. Probability it is a king is:", "1/13", "1/4", "4/13", "1/52", "A", "hard", "There are 4 kings among 52 cards, so 4/52 = 1/13."),
    ("Mathematics", "Probability", "Two fair dice are rolled. Probability their sum is 7 is:", "1/12", "1/6", "5/36", "7/36", "B", "hard", "Six outcomes sum to 7 out of 36 equally likely ordered outcomes."),
    ("Mathematics", "Probability", "Events A and B are independent, with P(A)=0.4 and P(B)=0.5. Find P(A and B).", "0.1", "0.2", "0.4", "0.9", "B", "extreme hard", "For independent events, P(A∩B) = P(A)P(B) = 0.4 × 0.5 = 0.2."),
    # MATHEMATICS — Statistics
    ("Mathematics", "Statistics", "Find the mean of 2, 4, 6.", "3", "4", "5", "6", "B", "easy", "Mean = (2 + 4 + 6)/3 = 4."),
    ("Mathematics", "Statistics", "Find the median of 3, 8, 1, 5, 7.", "3", "5", "7", "8", "B", "easy", "Sorted data are 1, 3, 5, 7, 8; the middle value is 5."),
    ("Mathematics", "Statistics", "The mode of 2, 3, 3, 4, 5 is:", "2", "3", "4", "5", "B", "medium", "The value 3 occurs most often."),
    ("Mathematics", "Statistics", "If every value in a data set is increased by 5, the mean:", "Decreases by 5", "Does not change", "Increases by 5", "Doubles", "C", "medium", "Adding a constant to every observation adds that constant to the mean."),
    ("Mathematics", "Statistics", "For data 2, 4, 6, 8, 10, the population variance is:", "4", "8", "10", "16", "B", "hard", "Mean is 6; squared deviations sum to 40; divide by 5 to get 8."),
    ("Mathematics", "Statistics", "A data set has standard deviation 3. Its variance is:", "1.5", "3", "6", "9", "D", "hard", "Variance is the square of standard deviation: 3² = 9."),
    ("Mathematics", "Statistics", "For a normal distribution, approximately what percentage of values lie within two standard deviations of the mean?", "68%", "90%", "95%", "99.7%", "C", "extreme hard", "The empirical rule states approximately 95% lie within ±2 standard deviations."),
    # MATHEMATICS — Trigonometry (created only if topic already exists; script reports missing topics)
    ("Mathematics", "Trigonometry", "In a right triangle, sin θ equals:", "Adjacent/hypotenuse", "Opposite/hypotenuse", "Opposite/adjacent", "Hypotenuse/opposite", "B", "easy", "Sine is opposite side divided by hypotenuse."),
    ("Mathematics", "Trigonometry", "The value of cos 0° is:", "0", "1/2", "1", "Undefined", "C", "easy", "Cosine of 0° is 1."),
    ("Mathematics", "Trigonometry", "If sin θ = 3/5 for an acute angle, then cos θ is:", "2/5", "3/4", "4/5", "5/4", "C", "medium", "Using sin²θ + cos²θ = 1 gives cos θ = √(1−9/25) = 4/5."),
    ("Mathematics", "Trigonometry", "The value of tan 45° + sin 30° is:", "1/2", "1", "3/2", "2", "C", "medium", "tan 45° = 1 and sin 30° = 1/2, total 3/2."),
    ("Mathematics", "Trigonometry", "If tan θ = 3/4 for an acute angle, then sec² θ is:", "7/16", "1", "25/16", "25/7", "C", "hard", "sec²θ = 1 + tan²θ = 1 + 9/16 = 25/16."),
    ("Mathematics", "Trigonometry", "If sin A = cos 2A and A is acute, then A is:", "15°", "20°", "30°", "45°", "A", "extreme hard", "cos 2A = sin(90°−2A); for acute A, A = 90°−2A, so A = 30°."),
    # PHYSICS — Motion
    ("Physics", "Motion", "The SI unit of speed is:", "km", "m/s", "m/s²", "N", "B", "easy", "Speed is distance divided by time, measured in metres per second."),
    ("Physics", "Motion", "A car travels 100 m in 5 s. Its average speed is:", "5 m/s", "10 m/s", "20 m/s", "50 m/s", "C", "easy", "Average speed = 100/5 = 20 m/s."),
    ("Physics", "Motion", "A body starts from rest and accelerates at 2 m/s² for 4 s. Final velocity is:", "2 m/s", "4 m/s", "6 m/s", "8 m/s", "D", "medium", "v = u + at = 0 + 2×4 = 8 m/s."),
    ("Physics", "Motion", "The slope of a velocity-time graph represents:", "Distance", "Acceleration", "Displacement", "Momentum", "B", "medium", "The gradient is change in velocity divided by time, i.e. acceleration."),
    ("Physics", "Motion", "A body moving at 10 m/s stops uniformly in 5 s. Its acceleration is:", "−2 m/s²", "−5 m/s²", "2 m/s²", "5 m/s²", "A", "hard", "a = (v−u)/t = (0−10)/5 = −2 m/s²."),
    ("Physics", "Motion", "A body covers equal distances at speeds v and 2v. Its average speed is:", "3v/2", "4v/3", "2v/3", "v", "B", "extreme hard", "For equal distances, average speed = 2(v)(2v)/(v+2v) = 4v/3."),
    # PHYSICS — Force and Laws of Motion
    ("Physics", "Force and Laws of Motion", "The SI unit of force is:", "Joule", "Watt", "Newton", "Pascal", "C", "easy", "Force is measured in newtons (N)."),
    ("Physics", "Force and Laws of Motion", "A 2 kg object accelerates at 3 m/s². Net force is:", "1.5 N", "5 N", "6 N", "9 N", "C", "easy", "Newton's second law: F = ma = 2 × 3 = 6 N."),
    ("Physics", "Force and Laws of Motion", "Newton's third law states that action and reaction are:", "Equal and opposite", "Equal and in the same direction", "Unequal", "Always balanced on one object", "A", "medium", "Action and reaction are equal and opposite and act on different bodies."),
    ("Physics", "Force and Laws of Motion", "A 5 kg object is acted on by a net force of 20 N. Its acceleration is:", "2 m/s²", "4 m/s²", "10 m/s²", "100 m/s²", "B", "medium", "a = F/m = 20/5 = 4 m/s²."),
    ("Physics", "Force and Laws of Motion", "A 0.2 kg ball changes velocity from 10 m/s to −5 m/s. Magnitude of impulse is:", "1 Ns", "2 Ns", "3 Ns", "5 Ns", "C", "hard", "Impulse magnitude = m|Δv| = 0.2 × 15 = 3 Ns."),
    ("Physics", "Force and Laws of Motion", "A 2 kg body moving at 6 m/s collides and sticks to a stationary 4 kg body. Their final speed is:", "1 m/s", "2 m/s", "3 m/s", "6 m/s", "B", "extreme hard", "Conservation of momentum: 2×6 = (2+4)v, so v = 2 m/s."),
    # PHYSICS — Work, Energy and Power
    ("Physics", "Work, Energy and Power", "Work done when a 10 N force moves an object 2 m in its direction is:", "5 J", "12 J", "20 J", "40 J", "C", "easy", "W = Fs = 10 × 2 = 20 J."),
    ("Physics", "Work, Energy and Power", "The SI unit of power is:", "Joule", "Newton", "Watt", "Pascal", "C", "easy", "Power is measured in watts."),
    ("Physics", "Work, Energy and Power", "The kinetic energy of a 2 kg object moving at 3 m/s is:", "3 J", "6 J", "9 J", "18 J", "C", "medium", "KE = ½mv² = ½ × 2 × 9 = 9 J."),
    ("Physics", "Work, Energy and Power", "A machine performs 600 J of work in 3 s. Its average power is:", "100 W", "200 W", "300 W", "1800 W", "B", "medium", "Power = work/time = 600/3 = 200 W."),
    ("Physics", "Work, Energy and Power", "An object of mass 2 kg is raised by 5 m. Taking g = 10 m/s², its gain in potential energy is:", "10 J", "25 J", "50 J", "100 J", "D", "hard", "ΔPE = mgh = 2 × 10 × 5 = 100 J."),
    ("Physics", "Work, Energy and Power", "If speed doubles, the kinetic energy becomes:", "Twice", "Three times", "Four times", "Eight times", "C", "extreme hard", "Kinetic energy is proportional to speed squared."),
    # PHYSICS — Electricity
    ("Physics", "Electricity", "Electric current is measured in:", "Volts", "Amperes", "Ohms", "Watts", "B", "easy", "The SI unit of electric current is the ampere."),
    ("Physics", "Electricity", "A 12 V battery is connected across a 4 Ω resistor. Current is:", "2 A", "3 A", "4 A", "48 A", "B", "easy", "Ohm's law: I = V/R = 12/4 = 3 A."),
    ("Physics", "Electricity", "Two 2 Ω resistors in series have equivalent resistance:", "1 Ω", "2 Ω", "4 Ω", "8 Ω", "C", "medium", "Series resistances add: 2 + 2 = 4 Ω."),
    ("Physics", "Electricity", "A 60 W appliance runs for 2 hours. Energy consumed is:", "30 Wh", "60 Wh", "120 Wh", "240 Wh", "C", "medium", "Energy = power × time = 60 × 2 = 120 Wh."),
    ("Physics", "Electricity", "Three resistors 2 Ω, 3 Ω and 6 Ω are connected in parallel. Equivalent resistance is:", "1 Ω", "2 Ω", "3 Ω", "11 Ω", "A", "hard", "1/R = 1/2 + 1/3 + 1/6 = 1, so R = 1 Ω."),
    ("Physics", "Electricity", "A 10 Ω resistor carries 2 A for 5 minutes. Heat produced is:", "200 J", "1200 J", "6000 J", "12000 J", "D", "extreme hard", "H = I²Rt = 4 × 10 × 300 = 12000 J."),
    # PHYSICS — Waves and Optics
    ("Physics", "Waves and Optics", "The SI unit of frequency is:", "Metre", "Second", "Hertz", "Decibel", "C", "easy", "Frequency is measured in hertz (Hz)."),
    ("Physics", "Waves and Optics", "A wave has frequency 5 Hz and wavelength 2 m. Its speed is:", "2.5 m/s", "7 m/s", "10 m/s", "15 m/s", "C", "easy", "Wave speed v = fλ = 5 × 2 = 10 m/s."),
    ("Physics", "Waves and Optics", "The angle of reflection is measured from the:", "Mirror surface", "Normal to the surface", "Incident ray only", "Tangent", "B", "medium", "Angles of incidence and reflection are measured from the normal."),
    ("Physics", "Waves and Optics", "A convex lens converges parallel rays to its:", "Optical centre", "Principal focus", "Centre of curvature only", "Aperture", "B", "medium", "A convex lens brings parallel rays to the principal focus."),
    ("Physics", "Waves and Optics", "A lens has focal length 0.5 m. Its power is:", "0.5 D", "1 D", "2 D", "5 D", "C", "hard", "Power P = 1/f in metres = 1/0.5 = 2 dioptres."),
    ("Physics", "Waves and Optics", "A wave travels at 340 m/s with frequency 170 Hz. Its wavelength is:", "0.5 m", "2 m", "170 m", "510 m", "B", "extreme hard", "Wavelength λ = v/f = 340/170 = 2 m."),
    # CHEMISTRY — Atomic Structure
    ("Chemistry", "Atomic Structure", "Which subatomic particle has a negative charge?", "Proton", "Neutron", "Electron", "Nucleus", "C", "easy", "Electrons carry a negative electric charge."),
    ("Chemistry", "Atomic Structure", "The atomic number equals the number of:", "Neutrons", "Protons", "Protons plus neutrons", "Electron shells", "B", "easy", "Atomic number is defined as the number of protons."),
    ("Chemistry", "Atomic Structure", "An atom has 11 protons and 12 neutrons. Its mass number is:", "11", "12", "23", "132", "C", "medium", "Mass number = protons + neutrons = 11 + 12 = 23."),
    ("Chemistry", "Atomic Structure", "The maximum number of electrons in the second shell is:", "2", "8", "18", "32", "B", "medium", "The shell capacity formula is 2n²; for n = 2, it is 8."),
    ("Chemistry", "Atomic Structure", "Isotopes of an element have the same number of:", "Neutrons", "Nucleons", "Protons", "Neutrons and mass number", "C", "hard", "Isotopes have the same atomic number but different neutron counts."),
    ("Chemistry", "Atomic Structure", "An ion X²⁺ has 10 electrons. The atomic number of X is:", "8", "10", "12", "14", "C", "extreme hard", "A 2+ ion has lost two electrons, so neutral X had 12 electrons and 12 protons."),
    # CHEMISTRY — Periodic Table
    ("Chemistry", "Periodic Table", "Elements in the same group generally have the same number of:", "Neutrons", "Electron shells", "Valence electrons", "Protons", "C", "easy", "For main-group elements, group members generally share valence-electron counts."),
    ("Chemistry", "Periodic Table", "The modern periodic table is arranged by increasing:", "Atomic mass", "Atomic number", "Density", "Melting point", "B", "easy", "The modern periodic law uses atomic number."),
    ("Chemistry", "Periodic Table", "Which is a noble gas?", "Oxygen", "Nitrogen", "Neon", "Chlorine", "C", "medium", "Neon is in Group 18, the noble gases."),
    ("Chemistry", "Periodic Table", "Across a period from left to right, atomic radius generally:", "Increases", "Decreases", "Stays identical", "First doubles", "B", "medium", "Increasing effective nuclear charge generally pulls electrons closer."),
    ("Chemistry", "Periodic Table", "Which element is most electronegative?", "Sodium", "Carbon", "Oxygen", "Fluorine", "D", "hard", "Fluorine has the highest electronegativity."),
    ("Chemistry", "Periodic Table", "An element has electron configuration 2, 8, 7. It is most likely in:", "Group 1", "Group 7/17", "Group 2", "Group 18", "B", "extreme hard", "Seven valence electrons identify a halogen in Group 17 (modern numbering)."),
    # CHEMISTRY — Chemical Reactions
    ("Chemistry", "Chemical Reactions", "A reaction in which two or more substances form one product is a:", "Decomposition reaction", "Combination reaction", "Displacement reaction", "Neutralisation only", "B", "easy", "A combination reaction forms a single product from reactants."),
    ("Chemistry", "Chemical Reactions", "Which gas is commonly released when an acid reacts with many metals?", "Oxygen", "Nitrogen", "Hydrogen", "Carbon dioxide", "C", "easy", "Acid + reactive metal commonly produces a salt and hydrogen gas."),
    ("Chemistry", "Chemical Reactions", "Balance: H₂ + O₂ → H₂O. The coefficient of H₂ is:", "1", "2", "3", "4", "B", "medium", "Balanced equation: 2H₂ + O₂ → 2H₂O."),
    ("Chemistry", "Chemical Reactions", "Oxidation can be described as:", "Gain of electrons", "Loss of electrons", "Gain of neutrons", "Loss of protons only", "B", "medium", "In electron-transfer terms, oxidation is loss of electrons."),
    ("Chemistry", "Chemical Reactions", "In Zn + CuSO₄ → ZnSO₄ + Cu, zinc:", "Is reduced", "Is oxidised", "Acts as a catalyst only", "Does not change", "B", "hard", "Zinc loses electrons to form Zn²⁺, so it is oxidised."),
    ("Chemistry", "Chemical Reactions", "For 2H₂ + O₂ → 2H₂O, how many moles of water form from 3 mol H₂ with excess O₂?", "1 mol", "1.5 mol", "2 mol", "3 mol", "D", "extreme hard", "The H₂:H₂O mole ratio is 1:1, so 3 mol H₂ forms 3 mol H₂O."),
    # CHEMISTRY — Acids and Bases
    ("Chemistry", "Acids and Bases", "A solution with pH 3 is:", "Acidic", "Neutral", "Basic", "Always a salt", "A", "easy", "A pH below 7 is acidic at ordinary conditions."),
    ("Chemistry", "Acids and Bases", "Blue litmus paper in an acidic solution turns:", "Blue", "Red", "Green", "Colourless", "B", "easy", "Acids turn blue litmus red."),
    ("Chemistry", "Acids and Bases", "Neutralisation between an acid and a base typically forms:", "Metal only", "Salt and water", "Hydrogen only", "Oxygen and water", "B", "medium", "Acid + base → salt + water in a typical neutralisation."),
    ("Chemistry", "Acids and Bases", "At 25°C, a neutral aqueous solution has pH:", "0", "5", "7", "14", "C", "medium", "Neutral water at 25°C has pH 7."),
    ("Chemistry", "Acids and Bases", "If [H⁺] = 1 × 10⁻⁴ mol/L, the pH is:", "2", "4", "10", "14", "B", "hard", "pH = −log₁₀[H⁺] = 4."),
    ("Chemistry", "Acids and Bases", "How many mL of 1.0 M NaOH are needed to neutralise 25 mL of 0.5 M HCl?", "6.25 mL", "12.5 mL", "25 mL", "50 mL", "B", "extreme hard", "For 1:1 neutralisation, M₁V₁ = M₂V₂; VNaOH = 0.5×25/1.0 = 12.5 mL."),
    # CHEMISTRY — Chemical Bonding
    ("Chemistry", "Chemical Bonding", "An ionic bond forms mainly through:", "Sharing electrons equally", "Transfer of electrons and electrostatic attraction", "Sharing neutrons", "Overlapping nuclei", "B", "easy", "Ionic bonding involves electron transfer and attraction between oppositely charged ions."),
    ("Chemistry", "Chemical Bonding", "A covalent bond generally involves:", "Sharing electron pairs", "Transferring protons", "Sharing nuclei", "Losing all electrons", "A", "easy", "Covalent bonds form when atoms share electron pairs."),
    ("Chemistry", "Chemical Bonding", "Which compound is predominantly ionic?", "NaCl", "CH₄", "CO₂", "H₂O", "A", "medium", "Sodium transfers an electron to chlorine, forming Na⁺ and Cl⁻."),
    ("Chemistry", "Chemical Bonding", "The shape of a methane (CH₄) molecule is:", "Linear", "Trigonal planar", "Tetrahedral", "Bent", "C", "medium", "Four bonding pairs around carbon arrange tetrahedrally."),
    ("Chemistry", "Chemical Bonding", "The approximate bond angle in a trigonal planar molecule is:", "90°", "109.5°", "120°", "180°", "C", "hard", "Trigonal planar geometry has bond angles near 120°."),
    ("Chemistry", "Chemical Bonding", "Which molecule has a polar covalent bond but is overall nonpolar due to symmetry?", "H₂O", "NH₃", "CO₂", "HCl", "C", "extreme hard", "Each C=O bond is polar, but the linear symmetric molecule's dipoles cancel."),
    # BIOLOGY — Cell Biology
    ("Biology", "Cell Biology", "Which organelle is often called the powerhouse of the cell?", "Nucleus", "Mitochondrion", "Ribosome", "Golgi apparatus", "B", "easy", "Mitochondria produce much of the cell's ATP."),
    ("Biology", "Cell Biology", "The cell membrane is mainly composed of:", "Cellulose only", "A phospholipid bilayer with proteins", "DNA only", "Starch", "B", "easy", "The fluid-mosaic membrane contains phospholipids and proteins."),
    ("Biology", "Cell Biology", "Which structure contains most genetic material in a typical eukaryotic cell?", "Nucleus", "Lysosome", "Vacuole", "Cell wall", "A", "medium", "Most eukaryotic DNA is located in the nucleus."),
    ("Biology", "Cell Biology", "Ribosomes are the main site of:", "Photosynthesis", "Protein synthesis", "Lipid storage", "DNA packaging only", "B", "medium", "Ribosomes translate mRNA to build proteins."),
    ("Biology", "Cell Biology", "During mitosis, sister chromatids separate in:", "Prophase", "Metaphase", "Anaphase", "Interphase", "C", "hard", "Sister chromatids move to opposite poles during anaphase."),
    ("Biology", "Cell Biology", "A cell placed in a strongly hypertonic solution will generally:", "Gain water and swell", "Lose water and shrink", "Remain unchanged always", "Divide immediately", "B", "extreme hard", "Water moves out by osmosis toward the higher solute concentration."),
    # BIOLOGY — Human Biology
    ("Biology", "Human Biology", "Which organ pumps blood around the body?", "Liver", "Lung", "Heart", "Kidney", "C", "easy", "The heart pumps blood through the circulatory system."),
    ("Biology", "Human Biology", "Which blood cells transport most oxygen?", "White blood cells", "Red blood cells", "Platelets", "Neurons", "B", "easy", "Haemoglobin in red blood cells carries oxygen."),
    ("Biology", "Human Biology", "Most nutrient absorption occurs in the:", "Stomach", "Large intestine", "Small intestine", "Oesophagus", "C", "medium", "Villi in the small intestine provide a large absorption surface."),
    ("Biology", "Human Biology", "Insulin is produced by the:", "Thyroid gland", "Pancreas", "Adrenal gland", "Pituitary gland", "B", "medium", "Beta cells in pancreatic islets produce insulin."),
    ("Biology", "Human Biology", "Gas exchange in human lungs occurs mainly in the:", "Trachea", "Bronchi", "Alveoli", "Diaphragm", "C", "hard", "Thin-walled alveoli enable oxygen and carbon dioxide diffusion."),
    ("Biology", "Human Biology", "If a person has blood group AB positive, which statement is correct for red-cell antigens?", "A antigen only", "B antigen only", "A and B antigens, and Rh D antigen", "No A, B, or Rh D antigens", "C", "extreme hard", "AB+ red cells express A, B, and Rh D antigens."),
    # BIOLOGY — Genetics
    ("Biology", "Genetics", "The basic unit of heredity is a:", "Tissue", "Gene", "Organ", "Cell membrane", "B", "easy", "Genes are DNA sequences that contribute to inherited traits."),
    ("Biology", "Genetics", "DNA stands for:", "Deoxyribonucleic acid", "Dinuclear ribose acid", "Deoxyribose nitrogen atom", "Double nucleic arrangement", "A", "easy", "DNA is deoxyribonucleic acid."),
    ("Biology", "Genetics", "If T is dominant over t, which genotype is heterozygous?", "TT", "Tt", "tt", "None", "B", "medium", "Heterozygous means two different alleles: T and t."),
    ("Biology", "Genetics", "A cross Tt × Tt gives what probability of tt offspring?", "0%", "25%", "50%", "75%", "B", "medium", "The genotypes are TT, Tt, Tt, tt; one in four is tt."),
    ("Biology", "Genetics", "DNA replication is described as semiconservative because each new DNA molecule has:", "Two entirely new strands", "Two entirely old strands", "One old strand and one new strand", "No original DNA", "C", "hard", "Each daughter molecule retains one parental strand and contains one newly synthesised strand."),
    ("Biology", "Genetics", "For an autosomal recessive condition, two unaffected carrier parents (Aa × Aa) have what probability of an affected child (aa) per pregnancy?", "0%", "25%", "50%", "75%", "B", "extreme hard", "The offspring ratio is 1 AA : 2 Aa : 1 aa; affected aa probability is 1/4."),
    # BIOLOGY — Plant Biology
    ("Biology", "Plant Biology", "Photosynthesis mainly takes place in:", "Mitochondria", "Chloroplasts", "Nucleus", "Ribosomes", "B", "easy", "Chloroplasts contain chlorophyll and host photosynthesis."),
    ("Biology", "Plant Biology", "Which gas is taken in by plants for photosynthesis?", "Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen", "C", "easy", "Plants use carbon dioxide and water to produce sugars and oxygen."),
    ("Biology", "Plant Biology", "Xylem mainly transports:", "Sugars from leaves", "Water and mineral ions", "Hormones only", "Oxygen to roots", "B", "medium", "Xylem carries water and dissolved minerals from roots upward."),
    ("Biology", "Plant Biology", "Stomata primarily help with:", "Seed formation only", "Gas exchange and water-vapour loss", "Absorbing minerals from soil", "Anchoring roots", "B", "medium", "Stomata regulate gas exchange and transpiration."),
    ("Biology", "Plant Biology", "The plant hormone most associated with cell elongation and phototropism is:", "Auxin", "Insulin", "Adrenaline", "Haemoglobin", "A", "hard", "Auxin distribution contributes to differential growth toward light."),
    ("Biology", "Plant Biology", "A plant cell placed in a hypotonic solution becomes turgid mainly because:", "Water leaves by osmosis", "Water enters by osmosis and the wall resists expansion", "The cell wall dissolves", "Active transport stops permanently", "B", "extreme hard", "Water enters by osmosis; the rigid cell wall limits expansion and builds turgor pressure."),
    # BIOLOGY — Ecology
    ("Biology", "Ecology", "An organism that makes its own food is a:", "Producer", "Primary consumer", "Decomposer only", "Parasite", "A", "easy", "Producers make organic matter, usually using light or chemical energy."),
    ("Biology", "Ecology", "Which is a decomposer?", "Grass", "Deer", "Fungus", "Eagle", "C", "easy", "Fungi break down dead organic matter."),
    ("Biology", "Ecology", "In a food chain, energy generally flows from:", "Consumers to the Sun", "Producers to consumers", "Decomposers to sunlight", "Top predators to plants only", "B", "medium", "Energy captured by producers passes to consumers through feeding."),
    ("Biology", "Ecology", "If producers store 10,000 kJ, approximately how much may reach primary consumers using the 10% rule?", "100 kJ", "1,000 kJ", "5,000 kJ", "10,000 kJ", "B", "medium", "About 10% transfers to the next trophic level: 1,000 kJ."),
    ("Biology", "Ecology", "A relationship where both species benefit is called:", "Parasitism", "Competition", "Mutualism", "Predation", "C", "hard", "Mutualism benefits both participating species."),
    ("Biology", "Ecology", "A pollutant becomes more concentrated at higher trophic levels. This is:", "Nitrogen fixation", "Biomagnification", "Succession", "Transpiration", "B", "extreme hard", "Persistent pollutants can accumulate and increase in concentration up the food chain."),
    # COMPUTER SCIENCE — Programming Fundamentals
    ("Computer Science", "Programming Fundamentals", "Which data type is commonly used to store true or false?", "Integer", "Boolean", "String", "Float", "B", "easy", "A Boolean represents a logical true/false value."),
    ("Computer Science", "Programming Fundamentals", "In Python, which symbol begins a single-line comment?", "//", "#", "/*", "--", "B", "easy", "Python uses # for comments."),
    ("Computer Science", "Programming Fundamentals", "What is the value of 7 // 2 in Python?", "3.5", "3", "4", "1", "B", "medium", "Floor division returns the integer quotient 3."),
    ("Computer Science", "Programming Fundamentals", "Which construct repeats a block while a condition remains true?", "if", "while loop", "return", "import", "B", "medium", "A while loop repeats while its condition evaluates to true."),
    ("Computer Science", "Programming Fundamentals", "What is the time complexity of a loop that visits each of n items once?", "O(1)", "O(log n)", "O(n)", "O(n²)", "C", "hard", "One constant-time operation per item gives linear time."),
    ("Computer Science", "Programming Fundamentals", "A recursive function must have a base case mainly to:", "Increase memory use", "Prevent recursion from continuing indefinitely", "Make every call slower", "Avoid parameters", "B", "extreme hard", "A base case stops recursive calls when the problem is sufficiently small."),
    # COMPUTER SCIENCE — Data Structures
    ("Computer Science", "Data Structures", "Which data structure follows LIFO?", "Queue", "Stack", "Tree", "Graph", "B", "easy", "A stack is Last In, First Out."),
    ("Computer Science", "Data Structures", "Which data structure follows FIFO?", "Stack", "Queue", "Heap", "Binary search tree", "B", "easy", "A queue is First In, First Out."),
    ("Computer Science", "Data Structures", "In a zero-indexed array, the first element is at index:", "0", "1", "−1", "Depends on the value", "A", "medium", "Zero-indexed arrays begin at index 0."),
    ("Computer Science", "Data Structures", "Binary search requires the input array to be:", "Randomly shuffled", "Sorted", "All negative", "A linked list only", "B", "medium", "Binary search eliminates half the search range based on sorted order."),
    ("Computer Science", "Data Structures", "A stack performs push and pop at the same end, called the:", "Front", "Rear", "Top", "Root", "C", "hard", "The stack top is where elements are inserted and removed."),
    ("Computer Science", "Data Structures", "In a min-heap, the key at each parent node is:", "Always larger than children", "No greater than its children", "Always equal to all leaves", "Always negative", "B", "extreme hard", "The min-heap property requires each parent key to be ≤ its child keys."),
    # COMPUTER SCIENCE — Algorithms
    ("Computer Science", "Algorithms", "An algorithm is:", "A computer brand", "A finite sequence of steps to solve a problem", "Only a programming language", "A storage device", "B", "easy", "An algorithm describes a finite, well-defined problem-solving procedure."),
    ("Computer Science", "Algorithms", "Which search algorithm checks items sequentially?", "Binary search", "Linear search", "Merge sort", "Dijkstra's algorithm", "B", "easy", "Linear search examines items one by one."),
    ("Computer Science", "Algorithms", "The worst-case time complexity of linear search over n items is:", "O(1)", "O(log n)", "O(n)", "O(n log n)", "C", "medium", "In the worst case, every item is checked."),
    ("Computer Science", "Algorithms", "Merge sort has typical worst-case time complexity:", "O(n)", "O(log n)", "O(n log n)", "O(n²)", "C", "medium", "Merge sort divides recursively and merges in linear work per level."),
    ("Computer Science", "Algorithms", "Dijkstra's standard algorithm assumes edge weights are:", "All negative", "Non-negative", "All equal to zero", "Strings only", "B", "hard", "Dijkstra's algorithm is correct with non-negative edge weights."),
    ("Computer Science", "Algorithms", "For a recurrence T(n)=2T(n/2)+n, the asymptotic solution is:", "O(log n)", "O(n)", "O(n log n)", "O(n²)", "C", "extreme hard", "The Master Theorem gives Θ(n log n) because each level does Θ(n) work over Θ(log n) levels."),
    # COMPUTER SCIENCE — Database Management
    ("Computer Science", "Database Management", "SQL is primarily used to:", "Style web pages", "Manage and query relational data", "Compile operating systems", "Edit images", "B", "easy", "SQL defines, queries, and manipulates relational databases."),
    ("Computer Science", "Database Management", "Which SQL command retrieves rows from a table?", "SELECT", "DELETE", "UPDATE", "DROP", "A", "easy", "SELECT retrieves data from one or more tables."),
    ("Computer Science", "Database Management", "A primary key must uniquely identify each row and cannot be:", "Indexed", "Null", "Numeric", "Referenced", "B", "medium", "A primary key is unique and non-null."),
    ("Computer Science", "Database Management", "Which clause filters rows before grouping?", "ORDER BY", "WHERE", "HAVING", "LIMIT only", "B", "medium", "WHERE filters rows before GROUP BY aggregation."),
    ("Computer Science", "Database Management", "The main purpose of database normalization is to reduce:", "Data consistency", "Redundancy and update anomalies", "All tables", "Query language", "B", "hard", "Normalization structures data to reduce duplication and anomalies."),
    ("Computer Science", "Database Management", "A relation is in BCNF if every non-trivial functional dependency X → Y has X as a:", "Foreign key only", "Superkey", "Non-key attribute", "Nullable field", "B", "extreme hard", "BCNF requires every determinant of a non-trivial dependency to be a superkey."),
    # COMPUTER SCIENCE — Computer Networks
    ("Computer Science", "Computer Networks", "Which device forwards packets between different IP networks?", "Hub", "Router", "Repeater", "Keyboard", "B", "easy", "Routers forward packets between networks using IP addresses."),
    ("Computer Science", "Computer Networks", "HTTP is an application-layer protocol used mainly for:", "Routing IP packets", "Transferring web resources", "Allocating memory", "Encrypting hard drives", "B", "easy", "HTTP is used for communication between web clients and servers."),
    ("Computer Science", "Computer Networks", "Which protocol provides reliable, ordered byte-stream delivery?", "UDP", "TCP", "IP", "ARP", "B", "medium", "TCP provides reliable, ordered delivery with retransmission and sequencing."),
    ("Computer Science", "Computer Networks", "An IPv4 address contains how many bits?", "16", "32", "64", "128", "B", "medium", "IPv4 addresses are 32 bits long."),
    ("Computer Science", "Computer Networks", "Which OSI layer is responsible for end-to-end transport services?", "Physical", "Network", "Transport", "Data Link", "C", "hard", "The transport layer provides end-to-end services such as TCP and UDP."),
    ("Computer Science", "Computer Networks", "How many usable host addresses are in a typical IPv4 /26 subnet?", "30", "62", "64", "126", "B", "extreme hard", "A /26 leaves 6 host bits: 2⁶ = 64 addresses, minus network and broadcast = 62 usable."),
]

def seed_questions():
    db = SessionLocal()
    added = 0
    skipped_existing = 0
    skipped_missing_topic = set()

    try:
        for row in QUESTION_BANK:
            subject, topic_name, question_text, a, b, c, d, answer, difficulty, explanation = row
            topic = (
                db.query(Topic)
                .filter(Topic.name == topic_name, Topic.subject == subject)
                .first()
            )

            if topic is None:
                skipped_missing_topic.add(f"{subject} / {topic_name}")
                continue

            duplicate = (
                db.query(Question)
                .filter(
                    Question.topic_id == topic.id,
                    Question.question_text == question_text,
                )
                .first()
            )
            if duplicate:
                skipped_existing += 1
                continue

            question = Question(
                question_text=question_text,
                option_a=a,
                option_b=b,
                option_c=c,
                option_d=d,
                correct_answer=answer,
                difficulty=difficulty,
                explanation=explanation,
                topic_id=topic.id,
            )
            db.add(question)
            added += 1

        db.commit()
        print(f"New questions added: {added}")
        print(f"Duplicates skipped: {skipped_existing}")
        if skipped_missing_topic:
            print("Topics not found (those questions were skipped):")
            for topic_label in sorted(skipped_missing_topic):
                print(f"  - {topic_label}")
        print("\nQuestion counts by subject and difficulty:")
        from sqlalchemy import func
        rows = (
            db.query(Topic.subject, Question.difficulty, func.count(Question.id))
            .join(Question, Question.topic_id == Topic.id)
            .group_by(Topic.subject, Question.difficulty)
            .order_by(Topic.subject, Question.difficulty)
            .all()
        )
        for subject, difficulty, count in rows:
            print(f"  {subject} | {difficulty}: {count}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_questions()
