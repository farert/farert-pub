#pragma once



// CTermSel ダイアログ

/*!	@file CTermSel diaglog.
 *	Copyright(c) sutezo 2014.
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
class CTermSel : public CDialogEx
{
	DECLARE_DYNAMIC(CTermSel)

public:
	CTermSel(bool bTerm, CWnd* pParent = NULL);   // 標準コンストラクター
	virtual ~CTermSel();

// ダイアログ データ
	enum { IDD = IDD_DIALOG_TERM_SEL };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV サポート
	bool m_bTerm;

	int	m_stationId;
	CString m_pszStation;

	DECLARE_MESSAGE_MAP()
	
	DWORD	m_dwSystime;
	DWORD	m_lastListChange;

	void	ClearData();
	void	SetTerminalLineLabel(int staionId);
	void 	saveHistory();
	void 	loadHistory();
public:
	int		getStationId() {
		return m_stationId;
	}
	LPCTSTR getStationName() {
		return m_pszStation;
	}

	afx_msg void OnBnClickedButtonCompanySel();
	afx_msg void OnBnClickedButtonLineSel();
	afx_msg void OnLbnSelchangeListCompany();
	afx_msg void OnLbnDblclkListCompany();
	afx_msg void OnLbnDblclkListLines();
	afx_msg void OnLbnDblclkListTerminals();
	afx_msg void OnBnClickedOk();
	afx_msg void OnBnClickedCancel();
	virtual BOOL OnInitDialog();
	afx_msg void OnBnClickedButtonStationSel();
	afx_msg void OnLbnSelchangeListLines();
	afx_msg void OnLbnSelchangeListTerminals();
	afx_msg void OnCbnSelchangeComboStation();
	afx_msg void OnCbnEditchangeComboStation();
	afx_msg void OnCbnSetfocusComboStation();
	afx_msg void OnCbnKillfocusComboStation();
	afx_msg void OnCbnEditupdateComboStation();
	afx_msg void OnCbnSelendokComboStation();
//	afx_msg void OnChar(UINT nChar, UINT nRepCnt, UINT nFlags);
	virtual BOOL PreTranslateMessage(MSG* pMsg);
	afx_msg void OnTimer(UINT_PTR nIDEvent);
};
