import os
import json
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_csv():
    os.makedirs('corpus/tables', exist_ok=True)
    with open('corpus/tables/fee_schedule.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Fee Type', 'Deadline', 'Late Penalty Details', 'Description'])
        writer.writerow(['Autumn Semester Tuition', 'September 10, 2026', 'Late fee applies after this date. Rs. 500 per day for first 5 days, then Rs. 1000 per day.', 'Covers basic tuition and laboratory usage for the autumn term.'])
        writer.writerow(['Spring Semester Tuition', 'January 15, 2027', 'Late fee applies. Registration blocked if unpaid by Jan 31.', 'Covers basic tuition and laboratory usage for the spring term.'])
        writer.writerow(['Hostel Accommodation', 'August 1, 2026', 'Room allocation cancelled if unpaid. No grace period.', 'Annual boarding charge for on-campus residents.'])
        writer.writerow(['Library Security Deposit', 'At time of admission', 'Refundable upon graduation or withdrawal.', 'One-time refundable caution money for library access.'])
        writer.writerow(['Attendance Condonation Fee', 'Before exams begin', 'Rs. 2000 flat fee. Non-refundable.', 'Processing fee for medical condonation applications.'])
        writer.writerow(['Revaluation Application Fee', '14 days post results', 'Rs. 500 per subject. Refunded if grade improves.', 'Fee for double-blind grading review.'])
        writer.writerow(['Transcript Issuance', 'N/A', 'Rs. 300 per copy.', 'Charge for printing and sealing official academic records.'])
        writer.writerow(['Convocation Fee', 'May 1, 2027', 'Degree withheld until paid.', 'Covers academic dress rental and ceremony logistics.'])

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
    
    text1_1 = """1.1 General Fee Structure: The Institute relies heavily on timely and complete fee payments to maintain its state-of-the-art facilities, fund cutting-edge research, and retain distinguished faculty members. The overarching fee structure is meticulously reviewed annually by the Board of Governors to ensure it aligns with operational costs and inflation. It is the responsibility of the student and their sponsors to ensure that sufficient funds are available to meet these obligations. All fees, once paid, are strictly non-refundable unless a student officially withdraws from the program entirely before the official commencement of the academic session. In such cases of early withdrawal, a standard administrative processing fee will be deducted, and the remaining balance will be refunded within 90 working days."""
    
    # We will expand this massively to ensure high word count.
    text1_1_extended = text1_1 + " " + """The finance department issues detailed invoices to students via their official university email addresses at least thirty days prior to the start of the semester. Students are expected to check their email regularly. Payment can be made via authorized banking channels, secure online payment gateways integrated into the ERP, or via demand draft. Cash payments exceeding Rs. 10,000 are not accepted under any circumstances to comply with national tax regulations. Educational loan disbursement cheques must be deposited directly into the university's designated account. In cases where loan disbursements are delayed by the banking institution, the student must provide official documentation from the bank manager requesting an extension to avoid late fees. The university does not offer installment plans for regular semester tuition fees."""
    
    Story.append(Paragraph(text1_1_extended, styles['Normal']))
    Story.append(Spacer(1, 12))
    
    text1_2 = """1.2 Fee Deadlines and Penalties: Timely payment is crucial for the smooth functioning of the institution. All students must complete their autumn semester fee payments on or before September 15, 2026, without penalty. Payments received after this date will attract significant late fines. The late fine is calculated automatically by the financial system and cannot be waived by individual faculty members or department heads. Repeated failure to meet fee deadlines may result in the suspension of access to university portals, denial of library facilities, withholding of examination admit cards, and ultimately, forced cancellation of course registration for the semester. Students facing genuine, extreme financial hardship may apply for a short-term emergency loan from the university's student welfare fund, but this application must be made well before the fee deadline."""
    Story.append(Paragraph(text1_2, styles['Normal']))
    Story.append(Spacer(1, 12))
    
    section2_title = Paragraph("2. Administrative Policies", styles['Heading2'])
    Story.append(section2_title)

    text2_1 = """2.1 Condonation of Attendance Shortage: The Institute recognizes that students may face unforeseen difficulties and medical emergencies that disrupt their academic schedule. While regular attendance is mandatory, the administration provides a mechanism for relief in genuine cases. Students seeking attendance condonation may be granted a waiver up to 15% upon payment of the condonation fee, provided they submit the required application, supported by medical certificates, directly to the Dean's office. This ensures that students who have missed classes due to legitimate, documented health reasons can still participate in the final examinations, provided their overall physical attendance does not fall below 60%. The condonation fee covers the administrative overhead of verifying medical documents and convening the review board. It is important to note that condonation applies only to the eligibility to sit for exams, and does not award free marks for the classes missed."""
    
    text2_1_extended = text2_1 + " " + """The Dean's office retains the right to reject applications if the medical documentation is found to be incomplete, retroactively dated, or issued by an unverified practitioner. Students are advised to keep copies of all medical records submitted."""
    
    Story.append(Paragraph(text2_1_extended, styles['Normal']))
    Story.append(Spacer(1, 12))

    text2_2 = """2.2 Semester Withdrawal: A student may officially request a semester withdrawal if they are unable to continue their studies due to severe prolonged illness, severe mental health crises, or compelling personal circumstances such as the death of an immediate caregiver. The withdrawal application must be formally requested and processed before the commencement of the mid-semester examinations. If approved by the Dean of Academic Affairs, the student's status becomes 'Withdrawn' for that specific semester. 

When a student withdraws, they must vacate the hostel premises within 48 hours. They are required to re-register for the same courses when they are next offered, essentially repeating the semester. No fee refunds of any kind are provided for mid-semester withdrawals, as the university has already committed resources for the student's education. The withdrawn semester counts towards the maximum duration permitted to complete the degree program."""
    Story.append(Paragraph(text2_2, styles['Normal']))
    Story.append(Spacer(1, 12))

    section3_title = Paragraph("3. Scholarship and Financial Aid Criteria", styles['Heading2'])
    Story.append(section3_title)

    text3 = """The university believes that financial constraints should not be a barrier to high-quality education for exceptionally talented students. To this end, the university awards prestigious merit scholarships to the top 5% of students in each batch. These awards are based strictly on the Cumulative Grade Point Average (CGPA) calculated at the end of the previous academic year. 

To retain this scholarship for subsequent years, a student must meet stringent criteria: they must maintain a minimum CGPA of 8.5, have absolutely no record of disciplinary action or academic malpractice, and clear all registered courses in their first attempt without any supplementary examinations or 'W' grades. Scholarships cover tuition fees either partially (50%) or fully (100%), depending entirely on the endowment funds available in that fiscal year and the student's exact rank. 

Additionally, need-based financial aid is available for students from economically weaker sections. Applicants for need-based aid must submit verified income tax returns of their parents or guardians. The Financial Aid Committee reviews all applications in July. Aid usually takes the form of a tuition fee waiver, and recipients are often required to contribute 10 hours per week of academic assistance or administrative work on campus under the "Earn While You Learn" scheme."""
    
    text3_extended = text3 + " " + """The total number of scholarships and financial aid packages awarded in any given year is capped. The decisions of the Financial Aid Committee are final and binding. Students who lose their scholarship due to poor academic performance may reapply in the future if their CGPA recovers above the 8.5 threshold, though reinstatement is not guaranteed and depends on the available pool of funds."""
    
    Story.append(Paragraph(text3_extended, styles['Normal']))

    doc.build(Story)

if __name__ == "__main__":
    generate_csv()
    generate_pdf()
