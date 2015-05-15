#include <stdio.h>

#define _TAX	5	/* Á”ïÅ [%] */

/* Á”ïÅ(lÌŒÜ“ü)‰ÁZ */
#define taxadd(fare) (fare + ((fare * 1000 * _TAX / 100000) + 5) / 10 * 10)

#define FALSE 0
#define ASSERT(c) 

int Fare_d(int km)
{
	int fare;
	int c_km;

	if (km <= 30) {							// 1 to 3km
		return 130;
	}
	if (km <= 60) {							// 4 to 6km
		return 150;
	}
	if (km <= 100) {						// 7 to 10km
		return 160;
	}
	if (3000 < km) {						// 300km‰z‚¦‚Í–¢’è‹`
		ASSERT(FALSE);
		return -1;
	} else if (1000 < km) {					// 100.1-300km‚Í20ƒLƒ‚İ
		c_km = (km - 1) / 200 * 200 + 100;
	} else if (500 < km) {					// 50.1-100km‚Í10ƒLƒ‚İ
		c_km = (km - 1) / 100 * 100 + 50;
	} else if (100 < km) {					// 10.1-50km‚Í5ƒLƒ‚İ
		c_km = (km - 1) / 50 * 50 + 30;
	} else {
		ASSERT(FALSE);
	}
	fare = 1325 * c_km;
	
	if (c_km <= 1000) {	// 100kmˆÈ‰º‚ÍØ‚èã‚°
		// 1‚ÌˆÊ‚ğØ‚èã‚°
		fare = (fare + 9999) / 10000 * 10;
	} else {								// 100‡q‰z‚¦‚ÍlÌŒÜ“ü
		fare = (fare + 50000) / 100000 * 100;
	}
	return taxadd(fare);	// tax = +5%, lÌŒÜ“ü
}

int main(int argc, char** argv)
{
	int i;
	int c;
	int f;
	c = 0;
	for (i = 0; i < 1000; i++) {
		f = Fare_d(i);
		if (c != f) {
			printf("%d=>%d ", i, f);
			c = f;
		}
	}
	return 0;
}
