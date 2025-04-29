class Subject:

    def __init__(self, name, credits, grade):
        self.name = name
        self.credits = credits
        self.grade = grade
        if self.grade >= 7:
            self.result = "OK"
        else:
            self.result = "Fail"

class Period:

    def __init__(self, name):
        self.name = name
        self.subjects = []

    def insert_subject(self, subject):
        self.subjects.append(subject)
    
    def calculate_subject_average(self):
        periodPonderateSum = 0
        periodCreditsSum = 0
        for d in self.subjects:
            periodPonderateSum += (d.grade * d.credits)
            periodCreditsSum += d.credits
        return periodPonderateSum / periodCreditsSum
    
    def period_total_credits(self):
        periodTotalCredits = 0
        for d in self.subjects:
            periodTotalCredits += d.credits
        return periodTotalCredits
    
    def earned_credits(self):
        periodEarnedCredits = 0
        for d in self.subjects:
            if d.result == "OK":
                periodEarnedCredits += d.credits
        return periodEarnedCredits
    
class ReportCard:

    def __init__(self, name):
        self.name = name
        self.periods = []

    def insert_periods(self, period):
        self.periods.append(period)

    def calculate_total_average(self):
        totalPonderateSum = 0
        totalCredits = 0

        for p in self.periods:
            periodAverage = p.calculate_subject_average()
            periodCredits = p.period_total_credits()
            totalPonderateSum += (periodAverage * periodCredits)
            totalCredits += periodCredits
        if totalCredits > 0:
            return totalPonderateSum / totalCredits
        else:
            return 0