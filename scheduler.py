import random

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

	def get_earliest_class(self):
		return self.classes[0].time

	def get_end_time(self):
		return self.classes[len(self.classes)-1].time + self.classes[len(self.classes)-1].get_length()

	def get_total_class_time(self):
		return get_end_time - get_earliest_class

	def get_score(self):
		#Where some of the genetics come in
		score = 0
		#I REALLY want late classes after 11am so score increases 2. Will change to get_score(self, early_time) so the user can change it
		if self.get_earliest_class() >= 11:
			score += 3
		elif self.get_earliest_class() >= 10:
			score += 1
		else:
			#If it is this early subtract 3
			if self.get_earliest_class() <= 8:
				score -= 3
			elif self.get_earliest_class() <= 9:
				score -= 2
		#Check how late your day ends, if its past 5 its too late
		if self.get_end_time() < 16:
			score += 2
		elif self.get_end_time() < 17:
			score += 1
		else:
			#If the score ends after  
			if self.get_end_time() > 20:
				score -= 3
			elif self.get_end_time() > 19:
				score -= 2
			elif self.get_end_time() > 18:
				score =- 1

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


#print [str(clas) for clas in classes]

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

def overlapping(class1, class2):
	class1_start = class1.time
	class1_end = class1_start + class1.length

	class2_start = class2.time
	class2_end = class2_start + class2.length

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

def create_random_schedule(potential_classes):
	classes = []
	classes.append(random.choice(potential_classes))
	while len(classes) < 5:
		randclas = random.choice(potential_classes)
		flag = True
		for clas in classes:
			if overlapping(randclas, clas):
				flag = False
				break
		if flag == True:
			classes.append(randclas)
	schedule = Schedule(classes)
	return schedule


def create_fifty_schedules(classes):
	schedules = []
	for i in xrange(50):
		schedules.append(create_random_schedule(classes))
	return schedules

def create_classes():
	all_classes = {}
	for thing in class_names:
		#times in random range between 7am and 8:30 pm, aka 20.5. Days are a random list of size 1-5 with numbers between 1-5, 1 being monday, 5 being friday
		all_classes[thing] = {"time" : float(random.randrange(14,41))/2, "length" : weighted_random_time(), "days" : sorted(set((random.randint(1,5) for i in xrange(random.randint(1,5)))))}
	
	classes= []
	for name, desc in all_classes.iteritems():
		classes.append(Class(name, desc["time"], desc["length"], desc["days"]))

	return classes

def main():
	classes = create_classes()

	schedules = create_fifty_schedules(classes)
	schedules = sorted(schedules)


	for schedule in schedules:
		print schedule

	


if __name__ == '__main__':
	main()