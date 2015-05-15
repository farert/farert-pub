
#include "../../alps_mfc/stdafx.h"
#include "db.h"

/*!	@file db.cpp
 *	Copyright(c) sutezo  2014.
 */

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

//static 
map<string, sqlite3_stmt*> DBS::cache_pool;


bool DBS::open(LPCTSTR dbpath) 
{
	int rc;
	int rtc;

	sqlite3_backup* pBackup;
	sqlite3* dbtmp;
	CT2A utf8_dbpath(dbpath, CP_UTF8);
	if (0 != sqlite3_open_v2(utf8_dbpath, &dbtmp, SQLITE_OPEN_READONLY, 0)) {
		TRACE("temporary database can't open\n");
		cleanup();
		return false;
	}
	pBackup = sqlite3_backup_init(m_db, "main", dbtmp, "main");
	if (pBackup == 0) {
		TRACE("error: %s\n", errmsg());
		cleanup();
		return false;
	}
	rtc = 0;
	while ((rc = sqlite3_backup_step(pBackup, 100)) == SQLITE_OK ||
			rc == SQLITE_BUSY) {
		if (rc == SQLITE_BUSY) {
			if (3 <= rtc++) {
				break;
			}
			sqlite3_sleep(100);
		}
	}
	sqlite3_backup_finish(pBackup);
	sqlite3_close(dbtmp);

	if (rc != SQLITE_DONE) {
		if (rc == SQLITE_BUSY || rc == SQLITE_LOCKED) {
			TRACE("Error: source database is busy\n");
		} else {
			TRACE("Error %d, %s\n", rc, errmsg());
		}
		return false;
	}
	return true;
}

//static 
void DBS::cache_cleanup(bool special)
{
	map<string, sqlite3_stmt*>::iterator itr = cache_pool.begin();
	while (itr != cache_pool.end()) {
						/* sql文の行頭が、空複数行コメントの場合、キャッシュ削除する
						 */
		if (!special || (itr->first.substr(0, 4).compare("/**/") == 0)) {
			DBO dbo(itr->second, false);
			cache_pool.erase(itr++);
		} else {
			itr++;
		}
	}
}

bool DBO::setParam(int index, int value) 
{
	int rc;
	rc = sqlite3_bind_int(m_stmt, index, value);
	if (rc != SQLITE_OK) {
		TRACE("Error: bind(int)=%d, %s\n", rc, DBS::getInstance()->errmsg());
		return false;
	}
	return true;
}

bool DBO::setParam(int index, LPCTSTR value) 
{
	int rc;

	CT2A utftext(value, CP_UTF8);

	rc = sqlite3_bind_text(m_stmt, index, utftext, -1, SQLITE_TRANSIENT);
	if (rc != SQLITE_OK) {
		TRACE("Error: bind(text)=%d, %s\n", rc, DBS::getInstance()->errmsg());
		return false;
	}
	return true;
}

bool DBO::setParam(int index, const char* value) 
{
	int rc;

	rc = sqlite3_bind_text(m_stmt, index, value, -1, SQLITE_TRANSIENT);
	if (rc != SQLITE_OK) {
		TRACE("Error: bind(text)=%d, %s\n", rc, DBS::getInstance()->errmsg());
		return false;
	}
	return true;
}

bool DBO::moveNext() 
{
	int rc;
	if (m_bEof) {
		return false;
	}
	rc = sqlite3_step(m_stmt);
	if ((SQLITE_DONE != rc) && (SQLITE_ROW != rc)) {
		TRACE("Error: step=%d, %s\n", rc, DBS::getInstance()->errmsg());
		return false;
	}
	if (SQLITE_DONE == rc) {
		m_bEof = true;
		return false;
	}
	return true;
}

tstring DBO::getText(int col) 
{
	CA2T text(reinterpret_cast<LPCSTR>(sqlite3_column_text(m_stmt, col)), CP_UTF8);
	return tstring(text);
}

int DBO::getInt(int col) 
{
	return sqlite3_column_int(m_stmt, col);
}

bool DBO::finalize() 
{
	int rc;
	if (m_lock || !m_stmt) {
#ifdef DEB_PRINT
		TRACE("fin lock %d\n", m_stmt);
#endif
		return true;
	}
	rc = sqlite3_finalize(m_stmt);
	if (SQLITE_OK != rc) {
		TRACE("Error: sqlite3 finalize()=%d, %s\n", rc, DBS::getInstance()->errmsg());
		return false;
	}
#ifdef DEB_PRINT
	TRACE("fin=%d\n", m_stmt);
#endif
	m_stmt = 0;
	m_bEof = false;
	return true;
}

bool DBO::reset() 
{
	int rc = sqlite3_reset(m_stmt);
	if (SQLITE_OK != rc) {
		TRACE("Error: sqlite3 reset()=%d, %s\n", rc, DBS::getInstance()->errmsg());
		return false;
	} else {
		m_bEof = false;
		return true;
	}
}

int DBO::getNumOfCol() 
{
	return sqlite3_column_count(m_stmt);
}

/*	index: Number of Column(0 to sqlite3_column_count(m_stmt) - 1)
 *	@return SQLITE_INTEGER, SQLITE_FLOAT, SQLITE_TEXT, SQLITE_BLOB, SQLITE_NULL
 */
int DBO::colType(int index) 
{
	return sqlite3_column_type(m_stmt, index);
}


