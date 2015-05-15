#if !defined _ALPDB_H__

#define _ALPDB_H__
#if 0
'Farert'
Copyright (C) 2014 Sutezo (sutezo666@gmail.com)

   'Farert' is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    'Farert' is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with 'Farert'.  If not, see <http://www.gnu.org/licenses/>.

このプログラムはフリーソフトウェアです。あなたはこれを、フリーソフトウェ
ア財団によって発行された GNU 一般公衆利用許諾契約書(バージョン3か、希
望によってはそれ以降のバージョンのうちどれか)の定める条件の下で再頒布
または改変することができます。

このプログラムは有用であることを願って頒布されますが、*全くの無保証* 
です。商業可能性の保証や特定の目的への適合性は、言外に示されたものも含
め全く存在しません。詳しくはGNU 一般公衆利用許諾契約書をご覧ください。
 
あなたはこのプログラムと共に、GNU 一般公衆利用許諾契約書の複製物を一部
受け取ったはずです。もし受け取っていなければ、フリーソフトウェア財団ま
で請求してください

#endif
extern int g_tax;	/* in alps_mfc.cpp */

using namespace std;
#include <vector>

/*!	@file alpdb core logic implement.
 *	Copyright(c) sutezo9@me.com 2012.
 */
extern bool isKanaString(LPCTSTR szStr);
extern void conv_to_kana2hira(tstring& kana_str);

#define iskana(c) (_T('ァ') <= (c)) && ((c) <= _T('ン'))

typedef short IDENT;
typedef unsigned int PAIRIDENT;
typedef unsigned int SPECIFICFLAG;

#define MAKEPAIR(ident1, ident2) ((PAIRIDENT)(0xffff & ident1) | ((PAIRIDENT)ident2 << 16))
#define IDENT1(ident) ((IDENT)(0xffff & ident))
#define IDENT2(ident) ((IDENT)(0xffff & ((PAIRIDENT)ident >> 16)))

#define FLG_HIDE_LINE					(1<<19)
#define FLG_HIDE_STATION				(1<<18)
#define IS_FLG_HIDE_LINE(lflg)			(0!=(lflg&FLG_HIDE_LINE))		// 路線非表示
#define IS_FLG_HIDE_STATION(lflg)		(0!=(lflg&FLG_HIDE_STATION))		// 駅非表示

#define BSRJCTSP		31		// 分岐特例
#define	BSRJCTHORD		31		// 水平型検知フラグ

#define BSRNOTYET_NA	30		// 不完全ルート
#define BSRJCTSP_B		29		// 分岐特例B

#define BSR69TERM		24
#define BSR69CONT		23

#define JCTSP				 	1
#define JCTSP_2L			 	2
#define JCTSP_B_NISHIKOKURA 	3
#define JCTSP_B_YOSHIZUKA	 	4
#define JCTSP_B_NAGAOKA 		5

/* --------------------------------------- */
/* util */
#define NumOf(c)  (sizeof(c) / sizeof(c[0]))
#define Min(a, b) ((a)>(b)?(b):(a))
#define Max(a, b) ((a)>(b)?(a):(b))

#define MASK(bdef)	(1 << bdef)
#define BIT_CHK(flg, bdef) (0 != (flg & MASK(bdef)))
#define BIT_CHK2(flg, bdef1, bdef2) (0 != (flg & (MASK(bdef1)|MASK(bdef2))))
#define BIT_CHK3(flg, bdef1, bdef2, bdef3) (0 != (flg & (MASK(bdef1)|MASK(bdef2)|MASK(bdef3))))
#define BIT_ON(flg, bdef)  (flg |= MASK(bdef))
#define BIT_OFF(flg, bdef) (flg &= ~MASK(bdef))

#define HWORD_BIT	16		/* Number of bit in half word(unsigned short) */

/* --------------------------------------- */
#define MAX_STATION     4590
#define MAX_LINE        209
#define IS_SHINKANSEN_LINE(id)  ((0<(id))&&((id)<=7))	/* 新幹線は将来的にも10または15以内 */
#define IS_COMPANY_LINE_OF(id)     (202<(id))
//#define MAX_JCT 311

// 駅は分岐駅か
#define STATION_IS_JUNCTION(sid)	(0 != (Route::AttrOfStationId(sid) & (1<<12)))
#define STATION_IS_JUNCTION_F(flg)	(0 != (flg & (1<<12)))

	/* ID for line_id on t_lines */
#define ID_L_RULE70		-10


// length define(UTF-8)
#define MAX_STATION_CHR	32		// 38
#define MAX_LINE_CHR	32
#define MAX_COMPANY_CHR	32		// 
#define MAX_PREFECT_CHR	16

#define MAX_NUM_JCT_STATION	103
#define MAX_JCT_NUM			6		// 東京駅乗り入れ路線数が最大で6
#define MAX_JCT				320		// 311

const LPCTSTR CLEAR_HISTORY = _T("(clear)");


/* 消費税(四捨五入)加算 */
#define taxadd(fare, tax)    (fare + ((fare * 1000 * tax / 100000) + 5) / 10 * 10)
#define taxadd_ic(fare, tax) (fare + (fare * 1000 * tax / 100000))

/* round up on 5 */
#define round(d) 		(((d) + 5) / 10 * 10)	/* 10円未満四捨五入 */ 
#define round_up(d)     (((d) + 9) / 10 * 10)	/* 10円未満切り上げ */
#define round_down(d)   ((d) / 10 * 10)			/* 10円未満切り捨て */

#define KM(kmx10) ((kmx10 + 9) / 10)	/* km単位で端数は切り上げ */

/* discount */
#define fare_discount(fare, per) ((fare) / 10 * (10 - (per)) / 10 * 10)

#define CSTART	1
#define CEND	2

// DB 固定定義(DB変更のない前提のDB値定義)
//	速度考慮しSQLで取得しない
//
#define JR_HOKKAIDO	1	
#define JR_EAST		2	
#define JR_CENTRAL	3	
#define JR_WEST		4	
#define JR_KYUSYU	5	
#define JR_SHIKOKU	6	
#define JR_GROUP_MASK   ((1<<5)|(1<<4)|(1<<3)|(1<<2)|(1<<1)|(1<<0))

#define	LINE_TOHOKU_SINKANSEN	1	// 東北新幹線
#define	LINE_JYOETSU_SINKANSEN	2	// 上越新幹線
#define	LINE_HOKURIKU_SINKANSEN	3	// 北陸長野新幹線
#define	LINE_TOKAIDO_SINKANSEN	4	// 東海道新幹線
#define	LINE_SANYO_SINKANSEN	5	// 山陽新幹線
#define	LINE_KYUSYU_SINKANSEN	6	// 九州新幹線
#define	LINE_HOKKAIDO_SINKANSEN	7	// 北海道新幹線


#define CITYNO_TOKYO		1		// 東京都区内[区]
#define CITYNO_YOKOHAMA		2		// 横浜市内[浜]
#define CITYNO_NAGOYA		3		// 名古屋市内[名]
#define CITYNO_KYOUTO		4		// 京都市内[京]
#define CITYNO_OOSAKA		5		// 大阪市内[阪]
#define CITYNO_KOUBE		6		// 神戸市内[神]
#define CITYNO_HIROSIMA		7		// 広島市内[広]
#define CITYNO_KITAKYUSYU	8		// 北九州市内[九]
#define CITYNO_FUKUOKA		9		// 福岡市内[福]
#define CITYNO_SENDAI		10		// 仙台市内[仙]
#define CITYNO_SAPPORO		11		// 札幌市内[札]

#define URB_TOKYO			1
#define URB_NIGATA			2
#define URB_OSAKA			3
#define URB_FUKUOKA			4
#define URB_SENDAI			5

#define BSHINKANSEN					16
#define FLAG_FARECALC_INITIAL		(1<<15)				
#define FLAG_TOHOKU_SHINKANSEN		(1<<BSHINKANSEN)				// 1:東北新幹線
#define FLAG_JYOETSU_SHINKANSEN		(2<<BSHINKANSEN)				// 2:上越新幹線
#define FLAG_HOKURIKU_SHINKANSEN	(3<<BSHINKANSEN)				// 3:北陸長野新幹線
#define FLAG_TOKAIDO_SHINKANSEN		(4<<BSHINKANSEN)				// 4:東海道新幹線
#define FLAG_SANYO_SHINKANSEN		(5<<BSHINKANSEN)				// 5:山陽新幹線
#define FLAG_KYUSYU_SHINKANSEN		(6<<BSHINKANSEN)				// 6:九州新幹線
#define FLAG_HOKKAIDO_SHINKANSEN	(7<<BSHINKANSEN)				// 7:北海道新幹線
#define FLAG_SHINKANSEN				0x000f0000			// 新幹線	aggregate_fare_info()の最後で設定
#define MASK_SHINKANSEN				0x0f				// 新幹線	aggregate_fare_info()の最後で設定
#define MASK_FLAG_SHINKANSEN(flg)	((flg)&FLAG_SHINKANSEN)	// 新幹線	aggregate_fare_info()の最後で設定
#define MASK_CITYNO(flg)			((flg)&0x0f)
/* 近郊区間 */
#define BCSUBURB					7
#define MASK_URBAN		0x380
#define URBAN_ID(flg)		(((unsigned int)(flg)>>7)&7)
#define IS_OSMSP(flg)				(((flg)&(1 << 11))!=0)	/* 大阪電車特定区間 ?*/
#define IS_TKMSP(flg)				(((flg)&(1 << 10))!=0)	/* 東京電車特定区間 ?*/
#define IS_YAMATE(flg)				(((flg)&(1 << 5))!=0)	/* 山点線内／大阪環状線内 ?*/

#define IS_COMPANY_LINE(d)			(((d) & (1<<31)) != 0)

#if 0
  vector<RouteItem> 先頭のlineId
  0x01 発駅が都区市内
  0x02 着駅が都区市内


#endif

#define MASK_ROUTE_FLAG_LFLG	0xff000000
#define MASK_ROUTE_FLAG_SFLG	0x0000ffff

class RouteItem
{
	RouteItem() {}
public:
	IDENT lineId;
	IDENT stationId;
	SPECIFICFLAG flag;
	RouteItem(IDENT lineId_, IDENT stationId_, SPECIFICFLAG flag_);
	RouteItem(IDENT lineId_, IDENT stationId_);

	RouteItem(const RouteItem& item_) {
		lineId = item_.lineId; 
		stationId = item_.stationId; 
		flag = item_.flag; 
	}
	RouteItem& operator=(const RouteItem& item_) { 
		lineId = item_.lineId; 
		stationId = item_.stationId; 
		flag = item_.flag; 
		return *this; 
	}
	bool operator==(const RouteItem& item_) const { 
		return lineId == item_.lineId && 
			   stationId == item_.stationId /* && 
			   flag == item_.flag */; 
	}
	bool is_equal(const RouteItem& item_) const { 
		return lineId == item_.lineId && 
			   stationId == item_.stationId /* && 
			   flag == item_.flag */; 
	}
};

class FARE_INFO {
public:
	FARE_INFO() { reset(); if (FARE_INFO::tax <= 0) { FARE_INFO::tax = g_tax; }}
private:
	int sales_km;			//*** 有効日数計算用(会社線含む)

	int base_sales_km;		//*** JR本州3社
	int base_calc_km;		//***

	int kyusyu_sales_km;	//***
	int kyusyu_calc_km;		//***

	int hokkaido_sales_km;
	int hokkaido_calc_km;

	int shikoku_sales_km;
	int shikoku_calc_km;

	bool local_only;				/* True: 地方交通線のみ (0 < base_sales_km時のみ有効)*/
	bool local_only_as_hokkaido;	/* True: 北海道路線地方交通線のみ(0 < hokkaidou_sales_km時のみ有効) */
	//幹線のみ
	// (base_sales_km == base_calc_km) && (kyusyu_sales_km == kyusyu_calc_km) && 
	// (hokkaido_sales_km == hokkaido_calc_km) && (shikoku_sales_km == shikoku_calc_km)
	bool major_only;				/* 幹線のみ */
	int total_jr_sales_km;			//***
	int total_jr_calc_km;			//***

	int company_fare;				/* 会社線料金 */
	int flag;						//***/* IDENT1: 全t_station.sflgの論理積 IDENT2: bit16-22: shinkansen ride mask  */
	int fare;						//***
	int fare_ic;					//*** 0以外で有効
	int avail_days;					//***
	static int tax;					/* 消費税 */
	int companymask;
	bool retr_fare();
	int aggregate_fare_info(int line_id, int station_id1, int station_id2, int before_staion_id1);
public:
	bool calc_fare(const vector<RouteItem>& routeList, bool applied_rule = true);	//***
	void reset() {				//***
		companymask = 0;
		sales_km = 0;

		base_sales_km = 0;
		base_calc_km = 0;

		kyusyu_sales_km = 0;
		kyusyu_calc_km = 0;

		hokkaido_sales_km = 0;
		hokkaido_calc_km = 0;

		shikoku_sales_km = 0;
		shikoku_calc_km = 0;

		local_only = false;
		local_only_as_hokkaido = false;

		major_only = false;
		total_jr_sales_km = 0;
		total_jr_calc_km = 0;

		company_fare = 0;
		flag = 0;
		fare = 0;
		fare_ic = 0;
		avail_days = 0;
	}
	int 	roundTripFareWithComapnyLine(bool& return_discount);
	bool 	isUrbanArea();
	int 	getTotalSalesKm();
	int		getJRSalesKm();
	int		getJRCalcKm();
	int		getCompanySalesKm();
	int		getSalesKmForHokkaido();
	int		getSalesKmForShikoku();
	int		getSalesKmForKyusyu();
	int		getCalcKmForHokkaido();
	int		getCalcKmForShikoku();
	int		getCalcKmForKyusyu();
	int		getTicketAvailDays();
	int		getFareForCompanyline();
	int		getFareForJR();
	int 	getFareStockDistount(int index, tstring& title);
	int		getAcademicDiscount();
	int		getFareForIC();

private:
	static int	 	Fare_basic_f(int km);
	static int	 	Fare_sub_f(int km);
	static int	 	Fare_tokyo_f(int km);
	static int	 	Fare_osaka(int km);
	static int	 	Fare_yamate_f(int km);
	static int	 	Fare_osakakan(int km);
	static int	 	Fare_hokkaido_basic(int km);
	static int	 	Fare_hokkaido_sub(int km);
	static int	 	Fare_shikoku(int skm, int ckm);
	static int	 	Fare_kyusyu(int skm, int ckm);
	static int		days_ticket(int sales_km);
	static int		Fare_company(int station_id1, int station_id2);
	static int		Fare_table(const char* tbl, const char* field, int km);
	static int		Fare_table(int dkm, int skm, char c);
	static int		Fare_table(const char* tbl, char c, int km);
	static int		CheckSpecficFarePass(int line_id, int station_id1, int station_id2);
	static int		SpecficFareLine(int station_id1, int station_id2);
	static vector<int> GetDistanceEx(int line_id, int station_id1, int station_id2);
	static int		Retrieve70Distance(int station_id1, int station_id2);
	static bool     IsIC_area(int urban_id);
};

// 1レコードめのlineIdの定義
#define B1LID_MARK				0x8000		// line_idとの区別で負数になるように
#define B1LID_BEGIN_CITY		0
#define B1LID_FIN_CITY			1
#define B1LID_BEGIN_YAMATE		2
#define B1LID_FIN_YAMATE		3
#define B1LID_BEGIN_2CITY		4	// not used
#define B1LID_FIN_2CITY			5	// not used
#define B1LID_BEGIN_CITY_OFF	6
#define B1LID_FIN_CITY_OFF		7
#define B1LID_BEGIN_OOSAKA		8
#define B1LID_FIN_OOSAKA		9

#define BCRULE70	6

/* cooked flag for shoFare(), show_route() */
#define	RULE_NO_APPLIED			0x8000
#define	RULE_APPLIED			0
#define APPLIED_START			0x0010
#define APPLIED_TERMINAL		0x0000


// station_id & line_id
//
class Station
{
public:
	IDENT lineId;
	IDENT stationId;

	Station(){
		lineId = stationId = 0;
	}

	Station(IDENT lineId_, IDENT stationId_) {
		lineId = lineId_;
		stationId = stationId_;
	}

	Station(const Station& item_) {
		lineId = item_.lineId; 
		stationId = item_.stationId; 
	}
	Station& operator=(const Station& item_) { 
		lineId = item_.lineId; 
		stationId = item_.stationId; 
		return *this; 
	}
	
	void set(int lineId_, int stationId_) {
		lineId = lineId_;
		stationId = stationId_;
	}
	
	void set(const RouteItem& routeItem) {
		lineId = routeItem.lineId;
		stationId = routeItem.stationId;
	}
	
	bool operator==(const Station& item_) const { 
		return lineId == item_.lineId && 
			   stationId == item_.stationId;
	}
	bool is_equal(const Station& item_) const { 
		return lineId == item_.lineId && 
			   stationId == item_.stationId; 
	}
	bool is_equal(const RouteItem& item_) const { 
		return lineId == item_.lineId && 
			   stationId == item_.stationId; 
	}
};

class Node
{
public:
	IDENT lineId;
	IDENT stationId1;
	IDENT stationId2;
	Node() { lineId = 0; stationId1 = 0; stationId2 = 0; }
};

class DbidOf
{
public:
	DbidOf();
	static int StationIdOf_SHINOSAKA;	// 新大阪
	static int StationIdOf_OSAKA;    	// 大阪
	static int StationIdOf_KOUBE;     	// 神戸
	static int StationIdOf_HIMEJI;    	// 姫路
	static int StationIdOf_NISHIAKASHI; // 西明石
	static int LineIdOf_TOKAIDO;       	// 東海道線
	static int LineIdOf_SANYO;        	// 山陽線
	static int LineIdOf_SANYOSHINKANSEN; // 山陽新幹線
	static int LineIdOf_HAKATAMINAMISEN; // 博多南線

	static int StationIdOf_KITASHINCHI; 	// 北新地
	static int StationIdOf_AMAGASAKI;		// 尼崎

	static int StationIdOf_KOKURA;  		// 小倉
	static int StationIdOf_NISHIKOKURA;  	// 西小倉
	static int StationIdOf_HAKATA;  		// 博多
	static int StationIdOf_YOSHIZUKA;	  	// 吉塚
};

typedef struct 
{
	int		jctSpMainLineId;		// 分岐特例:本線(b)
	int		jctSpStationId;			// 分岐特例:分岐駅(c)
	int		jctSpMainLineId2;		// 分岐特例:本線(b)
	int		jctSpStationId2;		// 分岐特例:分岐駅(c)
} JCTSP_DATA;

/* last_flag */
#define BLF_TRACKMARKCTL		5
#define BLF_JCTSP_ROUTE_CHANGE	6
#define LASTFLG_OFF				0
#define BLF_END					16

/*   route
 *
 */
class Route
{
	BYTE jct_mask[(MAX_JCT + 7)/ 8];	// about 40byte
	vector<RouteItem> route_list_raw;
	vector<RouteItem> route_list_cooked;
	FARE_INFO fare_info;
private:
	SPECIFICFLAG last_flag;	// add() - removeTail() work
public:
	int startStationId() 
	{ return (route_list_raw.size() <= 0) ? 0 : route_list_raw.front().stationId; }

	int endStationId;

	enum LINE_DIR {
		LDIR_ASC  = 1,		// 下り
		LDIR_DESC = 2		// 上り
	};

public:
	Route();
	~Route();

	const FARE_INFO& getCurFare() {
		return fare_info;
	}
	vector<RouteItem>& routeList() { return route_list_raw; }
	vector<RouteItem>& cookedRouteList() { return route_list_cooked; }
	bool isModified() {
		return (last_flag & (1 << 6)) != 0;
	}
	void end()		{ BIT_ON(last_flag, BLF_END); }

private:
	bool			checkOfRuleSpecificCoreLine(int dis_cityflag, int* rule114);
	static DBO	 	Enum_junctions_of_line(int line_id, int begin_station_id, int to_station_id);

private:
	static int	 	InStation(int stationId, int lineId, int b_stationId, int e_stationId);
	static int		RetrieveOut70Station(int line_id);
	
	vector<vector<int>> Node_next(int jctId);

	static int	 	ReRouteRule69j(const vector<RouteItem>& in_route_list, vector<RouteItem>* out_route_list);
	static int  	ReRouteRule70j(const vector<RouteItem>& in_route_list, vector<RouteItem>* out_route_list);
	static bool 	Query_a69list(int line_id, int station_id1, int station_id2, vector<PAIRIDENT>* results, bool continue_flag);
	static bool 	Query_rule69t(const vector<RouteItem>& in_route_list, const RouteItem& cur, int ident, vector<vector<PAIRIDENT>>* results);
	static int  	CheckOfRule86(const vector<RouteItem>& in_route_list, Station* exit, Station* entr, PAIRIDENT* cityId_pair);
	static int  	CheckOfRule87(const vector<RouteItem>& in_route_list);

	static void  	ReRouteRule86j87j(PAIRIDENT cityId, int mode, const Station& exit, const Station& enter, vector<RouteItem>* out_route_list);

	static int		InCityStation(int cityno, int lineId, int stationId1, int stationId2);

public:
	static int 		Id2jctId(int stationId);
	static int 		Jct2id(int jctId);
	static tstring 	JctName(int jctId);
	static tstring 	StationName(int id);
	static tstring 	StationNameEx(int id);
	static tstring 	LineName(int id);
	static SPECIFICFLAG AttrOfStationId(int id);
	static SPECIFICFLAG AttrOfStationOnLineLine(int line_id, int station_id);
	static int		InStationOnLine(int line_id, int station_id);

	static int		LineIdFromStationId(int station_id);

	static int 		GetStationId(LPCTSTR stationName);
	static int 		GetLineId(LPCTSTR lineName);


public:	// termsel
	static DBO 		Enum_company_prefect();
	static DBO 		Enum_station_match(LPCTSTR station);
	static tstring 	GetPrefectByStationId(int stationId);
	static DBO 		Enum_lines_from_company_prefect(int id);
	static DBO		Enum_station_located_in_prefect_or_company_and_line(int prefectOrCompanyId, int lineId);
	static tstring 	GetKanaFromStationId(int stationId);
	static DBO	 	Enum_line_of_stationId(int stationId);

private:
	void		routePassOff(int line_id, int to_station_id, int begin_station_id);
	static int 	retrieveJunctionSpecific(int jctLineId, int transferStationId, JCTSP_DATA* jctspdt);
	int			getBsrjctSpType(int line_id, int station_id);
	int			junctionStationExistsInRoute(int stationId);

public:
	// alps_mfcDlg
	tstring 		showFare(int cooked);
	int				fareCalcOption();
	
	tstring 		show_route(bool cooked);
	tstring         route_script();

	int				setup_route(LPCTSTR route_str);

	bool			chk_jctsb_b(int kind, int num);

	int 			add(int line_id, int stationId2, int ctlflg = 0);
	int 			add(int stationId);
	void 			removeTail(bool begin_off = false);
	void 			removeAll(bool bWithStart =true, bool bWithEnd =true);
	int				reverse();
	bool 			checkPassStation(int stationId);
	void 			terminate(int stationId);
	int				changeNeerest(bool useBulletTrain);

	static DBO	 	Enum_junction_of_lineId(int lineId, int stationId);
	static DBO	 	Enum_station_of_lineId(int lineId);

	static DBO	 	Enum_neer_node(int stationId);
	static int 		NumOfNeerNode(int stationId);
	static int 		RemoveDupRoute(vector<RouteItem> *routeList);

	static int  	DirLine(int line_id, int station_id1, int station_id2);
	static bool 	IsSpecificCoreDistance(const vector<RouteItem>& route);
	static vector<int>		GetDistance(int line_id, int station_id1, int station_id2);
	static int				Get_node_distance(int line_id, int station_id1, int station_id2);
	static vector<int>		Get_route_distance(const vector<RouteItem>& route);
	static vector<Station>	SpecificCoreAreaFirstTransferStationBy(int lineId, int cityId);
	static int 		Retrieve_SpecificCoreStation(int cityId);
	static int		Retreive_SpecificCoreAvailablePoint(int km, int km_offset, int line_id, int station_id);
	static int		CheckAndApplyRule43_2j(const vector<RouteItem> &route);
	static bool		CheckOfRule114j(const vector<RouteItem>& route, const vector<RouteItem>& routeSpecial, int kind, int* result);
	static int		CheckOfRule88j(vector<RouteItem> *route);
	static int		CheckOfRule89j(const vector<RouteItem> &route);

	static tstring  CoreAreaNameByCityId(int startEndFlg, int flg, SPECIFICFLAG flags);
	static bool		IsAbreastShinkansen(int line_id1, int line_id2, int station_id1, int station_id2);
	static int      GetHZLine(int line_id, int station_id, int station_id2 = -1);
	static bool		CheckTransferShinkansen(int line_id1, int line_id2, int station_id1, int station_id2, int station_id3);
	static int		NextShinkansenTransferTerm(int line_id, int station_id1, int station_id2);

	static vector<PAIRIDENT> GetNeerNode(int station_id);
};



#endif	/* _ALPDB_H__ */


