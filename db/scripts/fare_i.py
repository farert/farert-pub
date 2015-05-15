import sys

def lf(km):
	km *= 10
	if 5460 < km:
		fare = 1780 * 2730 + 1410 * (5460 - 2730) + 705 * (km - 5460) 
	elif 2730 < km:
		fare = 1780 * 2730 + (km - 2730) * 1410
	else:
		fare = km * 1780


	#if km <= 1000:
	#	fare = int((fare + 999) / 1000) * 10
	#else:
	#	fare = int((fare + 5000) / 10000) * 100
	#
	#return fare + int((int(fare / 10) / 2 + 5) / 10) * 10
	##return fare + int((int(fare * 0.05) + 5) / 10) * 10

	if (km <= 1000) :	# 100km以下は切り上げ
		# 1の位を切り上げ
		fare = (fare + 9999) // 10000 * 10
	else:				# 100㎞越えは四捨五入
		fare = (fare + 50000) // 100000 * 100

	return fare + ((fare // 10 // 2) + 5) // 10 * 10 # tax = +5%, 四捨五入


if 1 < len(sys.argv):
	k = int(sys.argv[1])
	print(k, lf(k))
else:
	for k in [96, 119, 137, 155, 173, 191, 210, 228, 246, 264]:
		print(k, lf(k))

	print(":::")
	for k in [282,301,319,337,355,373,391,410,428,446,464,482,501,519,537]:
		print(k, lf(k))
	
	print(":::")
	for k in [564,601,637,673,710,746,782,819,855,892,928,964,1001,1037,1073,1110,1146,1182]:
		print(k, lf(k))



