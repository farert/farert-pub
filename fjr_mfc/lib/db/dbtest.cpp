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


int _tmain(int argc, TCHAR* argv[])
{
	int rc;

	setlocale(LC_ALL, "");

	CDBContext ctx;
	CDB* db = CDB::getInstance();
	
	if (db == NULL || !db->open(_T("../../jr.db"))) {
		_tprintf(_T("fatal error\n"));
		return -1;
	}

	_tprintf(_T("test1-sizeof(TCHAR) = %d\n"), sizeof(TCHAR));
	t2utf8(_T("select e.name from t_station e join t_prefect p on p.rowid=e.prefect_id where p.name='神奈川県' order by kana"), utf8sql);
	if (SQLITE_OK != db->prepare(utf8sql, &ctx)) {
		return -1;
	}
	while (SQLITE_ROW == (rc = ctx.step())) {
#ifdef UNICODE
		CA2T s(reinterpret_cast<LPCSTR>(ctx.column_text(0)), CP_UTF8);
#else
		CW2A s(CA2W(reinterpret_cast<LPCSTR>(ctx.column_text(0)), CP_UTF8));
#endif
		_tprintf(_T("%s\n"), s);
	}

////////////////////////////////////////////////////////////////
	_tprintf(_T("test2:\n"));
	if (SQLITE_OK != db->prepare("select * from t_company", &ctx)) {
		return -1;
	}
	while (SQLITE_ROW == (rc = ctx.step())) {
		utf82t(reinterpret_cast<LPCSTR>(ctx.column_text(0)), s);
		_tprintf(_T("%s\n"), s);
	}

	ctx.finalize();

///////////////////////////////////////////////////////////////////////
	_tprintf(_T("test3:\n"));
	CT2A utf8sql2(_T("select e.name from t_station e join t_prefect p on p.rowid=e.prefect_id where p.name=? order by kana"), CP_UTF8);
	if (SQLITE_OK != db->prepare(utf8sql2, &ctx)) {
		return -1;
	}
	CT2A prefect(_T("高知県"), CP_UTF8);
	// NG if (SQLITE_OK != ctx.bind(1, CT2A(_T("高知県"), CP_UTF8))) {
	if (SQLITE_OK != ctx.bind(1, prefect)) {
		return -1;
	}
	while (SQLITE_ROW == (rc = ctx.step())) {
		CA2T s(reinterpret_cast<LPCSTR>(ctx.column_text(0)), CP_UTF8);
		_tprintf(_T("%s\n"), s);
	}

///////////////////////////////////////////////////////////////////////
	_tprintf(_T("test4:\n"));
	if (SQLITE_OK != db->prepare("select rowid, name from t_station where name like ?", &ctx)) {
		return -1;
	}
	CT2A station_q(_T("西%"), CP_UTF8);
	if (SQLITE_OK != ctx.bind(1, station_q)) {
		return -1;
	}
	while (SQLITE_ROW == (rc = ctx.step())) {
		CA2T s(reinterpret_cast<LPCSTR>(ctx.column_text(1)), CP_UTF8);
		_tprintf(_T("%d, %s\n"), ctx.column_int(0), s);
	}

///////////////////////////////////////////////////////////////////////
	_tprintf(_T("test5:\n"));
	ctx.reset();
	while (SQLITE_ROW == (rc = ctx.step())) {
		CA2T s(reinterpret_cast<LPCSTR>(ctx.column_text(1)), CP_UTF8);
		_tprintf(_T("%d, %s\n"), ctx.column_int(0), s);
	}

///////////////////////////////////////////////////////////////////////
	_tprintf(_T("test6:\n"));
	ctx.reset();
	CT2A station_q2(_T("会津%"), CP_UTF8);
	if (SQLITE_OK != ctx.bind(1, station_q2)) {
		return -1;
	}
	while (SQLITE_ROW == (rc = ctx.step())) {
		CA2T s(reinterpret_cast<LPCSTR>(ctx.column_text(1)), CP_UTF8);
		_tprintf(_T("%d, %s\n"), ctx.column_int(0), s);
	}
	ctx.finalize();
///////////////////////////////////////////////////////////////////////
	_tprintf(_T("test7:\n"));
	char sq[256];
	
	CT2A qry(_T("えちぜん"), CP_UTF8);
	sqlite3_snprintf(sizeof(sq), sq, "select rowid, name from t_station where kana like '%q%%'", qry);
	///CT2A sq(_T("select rowid, name from t_station where kana like 'えちぜん%'"), CP_UTF8);
	
	if (SQLITE_OK != db->prepare(sq, &ctx)) {
		return -1;
	}
	while (SQLITE_ROW == (rc = ctx.step())) {
		CA2T s(reinterpret_cast<LPCSTR>(ctx.column_text(1)), CP_UTF8);
		_tprintf(_T("%d, %s\n"), ctx.column_int(0), s);
	}

	wprintf(L"end\n");
	return 0;
}

