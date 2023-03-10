class ConditionalSumWithBound:
	def __init__(self,x,w,v,lb,ub,name):
		self.__x__ = x
		self.__w__ = w
		self.__v__ = v
		self.__lb__ = lb #lower bound
		self.__ub__ = ub #upper bound
		self.__name__ = name
		if x == None or len(x) == 0:
			return
		self.__map__ = {}
		self.__mgr__ = x[0].getLocalSearchManager()
		self.__value__ = 0
		self.__mgr__.postInvariant(self)
		self.__depended__ = set()# set of components that depend on self
		for i in x:
			i.getDependedComponents().add(self)
		self.__minValue__ = 0
		self.__maxValue__ = 0
		self.__violations__ = 0
		self.__variables__ = [x,w,v]
		for wi in w:
			self.__maxValue__ += wi

		for i in range(len(self.__x__)):
			self.__map__[self.__x__[i]] = i

	def name(self):
		return self.__name__

	def getMinValue(self):
		return self.__minValue__

	def getMaxValue(self):
		return self.__maxValue__

	def getVariables(self):
		return self.__x__

	def getLocalSearchManager(self):
		return self.__mgr__

	def getDependedComponents(self):
		return self.__depended__

	def violations(self):
		return self.__violations__

	def initPropagation(self):
		self.__value__ = 0
		for i in range(len(self.__x__)):
			#print(self.name() + '::initPropagation, x[' + str(i) + '].getValue = ',self.__x__[i].getValue(),' v = ',self.__v__)
			if self.__x__[i].getValue() == self.__v__:
				self.__value__ += self.__w__[i]

		#print(self.__name__ + '::initPropagate, value = ' + str(self.__value__))

		if self.__value__ > self.__ub__ or self.__value__ < self.__lb__:
			self.__violations__ = 1
		else:
			self.__violations__ = 0

	def propagate(self,x):
		if self.__map__[x] == None:
			return
		k = self.__map__[x]
		nv = self.__value__
		t = x.getOldValue()
		if t == self.__v__:
			if x.getValue() == self.__v__:
				nv = nv
			else:
				nv = nv - self.__w__[k]
		else:
			if x.getValue() == self.__v__:
				nv = nv + self.__w__[k]
			else:
				nv = nv

		self.__value__ = nv

		#print(self.__name__ + '::propagate, violations = ' + str(self.__violations__))

	def getValue(self):
		return self.__value__

	def getSwapDelta(self,x,y):
		if self.__map__[x] == None and self.__map__[y] == None:
			return 0
		if self.__map__[x] == None:
			return self.getAssignDelta(y,x.getValue())
		if self.__map__[y] == None:
			return self.getAssignDelta(x,y.getValue())

		return 0

	def getAssignDelta(self,x,v):
		if self.__map__[x] == None:
			return 0
		'''if self.__value__ in range(self.__lb__,self.__ub__+1):
			newV = 0
			return newV + v - self.__violations__
		else:
			newV = 1
			return newV + v - self.__violations__
		return 0'''

		if self.__x__ == x:
			return v - self.__violations__

		return 0;


