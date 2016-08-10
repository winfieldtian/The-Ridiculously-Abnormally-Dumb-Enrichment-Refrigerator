#pylint: skip-file

import pdb
import sys

simpleMovingAverage = []
periodClose = []
stochasticsLow = []
stochasticsHigh = []
stochasticsK = []
stochasticsD = []
stochasticsDSlow = []
RSI = []

avgGain = 0
avgLoss = 0
initRSIGain = 0
initRSILoss = 0

PERIOD = 11 #must be greater than 2
INIT_CONSTANT = 250
MINUTE_PERIOD = 1
portfolioValue = 1000000
portfolioValueFee = 1000000
SKIP_DATE = 1600005 #1500000:2012, 1000000:2007

positiveMACross = False

prevClose = 0

def main():
	global positiveMACross
	global portfolioValue
	global portfolioValueFee
	global SKIP_DATE

	#OPEN FILE
	simpleMovingAverage = []
	periodClose = []
	stochasticsLow = []
	stochasticsHigh = []
	stochasticsK = []
	stochasticsD = []
	stochasticsDSlow = []
	RSI = []

	avgGain = 0
	avgLoss = 0
	initRSIGain = 0
	initRSILoss = 0

	PERIOD = 11 #must be greater than 2
	INIT_CONSTANT = 250
	MINUTE_PERIOD = 1
	portfolioValue = 1000000
	portfolioValueFee = 1000000
	SKIP_DATE = 0 #1500000:2012, 1000000:2007

	positiveMACross = False

	prevClose = 0

	initIterator = 0
	numStockPurchased = 0
	priceStockPurchased = 0
	brokerFee = 0
	counter = 0
	haveBought = 0

	minuteCount = 0

	minuteOpen = 0
	minuteHigh = 0
	minuteLow = 0
	minuteClose = 0
	mostRecentPortfolioValue = 0
	counterOn = True

	with open("data/SAMPLE_MSFT.txt", 'r') as tickDataFile:
		for tickDataLine in tickDataFile:
			if SKIP_DATE != 0:
				SKIP_DATE -= 1

			else:
				minuteTickValues = tickDataLine.split(',')
				minuteOpen = stringToCents(minuteTickValues[2])
				minuteHigh = stringToCents(minuteTickValues[3])
				minuteLow = stringToCents(minuteTickValues[4])
				minuteClose = stringToCents(minuteTickValues[5])

				if initIterator < INIT_CONSTANT:
					initData(initIterator, minuteOpen, minuteClose, minuteHigh, minuteLow)
					initIterator += 1
				else:
					computePeriodClose(minuteClose)
					computeSimpleMovingAverage()
					computeStochastics(minuteClose, minuteHigh, minuteLow)
					computeRSI(minuteOpen, minuteClose)
					#if computeSimpleMovingAveragePosCross() == True:
					#	positiveMACross = True


					if checkBuy() == True and numStockPurchased <= 0:


						numStockPurchased = portfolioValue / minuteClose

						priceStockPurchased = minuteClose
						brokerFee = computeBrokerFee(minuteClose, numStockPurchased)


						purchaseCost = numStockPurchased * priceStockPurchased


						#portfolioValue -= numStockPurchased * priceStockPurchased

						while (portfolioValue - purchaseCost) < brokerFee:
							numStockPurchased -= 1;
							brokerFee = computeBrokerFee(minuteClose, numStockPurchased)
							purchaseCost = numStockPurchased * priceStockPurchased

						portfolioValue -= purchaseCost
						portfolioValue -= brokerFee


						print "purchased at " + str(minuteClose)
						print RSI
						print stochasticsK
						print stochasticsD
						print stochasticsDSlow
						print "\n"

						"""
						counter += 1

						print "currently buying"
						print "portfolioValue: " + str(portfolioValue)
						print "priceStockPurchased: " + str(priceStockPurchased)
						print "minuteClose: " + str(minuteClose)
						print "numStockPurchased: " + str(numStockPurchased)
						print "counter: " + str(counter)
						pdb.set_trace()
						"""


					elif checkSell() == True and numStockPurchased > 0:
						#print "sold at " + str(minuteClose)



						brokerFee = computeBrokerFee(minuteClose, numStockPurchased)

						priceStockSold = minuteClose

						portfolioValue += numStockPurchased * priceStockSold
						portfolioValue -= brokerFee

						mostRecentPortfolioValue = portfolioValue;

						#print str(portfolioValue/100) + "  ->  " + minuteTickValues[0] + " " + arg1
						#print str(portfolioValue/100) + "  ->  " + minuteTickValues[0] + " with + " + str(numStockPurchased) + " stocks purchased "

						print RSI
						print stochasticsK
						print stochasticsD
						print stochasticsDSlow
						print "\n"

						numStockPurchased = 0
						priceStockPurchased = 0



	return mostRecentPortfolioValue


	print RSI
	print stochasticsK
	print stochasticsD
	print stochasticsDSlow

	#print "terminating"

def computeBrokerFee(minuteClose, numStockPurchased):
	maxBrokerFee = numStockPurchased * minuteClose / 200
	brokerFee = (3 * numStockPurchased ) / 4
	if brokerFee < 100:
		return 100
	if brokerFee > maxBrokerFee:
		return maxBrokerFee
	return brokerFee

def computeSimpleMovingAveragePosCross():
	idxMA = len(simpleMovingAverage)
	idxClose = len(periodClose)

	if periodClose[idxClose-2] < simpleMovingAverage[idxMA-2] and periodClose[idxClose-1] >= simpleMovingAverage[idxMA-1]:
		return True
	else:
	 	return False

def computeSimpleMovingAverageNegCross():
	idxMA = len(simpleMovingAverage)
	idxClose = len(periodClose)

	if periodClose[idxClose-2] >= simpleMovingAverage[idxMA-2] and periodClose[idxClose-1] < simpleMovingAverage[idxMA-1]:
		return True
	else:
	 	return False

def computePeriodClose(close):
	periodClose.append(close)
	periodClose.pop(0)

def computeSimpleMovingAverage():
	_computeSimpleMovingAverage()
	simpleMovingAverage.pop(0)

def _computeSimpleMovingAverage():
	MA = 0

	for val in periodClose:
		MA += val

	MA /= PERIOD
	simpleMovingAverage.append(MA)

def computeStochastics ( close, high, low ):
	computeStochasticsK(close,high,low)
	stochasticsK.pop(0)

	computeStochasticsD()
	stochasticsD.pop(0)

	computeStochasticsDSlow()
	stochasticsDSlow.pop(0)


def computeStochasticsK( close, high, low ):
	stochasticsLow.append(low)
	stochasticsLow.pop(0)

	stochasticsHigh.append(high)
	stochasticsHigh.pop(0)

	highestHigh = max(stochasticsHigh);
	lowestLow = min(stochasticsLow);

	if highestHigh - lowestLow != 0:
		K = ( 100 * ( close - lowestLow ) ) / ( highestHigh - lowestLow)
	else:
		K = 100
	stochasticsK.append(K)

def computeStochasticsD():
	D = 0
	last3 = len(stochasticsK)-1
	count = 3

	while count != 0:
		D += stochasticsK[last3]
		last3 -= 1
		count -= 1

	D /= 3
	stochasticsD.append(D)

def computeStochasticsDSlow():
	DSlow = 0

	for val in stochasticsD:
		DSlow += val

	DSlow /= 3
	stochasticsDSlow.append(DSlow)

def _computeRSI( open, close ):
	global avgGain
	global avgLoss

	diff = close - open

	if diff > 0:
		avgGain = (avgGain * (PERIOD-1) + (diff*100)) / PERIOD
		avgLoss = (avgLoss * (PERIOD-1)) / PERIOD
	else:
		avgLoss = (avgLoss * (PERIOD-1) + abs(diff*100)) / PERIOD
		avgGain = (avgGain * (PERIOD-1)) / PERIOD


	if avgGain == 0:
		currRSI = 0
	elif avgLoss == 0:
		currRSI = 100
	else:
		currRSI = 100 - (10000 / (100 + ((100*avgGain)/avgLoss ) ))

	RSI.append(currRSI)
	#RSI.pop(0)

def computeRSI( open, close):
	_computeRSI(open,close)
	RSI.pop(0)


def checkBuy():
	idxK = len(stochasticsK)
	idxD = len(stochasticsD)
	idxDSlow = len(stochasticsDSlow)
	idxRSI = len(RSI)



	#Fast Stoch
	#if stochasticsK[idxK-2] < stochasticsD[idxD-2] and stochasticsK[idxK-1] > stochasticsD[idxD-1] and stochasticsD[idxD-2] <= 20:
	#	return True

	"""
	#WTF
	if stochasticsK[idxK-2] < stochasticsDSlow[idxDSlow-2] and stochasticsK[idxK-1] > stochasticsDSlow[idxDSlow-1] and RSI[idxRSI-1] < 30 and stochasticsDSlow[idxDSlow-2] < 20:
		return True
	elif stochasticsD[idxD-2] > stochasticsDSlow[idxDSlow-2] and stochasticsD[idxD-1] < stochasticsDSlow[idxDSlow-1] and stochasticsDSlow[idxDSlow-2] < 35:
		return True
	"""
	#if stochasticsD[idxD-2] < stochasticsDSlow[idxDSlow-2] and stochasticsD[idxD-1] > stochasticsDSlow[idxDSlow-1] and RSI[idxRSI-1] < 30 and stochasticsDSlow[idxDSlow-2] < 20:
	#	return True
	#if stochasticsK[idxK-2] < stochasticsDSlow[idxDSlow-2] and stochasticsK[idxK-1] > stochasticsDSlow[idxDSlow-1] and RSI[idxRSI-1] < 30 and stochasticsDSlow[idxDSlow-2] < 20:
	#	return True
	#elif stochasticsD[idxD-2] > stochasticsDSlow[idxDSlow-2] and stochasticsD[idxD-1] < stochasticsDSlow[idxDSlow-1] and stochasticsDSlow[idxDSlow-2] < 25 and RSI[idxRSI-1] < 30:
	#	return True

	#Slow Stoch  #or if RSI[idxRSI-1] < 30 and stochasticsDSlow[DSlow-1] < 35:
	if RSI[idxRSI-1] < 25 and stochasticsK[idxK-1] < 40:
		return True
	elif stochasticsK[idxD-3] < stochasticsK[idxK-2] and stochasticsK[idxK-2] > stochasticsK[idxK-1] and stochasticsK[idxK-1] < 40:
		return True
	else:
		return False

def checkSell():
	idxK = len(stochasticsK)
	idxD = len(stochasticsD)
	idxDSlow = len(stochasticsDSlow)
	idxRSI = len(RSI)


	#WTF SELL
	if stochasticsK[idxD-3] > stochasticsK[idxK-2] and stochasticsK[idxK-2] < stochasticsK[idxK-1] and stochasticsK[idxK-1] > 70:
		return True

	elif stochasticsD[idxD-2] < stochasticsDSlow[idxDSlow-2] and stochasticsD[idxD-1] > stochasticsDSlow[idxDSlow-1] and stochasticsDSlow[idxDSlow-2] > 70:
		return True

	#Slow Stoch
	#elif stochasticsD[idxD-2] > stochasticsDSlow[idxDSlow-2] and stochasticsD[idxD-1] < stochasticsDSlow[idxDSlow-1] and stochasticsDSlow[idxDSlow-2] > 80:
	#	return True

	#Fast Stoch
	#if stochasticsK[idxK-2] > stochasticsD[idxD-2] and stochasticsK[idxK-1] < stochasticsD[idxD-1] and stochasticsD[idxD-2] >= 80:
	#	return True



	#if stochasticsK[idxD-2] > stochasticsDSlow[idxDSlow-2] and stochasticsK[idxD-1] < stochasticsDSlow[idxDSlow-1] and stochasticsDSlow[idxDSlow-2] > 80:
	#	return True
	#elif stochasticsD[idxD-2] < stochasticsDSlow[idxDSlow-2] and stochasticsD[idxD-1] > stochasticsDSlow[idxDSlow-1] and stochasticsDSlow[idxDSlow-2] > 75:
	#	return True
	else:
		return False

def initData(initIterator, open, close, high, low ):#needs 11 previous data for first RSI, #stochastics needs 15too
	global initRSIGain
	global initRSILoss
 	global avgGain
	global avgLoss

	gain = 0
	loss = 0

	diff = close - open

	if diff > 0:
		gain = diff
	else:
		loss = abs(diff)

	if initIterator < PERIOD:
		stochasticsLow.append(low)
		stochasticsHigh.append(high)
		periodClose.append(close)
		initRSIGain += gain
		initRSILoss += loss

	elif initIterator == PERIOD:
		_computeSimpleMovingAverage()
		#COMPUTE THE FIRST K AND FIRST RSI OF THE PREVIOUS 11 ITERATIONS
		highestHigh = max(stochasticsHigh);
		lowestLow = min(stochasticsLow);
		K = 100
		if highestHigh - lowestLow != 0:
			K = ( 100 * ( close - lowestLow ) ) / ( highestHigh - lowestLow)
		stochasticsK.append(K)

		if initRSIGain == 0:
			currRSI = 0
		elif initRSILoss == 0:
			currRSI = 100
		else:
			currRSI = 100 - (10000 / (100 + ((10000*initRSIGain)/PERIOD)/((100*initRSILoss)/PERIOD) ) )

		RSI.append(currRSI)
		avgGain = (initRSIGain*100)/PERIOD
		avgLoss = (initRSILoss*100)/PERIOD

		#COMPUTER THE 12TH ITERATION
		computePeriodClose(close)
		_computeSimpleMovingAverage()
		_computeRSI(open, close)
		computeStochasticsK(close,high,low)

	elif initIterator > PERIOD and initIterator <= (PERIOD+2):
		computePeriodClose(close)
		_computeSimpleMovingAverage()
		_computeRSI(open, close)
		computeStochasticsK(close,high,low)
		computeStochasticsD()

	elif initIterator == (PERIOD+3):
		computePeriodClose(close)
		_computeSimpleMovingAverage()
		_computeRSI(open, close)
		computeStochasticsK(close,high,low)
		computeStochasticsD()
		computeStochasticsDSlow()

	elif initIterator > (PERIOD+3) and initIterator <= (PERIOD+5):
		computePeriodClose(close)
		_computeSimpleMovingAverage()
		_computeRSI(open, close)
		computeStochasticsK(close,high,low)
		computeStochasticsD()
		stochasticsD.pop(0)
		computeStochasticsDSlow()

	elif initIterator > (PERIOD+5) and initIterator <= (PERIOD+9):
		computePeriodClose(close)
		_computeSimpleMovingAverage()

		_computeRSI(open, close)
		computeStochasticsK(close,high,low)
		computeStochasticsD()
		stochasticsD.pop(0)
		computeStochasticsDSlow()
		stochasticsDSlow.pop(0)

	else:
		computePeriodClose(close)
		computeSimpleMovingAverage()

		computeRSI(open, close)
		computeStochasticsK(close,high,low)
		stochasticsK.pop(0)
		computeStochasticsD()
		stochasticsD.pop(0)
		computeStochasticsDSlow()
		stochasticsDSlow.pop(0)


def stringToCents ( str ):
	value = 0
	cents = False
	truncate = 0
	for letter in str:
		if letter == '.':
			cents = True
			continue

		value *= 10
		value += int(letter)

		if cents == True:
			truncate += 1
			if truncate == 2:
				break

	if cents == False:
		return value * 100

	if truncate == 1:
		return value * 10

	return value


if __name__ == "__main__":
    main()
