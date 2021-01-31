import module
import tutor
import ReaderWriter
import timetable
import random
import math

class Scheduler:

	def __init__(self,tutorList, moduleList):
		self.tutorList = tutorList
		self.moduleList = moduleList

	#Using the tutorlist and modulelist, create a timetable of 5 slots for each of the 5 work days of the week.
	#The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
	#	timetableObj.addSession("Monday", 1, Smith, CS101, "module")
	#This line will set the session slot '1' on Monday to the module CS101, taught by tutor Smith.
	#Note here that Smith is a tutor object and CS101 is a module object, they are not strings.
	#The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
	#The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in tasks 2 and 3.
	#Tutor (3rd argument) and module (4th argument) can be assigned any value, but if the tutor or module is not in the original lists,
	#	your solution will be marked incorrectly.
	#The final, 5th argument, is the session type. For task 1, all sessions should be "module". For task 2 and 3, you should assign either "module" or "lab" as the session type.
	#Every module needs one "module" and one "lab" session type.

	#moduleList is a list of Module objects. A Module object, 'm' has the following attributes:
	# m.name  - the name of the module
	# m.topics - a list of strings, describing the topics that module covers e.g. ["Robotics", "Databases"]

	#tutorList is a list of Tutor objects. A Tutor object, 't', has the following attributes:
	# t.name - the name of the tutor
	# t.expertise - a list of strings, describing the expertise of the tutor.

	#For Task 1:
	#Keep in mind that a tutor can only teach a module if the module's topics are a subset of the tutor's expertise.
	#Furthermore, a tutor can only teach one module a day, and a maximum of two modules over the course of the week.
	#There will always be 25 modules, one for each slot in the week, but the number of tutors will vary.
	#In some problems, modules will cover 2 topics and in others, 3.
	#A tutor will have between 3-8 different expertise fields.

	#For Task 2 and 3:
	#A tutor can only teach a lab if they have at least one expertise that matches the topics of the lab
	#Tutors can only manage a 'credit' load of 4, where modules are worth 2 and labs are worth 1.
	#A tutor can not teach more than 2 credits per day.

	#You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need.
	#Furthermore, you should not import anything else beyond what has been imported above.

	#This method should return a timetable object with a schedule that is legal according to all constraints of task 1.
	def createSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(1)

		#Here is where you schedule your timetable

		#This line generates a random timetable, that may not be valid. You can use this or delete it.
		#self.randomModSchedule(timetableObj)

		self.modSchedule(timetableObj)

		#Do not change this line
		return timetableObj

	#Now, we have introduced lab sessions. Each day now has ten sessions, and there is a lab session as well as a module session.
	#All module and lab sessions must be assigned to a slot, and each module and lab session require a tutor.
	#The tutor does not need to be the same for the module and lab session.
	#A tutor can teach a lab session if their expertise includes at least one topic covered by the module.
	#We are now concerned with 'credits'. A tutor can teach a maximum of 4 credits. Lab sessions are 1 credit, module sessiosn are 2 credits.
	#A tutor cannot teach more than 2 credits a day.
	def createLabSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(2)
		#Here is where you schedule your timetable

		#This line generates a random timetable, that may not be valid. You can use this or delete it.
		self.labModSchedule(timetableObj)

		#Do not change this line
		return timetableObj

	#It costs £500 to hire a tutor for a single module.
	#If we hire a tutor to teach a 2nd module, it only costs £300. (meaning 2 modules cost £800 compared to £1000)
	#If those two modules are taught on consecutive days, the second module only costs £100. (meaning 2 modules cost £600 compared to £1000)

	#It costs £250 to hire a tutor for a lab session, and then £50 less for each extra lab session (£200, £150 and £100)
	#If a lab occurs on the same day as anything else a tutor teaches, then its cost is halved.

	#Using this method, return a timetable object that produces a schedule that is close, or equal, to the optimal solution.
	#You are not expected to always find the optimal solution, but you should be as close as possible.
	#You should consider the lecture material, particular the discussions on heuristics, and how you might develop a heuristic to help you here.
	def createMinCostSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(3)

		#Here is where you schedule your timetable

		#This line generates a random timetable, that may not be valid. You can use this or delete it.
		self.minCostLabModSchedule(timetableObj)

		#Do not change this line
		return timetableObj

	labmodList = []
	modList = []
	tutorListCopy = []
	labMatching = []
	modMatching = []

	# returns true is the tutors expertise is matching the module's topics
	def expertiseIsSufficientForMod(self, module, tutor):
		for topic in module.topics:
			if topic not in tutor.expertise:
				return False
		return True

	# returns true is the tutors expertise is sufficient to teach that lab
	def expertiseIsSufficientForLab(self, lab, tutor):
			for topic in lab.topics:
				if topic in tutor.expertise:
					return True
			return False

	#retur true if the expertise of the tutor is sufficient to teach the given module or lab
	def expertiseIsSufficient(self, labmod, tutor):
		if (labmod[1] == 'module'):
			return self.expertiseIsSufficientForMod(labmod[0], tutor)
		if (labmod[1] == 'lab'):
			return self.expertiseIsSufficientForLab(labmod[0], tutor)

	#returns the number of credits the tutor would be teaching if they were teaching the session (lab or module)
	def creditsTaught(self, labmod, tutor):
		credits = 0
		for match in self.labMatching:
			if(match[1] == tutor and match[0][1] == "module"):
				credits = credits + 2
			if(match[1] == tutor and match[0][1] == "lab"):
				credits = credits + 1
		if labmod[1] == 'module':
			return credits + 2
		if labmod[1] == 'lab':
			return credits + 1
		return False

	#Returns the number of labs and modules a tutor is teaching
	def labsModsTaught(self, tutor):
		labsmods = [[],[]]
		for match in self.labMatching:
			if(match[1] == tutor and match[0][1] == "module"):
				labsmods[1].append(match[0][0])
			if(match[1] == tutor and match[0][1] == "lab"):
				labsmods[0].append(match[0][0])
		return labsmods

	#returns the number of credits a tutor would be teaching with the given module (used when only modules are assigned)
	def modCreditsTaught(self, mod, tutor):
		credits = 0
		for match in self.modMatching:
			if(match[1] == tutor):
				credits = credits + 2
		return credits + 2

	def findModWOTut(self):
		for mod in self.modList:
			woTut = True
			for match in self.modMatching:
				if mod == match[0]:
					woTut = False
			if woTut:
				return mod
		return 'finished'

	#This method shcedules the 5x5 timetable with a module and tutor assigned to every slot
	def modSchedule(self, timetableObj):

		#list of pairs of the type : [module, number of tutors eligible to teach module]
		moduleTutors = []
		for i, mod in enumerate(self.moduleList):
			moduleTutors.append([mod, 'module'])
			self.modList.append([mod, 'module'])
			numTut = 0
			for tut in self.tutorList:
				if self.expertiseIsSufficientForMod(mod, tut):
					numTut = numTut + 1
			moduleTutors[i].append(numTut)

		#orderes the possible labs and modules by the number of tutors eligible to teach them in increasing order
		n = len(moduleTutors)
		for i in range(n):
			for j in range(n):
				if moduleTutors[i][2] > moduleTutors[j][2]:
					moduleTutors[i], moduleTutors[j] = moduleTutors[j], moduleTutors[i]
					self.modList[i], self.modList[j] = self.modList[j], self.modList[i]

		self.tutorListCopy = self.tutorList.copy()

		#orderes the tutors by the number of topics that is included in their expertise in decreasing order
		n = len(self.tutorListCopy)
		for i in range(n):
			for j in range(0, n):
				if len(self.tutorListCopy[i].expertise) < len(self.tutorListCopy[j].expertise):
					self.tutorListCopy[i], self.tutorListCopy[j] = self.tutorListCopy[j], self.tutorListCopy[i]
		n = len(self.tutorListCopy)

		self.recurModMatching()

		sessionTimes = []
		for slot in [1, 2, 3, 4, 5]:
			for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
				sessionTimes.append([day,slot])

		#in an order of the tutors add all sessions to a timeslot, since the timeslots are ordered by hour,
		#a tutor will not be teaching two classes on the same day
		n = len(self.modMatching)
		for tut in self.tutorList:
			for i in range(n):
				if (self.modMatching[i][1] == tut):
					match = self.modMatching[i]
					if not timetableObj.sessionAssigned(sessionTimes[0][0], sessionTimes[0][1]):
						timetableObj.addSession(sessionTimes[0][0], sessionTimes[0][1], match[1], match[0][0], match[0][1])
						del sessionTimes[0]

	#This method recursively with backtracking find a matching of a tutor to all modules
	def recurModMatching(self):

		#The recursion stops when there are no more modules without a tutor
		mod = self.findModWOTut()
		if mod == 'finished':
			return self.modMatching

		for i, tutor in enumerate(self.tutorListCopy):
			if(self.expertiseIsSufficient(mod, tutor) and self.modCreditsTaught(mod, tutor) <= 4):
				self.modMatching.append([mod, tutor])
				result = self.recurModMatching()
				if result != 'fail':
					return result
				del self.modMatching[-1]
		return 'fail'

	#This method shcedules the 5x10 timetable with a module or a lab and tutor assigned to every slot
	def labModSchedule(self, timetableObj):

		#list of : [module, number of tutors eligible to teach module]
		moduleTutors = []
		for i, mod in enumerate(self.moduleList):
			moduleTutors.append([mod, 'module'])
			self.labmodList.append([mod, 'module'])
			numTut = 0
			for tut in self.tutorList:
				if self.expertiseIsSufficientForMod(mod, tut):
					numTut = numTut + 1
			moduleTutors[i].append(numTut)

		#list of : [lab, number of tutors eligible to teach lab]
		labTutors = []
		for i, lab in enumerate(self.moduleList):
			labTutors.append([lab, 'lab'])
			self.labmodList.append([lab, 'lab'])
			numTut = 0
			for tut in self.tutorList:
				if self.expertiseIsSufficientForLab(lab, tut):
					numTut = numTut + 1
			labTutors[i].append(numTut)

		#orderes the possible labs and tutors by the number of tutors eligible to teach them in decreasing order
		labmodTutors = moduleTutors + labTutors
		n = len(labmodTutors)
		for i in range(n):
			for j in range(n):
				if labmodTutors[i][2] > labmodTutors[j][2]:
					labmodTutors[i], labmodTutors[j] = labmodTutors[j], labmodTutors[i]
					self.labmodList[i], self.labmodList[j] = self.labmodList[j], self.labmodList[i]

		self.tutorListCopy = self.tutorList.copy()

		#orderes the tutors by the nunber of topics that is included in their expertise in decreasing order
		n = len(self.tutorListCopy)
		for i in range(n):
			for j in range(0, n):
				if len(self.tutorListCopy[i].expertise) < len(self.tutorListCopy[j].expertise):
					self.tutorListCopy[i], self.tutorListCopy[j] = self.tutorListCopy[j], self.tutorListCopy[i]

		self.recurLabModMatching()

		sessionTimes = []
		for slot in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
			for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
				sessionTimes.append([day,slot])

		#in an order of the tutors add all sessions to a timeslot, since the timeslots are ordered by hour,
		#a tutor will not be teaching two classes on the same day
		n = len(self.labMatching)
		for tut in self.tutorList:
			for i in range(n):
				if (self.labMatching[i][1] == tut):
					match = self.labMatching[i]
					if not timetableObj.sessionAssigned(sessionTimes[0][0], sessionTimes[0][1]):
						timetableObj.addSession(sessionTimes[0][0], sessionTimes[0][1], match[1], match[0][0], match[0][1])
						del sessionTimes[0]

	#This method recursively with backtracking find a matching of a tutor to all modules or labs
	def recurLabModMatching(self):

		labmod = self.findLabModWOTut()
		if labmod == 'finished':
			return self.labMatching

		for tutor in self.tutorListCopy:
			if(self.expertiseIsSufficient(labmod, tutor) and self.creditsTaught(labmod, tutor) <= 4):
				self.labMatching.append([labmod, tutor])
				result = self.recurLabModMatching()
				if result != 'fail':
					return result
				del self.labMatching[-1]
		return 'fail'


	#This method shcedules the 5x10 timetable with a module or a lab and tutor assigned to every slot, while
	#it is aiming minimize the cost of tutors
	def minCostLabModSchedule(self, timetableObj):

		#list of : [module, number of tutors eligible to teach module]
		moduleTutors = []
		for i, mod in enumerate(self.moduleList):
			moduleTutors.append([mod, 'module'])
			self.labmodList.append([mod, 'module'])
			numTut = 0
			for tut in self.tutorList:
				if self.expertiseIsSufficientForMod(mod, tut):
					numTut = numTut + 1
			moduleTutors[i].append(numTut)

		#list of : [lab, number of tutors eligible to teach lab]
		labTutors = []
		for i, lab in enumerate(self.moduleList):
			labTutors.append([lab, 'lab'])
			self.labmodList.append([lab, 'lab'])
			numTut = 0
			for tut in self.tutorList:
				if self.expertiseIsSufficientForLab(lab, tut):
					numTut = numTut + 1
			labTutors[i].append(numTut)

		#orderes the possible labs and tutors by the number of tutors eligible to teach them in decreasing order
		labmodTutors = moduleTutors + labTutors
		n = len(labmodTutors)
		for i in range(n):
			for j in range(n):
				if labmodTutors[i][2] > labmodTutors[j][2]:
					labmodTutors[i], labmodTutors[j] = labmodTutors[j], labmodTutors[i]
					self.labmodList[i], self.labmodList[j] = self.labmodList[j], self.labmodList[i]

		self.tutorListCopy = self.tutorList.copy()

		#orderes the tutors by the nunber of topics that is included in their expertise in decreasing order
		n = len(self.tutorListCopy)
		for i in range(n):
			for j in range(0, n):
				if len(self.tutorListCopy[i].expertise) < len(self.tutorListCopy[j].expertise):
					self.tutorListCopy[i], self.tutorListCopy[j] = self.tutorListCopy[j], self.tutorListCopy[i]

		self.recurMinCostLabModMatching()

		days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
		sessionTimes = []
		for slot in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
			for day in [0, 1, 2, 3, 4]:
				sessionTimes.append([day,slot])

		#in an order of the tutors add all sessions to a timeslot, since the timeslots are ordered by hour,
		#a tutor will not be teaching two classes on the same day
		orderedMatching = []
		n = len(self.labMatching)
		for tut in self.tutorList:
			for i in range(n):
				if (self.labMatching[i][1] == tut):
					match = self.labMatching[i]
					orderedMatching.append(match)

		modSlots = []
		for slot in [1,2,3,4,5,6,7,8,9,10]:
			for day in ['Monday', 'Tuesday']:
				modSlots.append([day,slot])
		modSlots = modSlots + [['Wednesday', 1],['Thursday', 1],['Wednesday', 2],['Thursday', 2],['Friday', 1]]

		labSlots = []
		for slot in [3,5,7,9]:
			for day in ['Friday', 'Thursday', 'Wednesday']:
				labSlots.append([day,slot])
				labSlots.append([day, slot+1])
		labSlots.append(['Friday', 2])

		unsafeTutor = []

		#assign the matches from a tutor who teach 2 modules
		for tutor in self.tutorList:
			labmods = self.labsModsTaught(tutor)
			if len(labmods[1]) == 2:
				timetableObj.addSession(modSlots[0][0], modSlots[0][1], tutor, labmods[1][0], 'module')
				timetableObj.addSession(modSlots[1][0], modSlots[1][1], tutor, labmods[1][1], 'module')
				del modSlots[0]
				del modSlots[0]
		#assign the module of tutors how also teach 1 or 2 labs
		for tutor in self.tutorList:
			labmods = self.labsModsTaught(tutor)
			if len(labmods[1]) == 1 and len(labmods[0]) == 2:
				timetableObj.addSession(modSlots[0][0], modSlots[0][1], tutor, labmods[1][0], 'module')
				if (modSlots[0][0] in ['Wednesday', 'Thursday', 'Friday']):
					unsafeTutor.append(tutor)
					i=0
					while modSlots[0][0] == labSlots[i][0]:
						i = i + 1
					timetableObj.addSession(labSlots[i][0], labSlots[i][1], tutor, labmods[0][0], 'lab')
					timetableObj.addSession(labSlots[i+1][0], labSlots[i+1][1], tutor, labmods[0][1], 'lab')
					del labSlots[i]
					del labSlots[i]
				del modSlots[0]

			if len(labmods[1]) == 1 and len(labmods[0]) == 1:
				timetableObj.addSession(modSlots[0][0], modSlots[0][1], tutor, labmods[1][0], 'module')
				if (modSlots[0][0] in [ 'Friday', 'Thursday', 'Wednesday']):
					unsafeTutor.append(tutor)
					i=1
					while modSlots[0][0] == labSlots[-i][0]:
						i = i + 1
					timetableObj.addSession(labSlots[-i][0], labSlots[-i][1], tutor, labmods[0][0], 'lab')
					del labSlots[-i]
				del modSlots[0]
			if len(labmods[1]) == 1 and len(labmods[0]) == 0:
				timetableObj.addSession(modSlots[0][0], modSlots[0][1], tutor, labmods[1][0], 'module')
				del modSlots[0]

		#put tutors in with 4 labs
		for tutor in self.tutorList:
			labmods = self.labsModsTaught(tutor)
			if len(labmods[0]) == 4:
				timetableObj.addSession(labSlots[0][0], labSlots[0][1], tutor, labmods[0][0], 'lab')
				timetableObj.addSession(labSlots[1][0], labSlots[1][1], tutor, labmods[0][1], 'lab')
				day = labSlots[0][0]
				del labSlots[0]
				del labSlots[0]
				i=0
				while day == labSlots[i][0]:
					i = i + 1
				timetableObj.addSession(labSlots[i][0], labSlots[i][1], tutor, labmods[0][2], 'lab')
				timetableObj.addSession(labSlots[i+1][0], labSlots[i+1][1], tutor, labmods[0][3], 'lab')
				del labSlots[i]
				del labSlots[i]

		#tutors in with 3 labs
		for tutor in self.tutorList:
			labmods = self.labsModsTaught(tutor)
			if len(labmods[0]) == 3:
				day = labSlots[0][0]
				timetableObj.addSession(labSlots[0][0], labSlots[0][1], tutor, labmods[0][0], 'lab')
				timetableObj.addSession(labSlots[1][0], labSlots[1][1], tutor, labmods[0][1], 'lab')
				del labSlots[0]
				del labSlots[0]
				i=1
				while day == labSlots[-i][0]:
					i = i + 1
				timetableObj.addSession(labSlots[-i][0], labSlots[-i][1], tutor, labmods[0][2], 'lab')
				del labSlots[-i]

		#tutors in with 2 labs without module
		for tutor in self.tutorList:
			labmods = self.labsModsTaught(tutor)
			if len(labmods[0]) == 2 and tutor not in unsafeTutor:
				timetableObj.addSession(labSlots[0][0], labSlots[0][1], tutor, labmods[0][0], 'lab')
				timetableObj.addSession(labSlots[1][0], labSlots[1][1], tutor, labmods[0][1], 'lab')
				del labSlots[0]
				del labSlots[0]

		#tutors in with 1 lab without module
		for tutor in self.tutorList:
			labmods = self.labsModsTaught(tutor)
			if len(labmods[0]) == 1 and tutor not in unsafeTutor:
				timetableObj.addSession(labSlots[-1][0], labSlots[-1][1], tutor, labmods[0][0], 'lab')
				del labSlots[-1]

	days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

	#returns a module or a lab that has not been assigned a tutor yet
	def findLabModWOTut(self):
		for labmod in self.labmodList:
			woTut = True
			for match in self.labMatching:
				if labmod == match[0]:
					woTut = False
			if woTut:
				return labmod
		return 'finished'

	def teaching(self, tutor):
		module = False
		lab = False
		for match in self.labMatching:
			if match [1] == tutor:
				if match[0][1] == 'module':
					module = True
				if match[0][1] == 'lab':
					lab = True
		if module and lab:
			return 'X'
		if module:
			return 'M'
		if lab:
			return 'L'
		return '0'

	#This method recursively with backtracking find a matching of a tutor to all modules or labs
	def recurMinCostLabModMatching(self):

		labmod = self.findLabModWOTut()
		if labmod == 'finished':
			return self.labMatching

		# #For a faster higher-cost solution comment this in until specified
		# orderTutorList = self.tutorListCopy.copy()
		# orTutLi = []
		# typeList = []
		# for i, tutor in enumerate(self.tutorListCopy):
		# 	typeList.append(self.teaching(tutor))
		#
		# if labmod[1] == 'module':
		# 	for i, tutor in enumerate(self.tutorListCopy):
		# 		if typeList[i] == 'M':
		# 			orTutLi.append(tutor)
		#
		# 	for i, tutor in enumerate(self.tutorListCopy):
		# 		if typeList[i] == '0':
		# 			orTutLi.append(tutor)
		#
		# 	for i, tutor in enumerate(self.tutorListCopy):
		# 		if typeList[i] == 'L':
		# 			orTutLi.append(tutor)
		#
		# 	for i, tutor in enumerate(self.tutorListCopy):
		# 		if typeList[i] == 'X':
		# 			orTutLi.append(tutor)
		#
		# if labmod[1] == 'lab':
		# 	for i, tutor in enumerate(self.tutorListCopy):
		# 		if typeList[i] == 'L':
		# 			orTutLi.append(tutor)
		#
		# 	for i, tutor in enumerate(self.tutorListCopy):
		# 		if typeList[i] == 'X':
		# 			orTutLi.append(tutor)
		#
		# 	for i, tutor in enumerate(self.tutorListCopy):
		# 		if typeList[i] == '0':
		# 			orTutLi.append(tutor)
		#
		# 	for i, tutor in enumerate(self.tutorListCopy):
		# 		if typeList[i] == 'M':
		# 			orTutLi.append(tutor)
		# #until here

		#Slower,lower cost - comment in
		#for tutor in orTutLi:

		#Faster,higher cost - comment out
		for tutor in self.tutorListCopy:

			if(self.expertiseIsSufficient(labmod, tutor) and self.creditsTaught(labmod, tutor) <= 4):
				self.labMatching.append([labmod, tutor])
				result = self.recurMinCostLabModMatching()
				if result != 'fail':
					return result
				del self.labMatching[-1]
		return 'fail'
