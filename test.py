class Subject:

    def __init__(self, name, credits, grade, result):
        self.name = name
        self.credits = credits
        self.grade = grade
        self.result = result
    
    def SubjectResult(self):
        if self.grade >= 7:
            self.result = "OK"
        else:
            self.result = "Fail"

class Period:

    def __init__(self, name):
        self.name = name
        self.subjects = []

    def InsertSubject(self, subject):
        self.subjects.append(subject)
    
    def CalculateSubjectAverage(self):
        for d in self.subjects:
            periodPonderateSum += (d.grade * d.credits)
            periodCreditsSum += d.credits
        return periodPonderateSum / periodCreditsSum
    
    def PeriodTotalCredits(self):
        for d in self.subjects:
            periodTotalCredits += d.credits
        return periodTotalCredits
    
    def EarnedCredits(self):
        for d in self.subjects:
            if d.result == "OK":
                periodEarnedCredits += d.credits
            pass
        return periodEarnedCredits
    
class ReportCard:

    def __init__(self, name):
        self.name = name
        self.periods = []

    def InsertPeriods(self, period):
        self.periods.append(period)

    def CalculateTotalAverage(self):
        for p in self.periods:
            totalGradesSum += p.calculate
            totalCreditsSum += p.PeriodTotalCredits()