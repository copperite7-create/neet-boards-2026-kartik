import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///roadmap.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default='Student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StudyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_number = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    phase = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(20), nullable=False)  # biology, chemistry, physics, english, test
    block = db.Column(db.String(100))  # e.g. "B1", "B2"
    time_start = db.Column(db.String(10))
    time_end = db.Column(db.String(10))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    target = db.Column(db.String(500))  # e.g. "50 MCQs", "30 numericals"
    completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<Day {self.day_number} {self.subject} {self.title}>'

with app.app_context():
    db.create_all()

DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
START_DATE = datetime(2026, 8, 17)  # Sunday, Aug 17 2026

def get_date_for_day(day_number):
    return START_DATE + timedelta(days=day_number - 1)

def get_day_of_week(day_number):
    dt = get_date_for_day(day_number)
    return DAYS_OF_WEEK[dt.weekday()] if dt.weekday() < 6 else 'Sunday'

# ============================================================
# PHASE 1: ZERO -> FOUNDATION (Days 1-21)
# ============================================================
PHASE_1_TASKS = []

# Day 1
PHASE_1_TASKS.extend([
    (1, 'biology', 'B1', '7:30-9:30', 'Cellular Division & Genetics Basics',
     'Concepts: Mitosis vs Meiosis, Chromosomes, Genes, Alleles, Genotype/Phenotype',
     '30 basic MCQs + NCERT Reading'),
    (1, 'chemistry', 'B2', '9:45-11:15', 'GOC Foundation',
     'Concepts: Bond fission, Electrophile, Nucleophile, Carbocation, Resonance, Inductive effect',
     '25-30 questions on GOC basics'),
    (1, 'physics', 'B3', '11:45-1:15', 'Mathematical Foundation',
     'Units, Dimensions, Vectors, Basic Algebra & Trigonometry, Graphs',
     '20 questions on math basics + start Electric Charges & Fields'),
    (1, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 15 Physics + 20 Chemistry + 25 Biology questions',
     'Complete 55+ mixed questions'),
    (1, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Close books, explain what you learned. Mark understood/understood-later.',
     'Daily recall of today\'s concepts'),
    (1, 'english', 'B6', '7:30-8:15', 'English - Literature',
     'Reading comprehension + grammar',
     'Complete 1 passage + 10 grammar questions'),
])

# Day 2
PHASE_1_TASKS.extend([
    (2, 'biology', 'B1', '7:30-9:30', 'Principles of Inheritance',
     'Mendel\'s Laws, Monohybrid Cross, Dominance, Segregation',
     '40 MCQs + NCERT 13.1-13.3'),
    (2, 'chemistry', 'B2', '9:45-11:15', 'GOC - Resonance & Effects',
     'Resonance, Hyperconjugation, Electromeric Effect, Acidic Strength',
     '25-30 questions on reactions and stability'),
    (2, 'physics', 'B3', '11:45-1:15', 'Electric Charges & Fields',
     'Charge, Coulomb\'s Law, Superposition, Electric Field',
     '20 numerical problems'),
    (2, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 20 Biology + 15 Chemistry + 15 Physics',
     'Complete 50+ mixed questions'),
    (2, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain Mendel\'s laws and GOC concepts without books',
     'Identify weak areas'),
    (2, 'english', 'B6', '7:30-8:15', 'English - Reading',
     'Reading comprehension practice',
     'Complete 1 long passage + vocabulary'),
])

# Day 3
PHASE_1_TASKS.extend([
    (3, 'biology', 'B1', '7:30-9:30', 'Dihybrid Cross & Independent Assortment',
     'Mendel\'s Dihybrid Cross, Test Cross, Principle of Independent Assortment',
     '50 MCQs + NCERT 13.4'),
    (3, 'chemistry', 'B2', '9:45-11:15', 'GOC - Reaction Mechanisms',
     'Organic reaction types, SN1/SN2, Addition, Elimination, Redox',
     '25 reaction mechanism questions'),
    (3, 'physics', 'B3', '11:45-1:15', 'Electric Field & Gauss Law',
     'Field due to point charge, dipole, field lines, flux',
     '20 numerical problems'),
    (3, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 25 Biology + 20 Chemistry + 15 Physics',
     'Complete 60+ mixed questions'),
    (3, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain dihybrid cross and reaction mechanisms',
     'Daily recall notes'),
])

# Day 4
PHASE_1_TASKS.extend([
    (4, 'biology', 'B1', '7:30-9:30', 'Codominance & Blood Groups',
     'Codominance, Incomplete Dominance, Multiple Alleles, ABO Blood Groups',
     '40 MCQs + NCERT 13.5-13.6'),
    (4, 'chemistry', 'B2', '9:45-11:15', 'Haloalkanes - Foundation',
     'Classification, Nomenclature, C-X Bond, Preparation (SN1/SN2)',
     '30 reaction questions'),
    (4, 'physics', 'B3', '11:45-1:15', 'Gauss Law & Applications',
     'Spherical symmetry, cylindrical symmetry, applications',
     '20 numerical problems'),
    (4, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 20 Biology + 25 Chemistry + 15 Physics',
     'Complete 60+ mixed questions'),
    (4, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain codominance and haloalkane reactions',
     'Mark weak concepts'),
])

# Day 5
PHASE_1_TASKS.extend([
    (5, 'biology', 'B1', '7:30-9:30', 'Sex Determination & Linkage',
     'Sex determination, genetic linkage, recombination frequency',
     '40 MCQs + NCERT 13.7'),
    (5, 'chemistry', 'B2', '9:45-11:15', 'Haloalkanes - SN1/SN2 Reactions',
     'Nucleophilic substitution mechanisms, elimination, stereochemistry',
     '25 reaction mechanism questions'),
    (5, 'physics', 'B3', '11:45-1:15', 'Electrostatic Potential',
     'Potential difference, potential due to charge, equipotential surfaces',
     '20 numerical problems'),
    (5, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 20 Biology + 20 Chemistry + 15 Physics',
     'Complete 55+ mixed questions'),
    (5, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain linkage and SN1/SN2 differences',
     'Daily recall'),
    (5, 'english', 'B6', '7:30-8:15', 'English - Writing',
     'Formal letter writing + paragraph writing',
     'Write 1 letter + 1 paragraph'),
])

# Day 6
PHASE_1_TASKS.extend([
    (6, 'biology', 'B1', '7:30-9:30', 'Genetic Disorders',
     'Haemophilia, Color blindness, Thalassemia, Sickle cell, Down/Turner/Klinefelter',
     '50 MCQs + NCERT 14.1-14.4'),
    (6, 'chemistry', 'B2', '9:45-11:15', 'Haloalkanes - Revision & Practice',
     'Complete chapter + solve 50 MCQs/reaction questions',
     '50 comprehensive questions'),
    (6, 'chemistry', 'B3', '11:45-1:15', 'Haloalkanes Review',
     'Review all reactions + common mistakes',
     'Identify weak areas in reactions'),
    (6, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 30 Biology + 25 Chemistry + 20 Physics',
     'Complete 75+ mixed questions'),
    (6, 'physics', 'B5', '3:30-4:30', 'Capacitors',
     'Combination, Energy, Dielectric, Numerical problems',
     '20 numerical problems'),
    (6, 'english', 'B6', '7:30-8:15', 'English - Literature Review',
     'Poetry comprehension + prose summary',
     'Complete 2 passages + summary'),
])

# Day 7 - Week 1 Assessment
PHASE_1_TASKS.extend([
    (7, 'biology', 'B1', '7:30-9:00', 'WEEK 1 TEST - BIOLOGY',
     'Test on Mendel\'s laws, GOC, Genetic disorders, Blood groups, Linkage',
     '60 MCQs under timed conditions'),
    (7, 'chemistry', 'B2', '9:30-11:00', 'WEEK 1 TEST - CHEMISTRY',
     'Test on GOC, Haloalkanes, reaction mechanisms',
     '40 questions under timed conditions'),
    (7, 'physics', 'B3', '11:30-1:00', 'WEEK 1 TEST - PHYSICS',
     'Test on Electric charges, fields, Gauss law, potential',
     '30 numericals + 10 MCQs'),
    (7, 'biology', 'B4', '2:00-4:00', 'TEST ANALYSIS',
     'Analyze weak areas, errors, time management',
     'Score: Bio ___/60, Chem ___/40, Physics ___/40'),
    (7, 'english', 'B6', '7:30-8:15', 'English - Weekly Revision',
     'Review week\'s grammar + comprehension',
     'Complete 2 passages'),
])

# Day 8
PHASE_1_TASKS.extend([
    (8, 'biology', 'B1', '7:30-9:30', 'Molecular Basis - DNA Structure',
     'Watson-Crick model, Base pairing, Antiparallel strands, Functions',
     '40 MCQs + NCERT 6.1-6.2'),
    (8, 'chemistry', 'B2', '9:45-11:15', 'Alcohols - Foundation',
     'Classification, Nomenclature, Physical properties, Preparation',
     '30 questions'),
    (8, 'physics', 'B3', '11:45-1:15', 'Current Electricity Basics',
     'Current, Drift velocity, Resistance, Ohm\'s law, Resistivity',
     '20 numerical problems'),
    (8, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 25 Biology + 20 Chemistry + 15 Physics',
     'Complete 60+ mixed questions'),
    (8, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain DNA structure and alcohol properties',
     'Daily recall'),
])

# Day 9
PHASE_1_TASKS.extend([
    (9, 'biology', 'B1', '7:30-9:30', 'DNA Replication',
     'Mechanism, Enzymes involved, Semi-conservative replication',
     '40 MCQs + NCERT 6.3'),
    (9, 'chemistry', 'B2', '9:45-11:15', 'Alcohols - Chemical Properties',
     'Acidity, Esterification, Oxidation, Dehydration reactions',
     '25 reaction questions'),
    (9, 'physics', 'B3', '11:45-1:15', 'Resistors & Networks',
     'Series/parallel combinations, Temperature dependence',
     '20 numerical problems'),
    (9, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 20 Biology + 25 Chemistry + 15 Physics',
     'Complete 60+ mixed questions'),
    (9, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain replication and alcohol reactions',
     ''),
])

# Day 10
PHASE_1_TASKS.extend([
    (10, 'biology', 'B1', '7:30-9:30', 'Transcription & RNA Processing',
     'Transcription mechanism, RNA types, processing in eukaryotes',
     '40 MCQs + NCERT 6.4-6.5'),
    (10, 'chemistry', 'B2', '9:45-11:15', 'Phenols - Properties & Reactions',
     'Acidity, Electrophilic substitution, Uses',
     '30 reaction questions'),
    (10, 'physics', 'B3', '11:45-1:15', 'Kirchhoff\'s Laws & Applications',
     'KVL, KCL, Wheatstone bridge, Potentiometer',
     '20 numerical problems'),
    (10, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 25 Biology + 25 Chemistry + 15 Physics',
     'Complete 65+ mixed questions'),
    (10, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain transcription and phenol reactions',
     ''),
])

# Day 11
PHASE_1_TASKS.extend([
    (11, 'biology', 'B1', '7:30-9:30', 'Translation & Genetic Code',
     'Translation mechanism, tRNA, rRNA, Genetic code degeneracy',
     '40 MCQs + NCERT 6.6-6.7'),
    (11, 'chemistry', 'B2', '9:45-11:15', 'Ethers - Properties & Reactions',
     'Nomenclature, Preparation (Williamson), Physical properties',
     '25 questions'),
    (11, 'physics', 'B3', '11:45-1:15', 'Metre Bridge & Potentiometer',
     'Practical applications, measurements',
     '20 numerical problems'),
    (11, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 20 Biology + 20 Chemistry + 20 Physics',
     'Complete 60+ mixed questions'),
    (11, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain translation and ether preparation',
     ''),
    (11, 'english', 'B6', '7:30-8:15', 'English - Literature',
     'Poetry analysis + prose summary',
     'Complete 1 poem + 1 prose summary'),
])

# Day 12
PHASE_1_TASKS.extend([
    (12, 'biology', 'B1', '7:30-9:30', 'Gene Expression & Regulation',
     'Gene expression, operon concept (Lac, Trp), regulation',
     '40 MCQs + NCERT 6.8-6.9'),
    (12, 'chemistry', 'B2', '9:45-11:15', 'Aldehydes - Foundation',
     'Carbonyl group, Nomenclature, Preparation, Properties',
     '30 questions'),
    (12, 'physics', 'B3', '11:45-1:15', 'Moving Charges & Magnetism',
     'Biot-Savart law, Ampere\'s law, Solenoid, Toroid',
     '20 numerical problems'),
    (12, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 25 Biology + 25 Chemistry + 15 Physics',
     'Complete 65+ mixed questions'),
    (12, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain operon regulation and aldehyde reactions',
     ''),
])

# Day 13
PHASE_1_TASKS.extend([
    (13, 'biology', 'B1', '7:30-9:30', 'DNA Fingerprinting & Human Genome',
     'Mutation, DNA fingerprinting techniques, HGP, applications',
     '40 MCQs + NCERT summary'),
    (13, 'chemistry', 'B2', '9:45-11:15', 'Aldehydes/Ketones - Reactions',
     'Nucleophilic addition, Oxidation, Reduction, Wolff-Kishner',
     '25 reaction questions'),
    (13, 'physics', 'B3', '11:45-1:15', 'Ampere\'s Law & Applications',
     'Applications of Ampere\'s law, Solenoid, Toroid, Cyclotron',
     '20 numerical problems'),
    (13, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 20 Biology + 20 Chemistry + 20 Physics',
     'Complete 60+ mixed questions'),
    (13, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain DNA fingerprinting and ketone reactions',
     ''),
])

# Day 14 - Week 2 Assessment
PHASE_1_TASKS.extend([
    (14, 'biology', 'B1', '7:30-9:30', 'WEEK 2 TEST - BIOLOGY',
     'Test on Molecular basis, DNA replication, transcription, translation',
     '80 MCQs under timed conditions'),
    (14, 'chemistry', 'B2', '9:45-11:15', 'WEEK 2 TEST - CHEMISTRY',
     'Test on Alcohols, Phenols, Ethers, Aldehydes',
     '50 questions under timed conditions'),
    (14, 'physics', 'B3', '11:45-1:15', 'WEEK 2 TEST - PHYSICS',
     'Test on Current electricity, Magnetism',
     '40 numericals + 10 MCQs'),
    (14, 'biology', 'B4', '2:00-4:00', 'TEST ANALYSIS',
     'Analyze errors, weak chapters, time management',
     'Score: Bio ___/80, Chem ___/50, Physics ___/50'),
    (14, 'english', 'B6', '7:30-8:15', 'English - Weekly Revision',
     'Review week\'s grammar + comprehension',
     'Complete 2 passages'),
])

# Day 15
PHASE_1_TASKS.extend([
    (15, 'biology', 'B1', '7:30-9:30', 'Molecular Basis - Mutations & Applications',
     'Mutation types, DNA repair, DNA fingerprinting, HGP, biotechnology',
     '40 MCQs + NCERT review'),
    (15, 'chemistry', 'B2', '9:45-11:15', 'Aldehydes/Ketones - NCERT + PYQs',
     'Complete NCERT examples + Previous year questions',
     '30 PYQs + 20 reaction questions'),
    (15, 'physics', 'B3', '11:45-1:15', 'Magnetic Field & Sources',
     'Moving charges, Biot-Savart, Ampere\'s law, numericals',
     '20 numerical problems'),
    (15, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 20 Biology + 25 Chemistry + 20 Physics',
     'Complete 65+ mixed questions'),
    (15, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain mutation mechanisms and aldehyde PYQs',
     ''),
])

# Day 16
PHASE_1_TASKS.extend([
    (16, 'biology', 'B1', '7:30-9:30', 'Human Reproduction',
     'Male/female reproductive system, Gametogenesis, Hormones',
     '40 MCQs + NCERT 4.1-4.4'),
    (16, 'chemistry', 'B2', '9:45-11:15', 'Carboxylic Acids - Properties',
     'Acidity, Preparation, Reactions, Uses',
     '30 reaction questions'),
    (16, 'physics', 'B3', '11:45-1:15', 'Magnetism & Matter',
     'Bar magnet, Earth\'s magnetism, properties of materials',
     '20 numerical problems'),
    (16, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 25 Biology + 20 Chemistry + 15 Physics',
     'Complete 60+ mixed questions'),
    (16, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain gametogenesis and carboxylic acid reactions',
     ''),
    (16, 'english', 'B6', '7:30-8:15', 'English - Reading',
     'Reading comprehension + vocabulary',
     'Complete 1 long passage'),
])

# Day 17
PHASE_1_TASKS.extend([
    (17, 'biology', 'B1', '7:30-9:30', 'Reproductive Health',
     'Population explosion, birth control, STIs, infertility',
     '40 MCQs + NCERT 4.5-4.7'),
    (17, 'chemistry', 'B2', '9:45-11:15', 'Amines - Classification & Prep',
     'Classification, Nomenclature, Preparation, Physical properties',
     '25 questions'),
    (17, 'physics', 'B3', '11:45-1:15', 'Electromagnetic Induction',
     'Faraday\'s law, Lenz\'s law, Motional EMF, Eddy currents',
     '20 numerical problems'),
    (17, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 20 Biology + 25 Chemistry + 15 Physics',
     'Complete 60+ mixed questions'),
    (17, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain reproductive health and amine preparation',
     ''),
])

# Day 18
PHASE_1_TASKS.extend([
    (18, 'biology', 'B1', '7:30-9:30', 'Sexual Reproduction in Plants',
     'Flower structure, Micro/Macrosporogenesis, Pollen, Double fertilization',
     '40 MCQs + NCERT 2.1-2.4'),
    (18, 'chemistry', 'B2', '9:45-11:15', 'Amines - Reactions & Uses',
     'Basic reactions, Diazonium salts, Reactions, Uses',
     '25 reaction questions'),
    (18, 'physics', 'B3', '11:45-1:15', 'EMI - Applications',
     'Self inductance, RL circuits, AC generator',
     '20 numerical problems'),
    (18, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 25 Biology + 20 Chemistry + 15 Physics',
     'Complete 60+ mixed questions'),
    (18, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain plant reproduction and diazonium reactions',
     ''),
])

# Day 19
PHASE_1_TASKS.extend([
    (19, 'biology', 'B1', '7:30-9:30', 'Plant Reproduction - Pollination & Seeds',
     'Pollination, Fertilization, Seed and Fruit Development, Apomixis',
     '40 MCQs + NCERT 2.5-2.6'),
    (19, 'chemistry', 'B2', '9:45-11:15', 'Biomolecules - Carbohydrates',
     'Classification, Structure, Functions, Glycosidic linkage',
     '25 questions'),
    (19, 'physics', 'B3', '11:45-1:15', 'Alternating Current',
     'AC representation, Peak/RMS values, Phase relationship',
     '20 numerical problems'),
    (19, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 20 Biology + 25 Chemistry + 20 Physics',
     'Complete 65+ mixed questions'),
    (19, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain fertilization and biomolecules',
     ''),
    (19, 'english', 'B6', '7:30-8:15', 'English - Writing',
     'Formal letter + paragraph writing',
     'Write 1 letter + 1 paragraph'),
])

# Day 20
PHASE_1_TASKS.extend([
    (20, 'biology', 'B1', '7:30-9:30', 'Plant Reproduction - Advanced',
     'Seed development, Fruit formation, Apomixis, Polyembryony',
     '40 MCQs + NCERT review'),
    (20, 'chemistry', 'B2', '9:45-11:15', 'Biomolecules - Proteins & Enzymes',
     'Protein structure, Enzymes, Co-enzymes, Catalysis',
     '25 questions'),
    (20, 'physics', 'B3', '11:45-1:15', 'Ray Optics - Introduction',
     'Ray optics basics, Reflection, Refraction, Mirrors',
     '20 numerical problems'),
    (20, 'biology', 'B4', '2:15-3:15', 'Question Practice',
     'Daily practice: 25 Biology + 20 Chemistry + 15 Physics',
     'Complete 60+ mixed questions'),
    (20, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
     'Explain apomixis and enzyme catalysis',
     ''),
])

# Day 21 - Phase 1 Major Assessment
PHASE_1_TASKS.extend([
    (21, 'biology', 'B1', '7:30-10:00', 'MAJOR ASSESSMENT - BIOLOGY',
     'Full test on all completed chapters: Inheritance, Molecular basis, Reproduction',
     '100 MCQs under timed conditions'),
    (21, 'chemistry', 'B2', '10:30-12:00', 'MAJOR ASSESSMENT - CHEMISTRY',
     'Full test on GOC, Haloalkanes, Alcohols, Aldehydes, Amines, Biomolecules',
     '60 questions under timed conditions'),
    (21, 'physics', 'B3', '1:00-2:30', 'MAJOR ASSESSMENT - PHYSICS',
     'Full test on Electrostatics, Current, Magnetism, EMI, AC',
     '50 numericals + 20 MCQs'),
    (21, 'biology', 'B4', '3:00-5:00', 'COMPREHENSIVE ANALYSIS',
     'Analyze all weak areas, errors, knowledge gaps',
     'Bio: ___/100, Chem: ___/60, Physics: ___/70'),
    (21, 'english', 'B6', '7:30-8:15', 'English - Reading Comprehension',
     'Full comprehension test',
     'Complete 2 passages + summary'),
])

# ============================================================
# PHASE 2: SYLLABUS COMPLETION (Days 22-42)
# ============================================================
PHASE_2_TASKS = []

phase2_chapters = {
    'biology': [
        'Genetics & Evolution: Principles of Inheritance, Molecular Basis, Evolution',
        'Reproduction: Sexual Reproduction, Human Reproduction, Reproductive Health',
        'Biology & Human Welfare: Human Health & Disease, Microbes in Human Welfare',
        'Biotechnology: Principles & Processes, Applications',
        'Ecology: Organisms & Populations, Ecosystem, Biodiversity & Conservation',
    ],
    'chemistry': [
        'Electrochemistry: Redox, Conductance, Corrosion',
        'Chemical Kinetics: Rate laws, Order, Half-life',
        'd & f Block: Properties, Preparation, Uses',
        'Coordination Compounds: Structure, Bonding, Isomerism',
        'Solutions: Colligative properties, Osmosis',
        'Biomolecules: Nutrition, Vitamins, Hormones',
    ],
    'physics': [
        'Wave Optics: Huygens principle, Interference, Diffraction',
        'Semiconductors: Diodes, Transistors, Logic gates',
        'Atoms: Rutherford, Bohr model, X-rays',
        'Nuclei: Radioactivity, Binding energy, Decay',
        'Communication Systems: Basic concepts',
    ]
}

# Generate Phase 2 tasks (Days 22-42)
for day_num in range(22, 43):
    day_offset = day_num - 22
    week_num = day_offset // 7 + 1
    day_in_week = day_offset % 7  # 0-6 (Mon-Sun)
    
    dow = DAYS_OF_WEEK[day_in_week] if day_in_week < 6 else 'Sunday'
    
    if dow == 'Sunday':
        # Weekly test
        PHASE_2_TASKS.extend([
            (day_num, 'biology', 'B1', '7:30-9:30', f'WEEK {week_num} TEST - BIOLOGY',
             f'Test on chapters completed this week',
             '100 MCQs + 2 long answers'),
            (day_num, 'chemistry', 'B2', '10:00-11:30', f'WEEK {week_num} TEST - CHEMISTRY',
             f'Test on chapters completed this week',
             '50 questions'),
            (day_num, 'physics', 'B3', '12:00-1:30', f'WEEK {week_num} TEST - PHYSICS',
             f'Test on chapters completed this week',
             '40 numericals + 10 MCQs'),
            (day_num, 'biology', 'B4', '2:30-4:30', 'TEST ANALYSIS & REVISION',
             f'Analyze errors and weak areas',
             f'Score recording + error notebook update'),
        ])
    else:
        # Daily study
        bio_ch = phase2_chapters['biology'][min(day_offset % len(phase2_chapters['biology']), 4)]
        chem_ch = phase2_chapters['chemistry'][min(day_offset % len(phase2_chapters['chemistry']), 5)]
        phys_ch = phase2_chapters['physics'][min(day_offset % len(phase2_chapters['physics']), 4)]
        
        PHASE_2_TASKS.extend([
            (day_num, 'biology', 'B1', '7:30-9:30', f'Biology: {bio_ch}',
             f'Complete lecture + NCERT reading + concept mapping',
             '50 MCQs + diagram practice + short notes'),
            (day_num, 'chemistry', 'B2', '9:45-11:15', f'Chemistry: {chem_ch}',
             f'Complete concept + reactions + NCERT + examples',
             '30 reaction questions + 20 MCQs'),
            (day_num, 'physics', 'B3', '11:45-1:15', f'Physics: {phys_ch}',
             f'Concepts + formulas + derivations + numericals',
             '20 numerical problems + 10 MCQs'),
            (day_num, 'biology', 'B4', '2:15-3:15', 'Question Practice',
             'Daily practice across all subjects',
             '40 Biology + 25 Chemistry + 20 Physics = 85 questions'),
            (day_num, 'biology', 'B5', '3:30-4:30', 'Revision & Recall',
             'Explain today\'s concepts without books',
             'Update mistake notebook + formula cards'),
        ])
        
        if day_offset % 4 == 3:
            PHASE_2_TASKS.append((day_num, 'english', 'B6', '7:30-8:15', 'English - Writing',
                                 'Formal letter + paragraph writing',
                                 'Write 1 letter + 1 paragraph'))
        elif day_offset % 6 == 5:
            PHASE_2_TASKS.append((day_num, 'english', 'B6', '7:30-8:15', 'English - Literature',
                                 'Poetry comprehension + prose summary',
                                 'Complete 1 poem + 1 prose summary'))

# ============================================================
# PHASE 3: FIRST REVISION (Days 43-60)
# ============================================================
PHASE_3_TASKS = []

phase3_biology = ['Reproduction', 'Genetics', 'Molecular Basis', 'Evolution', 
                  'Human Health', 'Biotechnology', 'Biology & Human Welfare', 'Ecology']
phase3_chemistry = ['Solid State', 'Solutions', 'Electrochemistry', 'Chemical Kinetics',
                    'Surface Chemistry', 'p-Block', 'd&f-Block', 'Coordination Compounds',
                    'Haloalkanes', 'Alcohols', 'Aldehydes', 'Carboxylic Acids', 'Amines',
                    'Nitro Compounds', 'Biomolecules', 'Polymers']
phase3_physics = ['Ray Optics', 'Wave Optics', 'Electromagnetic Waves', 'Dual Nature',
                  'Atoms', 'Nuclei', 'Semiconductors', 'Communication Systems']

for day_num in range(43, 61):
    day_offset = day_num - 43
    dow = DAYS_OF_WEEK[(START_DATE + timedelta(days=day_num - 1)).weekday()]
    
    if dow == 'Sunday':
        PHASE_3_TASKS.extend([
            (day_num, 'biology', 'B1', '7:30-9:00', 'CHAPTER TEST - BIOLOGY',
             'Test on chapters covered in this week\'s revision',
             '100 MCQs + 3 diagram-based questions'),
            (day_num, 'chemistry', 'B2', '9:30-11:00', 'CHAPTER TEST - CHEMISTRY',
             'Test on chapters covered in this week\'s revision',
             '60 questions + 20 NCERT-based questions'),
            (day_num, 'physics', 'B3', '11:30-1:00', 'CHAPTER TEST - PHYSICS',
             'Test on chapters covered in this week\'s revision',
             '40 numericals + 15 MCQs'),
            (day_num, 'biology', 'B4', '2:00-4:00', 'TEST ANALYSIS + PYQ SESSION',
             'Analyze errors and solve previous year questions',
             'Update mistake notebook'),
        ])
    else:
        bio_idx = min(day_offset % len(phase3_biology), 7)
        chem_idx = min(day_offset % len(phase3_chemistry), 15)
        phys_idx = min(day_offset % len(phase3_physics), 7)
        
        PHASE_3_TASKS.extend([
            (day_num, 'biology', 'B1', '7:30-9:00', f'Revision: {phase3_biology[bio_idx]}',
             'NCERT highlight + Concept mapping + PYQs from 2019-23',
             '50 MCQs + 2 long answer practice + diagram revision'),
            (day_num, 'chemistry', 'B2', '9:30-11:00', f'Revision: {phase3_chemistry[chem_idx]}',
             'NCERT revision + Reaction summary + PYQs from 2019-23',
             '40 reaction questions + 20 MCQs'),
            (day_num, 'physics', 'B3', '11:30-1:00', f'Revision: {phase3_physics[phys_idx]}',
             'Formula revision + Derivation practice + PYQs from 2019-23',
             '30 numericals + 10 important questions'),
            (day_num, 'biology', 'B4', '2:00-3:30', 'PYQ SESSION',
             'Solve 2019-23 board PYQs for all three subjects',
             '50 Biology + 40 Chemistry + 30 Physics PYQs'),
            (day_num, 'biology', 'B5', '3:30-4:30', 'MISTAKE NOTEBOOK',
             'Review errors from tests + PYQs + update formula cards',
             'Write 10 mistakes + corrections'),
        ])

# ============================================================
# PHASE 4: BOARD ATTACK (Days 61-75)
# ============================================================
PHASE_4_TASKS = []

for day_num in range(61, 76):
    day_offset = day_num - 61
    dow = DAYS_OF_WEEK[(START_DATE + timedelta(days=day_num - 1)).weekday()]
    
    if day_offset % 7 == 6:  # Sunday
        PHASE_4_TASKS.extend([
            (day_num, 'biology', 'B1', '7:30-10:00', 'BOARD-STYLE FULL TEST',
             'Full syllabus test with board marking scheme',
             '120 MCQs + 10 long answer + diagrams'),
            (day_num, 'chemistry', 'B2', '10:30-12:00', 'BOARD-STYLE FULL TEST',
             'Full chemistry test with NCERT-based questions',
             '70 questions with solutions'),
            (day_num, 'physics', 'B3', '12:30-2:00', 'BOARD-STYLE FULL TEST',
             'Full physics test with derivations + numericals',
             '50 questions + 10 derivations'),
            (day_num, 'biology', 'B4', '3:00-5:00', 'FULL TEST ANALYSIS',
             'Detailed analysis with marking scheme',
             'Score: Bio ___%, Chem ___%, Physics ___%'),
        ])
    else:
        PHASE_4_TASKS.extend([
            (day_num, 'biology', 'B1', '7:30-9:00', f'Answer Writing Practice - {phase3_biology[day_offset % 8]}',
             'Write 2-3 long answers with diagrams in board format',
             'Focus on marks distribution + keyword usage'),
            (day_num, 'chemistry', 'B2', '9:30-11:00', f'Short Answer Practice - {phase3_chemistry[day_offset % 16]}',
             'Write reactions + mechanisms + short answers',
             'Follow NCERT marks distribution'),
            (day_num, 'physics', 'B3', '11:30-1:00', f'Derivation + Numerical Practice',
             f'Derivations from {phase3_physics[day_offset % 8]}',
             '5 derivations + 15 numericals with solutions'),
            (day_num, 'biology', 'B4', '2:00-3:30', 'Sample Paper Practice',
             'Complete 1 subject paper in 3 hours with strict timing',
             'Time yourself + check with marking scheme'),
            (day_num, 'biology', 'B5', '3:30-4:30', 'Weak Chapter Fix',
             'Target: fix identified weak areas from test analysis',
             '50 targeted questions + NCERT revision'),
        ])

# ============================================================
# PHASE 5: NEET ATTACK (Days 76-95)
# ============================================================
PHASE_5_TASKS = []

for day_num in range(76, 96):
    day_offset = day_num - 76
    dow = DAYS_OF_WEEK[(START_DATE + timedelta(days=day_num - 1)).weekday()]
    
    if day_offset % 7 == 6:  # Sunday
        PHASE_5_TASKS.extend([
            (day_num, 'biology', 'B1', '7:30-11:00', 'NEET MOCK - BIOLOGY',
             'Full Biology test: 180 MCQs in 3 hours',
             'NEET-pattern questions from all chapters'),
            (day_num, 'chemistry', 'B2', '11:30-2:00', 'NEET MOCK - CHEMISTRY',
             'Full Chemistry: 75 MCQs + 35 numericals in 3 hours',
             'NEET-pattern questions'),
            (day_num, 'physics', 'B3', '3:00-6:00', 'NEET MOCK - PHYSICS',
             'Full Physics: 50 MCQs + 30 numericals in 3 hours',
             'NEET-pattern questions'),
            (day_num, 'biology', 'B4', '7:00-9:00', 'MOCK ANALYSIS',
             'Detailed analysis of all 3 papers',
             'Score: Bio ___%, Chem ___%, Physics ___%'),
        ])
    else:
        PHASE_5_TASKS.extend([
            (day_num, 'biology', 'B1', '7:30-9:30', 'NEET MCQ Practice - Biology',
             f'Daily target: 120 MCQs from Chapter Complete + NEET prep',
             'Focus on NCERT-based + statement-based questions'),
            (day_num, 'chemistry', 'B2', '10:00-11:30', 'NEET MCQ Practice - Chemistry',
             f'Daily target: 80 MCQs + 40 reaction questions',
             'Focus on MCQs + reaction speed + accuracy'),
            (day_num, 'physics', 'B3', '12:00-2:00', 'NEET MCQ + Numerical Practice',
             f'Daily target: 50 numericals + 30 MCQs',
             'Focus on problem-solving speed + formula application'),
            (day_num, 'biology', 'B4', '3:00-4:00', 'NEET Weak Area Fixing',
             'Target chapters with <70% accuracy',
             '50 targeted MCQs + NCERT revision'),
            (day_num, 'biology', 'B5', '4:00-4:30', 'Formula/MCQ Revision',
             'Revise formula cards + high-weightage topics',
             'Update mistake notebook'),
        ])

# ============================================================
# PHASE 6: FINAL REVISION (Days 96-105)
# ============================================================
PHASE_6_TASKS = []

final_revision_subjects = ['Biology', 'Chemistry', 'Physics']
final_revision_materials = ['NCERT Lines', 'Formula Cards', 'MCQ Revision', 'Reaction Summary']

for day_num in range(96, 106):
    day_offset = day_num - 96
    subject = final_revision_subjects[day_offset % 3]
    material = final_revision_materials[day_offset % 4]
    
    PHASE_6_TASKS.extend([
        (day_num, 'biology' if subject == 'Biology' else 'chemistry' if subject == 'Chemistry' else 'physics', 
         'B1', '7:30-10:30', f'FINAL REVISION - {subject}: {material}',
         f'Intensive revision of {subject} using {material}',
         f'Complete NCERT review + formula cards + 200 MCQs'),
        (day_num, 'biology' if subject == 'Biology' else 'chemistry' if subject == 'Chemistry' else 'physic',
         'B2', '11:00-1:00', f'Subject Mix - Weak Topic Fixing',
         f'Solve previous weak topics across all subjects',
         f'50 Biology + 50 Chemistry + 50 Physics targeted questions'),
        (day_num, 'biology' if subject == 'Biology' else 'chemistry' if subject == 'Chemistry' else 'physics',
         'B3', '2:00-4:00', f'Revision Test - {subject}',
         f'Short test on today\'s revision topics',
         f'30 Biology + 30 Chemistry + 30 Physics questions'),
        (day_num, 'biology', 'B4', '4:30-5:30', 'MISTAKE NOTEBOOK FINAL REVIEW',
         'Review all mistakes from entire preparation',
         'Write 20 most important corrections'),
    ])

# ============================================================
# PHASE 7: FINAL PREP (Days 106-120)
# ============================================================
PHASE_7_TASKS = []

for day_num in range(106, 121):
    day_offset = day_num - 106
    dow = DAYS_OF_WEEK[(START_DATE + timedelta(days=day_num - 1)).weekday()]
    
    if day_offset % 7 == 6:  # Sunday
        PHASE_7_TASKS.extend([
            (day_num, 'biology', 'B1', '7:30-5:00', 'FULL NEET MOCK TEST',
             'Full NEET: 200 MCQs (Biology 100 + Chemistry 75 + Physics 25) in 5 hours',
             'Strict NEET timing'),
            (day_num, 'biology', 'B2', '7:00-9:00', 'COMPREHENSIVE ANALYSIS',
             'Full solution review + weak area identification',
             'Score + percentile estimation'),
        ])
    else:
        subject_cycle = ['Biology', 'Chemistry', 'Physics'][day_offset % 3]
        
        if subject_cycle == 'Biology':
            PHASE_7_TASKS.append((day_num, 'biology', 'B1', '7:30-11:00', 
                'Biology Final Revision', 'Complete chapter-wise NCERT review',
                '200 MCQs + 5 diagram practice'))
            PHASE_7_TASKS.append((day_num, 'biology', 'B2', '11:30-1:00',
                'Chemistry Quick Review', 'Formula revision + reaction summary',
                '100 Chemistry questions'))
        elif subject_cycle == 'Chemistry':
            PHASE_7_TASKS.append((day_num, 'biology', 'B1', '7:30-10:30',
                'Chemistry Final Revision', 'NCERT + reaction + formula revision',
                '200 questions + reaction maps'))
            PHASE_7_TASKS.append((day_num, 'physics', 'B2', '11:00-1:00',
                'Physics Quick Review', 'Formula + derivation revision',
                '100 Physics questions'))
        else:
            PHASE_7_TASKS.append((day_num, 'physics', 'B1', '7:30-10:30',
                'Physics Final Revision', 'NCERT + formula + numerical revision',
                '200 questions + 20 derivations'))
            PHASE_7_TASKS.append((day_num, 'biology', 'B2', '11:00-1:00',
                'Biology Quick Review', 'Diagram + MCQ revision',
                '100 Biology MCQs'))
        
        PHASE_7_TASKS.append((day_num, 'biology', 'B3', '2:00-3:30',
            'Mixed Revision Test', 'Short test on weak topics',
            f'50 {subject_cycle} + 20 mixed questions'))
        PHASE_7_TASKS.append((day_num, 'biology', 'B4', '3:30-4:30',
            'Formula Card Final Review', 'Revise all formula cards + NCERT lines',
            'Quick review of all cards'))

# Combine all phases
ALL_TASKS = PHASE_1_TASKS + PHASE_2_TASKS + PHASE_3_TASKS + PHASE_4_TASKS + PHASE_5_TASKS + PHASE_6_TASKS + PHASE_7_TASKS

def populate_database():
    """Populate the database with all roadmap tasks."""
    existing_count = StudyTask.query.count()
    if existing_count > 0:
        print(f"Database already has {existing_count} tasks")
        return
    
    for task_data in ALL_TASKS:
        day_number, subject, block, time_start_end, title, description, target = task_data
        date_obj = get_date_for_day(day_number)
        time_parts = time_start_end.split('-')
        
        task = StudyTask(
            day_number=day_number,
            date=date_obj,
            phase=get_phase_for_day(day_number),
            subject=subject,
            block=block,
            time_start=time_parts[0],
            time_end=time_parts[1],
            title=title,
            description=description,
            target=target
        )
        db.session.add(task)
    
    db.session.commit()
    print(f"Added {len(ALL_TASKS)} tasks to database")

def get_phase_for_day(day_number):
    """Return the phase name for a given day number."""
    if day_number <= 21:
        return 'Phase 1: Foundation (Days 1-21)'
    elif day_number <= 42:
        return 'Phase 2: Syllabus Completion (Days 22-42)'
    elif day_number <= 60:
        return 'Phase 3: First Revision (Days 43-60)'
    elif day_number <= 75:
        return 'Phase 4: Board Attack (Days 61-75)'
    elif day_number <= 95:
        return 'Phase 5: NEET Attack (Days 76-95)'
    elif day_number <= 105:
        return 'Phase 6: Final Revision (Days 96-105)'
    else:
        return 'Phase 7: Final Prep (Days 106-120)'

def get_phase_label(day_number):
    """Return just the phase label for display."""
    if day_number <= 21:
        return 'Phase 1: Foundation'
    elif day_number <= 42:
        return 'Phase 2: Syllabus Completion'
    elif day_number <= 60:
        return 'Phase 3: First Revision'
    elif day_number <= 75:
        return 'Phase 4: Board Attack'
    elif day_number <= 95:
        return 'Phase 5: NEET Attack'
    elif day_number <= 105:
        return 'Phase 6: Final Revision'
    else:
        return 'Phase 7: Final Prep'

@app.context_processor
def inject_template_globals():
    """Make helper functions available in all templates."""
    from datetime import datetime as dt, timedelta as td
    return {
        'get_date_for_day': get_date_for_day,
        'current_date': dt.now().date(),
        'timedelta': td
    }

@app.route('/')
def index():
    today = datetime.now().date()
    start = START_DATE.date()
    current_day = (today - start).days + 1 if today >= start else 1
    
    tasks = StudyTask.query.filter_by(day_number=current_day).order_by(StudyTask.block).all()
    phases = []
    for d in range(1, 121):
        phases.append({'day': d, 'phase': get_phase_label(d)})
    
    # Get phase ranges
    phase_ranges = [
        {'label': 'Phase 1: Foundation', 'start': 1, 'end': 21},
        {'label': 'Phase 2: Syllabus Completion', 'start': 22, 'end': 42},
        {'label': 'Phase 3: First Revision', 'start': 43, 'end': 60},
        {'label': 'Phase 4: Board Attack', 'start': 61, 'end': 75},
        {'label': 'Phase 5: NEET Attack', 'start': 76, 'end': 95},
        {'label': 'Phase 6: Final Revision', 'start': 96, 'end': 105},
        {'label': 'Phase 7: Final Prep', 'start': 106, 'end': 120},
    ]
    
    completed_today = StudyTask.query.filter_by(day_number=current_day, completed=True).count()
    total_today = StudyTask.query.filter_by(day_number=current_day).count()
    
    return render_template('index.html', 
                         tasks=tasks, 
                         current_day=current_day,
                         total_days=120,
                         completed_today=completed_today,
                         total_today=total_today,
                         phase_ranges=phase_ranges,
                         phase_label=get_phase_label(current_day),
                         phase_short=get_phase_label(current_day).split(':')[0])

@app.route('/day/<int:day_number>')
def day_view(day_number):
    tasks = StudyTask.query.filter_by(day_number=day_number).order_by(StudyTask.block).all()
    date_obj = get_date_for_day(day_number)
    dow = get_day_of_week(day_number)
    phase = get_phase_label(day_number)
    
    completed = StudyTask.query.filter_by(day_number=day_number, completed=True).count()
    total = StudyTask.query.filter_by(day_number=day_number).count()
    completion = round((completed / total * 100), 1) if total > 0 else 0
    
    return render_template('day.html', 
                         tasks=tasks, 
                         day_number=day_number,
                         date_obj=date_obj,
                         dow=dow,
                         phase=phase,
                         completed=completed,
                         total=total,
                         completion=completion)

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    task = StudyTask.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('day_view', day_number=task.day_number))

@app.route('/toggle_ajax/<int:task_id>')
def toggle_task_ajax(task_id):
    task = StudyTask.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return jsonify({'completed': task.completed, 'task_id': task_id})

@app.route('/add_note', methods=['POST'])
def add_note():
    task_id = request.form.get('task_id')
    note = request.form.get('note')
    task = StudyTask.query.get_or_404(task_id)
    task.notes = note
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/calendar')
def calendar():
    all_tasks = StudyTask.query.order_by(StudyTask.day_number).all()
    return render_template('calendar.html', tasks=all_tasks, start_date=START_DATE.date())

@app.route('/progress')
def progress():
    total_tasks = StudyTask.query.count()
    completed_tasks = StudyTask.query.filter_by(completed=True).count()
    overall_completion = round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0
    
    subject_completion = {}
    for subject in ['biology', 'chemistry', 'physics', 'english']:
        sub_total = StudyTask.query.filter_by(subject=subject).count()
        sub_done = StudyTask.query.filter_by(subject=subject, completed=True).count()
        subject_completion[subject] = {
            'total': sub_total,
            'done': sub_done,
            'percentage': round((sub_done / sub_total * 100), 1) if sub_total > 0 else 0
        }
    
    return render_template('progress.html',
                          total_tasks=total_tasks,
                          completed_tasks=completed_tasks,
                          overall_completion=overall_completion,
                          subject_completion=subject_completion)

with app.app_context():
    populate_database()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
