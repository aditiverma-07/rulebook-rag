import os
import json
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import pdfplumber

def generate_markdown_01():
    text = """# Medicaps Institute of Technology — Academic & Student Regulations 2026
## 1. Introduction
The Medicaps Institute of Technology (hereinafter referred to as the "Institute") is dedicated to fostering a rigorous academic environment. These regulations govern all undergraduate and postgraduate academic programs. It is the responsibility of every enrolled student to familiarize themselves with these policies. Ignorance of the regulations is not a valid excuse for non-compliance. These regulations take effect from the commencement of the Autumn Semester of the 2026 academic year. The Institute reserves the right to amend, suspend, or revoke any regulation contained herein at its sole discretion, provided that students are given reasonable notice of such changes. In cases of ambiguity or dispute, the interpretation provided by the Dean of Academic Affairs shall be final and binding. The Academic Senate oversees the implementation of these regulations and periodically reviews their effectiveness in maintaining educational standards.
""" * 3 + """
## 2. Course Registration and Add/Drop Rules
### 2.1 Standard Course Registration
All students must complete their course registration online via the university portal prior to the start of each semester. The registration window typically opens four weeks before the first day of classes and closes on the first Friday of the semester. Students must consult with their assigned academic advisors before finalizing their schedules. Registration is considered complete only when all outstanding tuition and hostel fees from previous semesters have been cleared. Late registration is permitted only under exceptional circumstances, such as a documented medical emergency or administrative error on the part of the Institute, and requires the explicit approval of the Head of the Department. A late registration fee will be applied to all such cases.

### 2.2 Add/Drop Period
Students may add or drop courses without academic penalty during the official Add/Drop period, which spans the first two weeks of the semester. Courses dropped during this period will not appear on the student's official transcript. Adding a course is subject to availability and prerequisite satisfaction. If a student drops a course after the Add/Drop period but before the withdrawal deadline (the end of the eighth week), a grade of 'W' (Withdrawal) will be recorded on the transcript. This grade does not affect the Semester Grade Point Average (SGPA). Withdrawals after the eighth week are generally not permitted unless approved by the Academic Appeals Committee under severe extenuating circumstances.
""" * 3 + """
## 3. Attendance Requirements
### 3.1 Minimum Attendance Policy
The Institute mandates strict attendance for all scheduled academic activities, including lectures, tutorials, laboratory sessions, and seminars. A student must maintain a minimum attendance of 75% in each course to be eligible to appear for the end-semester examination in that course. Attendance is calculated from the first day of the semester, regardless of the student's date of registration. The course instructor is responsible for maintaining accurate attendance records and publishing them on the student portal on a fortnightly basis. Students whose attendance falls below the 75% threshold will be awarded an 'F-A' (Fail due to Attendance) grade and will be debarred from writing the final examination.

### 3.2 Attendance Shortage and Condonation
Under extraordinary circumstances, such as severe illness, hospitalization, or a family bereavement, an exception to the minimum attendance rule may be requested. The Principal may condone an attendance shortage of up to 10% for valid medical reasons. This means the absolute minimum attendance permitted under this section is 65%. To apply for condonation, the student must submit a formal petition along with verifiable documentation within the specified deadlines. Condonation is not a right but a privilege granted at the discretion of the Principal upon recommendation by the Head of the Department.
""" * 3 + """
## 4. Medical Leave and Exemptions
### 4.1 Applying for Medical Leave
Students experiencing health issues that prevent them from attending classes for more than three consecutive days must officially apply for medical leave. The application must be submitted to the University Health Center and must include a detailed certificate from a registered medical practitioner. The certificate must clearly state the nature of the illness, the recommended period of rest, and the date the student is declared fit to resume academic activities.

### 4.5 Medical Leave Documentation Deadline
Timely submission of medical records is critical for the approval of medical leave and any associated attendance condonation or examination exemptions. Students must submit valid medical documentation within 7 calendar days of returning to campus. Failure to submit the documentation within this 7-day window will result in the rejection of the medical leave application, and the student will be marked absent for the entire duration of the illness. Exceptions to this deadline are only made in cases where the student was physically incapacitated and unable to communicate, as verified by a hospital.
""" * 3 + """
## 5. Examinations and Internal Assessment
### 5.1 Structure of Assessment
The evaluation of a student's performance in a course is divided into Internal Assessment (IA) and End-Semester Examination (ESE). The weightage typically assigned is 40% for IA and 60% for ESE, although this may vary for laboratory and project-based courses. The IA comprises quizzes, mid-term examinations, assignments, and class participation.

### 5.2 End-Semester Examinations
End-Semester Examinations are conducted by the central examination cell. Students must carry their valid university ID card and the official hall ticket to the examination venue. Arriving more than 30 minutes after the commencement of the examination will result in denied entry. No student is allowed to leave the examination hall during the first hour or the last fifteen minutes of the examination.

## 6. Grading and Revaluation
### 6.1 Grading System
The Institute follows a 10-point absolute grading system. The letter grades and their corresponding grade points are: O (Outstanding) - 10, A+ (Excellent) - 9, A (Very Good) - 8, B+ (Good) - 7, B (Above Average) - 6, C (Average) - 5, P (Pass) - 4, F (Fail) - 0.

### 6.2 Revaluation Process
If a student is dissatisfied with their End-Semester Examination grade, they may apply for revaluation within two weeks of the declaration of results. The revaluation process involves a blind re-grading by a different faculty member. If the new grade differs from the original grade by more than one full letter grade, the higher of the two grades will be awarded, and the revaluation fee will be refunded.
""" * 3

    os.makedirs('corpus/markdown', exist_ok=True)
    with open('corpus/markdown/01_academic_regulations.md', 'w', encoding='utf-8') as f:
        f.write(text)

def generate_markdown_02():
    text = """# Medicaps Institute of Technology — Academic & Student Regulations 2026
## 7. Student Discipline
### 7.1 Code of Conduct
The Institute expects all students to maintain the highest standards of personal and academic integrity. The Code of Conduct applies to student behavior on campus, in university-affiliated housing, and during official university events off-campus. Violations of the Code of Conduct include, but are not limited to, harassment, bullying, vandalism, substance abuse, and theft. The Disciplinary Committee is empowered to investigate alleged violations and impose sanctions ranging from official warnings and community service to suspension and expulsion. The Institute maintains a zero-tolerance policy towards ragging and any form of discrimination based on race, gender, religion, or nationality.
""" * 4 + """
## 8. Examination Malpractice
### 8.1 Definition and Scope
Examination malpractice includes any attempt to gain an unfair advantage during an assessment. This encompasses bringing unauthorized materials into the examination hall, copying from another student, communicating with others during the exam, impersonation, and plagiarism in assignments. The use of electronic devices, unless explicitly permitted by the instructor, is strictly prohibited and constitutes malpractice.

### 8.2 Procedure for Handling Malpractice and Absences
When an invigilator suspects malpractice, they will confiscate the answer script and unauthorized materials immediately. The student will be provided with a new answer script to complete the remaining time. A detailed report will be forwarded to the Malpractice Inquiry Committee. The Committee will conduct a hearing where the student is given an opportunity to present their defense. If found guilty, the student may face cancellation of the examination result, suspension for a semester, or expulsion, depending on the severity of the offense. Furthermore, if a student misses a disciplinary hearing or examination due to health reasons, documentation is required. Any medical certificate supporting an absence must be filed with the disciplinary committee within 5 working days. Failure to do so will result in an ex-parte decision by the committee.
""" * 4 + """
## 9. Academic Appeals
### 9.1 Right to Appeal
Students have the right to appeal decisions related to academic standing, disciplinary actions, and examination malpractice. The appeal must be submitted in writing to the Chairman of the Academic Appeals Board within 14 days of receiving the official decision. The appeal must clearly state the grounds for the appeal, which are limited to procedural errors, new evidence not previously available, or disproportionate penalties.

### 9.2 The Appeals Board
The Appeals Board is composed of senior faculty members and a student representative. The Board's decision is final and binding on all parties within the university hierarchy.
""" * 4 + """
## 10. Hostel Regulations
### 10.1 Residency Requirements
First-year undergraduate students are required to reside in the university hostels, subject to availability. Hostel accommodation is allocated on a first-come, first-served basis. Residents must adhere strictly to the hostel curfew times. The main gates are locked at 10:30 PM on weekdays and 11:30 PM on weekends. Late entry is permitted only with prior written permission from the Hostel Warden.

### 10.2 Room Allocation and Upkeep
Students are responsible for the furniture and fixtures in their assigned rooms. Any damage will be billed to the occupants. The use of high-wattage electrical appliances, such as room heaters and hot plates, is strictly forbidden due to fire safety regulations. Subletting or allowing unauthorized guests to stay overnight is a severe offense that will lead to immediate eviction from the hostel.
""" * 4
    os.makedirs('corpus/markdown', exist_ok=True)
    with open('corpus/markdown/02_student_conduct.md', 'w', encoding='utf-8') as f:
        f.write(text)

def generate_markdown_03():
    text = """# Medicaps Institute of Technology — Academic & Student Regulations 2026
## 11. Library Regulations
### 11.1 Access and Membership
The Central Library is the primary resource center for all students, faculty, and staff. Access to the library is restricted to registered members carrying a valid university ID card. Library membership is automatically activated upon enrollment. The library remains open from 8:00 AM to midnight on weekdays and from 9:00 AM to 8:00 PM on weekends and public holidays. During examination periods, the reading rooms are open 24/7.

### 11.2 Borrowing Privileges
Undergraduate students may borrow up to 5 books for a period of 14 days. Postgraduate students may borrow up to 8 books for 21 days. Reference books, periodicals, and rare collections are for in-library use only and cannot be checked out. Books must be returned on or before the due date. A late fine of Rs. 10 per day is levied for overdue items. If a book is lost or damaged, the borrower must replace it with a new copy of the same edition or pay three times the current market price of the book.
""" * 5 + """
## 12. Academic Committees
### 12.1 Program Assessment Committee (PAC)
The PAC is responsible for monitoring the academic progress of a specific degree program. It reviews course curricula, evaluates student feedback, and suggests improvements to enhance the quality of education. The PAC meets at least twice a semester and submits its recommendations to the Board of Studies.

### 12.2 Departmental Academic Committee (DAC)
The DAC handles matters related to course registrations, elective offerings, and faculty assignments within a department. It also reviews cases of students facing academic probation and recommends remedial actions.
""" * 5
    os.makedirs('corpus/markdown', exist_ok=True)
    with open('corpus/markdown/03_library_and_facilities.md', 'w', encoding='utf-8') as f:
        f.write(text)

def generate_csv():
    os.makedirs('corpus/tables', exist_ok=True)
    with open('corpus/tables/fee_schedule.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Fee Type', 'Deadline', 'Late Penalty Details'])
        writer.writerow(['Autumn Semester Tuition', 'September 10, 2026', 'Late fee applies after this date. Rs. 500 per day for first 5 days, then Rs. 1000 per day.'])
        writer.writerow(['Spring Semester Tuition', 'January 15, 2027', 'Late fee applies. Registration blocked if unpaid by Jan 31.'])
        writer.writerow(['Hostel Accommodation', 'August 1, 2026', 'Room allocation cancelled if unpaid.'])
        writer.writerow(['Library Security Deposit', 'At time of admission', 'Refundable upon graduation.'])
        writer.writerow(['Attendance Condonation Fee', 'Before exams begin', 'Rs. 2000 flat fee.'])
        writer.writerow(['Revaluation Application Fee', '14 days post results', 'Rs. 500 per subject.'])
        writer.writerow(['Transcript Issuance', 'N/A', 'Rs. 300 per copy.'])

def generate_pdf():
    os.makedirs('corpus/pdf', exist_ok=True)
    doc = SimpleDocTemplate("corpus/pdf/04_financial_and_administrative.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    Story = []

    title = Paragraph("Medicaps Institute of Technology — Academic & Student Regulations 2026", styles['Title'])
    Story.append(title)
    Story.append(Spacer(1, 12))

    section1_title = Paragraph("1. Financial Policies", styles['Heading2'])
    Story.append(section1_title)
    
    text1_1 = """1.1 General Fee Structure: The Institute relies on timely fee payments to maintain its state-of-the-art facilities and retain distinguished faculty. The fee structure is reviewed annually by the Board of Governors. All fees are non-refundable unless a student officially withdraws before the commencement of the academic session, in which case a processing fee will be deducted.""" * 3
    Story.append(Paragraph(text1_1, styles['Normal']))
    Story.append(Spacer(1, 12))
    
    text1_2 = """1.2 Fee Deadlines and Penalties: Timely payment is crucial. All students must complete their autumn semester fee payments on or before September 15, 2026, without penalty. Payments received after this date will attract significant late fines and may result in the suspension of access to university portals, library facilities, and ultimately, cancellation of course registration.""" * 3
    Story.append(Paragraph(text1_2, styles['Normal']))
    Story.append(Spacer(1, 12))
    
    section2_title = Paragraph("2. Administrative Policies", styles['Heading2'])
    Story.append(section2_title)

    text2_1 = """2.1 Condonation of Attendance Shortage: The Institute recognizes that students may face unforeseen difficulties. Students seeking attendance condonation may be granted a waiver up to 15% upon payment of the condonation fee, provided they submit the required application to the Dean's office. This ensures that students who have missed classes due to legitimate reasons can still participate in examinations, provided their attendance does not fall below 60%.""" * 3
    Story.append(Paragraph(text2_1, styles['Normal']))
    Story.append(Spacer(1, 12))

    text2_2 = """2.2 Semester Withdrawal: A student may request a semester withdrawal if they are unable to continue their studies due to severe prolonged illness or compelling personal circumstances. The withdrawal must be requested before the mid-semester examinations. If approved, the student's status becomes 'Withdrawn' for that semester, and they must re-register for the courses when next offered. No fee refunds are provided for mid-semester withdrawals.""" * 3
    Story.append(Paragraph(text2_2, styles['Normal']))
    Story.append(Spacer(1, 12))

    text3 = """3. Scholarship Criteria: The university awards merit scholarships to the top 5% of students in each batch based on their CGPA at the end of the academic year. To retain the scholarship, a student must maintain a minimum CGPA of 8.5, have no disciplinary record, and clear all courses in the first attempt. Scholarships cover tuition fees partially or fully, depending on the endowment funds available.""" * 5
    Story.append(Paragraph(text3, styles['Normal']))

    doc.build(Story)

def generate_conflicts_and_tests():
    conflicts = [
        {
            "conflict_id": "C001",
            "topic": "Attendance Condonation Limit",
            "source_1": "01_academic_regulations.md",
            "section_1": "3.2 Attendance Shortage and Condonation",
            "statement_1": "The Principal may condone an attendance shortage of up to 10% for valid medical reasons.",
            "source_2": "04_financial_and_administrative.pdf",
            "section_2": "2.1 Condonation of Attendance Shortage",
            "statement_2": "Students seeking attendance condonation may be granted a waiver up to 15% upon payment of the condonation fee.",
            "explanation": "Markdown says up to 10% condonation is allowed, while PDF says up to 15%."
        },
        {
            "conflict_id": "C002",
            "topic": "Medical Leave Documentation Deadline",
            "source_1": "01_academic_regulations.md",
            "section_1": "4.5 Medical Leave Documentation Deadline",
            "statement_1": "Students must submit valid medical documentation within 7 calendar days of returning to campus.",
            "source_2": "02_student_conduct.md",
            "section_2": "8.2 Procedure for Handling Malpractice and Absences",
            "statement_2": "Any medical certificate supporting an absence must be filed with the disciplinary committee within 5 working days.",
            "explanation": "01_academic_regulations says 7 calendar days for medical documentation, while 02_student_conduct says 5 working days."
        },
        {
            "conflict_id": "C003",
            "topic": "Autumn Semester Fee Deadline",
            "source_1": "fee_schedule.csv",
            "section_1": "Autumn Semester Tuition row",
            "statement_1": "Deadline is September 10, 2026",
            "source_2": "04_financial_and_administrative.pdf",
            "section_2": "1.2 Fee Deadlines and Penalties",
            "statement_2": "All students must complete their autumn semester fee payments on or before September 15, 2026, without penalty.",
            "explanation": "CSV lists deadline as Sept 10, but PDF lists it as Sept 15."
        }
    ]
    with open('corpus/conflicts.json', 'w', encoding='utf-8') as f:
        json.dump(conflicts, f, indent=4)

    test_questions = []
    # 10 Answerable
    answered_qs = [
        "What is the minimum attendance required without condonation?",
        "When does the Add/Drop period close?",
        "What grade is given if a student withdraws before the eighth week?",
        "Who is responsible for maintaining attendance records?",
        "What is the late fine for overdue library books?",
        "What is the curfew time for hostels on weekdays?",
        "What constitutes examination malpractice?",
        "How much is the Revaluation Application Fee?",
        "What is the minimum CGPA required to retain a scholarship?",
        "What happens if a student misses a disciplinary hearing without documentation?"
    ]
    for i, q in enumerate(answered_qs):
        test_questions.append({
            "id": f"QA{i+1:03}",
            "question": q,
            "expected_type": "answered",
            "expected_sources": []
        })
    
    # 3 Conflict Questions
    test_questions.append({
        "id": "QC001",
        "question": "What is the maximum percentage of attendance shortage that can be condoned?",
        "expected_type": "conflict",
        "conflict_id": "C001"
    })
    test_questions.append({
        "id": "QC002",
        "question": "How many days do I have to submit a medical certificate after returning to campus?",
        "expected_type": "conflict",
        "conflict_id": "C002"
    })
    test_questions.append({
        "id": "QC003",
        "question": "What is the exact deadline to pay the autumn semester fee without penalty?",
        "expected_type": "conflict",
        "conflict_id": "C003"
    })

    # 25 Not Covered
    not_covered_qs = [
        "Can I bring a smartwatch into the examination hall?",
        "What is the process for changing my hostel room after a roommate dispute?",
        "Does the university provide reimbursement for conference travel?",
        "Can students take a semester abroad?",
        "What happens if I lose my student ID card?",
        "Is there a dress code for attending regular classes?",
        "Can I park my personal car on the university campus?",
        "Are pets allowed inside the hostel rooms?",
        "What is the procedure to apply for an internship semester?",
        "Do you provide a student discount for public transportation?",
        "How can I apply for a student loan through the university?",
        "What is the fine for breaking a test tube in the chemistry lab?",
        "Is smoking permitted anywhere on the campus grounds?",
        "Can I change my undergraduate major in the second year?",
        "Are visitors allowed in the hostel during daytime?",
        "How do I join the university sports teams?",
        "What is the policy for participating in political protests on campus?",
        "Does the medical center provide dental services?",
        "Is there a limit on the number of pages I can print in the library?",
        "Can I pay my tuition fees using a credit card?",
        "What are the working hours of the university cafeteria?",
        "Is financial aid available for international students?",
        "How do I request an official transcript to be sent to a foreign university?",
        "Can a student's parent submit an assignment on their behalf?",
        "Can I pay fees using cryptocurrency?"
    ]
    for i, q in enumerate(not_covered_qs):
        test_questions.append({
            "id": f"QN{i+1:03}",
            "question": q,
            "expected_type": "not_covered"
        })

    os.makedirs('tests', exist_ok=True)
    with open('tests/test_questions.json', 'w', encoding='utf-8') as f:
        json.dump(test_questions, f, indent=4)

if __name__ == "__main__":
    generate_markdown_01()
    generate_markdown_02()
    generate_markdown_03()
    generate_csv()
    generate_pdf()
    generate_conflicts_and_tests()
    print("Files generated successfully.")
