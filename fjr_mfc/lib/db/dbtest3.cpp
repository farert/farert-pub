#define UNICODE
#define _UNICODE
// sqliteope.cpp.cpp : コンソール アプリケーションのエントリ ポイントを定義します。
//	cl /W4 /D_UNICODE /DUNICODE dbtest.cpp sqlite3.c

#include <locale.h>
#include <stdio.h>
#include <string.h>
#include <tchar.h>
#include "db.h"


void db(const char* sql, int station_id, bool cache = false)
{
	TCHAR name[64];
	
	DBO ctx = DBS::getInstance()->compileSql(
		sql, cache);
	if (ctx.isvalid()) {

		ctx.setParam(1, station_id);

		if (ctx.moveNext()) {
			_tcscpy_s(name, ctx.getText(0).c_str());
		}
	} else {
		_tprintf(_T("error!!!!!!!!\n"));
	}
	_tprintf(_T("%s, %d\n"), name, (sqlite3_stmt*)ctx);
}

int _tmain(int argc, TCHAR** argv)
{
	_tsetlocale(LC_ALL, _T(""));
	
	int station_id;

	if (argc < 2) {
		printf("Usage: %s <station_id>\n", *argv);
		return -1;
	}
	printf("========\n");

	if (! DBS::getInstance()->open(_T("../../jr.db"))) {
		_tprintf(_T("fatal error\n"));
		return -1;
	}

	station_id = _ttoi(*++argv);
	db("select name from t_station where rowid=?", station_id + 0, true);
	db("select name from t_station where rowid=?", station_id + 1, false);
	db("select name from t_line where rowid=?", station_id + 0, true);
	db("select name from t_station where rowid=?", station_id + 2, false);
	db("select name from t_line where rowid=?", station_id + 1, true);
	db("select name from t_line where rowid=?", station_id + 2, false);
	db("select name from t_station where rowid=?", station_id + 3, true);
	db("select name from t_line where rowid=?", station_id + 3, true);
	db("select name from t_station where rowid=?", station_id + 4, true);
	db("select name from t_line where rowid=?", station_id + 7, false);
	db("select name from t_station where rowid=?", station_id + 7, false);

	return 0;
}


