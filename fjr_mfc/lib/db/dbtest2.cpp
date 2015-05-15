#define UNICODE
#define _UNICODE
// sqliteope.cpp.cpp : コンソール アプリケーションのエントリ ポイントを定義します。
//	cl /W4 /D_UNICODE /DUNICODE dbtest.cpp sqlite3.c

#pragma once
#include <locale.h>
#include <SDKDDKVer.h>
#include <stdio.h>
#include <tchar.h>
#include <AtlBase.h>
#include <AtlConv.h>
#include "db.h"

#ifdef UNICODE
#define t2utf8(s, d)	CT2A d(s, CP_UTF8)
#define utf82t(s, d)	CA2T d(s, CP_UTF8)
#else
#define t2utf8(s, d)	CW2A d(CA2W(s), CP_UTF8)
#define utf82t(s, d)	CW2A d(CA2W(s, CP_UTF8))
#endif



int	func(void* param, int nCol, char** colsValues, char** colNames)
{
	for (int i = 0; i < nCol; i++) {
		CA2T s(*(colsValues + i), CP_UTF8);
		_tprintf(_T("%s |"), s);
	}
	_tprintf(_T("\n"));
	return 0;
}

int _tmain(int argc, TCHAR* argv[])
{
	int rc;

	setlocale(LC_ALL, "");

	CDBContext ctx;
	CDB* db = CDB::getInstance();
	CDBTable tbl;
	
	if (db == NULL || !db->open(_T("../../jr.db"))) {
		_tprintf(_T("fatal error\n"));
		return -1;
	}

#if 10 /// NG debug now
	_tprintf(_T("test1:\n"));
	if (SQLITE_OK != db->exec_table("select prefect, company, line, station, sales_km, calc_km from lines where calc_km>=1000", tbl)) {
		return -1;
	}
	for (int i = 0; i < tbl.rows(); i++) {
		for (int j = 0; j < tbl.cols(); j++) {
			CA2T s(reinterpret_cast<LPCSTR>(tbl.get(i, j)), CP_UTF8);
			_tprintf(_T("%s |"), s);
		}
		_tprintf(_T("\n"));
		
	}
#endif
///////////////////////////////////////////////////////////////
	_tprintf(_T("test1-2:\n"));
	if (SQLITE_OK != db->exec("select * from lines where sales_km=0", func, 0)) {
		_tprintf(_T("fatal error\n"));
		return -1;
	}
//////////////////////////////////////////////////////////
	_tprintf(_T("test2:\n"));
	if (SQLITE_OK != db->prepare(
"select id from t_lines l join t_station t on t.rowid=l.station_id join t_jct j on j.station_id=l.station_id where line_id=?1 and jctflg!=0 and "
"(sales_km<=(select sales_km from t_lines where line_id=?1 and station_id=?2) and "
"sales_km>=(select sales_km from t_lines where  line_id=?1 and station_id=?3)) or "
"(sales_km>=(select sales_km from t_lines where line_id=?1 and station_id=?2) and "
"sales_km<=(select sales_km from t_lines where  line_id=?1 and station_id=?3))"
	, &ctx)) {
		return -1;
	}
	ctx.bind(1, 23);	// line_id
	ctx.bind(2, 537);	// station_id 1
	ctx.bind(3, 532);	// station_id 2
	while (SQLITE_ROW == (rc = ctx.step())) {
		_tprintf(_T("%d\n"), ctx.column_int(0));
	}
/////////////////////////////////////////////
	if (argc == 4) {
	_tprintf(_T("test3:\n"));
	if (SQLITE_OK != db->prepare(
"select t.name from t_lines l join t_line n on n.rowid=l.line_id join t_station t on t.rowid=l.station_id where n.name=?1 and jctflg!=0 and "
"((sales_km<=(select sales_km from t_lines l join t_line n on n.rowid=l.line_id join t_station t on t.rowid=l.station_id where n.name=?1 and t.name=?2) and "
"sales_km>=(select sales_km from t_lines l join t_line n on n.rowid=l.line_id join t_station t on t.rowid=l.station_id where n.name=?1 and t.name=?3)) or "
"(sales_km>=(select sales_km from t_lines l join t_line n on n.rowid=l.line_id join t_station t on t.rowid=l.station_id where n.name=?1 and t.name=?2) and " 
"sales_km<=(select sales_km from t_lines l join t_line n on n.rowid=l.line_id join t_station t on t.rowid=l.station_id where n.name=?1 and t.name=?3)))"
	, &ctx)) {
		return -1;
	}
	CT2A d1(*++argv, CP_UTF8);
	CT2A d2(*++argv, CP_UTF8);
	CT2A d3(*++argv, CP_UTF8);
	ctx.bind(1, d1);	// line_id
	ctx.bind(2, d2);	// station_id 1
	ctx.bind(3, d3);	// station_id 2
	while (SQLITE_ROW == (rc = ctx.step())) {
		CA2T s(reinterpret_cast<LPCSTR>(ctx.column_text(0)), CP_UTF8);
		_tprintf(_T("%s\n"), s);
	}
	}
	ctx.finalize();
}
