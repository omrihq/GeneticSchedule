import random
import copy

class Class:
    def __init__(self, name, time, length, days):
        self.name = name
        self.time = time
        self.length = length
        self.days = days

    def get_time(self, time):
        return self.time

    def get_name(self):
        return self.name

    def get_length(self):
        return self.length

    def get_days(self):
        return self.days

    #Checks to see if a class overlaps another one. Accounts for which day they're on. 
    def overlaps(self, other):
        class1_start = self.time
        class1_end = class1_start + self.length
    
        class2_start = other.time
        class2_end = class2_start + other.length
    
        intersection = [day for day in self.days if day in other.days]
        if intersection:
            if class1_start < class2_start:
                if class1_end >= class2_start:
                    return True
                else:
                    return False
            elif class1_start > class2_start:
                if class2_end >= class1_start:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    def __str__(self):
        return "%s { time : %s, length: %s, days: %s}" % (self.name, self.time, self.length, self.days)

    def __lt__ (self, other):
        if self.time == other.time:
            return self.time > other.time
        return self.time < other.time

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.time != other.time:
            return False
        if self.length != other.length:
            return False
        if self.days != other.days:
            return False
        return True
    
    def __hash__(self):
        return hash(repr(self.name))

class Schedule:
    def __init__(self, classes):
        self.classes = sorted(classes)
        self.score = self.get_score()

    def get_classes(self):
        return self.classes

    def get_earliest_class_score(self):
        #Gets the earliest of every day and add up
        #I REALLY want late classes after 11am so score increases 2. Will change to get_score(self, early_time) so the user can change it

        score = 0
        days = [1, 2, 3, 4, 5]
        day_sched = self.schedule_by_day()
        for day in day_sched:
            for clas in day_sched[day]:
                if day in days:
                    if clas.time <= 8:
                        days.remove(day)
                        score -= 3
                    elif clas.time <= 9:
                        days.remove(day)
                        score -= 2
                    elif clas.time >= 11.5:
                        days.remove(day)
                        score += 3
                    elif clas.time > 10:
                        days.remove(day)
                        score += 1
        return score
        
    def get_end_class_score(self):
        #Check the time the schedule ends, get the entire week's score
        score = 0
        days = [1, 2, 3, 4, 5]
        day_sched = self.schedule_by_day()

        for day in day_sched:
            last_class = day_sched[day][len(day_sched[day])-1]
            for clas in day_sched[day]:
                if day in days:
                    end_time = last_class.time + last_class.length
                    if end_time <= 15: 
                        days.remove(day)
                        score += 3
                    elif end_time <= 16:
                        days.remove(day)
                        score+= 2
                    elif end_time < 17:
                        days.remove(day)
                        score+=1
                    else:
                        if end_time > 20:
                            days.remove(day)
                            score -= 3
                        elif end_time > 19:
                            days.remove(day)
                            score -= 2
                        elif end_time > 18:
                            days.remove(day)
                            score -= 1
        return score

    def get_day_score(self):
        days = [1, 2, 3, 4, 5]
        for clas in self.classes:
            for day in clas.days:
                if day in days:
                    days.remove(day)
        score = 0
        #if there are no days off, score subtracts 1, otherwise it adds 2*(number of days off)-1
        score += 2*(len(days))-1
        #If friday is off, add 3
        if 5 in days:
            score+=3
        return score

    def get_lunch_score(self):
        #Check for a lunch break
        days = [1, 2, 3, 4, 5]
        score = 0
        for clas in self.classes:
            if clas.time < 11 and (clas.time + clas.length) > 12.5:
                #You have a lunch break
                for day in clas.days:
                    if day in days:
                        days.remove(day)
        score += 5-len(days)
        return score


    def schedule_by_day(self):
        d = {}
        for clas in self.classes:
            for day in clas.days:
                if day in d:
                    d[day].append(clas)
                else:
                    d[day] = [clas]
        return d



    def get_score(self):
        #Where some of the genetics come in
        score = 0
        score += self.get_earliest_class_score()
        score += self.get_end_class_score()
        score += self.get_day_score()
        score += self.get_lunch_score()

        return score

    def __str__(self):
        string = ""
        string = [str(clas) for clas in sorted(self.classes)]
        string = ' =/= '.join(string)
        string += " | Final Score: %s"%(self.score)
        return string
    
    def __lt__(self, other):
        if self.score == other.score:
            return self.score < other.score
        return self.score > other.score



#FOR AM-PM TIMES, PUT INTO MILITARY TIME
class_names =  [
                "AFAS",
                "MUSLIM",
                "INDIA",
                "PSYCH",
                "PHILOSOPHY",
                "HAPPINESS",
                "GLOBAL",
                "SCIENCE",
                "POLYSCI",
                "ALGORITHMS",
                "MATH 101",
                "MATH 202",
                "DATABASES",
                "ASTRONOMY",
                "PHYSICS",
                "BIOLOGY",
                "ACCOUNTING",
                "AGRICULTURE",
                "ART EDUCATION",
                "ARABIC",
                "CHEMISTRY",
                "CIVILENG",
                "LAW",
                "CHINESE",
                "SPANIS",
                "ANTRHO",
                "NEUROSCIENCE",
                "PHYSIOLOGY",
                "FILM",
                "GEOLOGY",
                "BIOCHEMISTRY",
                "COGNITIVE",
                "MARKETING",
                "ENTREPRENEURSHIP",
                "LINEAR ALGEBRA",
                "VECTOR CALCULUS",
                "GYMNASIUM",
                "COMMUNICATION",
                "ADMINISTRATION",
                "DANCE",
                "LATIN",
                "AEROSPACE",
                "ANIMALSCI",
                "ANTHROPOLOGY",
                "JUSTICEADMIN",
                "INFORMATICS",
                "MIS",
                "BIOINFORMATICS",
                "HEALTH",
                "NUTRITION",
                "DIETARY",
                "GREEKLANG",
                "ENGLISH",
                "JAPANESE",
                "HEBREW",
                "CRIMINAL",
                "FRENCH",
                "GEOGRAPHY",
                "GERMAN",
                "HISTORY",
                "JOURNALISM"
                ]



def weighted_random_time():
    #Some classes are 50 minutes, some are 1:50, some are 2:50, but around 60% are 50 minutes, 30% are 1:50, and 10% are 2:50
    weight = random.randint(1,100)
    if weight > 90:
        #For practical purposes, 2.9 will be 2:50 length
        return 2.9
    elif weight > 60:
        return 1.9
    else:
        return .9

def make_initial_classes():
    all_classes = {}
    for thing in class_names:
        #times in random range between 7am and 8:30 pm, aka 20.5. Days are a random list of size 1-5 with numbers between 1-5, 1 being monday, 5 being friday
        all_classes[thing] = {"time" : float(random.randrange(14,41))/2, "length" : weighted_random_time(), "days" : sorted(set((random.randint(1,5) for i in xrange(random.randint(1,5)))))}
    
    classes= []
    for name, desc in all_classes.iteritems():
        classes.append(Class(name, desc["time"], desc["length"], desc["days"]))

    return classes

def create_random_schedule(potential_classes):
    count = 0
    classes = []
    total = len(potential_classes)
    #The count ensures that there are no infinite loops if there are overlaps
    while len(classes) < 6 and count < total:
        randclas = random.choice(potential_classes)
        potential_classes.remove(randclas)

        flag = True
        for clas in classes:
            if randclas.overlaps(clas):
                flag = False
        if flag == True:
            classes.append(randclas)
        count+=1
    schedule = Schedule(classes)
    return schedule


def create_fifty_schedules(classes):
    schedules = []
    for i in xrange(50):
        temp = copy.copy(classes)
        schedules.append(create_random_schedule(temp))

    return schedules

def repopulate(top_schedules):
    new_classes = []
    schedule_scores = 0
    for sched in top_schedules:
        for clas in sched.get_classes():
            new_classes.append(clas)
        schedule_scores+= float(sched.score)

    print "Top Schedule average: %f"%(schedule_scores/15)

    new_classes = list(set(new_classes))

    schedules = sorted(create_fifty_schedules(new_classes))
    for sched in schedules[0:5]:
        print sched
    print "\n"
    return schedules

def genetic(schedules):
    for i in xrange(5):
        top_schedules = schedules[0:15]
        schedules = repopulate(top_schedules)
    return schedules

def main():
    classes = make_initial_classes()

    schedules = create_fifty_schedules(classes)
    schedules = sorted(schedules)

    schedules = genetic(schedules)
    
    #Test schedule
    for sched in schedules[0:5]:
        print sched
    

if __name__ == '__main__':
    main()

