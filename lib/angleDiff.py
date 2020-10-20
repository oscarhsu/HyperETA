def angleDiff(a ,b):
	result = abs(a - b)
	result = result.values
	if len(a) > 1:
		index = result > 180
		result[index] = 360 - result[index]
	else:
		if result > 180:
			result = 360 - result
	return result
