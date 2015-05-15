#include "stdafx.h"
#include "alpfile.h"

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

const LPCTSTR FILE_HISTORY = _T("history.txt");


///////////////////////////////////////////////////////////////
#if HISTORY_SEPARATE_MEMORY
HistoryFile::HistoryFile(bool bkind)
{
	b_kind = bkind;
}
#endif


///////////////////////////////////////////////////////////////
HistoryFile::HistoryFile()
{
	b_kind = false;
}



///////////////////////////////////////////////////////////////
//static
void HistoryFile::remove()
{
	DeleteFile(FILE_HISTORY);
}


///////////////////////////////////////////////////////////////
bool HistoryFile::save(LPCTSTR szStation)
{
	if (file.m_hFile != CFile::hFileNull) {
		file.Close();
	}

#if HISTORY_SEPARATE_MEMORY
	CString type(b_kind ? _T("着") : _T("発"));
#endif
	if (file.Open(FILE_HISTORY, CFile::modeReadWrite | CFile::modeNoTruncate)) {
		while (file.ReadString(record)) {
#if HISTORY_SEPARATE_MEMORY
			if (record.Left(record.FindOneOf(_T("\t "))) == type) {
				if (0 ==
					record.Mid(record.FindOneOf(_T("\t "))).TrimLeft().Compare(szStation)) {
					return true;
				}
			}
#else
			if (record == szStation) {
				return true;
			}
#endif
		}
		file.SeekToEnd();
	} else if (!file.Open(FILE_HISTORY, CFile::modeWrite | CFile::modeCreate)) {
		return false;
	}
#if HISTORY_SEPARATE_MEMORY
	record = type + _T("\t");
	record += szStation;
#else
	record = szStation;
#endif
	record += _T("\n");
	file.WriteString(record);

	return true;
}


///////////////////////////////////////////////////////////////
bool HistoryFile::first()
{
	if (file.m_hFile != CFile::hFileNull) {
		file.Close();
	}
	return TRUE == file.Open(FILE_HISTORY, CFile::modeRead | CFile::typeText);
}

///////////////////////////////////////////////////////////////
LPCTSTR HistoryFile::next()
{
#if HISTORY_SEPARATE_MEMORY
	CString type(b_kind ? _T("着") : _T("発"));
#endif
	if ((file.m_hFile != CFile::hFileNull) && file.ReadString(record)) {
		int pos;

#if HISTORY_SEPARATE_MEMORY
		if (record.Left(record.FindOneOf(_T("\t "))) == type) {
			record = record.Mid(record.FindOneOf(_T("\t "))).TrimLeft();
			pos = record.Find(_T('['));
			if (0 <= pos) {
				record = record.Left(pos);
			}
		}
#else
		pos = record.Find(_T('['));
		if (0 <= pos) {
			record = record.Left(pos);
		}
#endif
		return record.GetBuffer();
	} else {
		return 0;
	}
}
