'''a new threading to detect whether it is time to rollover'''

'''RM001 is on, RM005 is on'''

# catTemplate has self.dominance, RM001 is true, RM005 false
self.ndi = None  # ndi = next dominance infomation
self.hasNotWrittenOrdersToTxt = 1
self.hasNotReadOrdersFromTxt = 1
self.toRollin = 0
self.toRollinComfirmed = 0
self.toRollout = 0
self.toRolloutComfirmed = 0

self.toRolloutDirectory = str()

def set_toRollinComfirmed(self, x):
	self.toRollinComfirmed = x

def set_toRolloutComfirmed(self, x):
	self.toRolloutComfirmed = x

# for rollout dominance
if self.toRollout and self.toRolloutComfirmed:
	if tick.datetime.time() > time(14, 55, 20) and tick.datetime.second%10==0 :
		try:
			with open('nextDominanceInfo.txt', 'r') as f:
				self.ndi = eval(f.readline())  # ndi = next dominance info
		except IOError:
			print('nextDominanceInfo.txt does not exist!')
		except SyntaxError:
			self.ndi = None
			print('nextDominanceInfo.txt is empty')

		if self.ndi:
			if self.ndi['openInterest'] > tick.openInterest:
				priceGapBetNextAndCurrentDominance = self.ndi['lastPrice'] - tick.lastPrice
				if self.rolloverAndShiftSLTP:
					ordersToRoll = copy.deepcopy(self.current_orders)
					for order in ordersToRoll:
						ordersToRoll[order]['sl'] = ordersToRoll[order]['sl'] + priceGapBetNextAndCurrentDominance
						ordersToRoll[order]['tp'] = ordersToRoll[order]['tp'] + priceGapBetNextAndCurrentDominance
						# do we need to change open price? 
						closeAll(tick.lastPrice)
						if self.hasNotWrittenOrdersToTxt
							with open('ordersToRoll.txt', 'w') as f:
								f.wriet(str(ordersToRoll))
							self.hasNotWrittenOrdersToTxt = 0
				elif self.rolloverWithSameSLTP:	
					sltpUsingNextDominanceLastPrice(self.ndi['lastPrice'])
				else:
					pass

				self.toRollout = 0
				self.toRolloutComfirmed = 0

			else:
				pass
		else:
			pass






	'''
	try:
		open dominance.txt
		self.dominanceFromTxt = ' '
	except txt does not exist
		pass

	if self.instrument != self.dominanceFromTxt:
		ordersToRoll = ?
		self.closeAll()
		self.toRollout = 0
		save ordersToRoll to txt
		ordersToRoll = None
	'''

# for rollin dominance
if self.toRollin and self.toRollinComfirmed:
	if tick.datetime.time() > time(14, 55) and tick.datetime.second==5:
		with open(self.toRolloutDirectory+'nextDominanceInfo.txt', 'w') as f:
			f.write(str({'openInterest': tick.openInterest, 'lastPrice': tick.lastPrice}))
	
	if self.hasNotReadOrdersFromTxt:
		try:
			f =  open(self.toRolloutDirectory+"ordersToRoll.txt", 'r+'):
			orders = eval(f.readline())
			f.close()
			self.hasNotReadOrdersFromTxt = 0
		except SyntaxError:  # file is empty
			orders = dict()
			self.hasNotReadOrdersFromTxt = 0	
		except IOError:  # file doen not exist
		    orders = None

	if(os.path.exists(self.toRolloutDirectory+"ordersToRoll.txt")):
		os.remove(self.toRolloutDirectory+'ordersToRoll.txt')

	if orders is None:
	    pass
	
	else:
		if len(orders) == 0:
			pass
		else:
			for order in orders:
				if 'buy' == orders[order]['direction']:
					self.buy()
				else:
					self.short()
		# become dominance
		self.toRollin = 0
		self.toRollinComfirmed = 0


# for rollover
# get two openInterests in both txt to see if 005 has becomed dominance
# if RM005 is dominance, write dominance.txt


