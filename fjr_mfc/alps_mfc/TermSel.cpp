// TermSel.cpp : 実装ファイル
//
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

#include "stdafx.h"
#include "alps_mfc.h"
#include "TermSel.h"
#include "afxdialogex.h"
#include <Imm.h>

/*!	@file CTermSel diaglog.
 *	Copyright(c) sutezo9@me.com 2012.
 */

IMPLEMENT_DYNAMIC(CTermSel, CDialogEx)

CTermSel::CTermSel(bool bTerm, CWnd* pParent /*=NULL*/)
	: CDialogEx(CTermSel::IDD, pParent)
{
	m_bTerm = bTerm;
	m_stationId = 0;
}

CTermSel::~CTermSel()
{
	DBS::cache_cleanup(true);	/* SQL Cacheをクリアする */
							/* SQL文の行頭がコメントになっているもののみ */
}

void CTermSel::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}


BEGIN_MESSAGE_MAP(CTermSel, CDialogEx)
	ON_LBN_SELCHANGE(IDC_LIST_COMPANY, &CTermSel::OnLbnSelchangeListCompany)
	ON_LBN_DBLCLK(IDC_LIST_COMPANY, &CTermSel::OnLbnDblclkListCompany)
	ON_LBN_DBLCLK(IDC_LIST_LINES, &CTermSel::OnLbnDblclkListLines)
	ON_LBN_DBLCLK(IDC_LIST_TERMINALS, &CTermSel::OnLbnDblclkListTerminals)
	ON_BN_CLICKED(IDOK, &CTermSel::OnBnClickedOk)
	ON_BN_CLICKED(IDCANCEL, &CTermSel::OnBnClickedCancel)
	ON_BN_CLICKED(IDC_BUTTON_STATION_SEL, &CTermSel::OnBnClickedButtonStationSel)
	ON_LBN_SELCHANGE(IDC_LIST_LINES, &CTermSel::OnLbnSelchangeListLines)
	ON_LBN_SELCHANGE(IDC_LIST_TERMINALS, &CTermSel::OnLbnSelchangeListTerminals)
	ON_CBN_SELCHANGE(IDC_COMBO_STATION, &CTermSel::OnCbnSelchangeComboStation)
	ON_CBN_EDITCHANGE(IDC_COMBO_STATION, &CTermSel::OnCbnEditchangeComboStation)
	ON_CBN_SETFOCUS(IDC_COMBO_STATION, &CTermSel::OnCbnSetfocusComboStation)
	ON_CBN_KILLFOCUS(IDC_COMBO_STATION, &CTermSel::OnCbnKillfocusComboStation)
	ON_CBN_EDITUPDATE(IDC_COMBO_STATION, &CTermSel::OnCbnEditupdateComboStation)
	ON_CBN_SELENDOK(IDC_COMBO_STATION, &CTermSel::OnCbnSelendokComboStation)
//	ON_WM_CHAR()
ON_WM_TIMER()
END_MESSAGE_MAP()

#if 0
	test
		1. IDC_COMBO_STATION 不完全駅名入力（漢字） → Enter
		   1-1 IDC_LIST_TERMINALS No Match → Enter | OK Button -> 無視されること
		   1-2 IDC_LIST_TERMINALS 1件合致 → Enter | OK Button → 選択完了されること
		   1-3 IDC_LIST_TERMINALS N件合致 → Enter | OK Button → 無視されること
		   1-3 IDC_LIST_TERMINALS N件合致 → 選択 → Enter | OK Button → 選択完了されること
		2. IDC_COMBO_STATION 不完全駅名入力（JR） → Enter
		3. IDC_COMBO_STATION 不完全駅名入力(ひらがな） → Enter
		4. IDC_COMBO_STATION 不完全駅名入力(漢字同名駅をひらがな入力） → Enter
		5. IDC_COMBO_STATION 不完全駅名入力(ひらがな同名駅） → Enter
		6. IDC_COMBO_STATION 完全駅名入力(ひらがな） → Enter
		7. IDC_COMBO_STATION 完全駅名入力(漢字） → Enter
		8. IDC_COMBO_STATION 不完全駅名入力(ひらがな） → Enter → 複数駅マッチ → 
			8-1 IDC_LIST_TERMINALS 選択Double Click
			8-2 IDC_LIST_TERMINALS 選択 Enter
			8-3 IDC_LIST_TERMINALS 複数選択不可であること
			8-4 IDC_LIST_TERMINALS 
		9. IDC_LIST_COMPANY sel -> IDC_LIST_LINES sel -> IDC_LIST_TERMINALS
#endif

// CTermSel メッセージ ハンドラー


BOOL CTermSel::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	setlocale(LC_ALL, "");

	if (m_bTerm) {
		SetDlgItemText(IDC_STATIC_TITLE, _T("着駅指定"));
	} else {
		SetDlgItemText(IDC_STATIC_TITLE, _T("発駅指定"));
	}

	CListBox* pL = (CListBox*)GetDlgItem(IDC_LIST_COMPANY);
	pL->ResetContent();

	DBO dbo = Route::Enum_company_prefect();
	if (dbo.isvalid()) {
		while (dbo.moveNext()) {
			pL->SetItemData(pL->AddString(dbo.getText(0).c_str()), dbo.getInt(1));
		}
	}
	
	loadHistory();
	GetDlgItem(IDC_BUTTON_STATION_SEL)->EnableWindow(FALSE);
	GetDlgItem(IDC_COMBO_STATION)->SetFocus();

	SetTimer(101, 1000, NULL);
	return FALSE;
	//return TRUE;  // return TRUE unless you set the focus to a control
	// 例外 : OCX プロパティ ページは必ず FALSE を返します。
}


//	Start/End Station select filter. '>>' button. 
//	IDC_BUTTON_STATION_SEL
//	駅候補列挙表示ボタン
//
void CTermSel::OnBnClickedButtonStationSel()
{
	CString sStation;
	int nItem = 0;
	int itemId = 0;
	
	GetDlgItem(IDC_COMBO_STATION)->GetWindowText(sStation);
	
	CListBox* pL = reinterpret_cast<CListBox*>(GetDlgItem(IDC_LIST_TERMINALS));

		// 駅候補リストの列挙(ひらがな、部分一致）
	DBO dbo = Route::Enum_station_match(sStation);
	if (!dbo.isvalid()) {
		return; 
	}

	GetDlgItem(IDC_BUTTON_STATION_SEL)->EnableWindow(FALSE);

	pL->ResetContent();
	sStation = _T("");

		// 駅候補リストの列挙(ひらがな、部分一致）
	for (nItem = 0; dbo.moveNext(); nItem++) {
		sStation = dbo.getText(0).c_str();
		itemId = dbo.getInt(1);
		CString samename = dbo.getText(2).c_str();

		if (!samename.IsEmpty()) { // 同名駅?
			sStation += samename;
			CString prefect(Route::GetPrefectByStationId(itemId).c_str());
			if (!prefect.IsEmpty()) {
				sStation += _T("[");
				sStation += prefect;
				sStation += _T("]");
			} else {
				ASSERT(FALSE);	/* Error */
			}
		}
		pL->SetItemData(pL->AddString(sStation), itemId);
	}
	if (nItem == 1) {
		m_stationId = itemId;
		m_pszStation = sStation;
		SetTerminalLineLabel(m_stationId);
		GetDlgItem(IDOK)->SetFocus();
	} else {
		m_stationId = 0;
		m_pszStation = _T("");
		GetDlgItem(IDC_EDIT_LINE)->SetWindowText(_T(""));
		if (nItem == 0) {
			GetDlgItem(IDC_COMBO_STATION)->SetFocus();
		} else {
			GetDlgItem(IDC_LIST_TERMINALS)->SetFocus();
		}
	}
}

// List changed at Company or Prefect
//	IDC_BUTTON_COMPANY_SEL
//
void CTermSel::OnLbnSelchangeListCompany()
{
	if (500 < (GetTickCount() - m_dwSystime)) {
		reinterpret_cast<CListBox*>(GetDlgItem(IDC_LIST_LINES))->ResetContent();
		OnLbnDblclkListCompany();
		m_dwSystime = GetTickCount();
	} else {
		m_lastListChange = 1;
	}
}

//	List changed at Lines
//	IDC_LIST_LINES
//
void CTermSel::OnLbnSelchangeListLines()
{
	if (500 < (GetTickCount() - m_dwSystime)) {
		reinterpret_cast<CListBox*>(GetDlgItem(IDC_LIST_TERMINALS))->ResetContent();
		OnLbnDblclkListLines();
		m_dwSystime = GetTickCount();
	} else {
		m_lastListChange = 2;
	}
}

// IDC_COMBO_STATION: 
//
void CTermSel::OnCbnSelendokComboStation()
{
	CString sStation;
	GetDlgItem(IDC_COMBO_STATION)->GetWindowText(sStation);
	TRACE(_T("SelendOK: %s\n"), sStation);
}

//	Edit changed at Start/End station.
//	IDC_COMBO_STATION
//
void CTermSel::OnCbnSelchangeComboStation()
{
	CString sStation;
	CComboBox* pC = reinterpret_cast<CComboBox*>(GetDlgItem(IDC_COMBO_STATION));

	GetDlgItem(IDC_COMBO_STATION)->GetWindowText(sStation);
	TRACE(_T("SelChangeA: %s\n"), sStation);

	pC->GetLBText(pC->GetCurSel(), sStation);
	TRACE(_T("SelChangeB: %s\n"), sStation);

	if (sStation == CLEAR_HISTORY) {
		//pC->DeleteString(pC->FindStringExact(CLEAR_HISTORY));
		pC->ResetContent();

		HistoryFile::remove();

		pC->Clear();
		pC->SetWindowText(_T(""));

	} else {
		sStation.Trim();
		if (!sStation.IsEmpty() && (sStation == m_pszStation)) {
			return;
		}
		GetDlgItem(IDC_BUTTON_STATION_SEL)->EnableWindow(!sStation.IsEmpty());
		m_stationId = 0;
		GetDlgItem(IDC_EDIT_LINE)->SetWindowText(_T(""));
	}
}

// IDC_COMBO_STATION: 
//
void CTermSel::OnCbnEditupdateComboStation()
{
#if 1
	CString item;
	CComboBox* pC = reinterpret_cast<CComboBox*>(GetDlgItem(IDC_COMBO_STATION));
	pC->GetWindowText(item);
	TRACE(_T("A: %s\n"), item);
#endif
}

// IDC_COMBO_STATION: 
//
void CTermSel::OnCbnEditchangeComboStation()
{
	CString sStation;
	CComboBox* pC = reinterpret_cast<CComboBox*>(GetDlgItem(IDC_COMBO_STATION));

	//pC->GetLBText(pC->GetCurSel(), sStation);
	//TRACE(_T("B: %s\n"), sStation);

	GetDlgItem(IDC_COMBO_STATION)->GetWindowText(sStation);
	TRACE(_T("C: %s\n"), sStation);

	sStation.Trim();
	if (!sStation.IsEmpty() && (sStation == m_pszStation)) {
		return;
	}
	GetDlgItem(IDC_BUTTON_STATION_SEL)->EnableWindow(!sStation.IsEmpty());
	m_stationId = 0;
	GetDlgItem(IDC_EDIT_LINE)->SetWindowText(_T(""));
}

// IDC_COMBO_STATION: 
//
void CTermSel::OnCbnSetfocusComboStation()
{
	HIMC himc;

	himc = ImmGetContext(GetDlgItem(IDC_COMBO_STATION)->m_hWnd);
	ImmSetOpenStatus(himc, TRUE);
	//ImmSetConversionStatus(himc, IME_CMODE_KATAKANA |IME_CMODE_FULLSHAPE, IME_SMODE_AUTOMATIC);
	ImmSetConversionStatus(himc, /* IME_CMODE_ROMAN | */ IME_CMODE_NATIVE | IME_CMODE_FULLSHAPE, IME_SMODE_AUTOMATIC /* IME_SMODE_PHRASEPREDICT*/);
	UpdateData(FALSE);
}


// IDC_COMBO_STATION: 
//
void CTermSel::OnCbnKillfocusComboStation()
{
	HIMC himc;

	himc = ImmGetContext(GetDlgItem(IDC_COMBO_STATION)->m_hWnd);
	ImmSetOpenStatus(himc, FALSE);
}



//	[Company/Prefect] Listbox double click
//	IDC_LIST_COMPANY
//
void CTermSel::OnLbnDblclkListCompany()
{
	int idx;
	CListBox* pL = (CListBox*)GetDlgItem(IDC_LIST_COMPANY);
	if (0 <= (idx = pL->GetCurSel())) {
		DBO dbo = Route::Enum_lines_from_company_prefect((int)(DWORD_PTR)pL->GetItemData(idx));
		if (!dbo.isvalid()) {
			return;
		}
		pL = (CListBox*)GetDlgItem(IDC_LIST_LINES);
		pL->ResetContent();
		while (dbo.moveNext()) {
			pL->SetItemData(pL->AddString(dbo.getText(0).c_str()), dbo.getInt(1));
		}
		// GetDlgItem(IDC_LIST_LINES)->SetFocus();
	}
}


//	Double click to Lines list
//	IDC_LIST_LINES
//	[>>] line -> station
//	会社or都道府県 + 路線に属する駅を列挙
//
void CTermSel::OnLbnDblclkListLines()
{
	// update station list

	int idx0;
	int idx1;

	CListBox* pL0 = (CListBox*)GetDlgItem(IDC_LIST_COMPANY);
	CListBox* pL1 = (CListBox*)GetDlgItem(IDC_LIST_LINES);

	idx0 = pL0->GetCurSel();
	idx1 = pL1->GetCurSel();
	
	if ((0 <= idx0) && (0 <= idx1)) {
		DBO dbo = Route::Enum_station_located_in_prefect_or_company_and_line(
						(int)(DWORD_PTR)pL0->GetItemData(idx0),
						(int)(DWORD_PTR)pL1->GetItemData(idx1));
		if (!dbo.isvalid()) {
			return;
		}
		
		CListBox* pL = reinterpret_cast<CListBox*>(GetDlgItem(IDC_LIST_TERMINALS));
		pL->ResetContent();
		while (dbo.moveNext()) {
			pL->SetItemData(pL->AddString(dbo.getText(0).c_str()), dbo.getInt(1));
		}
		// GetDlgItem(IDC_LIST_TERMINALS)->SetFocus();
	}
}


//	Double click to Station List
//	IDC_LIST_TERMINALS
//
void CTermSel::OnLbnDblclkListTerminals()
{
	CListBox* pL = reinterpret_cast<CListBox*>(GetDlgItem(IDC_LIST_TERMINALS));
	int idx;
	
	if (0 <= (idx = pL->GetCurSel())) {

		int len = pL->GetTextLen(idx);

		if ((0 < len) && (len < MAX_STATION_CHR)) {
			if (m_stationId == (int)pL->GetItemData(idx)) {
				OnBnClickedOk();
			} else {
				CString station;
				pL->GetText(idx, station);
				int np = station.Find(_T('['));
				if (0 <= np) {
					m_pszStation = station.Left(np);
				} else {
					m_pszStation = station;
				}
				GetDlgItem(IDC_COMBO_STATION)->SetWindowText(m_pszStation);

				m_stationId = (int)pL->GetItemData(idx);
				SetTerminalLineLabel(m_stationId);
			}
		}
	}
}

//	[OK] button
//	IDOK
//
void CTermSel::OnBnClickedOk()
{
	if (0 < m_stationId) {	// 選択済みならOK Close
		saveHistory();
		CDialogEx::OnOK();
		return;
	}

	CString sStation;
	GetDlgItem(IDC_COMBO_STATION)->GetWindowText(sStation);
	sStation.Trim();
	
	CListBox* pL = reinterpret_cast<CListBox*>(GetDlgItem(IDC_LIST_TERMINALS));

	if (0 <= pL->GetCurSel()) {
		OnLbnDblclkListTerminals();
	} else {
		if (!sStation.IsEmpty()) {
			// 入力文字がある場合候補リスト
			OnBnClickedButtonStationSel();
		} else {
		// DONOTHING
		}
	}
}

//	[Cancel] button
//	IDCANCEL
//
void CTermSel::OnBnClickedCancel()
{
	CDialogEx::OnCancel();
}


//	List changed select of Station list.
//	IDC_LIST_TERMINALS
//
void CTermSel::OnLbnSelchangeListTerminals()
{
	CListBox* pL = reinterpret_cast<CListBox*>(GetDlgItem(IDC_LIST_TERMINALS));
	int idx;
	
	if (0 <= (idx = pL->GetCurSel())) {
		if (m_stationId == (int)pL->GetItemData(idx)) {
			return;
		}
	}
	m_stationId = 0;
}


void CTermSel::ClearData()
{
	m_stationId = 0;
	m_pszStation = _T("");
}

//	駅の所属路線を表示
//	
void CTermSel::SetTerminalLineLabel(int stationId)
{
	// get line from station
	CString labelText;

	labelText = Route::GetKanaFromStationId(stationId).c_str();
	if (!labelText.IsEmpty()) {
		labelText += _T(" - ");
	}
	DBO dbo = Route::Enum_line_of_stationId(stationId);
	if (!dbo.isvalid()) {
		return;
	}
	
	CString sJctList;
	while (dbo.moveNext()) {
		if (!BIT_CHK(dbo.getInt(2), BSRJCTSP)) {
			if (sJctList != _T("")) {
				sJctList += _T("/");
			}
			sJctList += dbo.getText(0).c_str();
		}
	}
	labelText += sJctList;
	GetDlgItem(IDC_EDIT_LINE)->SetWindowText(labelText);
}

//	load history
//
void CTermSel::loadHistory()
{
	CComboBox* pCmb = reinterpret_cast<CComboBox*>(GetDlgItem(IDC_COMBO_STATION));
	try {
		HistoryFile hf;
		hf.first();
		LPCTSTR p;
		while (NULL != (p = hf.next())) {
			pCmb->AddString(p);
		}
		if (0 < pCmb->GetCount()) {
			pCmb->AddString(CLEAR_HISTORY);
		}
	}
	catch (CFileException* e)
	{	e->Delete();
		TRACE("履歴ファイルが開けません: %d\n", e->m_lOsError);
	}
}


//	save history
//
void CTermSel::saveHistory()
{
	try {
		HistoryFile hf;
		hf.save(m_pszStation);
	}
	catch (CFileException* e)
	{	e->Delete();
		TRACE("履歴ファイルへ書込みできません: %d\n", e->m_lOsError);
	}
}






//void CTermSel::OnChar(UINT nChar, UINT nRepCnt, UINT nFlags)
//{
//	// TODO: ここにメッセージ ハンドラー コードを追加するか、既定の処理を呼び出します。
//	TRACE("OnChar %u, %u\n", nChar, nFlags);
//	CDialogEx::OnChar(nChar, nRepCnt, nFlags);
//}


BOOL CTermSel::PreTranslateMessage(MSG* pMsg)
{
	if ((pMsg->message == WM_KEYDOWN) && (pMsg->wParam == VK_SPACE)) {
		int id = GetFocus()->GetDlgCtrlID();
		if ((id == IDC_LIST_COMPANY) || (id == IDC_LIST_LINES) || (id == IDC_LIST_TERMINALS)) {
			CListBox* pCtl;
			if (id == IDC_LIST_COMPANY) {
				pCtl = reinterpret_cast<CListBox*>(GetDlgItem(IDC_LIST_LINES));
				if (0 < pCtl->GetCount()) {
					pCtl->SetFocus();
				}
				return FALSE;
			} else if (id == IDC_LIST_LINES) {
				pCtl = reinterpret_cast<CListBox*>(GetDlgItem(IDC_LIST_TERMINALS));
				if (0 < pCtl->GetCount()) {
					pCtl->SetFocus();
				}
				return FALSE;
			} else {
				pMsg->wParam = VK_RETURN;
			}
		}
	}
	return CDialogEx::PreTranslateMessage(pMsg);
}


void CTermSel::OnTimer(UINT_PTR nIDEvent)
{
	if (nIDEvent == 101) {
		if (500 < (GetTickCount() - m_dwSystime)) {
			if (1 == m_lastListChange) {
				OnLbnSelchangeListCompany();
			} else if (2 == m_lastListChange) {
				OnLbnSelchangeListLines();
			}
			m_lastListChange = 0;
		}
	}
}
