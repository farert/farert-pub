
// alps_mfcDlg.h : ヘッダー ファイル
//

/*!	@file alps_mfc.cpp application main.
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

#pragma once

#include "../lib/alps/alpdb.h"



// Calps_mfcDlg ダイアログ
class Calps_mfcDlg : public CDialogEx
{
// コンストラクション
public:
	Calps_mfcDlg(CWnd* pParent = NULL);	// 標準コンストラクター

// ダイアログ データ
	enum { IDD = IDD_ALPS_MFC_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV サポート


// 実装
protected:
	HICON m_hIcon;

	// 生成された、メッセージ割り当て関数
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()

private:
	void routeEnd();

protected:
	enum SELMODE { SEL_LINE, SEL_JUNCTION, SEL_TERMINATE };
	void setupForLinelistByStation(int stationId, int curLineId = 0);
	void setupForStationlistByLine(int lineId, int curStationId = 0);
	int UpdateRouteList();
	int ModifyRouteList();
	UINT CancelRouteQuery();
	void CantSameStartAndEnd();
	void ResetContent();
	void showFare();
	int parseAndSetupRoute(LPCTSTR route_str);

private:
	Route	m_route;
	Calps_mfcDlg::SELMODE m_selMode;
	int		m_curStationId;

	tstring m_lastRouteString;
	tstring m_lastResultString;

protected:
	afx_msg void OnBnClickedButtonStartsel();
	afx_msg void OnBnClickedButtonEndsel();
	afx_msg void OnBnClickedButtonSel();
	afx_msg void OnBnClickedButtonBs();
	afx_msg void OnNMDblclkListStations(NMHDR *pNMHDR, LRESULT *pResult);
	afx_msg void OnBnClickedRadioBranchSel();
	afx_msg void OnBnClickedRadioTerminalSel();
	afx_msg void OnBnClickedButtonAllClear();
	afx_msg void OnBnClickedButtonTermClear();
	afx_msg void OnBnClickedButtonStart8x();
	afx_msg void OnBnClickedButtonTerminal8x();
	afx_msg void OnBnClickedButtonAutoroute();
public:
	afx_msg void OnLButtonDblClk(UINT nFlags, CPoint point);
	virtual BOOL PreTranslateMessage(MSG* pMsg);
	afx_msg void OnDropFiles(HDROP hDropInfo);
	afx_msg void OnBnClickedCheckSpecialCity();
	afx_msg void OnBnClickedCheckRuleapply();
	afx_msg void OnBnClickedButtonReverse();
	afx_msg void OnBnClickedButtonRoutecopy();
	afx_msg void OnBnClickedButtonRoutein();
	afx_msg void OnBnClickedButtonResultcopy();
	afx_msg void OnBnClickedButtonRsltopen();
	afx_msg void OnBnClickedButtonRouteOpen();
};

