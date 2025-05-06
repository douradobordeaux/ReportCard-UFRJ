class Subject:
    def __init__(self, name, grade, credits):
        self.name = name
        self.grade = grade
        self.credits = credits
        self.result = True if grade >= 5 else False

class Period:
    def __init__(self, name):
        self.name = name
        self.subjects = []

    def insert_subject(self, subject):
        self.subjects.append(subject)

    def calculate_period_average(self):
        subject_grades_weighted_sum = sum(s.grade * s.credits for s in self.subjects)
        subject_credits_sum = sum(s.credits for s in self.subjects)
        return subject_grades_weighted_sum / subject_credits_sum if subject_credits_sum > 0 else 0

    def calculate_period_credits(self):
        return sum(s.credits for s in self.subjects)

    def calculate_period_earned_credits(self):
        return sum(s.credits for s in self.subjects if s.result == True)

    def calculate_period_fails(self):
        return sum(1 for s in self.subjects if s.result == False)
    

class ReportCard:

    def __init__(self):
        self.periods = []
    
    def insert_period(self, period):
        self.periods.append(period)

    def calculate_current_total_average(self, period):
        period_grades_weighted_sum = sum(p.calculate_period_average() * p.calculate_period_credits() for p in self.periods[:period])
        period_credits_sum = sum(p.calculate_period_credits() for p in self.periods[:period])
        return period_grades_weighted_sum / period_credits_sum if period_credits_sum > 0 else 0
    
    def calculate_current_total_credits(self, period):
        return sum(p.calculate_period_credits() for p in self.periods[:period])
    
    def calculate_current_total_earned_credits(self, period):
        return sum(p.calculate_period_earned_credits() for p in self.periods[:period])
    
    def calculate_current_total_fails(self, period):
        return sum(p.calculate_period_fails() for p in self.periods[:period])
    
    def register_report_card(self):
        periods_amount = int(input("Type how many periods you want to register: "))
        for p in range (periods_amount):
            period_name = input("Type the name of the period you want to register: ")
            period = Period(period_name)
            subjects_amount = int(input("Type how many subjects you want to register: "))
            for s in range (subjects_amount):
                subject_name = input("Type the name of the subject you want to register: ")
                subject_grade = float(input("Type the grade of the subject you want to register: "))
                subject_credits = int(input("Type the credits of the subject you want to register: "))
                subject = Subject(subject_name, subject_grade, subject_credits)
                period.insert_subject(subject)
            self.insert_period(period)
        
    def print_report_card(self):
        print("\n\n")
        for i, p in enumerate(self.periods):
            print("\n")
            print("====================")
            print(f"Period: {p.name}\n")
            for d in p.subjects:
                print(f"Subject: {d.name} / Grade: {d.grade} / Credits: {d.credits} / Result: {"Passed" if (d.result) == True else "Failed"}")
            print("\n")
            print(f"Period Average: {p.calculate_period_average():.2f} / Period Earned Credits: {p.calculate_period_earned_credits()} / Period Credits: {p.calculate_period_credits()} / Period Fails: {p.calculate_period_fails()}")
            print(f"Total Average: {self.calculate_current_total_average(i+1):.2f} / Total Earned Credits: {self.calculate_current_total_earned_credits(i+1)} / Total Credits: {self.calculate_current_total_credits(i+1)} / Total Fails: {self.calculate_current_total_fails(i+1)} ")
            print("====================")
        return

report_card = ReportCard()
report_card.register_report_card()
report_card.print_report_card()