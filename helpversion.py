class Subject:

    def __init__(self, name, grade, credits):
        self.name = name
        self.grade = grade
        self.credits = credits
        if self.grade >= 5:
            self.result = "OK"
        else:
            self.result = "Fail"

class Period:

    def __init__(self, name):
        self.name = name
        self.subjects = []

    def insert_subject(self, subject):
        self.subjects.append(subject)
    
    def calculate_period_average(self):
        grades_weighted_sum = 0
        subject_credits_sum = 0
        for d in self.subjects:
            grades_weighted_sum += (d.grade * d.credits)
            subject_credits_sum += d.credits
        return grades_weighted_sum / subject_credits_sum
    
    def calculate_period_total_credits(self):
        subject_credits_sum = 0
        for d in self.subjects:
            subject_credits_sum += d.credits
        return subject_credits_sum
    
    def calculate_period_earned_credits(self):
        period_earned_credits = 0
        for d in self.subjects:
            if d.result == "OK":
                period_earned_credits += d.credits
        return period_earned_credits
    
    def calculate_period_subjects_failed(self):
        fails_counter = 0
        for d in self.subjects:
            if d.result == "Fail":
                fails_counter += 1
        return fails_counter
    
class ReportCard:

    def __init__(self):
        self.periods = []

    def insert_periods(self, period):
        self.periods.append(period)

    def calculate_total_average(self):
        total_weighted_grades_sum = 0
        total_credits_sum = 0

        for p in self.periods:
            period_average = p.calculate_period_average()
            period_credits = p.calculate_period_total_credits()
            total_weighted_grades_sum += (period_average * period_credits)
            total_credits_sum += period_credits
        if total_credits_sum > 0:
            return total_weighted_grades_sum / total_credits_sum
        else:
            return 0
    
    def calculate_total_credits(self):
        total_credits = 0
        for p in self.periods:
            total_credits += p.calculate_period_total_credits()
        return total_credits
    
    def calculate_total_credits_earned(self):
        total_credits_earned = 0
        for p in self.periods:
            total_credits_earned += p.calculate_period_earned_credits()
        return total_credits_earned
    
    def calculate_total_fails(self):
        total_fails = 0
        for p in self.periods:
            total_fails += p.calculate_period_subjects_failed()
        return total_fails
    
    def print_report_card(self):
        for p in self.periods:
            print("\n")
            print("====================")
            print(f"Period: {p.name}\n")
            for d in p.subjects:
                print(f"Subject: {d.name} / Grade: {d.grade} / Credits: {d.credits} / Result: {d.result} ")
            print("\n")
            print(f"Period Average: {p.calculate_period_average():.2f} / Period Earned Credits: {p.calculate_period_earned_credits()} / Period Credits: {p.calculate_period_total_credits()} / Period Fails: {p.calculate_period_subjects_failed()} ",)
            print(f"Total Average: {self.calculate_total_average():.2f} / Total Earned Credits: {self.calculate_total_credits_earned()} / Total Credits: {self.calculate_total_credits()} / Total Fails: {self.calculate_total_fails()} ")
            print("====================")
        return


def open_program():

    report_card = ReportCard()
    
    period_quantity = int(input("Type the quantity of periods you want to register: "))
    for p in range (period_quantity):
        period_name = input("Type period name you want to register: ")
        period = Period(period_name)

        subjects_quantity = int(input("Type the quantity of subjects you want to register: ")) 
        for s in range (subjects_quantity):
            subject_name = input("Type the subject name you want to register: ")
            subject_grade = float(input("Type the subject grade you want to register: "))
            subject_credits = int(input("Type the subject credits you want to register: "))
            subject = Subject(subject_name, subject_grade, subject_credits)

            period.insert_subject(subject)
        report_card.insert_periods(period)
    
    report_card.print_report_card()

    return report_card

open_program()