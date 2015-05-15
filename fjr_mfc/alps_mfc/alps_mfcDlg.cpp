
// alps_mfcDlg.cpp : 実装ファイル
//
//	Copyright(c) sutezo9@me.com 2012 allrightreserved.
//	This source code is GPL license.

#include "stdafx.h"
#include "alps_mfc.h"
#include "alps_mfcDlg.h"
#include "afxdialogex.h"
#include "TermSel.h"
#include "RouteInputDlg.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

using namespace std;
#include <vector>

// ルート選択[完了]か?
#define isComplete()	((0 < m_route.routeList().size()) && \
						 (m_route.endStationId == m_curStationId))



// アプリケーションのバージョン情報に使われる CAboutDlg ダイアログ

class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// ダイアログ データ
	enum { IDD = IDD_ABOUTBOX };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV サポート

// 実装
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialogEx(CAboutDlg::IDD)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)
END_MESSAGE_MAP()


// Calps_mfcDlg ダイアログ




Calps_mfcDlg::Calps_mfcDlg(CWnd* pParent /*=NULL*/)
	: CDialogEx(Calps_mfcDlg::IDD, pParent)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void Calps_mfcDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(Calps_mfcDlg, CDialogEx)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDC_BUTTON_STARTSEL, &Calps_mfcDlg::OnBnClickedButtonStartsel)
	ON_BN_CLICKED(IDC_BUTTON_ENDSEL, &Calps_mfcDlg::OnBnClickedButtonEndsel)
	ON_BN_CLICKED(IDC_BUTTON_SEL, &Calps_mfcDlg::OnBnClickedButtonSel)
	ON_BN_CLICKED(IDC_BUTTON_BS, &Calps_mfcDlg::OnBnClickedButtonBs)
	ON_NOTIFY(NM_DBLCLK, IDC_LIST_LINESTATIONS, &Calps_mfcDlg::OnNMDblclkListStations)
	ON_BN_CLICKED(IDC_RADIO_BRANCH_SEL, &Calps_mfcDlg::OnBnClickedRadioBranchSel)
	ON_BN_CLICKED(IDC_RADIO_TERMINAL_SEL, &Calps_mfcDlg::OnBnClickedRadioTerminalSel)
	ON_BN_CLICKED(IDC_BUTTON_ALL_CLEAR, &Calps_mfcDlg::OnBnClickedButtonAllClear)
	ON_BN_CLICKED(IDC_BUTTON_TERM_CLEAR, &Calps_mfcDlg::OnBnClickedButtonTermClear)
	ON_BN_CLICKED(IDC_BUTTON_AUTOROUTE, &Calps_mfcDlg::OnBnClickedButtonAutoroute)
	ON_WM_LBUTTONDBLCLK()
	ON_WM_DROPFILES()
	ON_BN_CLICKED(IDC_CHECK_SPECIAL_CITY, &Calps_mfcDlg::OnBnClickedCheckSpecialCity)
	ON_BN_CLICKED(IDC_CHECK_RULEAPPLY, &Calps_mfcDlg::OnBnClickedCheckRuleapply)
	ON_BN_CLICKED(IDC_BUTTON_REVERSE, &Calps_mfcDlg::OnBnClickedButtonReverse)
	ON_BN_CLICKED(IDC_BUTTON_ROUTECOPY, &Calps_mfcDlg::OnBnClickedButtonRoutecopy)
	ON_BN_CLICKED(IDC_BUTTON_ROUTEIN, &Calps_mfcDlg::OnBnClickedButtonRoutein)
	ON_BN_CLICKED(IDC_BUTTON_RESULTCOPY, &Calps_mfcDlg::OnBnClickedButtonResultcopy)
	ON_BN_CLICKED(IDC_BUTTON_RSLTOPEN, &Calps_mfcDlg::OnBnClickedButtonRsltopen)
	ON_BN_CLICKED(IDC_BUTTON_ROUTE_OPEN, &Calps_mfcDlg::OnBnClickedButtonRouteOpen)
END_MESSAGE_MAP()


// Calps_mfcDlg メッセージ ハンドラー

BOOL Calps_mfcDlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// "バージョン情報..." メニューをシステム メニューに追加します。

	// IDM_ABOUTBOX は、システム コマンドの範囲内になければなりません。
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// このダイアログのアイコンを設定します。アプリケーションのメイン ウィンドウがダイアログでない場合、
	//  Framework は、この設定を自動的に行います。
	SetIcon(m_hIcon, TRUE);			// 大きいアイコンの設定
	SetIcon(m_hIcon, FALSE);		// 小さいアイコンの設定

	//--
	CListCtrl* pLSel = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_LINESTATIONS));
	pLSel->SetColumnWidth(pLSel->InsertColumn(0, _T("")), LVSCW_AUTOSIZE);
	pLSel->SetColumnWidth(pLSel->InsertColumn(1, _T("")), LVSCW_AUTOSIZE);

	pLSel = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_ROUTE));
	CRect rc;
	pLSel->GetWindowRect(rc);
	pLSel->InsertColumn(0, _T("路線"), LVCFMT_LEFT, rc.Width() / 5  * 3, 0);
	pLSel->InsertColumn(1, _T("乗換駅"), LVCFMT_LEFT, rc.Width() / 5 * 2, 0);

	ResetContent();	// 発駅、着駅、経路 => 全消去 IDC_BUTTON_ALL_CLEAR [X] Button pushed.

//////////////////////////////////////#####################
#ifdef _DEBUG
	test_exec();	// 単体テストを実行(結果はtest_result.txt)
#endif
//////////////////////////////////////#####################

	DragAcceptFiles();

	return TRUE;  // フォーカスをコントロールに設定した場合を除き、TRUE を返します。
}

void Calps_mfcDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialogEx::OnSysCommand(nID, lParam);
	}
}

// ダイアログに最小化ボタンを追加する場合、アイコンを描画するための
//  下のコードが必要です。ドキュメント/ビュー モデルを使う MFC アプリケーションの場合、
//  これは、Framework によって自動的に設定されます。

void Calps_mfcDlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // 描画のデバイス コンテキスト

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// クライアントの四角形領域内の中央
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// アイコンの描画
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}

// ユーザーが最小化したウィンドウをドラッグしているときに表示するカーソルを取得するために、
//  システムがこの関数を呼び出します。
HCURSOR Calps_mfcDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}


//	DialogなのでEnterやESCでウィンドウが閉じないようにするため.
//
BOOL Calps_mfcDlg::PreTranslateMessage(MSG* pMsg)
{
	if (pMsg->message == WM_KEYDOWN) {
		switch (pMsg->wParam) {
		case VK_RETURN:
		case VK_ESCAPE:
			return TRUE;
		default:
			break;
		}
	}
	return CDialogEx::PreTranslateMessage(pMsg);
}


// 発駅指定
//	IDC_BUTTON_STARTSEL [...] button pushed
//
void Calps_mfcDlg::OnBnClickedButtonStartsel()
{
	CTermSel dlg(false, this);
	int startStationId;

	if (IDOK == dlg.DoModal()) {
		startStationId = dlg.getStationId();
		if (startStationId != m_route.startStationId()) {
			// 開始駅=終着駅は盲腸線でないことを確認
			if (m_route.endStationId  == startStationId) {
				if (Route::NumOfNeerNode(startStationId) <= 1) {
					CantSameStartAndEnd();	// "指定した発駅＝着駅の経路は指定不可能です"
					return;
				}
			}
			// 既選択ルートの破棄確認
			if (0 < reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_ROUTE))->GetItemCount()) {
				if (IDYES != CancelRouteQuery()) {
					return;
				}
				ResetContent();	// 発駅、着駅、経路 => 全消去 IDC_BUTTON_ALL_CLEAR [X] Button pushed.
			}
			m_curStationId = startStationId;		// 発駅Id
			m_route.add(startStationId);
			GetDlgItem(IDC_EDIT_START)->SetWindowText(dlg.getStationName());	// 発駅表示
			setupForLinelistByStation(m_curStationId);				// 発駅の所属路線一覧の表示
			GetDlgItem(IDC_LIST_LINESTATIONS)->EnableWindow(TRUE);	// 駅/路線 選択リスト選択可
			GetDlgItem(IDC_BUTTON_SEL)->EnableWindow(TRUE);			// [+] button
		}// 不変更ならなにもしない
	}
}

// 着駅指定
//	IDC_BUTTON_ENDSEL [...] button pushed.
//
void Calps_mfcDlg::OnBnClickedButtonEndsel()
{
	int numList;
	int endStationId;
	CListCtrl* pLRoute = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_ROUTE));

	CTermSel dlg(true, this);

	if (IDOK != dlg.DoModal()) {
		return;
	}
	endStationId = dlg.getStationId();
	if (endStationId == m_route.endStationId) {
		return;
	}
	ASSERT(0 < endStationId);

	// 開始駅=終着駅は盲腸線でないことを確認
	if (endStationId == m_route.startStationId()) {
		if (Route::NumOfNeerNode(endStationId) <= 1) {
			CantSameStartAndEnd();	// "指定した発駅＝着駅の経路は指定不可能です"
			return;
		}
	}

	/* 開始駅≠終着駅で、終着駅が既に経路上に通過しているかチェック */
	if ((endStationId != m_route.startStationId()) && 
		m_route.checkPassStation(endStationId)) {
		if (isComplete() || (IDYES == MessageBox(
_T("着駅は経路内を既に通過しております. 着駅以降の経路をキャンセルしますか？"), 
_T("着駅挿入、経路短縮"), 
			MB_ICONEXCLAMATION|MB_YESNO|MB_DEFBUTTON2))) {

			m_route.terminate(endStationId);	/* set end station */
			/* numList = */UpdateRouteList();	/* IDC_LIST_ROUTE update view */

			ASSERT(m_curStationId == endStationId);
			//m_selMode = SEL_LINE;				/* for [-] button */
			//int curLineId = IDENT1(pLRoute->GetItemData(numList - 1));	// last line
			//ASSERT(0 < curLineId);
			//setupForLinelistByStation(m_curStationId, curLineId);	// 着駅の所属路線
			routeEnd();
			///* 運賃表示 */
			///showFare();
		} else {
			return;
		}
	} else { /* 終着駅は経路上まだ通過していない場合 */
		numList = pLRoute->GetItemCount();
		if (isComplete()) {
			// 既に別の終着駅で「完了」している場合、リスト終端をキャンセルし([-]ボタン同様)
			// 選択リストを「(終着)駅の所属路線一覧」->「路線の分岐駅一覧」へ変更
			m_route.removeTail();
			if (2 <= numList) {
				m_curStationId = IDENT2(pLRoute->GetItemData(numList - 2));
			} else {
				m_curStationId = m_route.startStationId();		// 発駅
			}
			GetDlgItem(IDC_LIST_LINESTATIONS)->EnableWindow(TRUE);	// 駅/路線 選択リスト
			GetDlgItem(IDC_BUTTON_SEL)->EnableWindow(TRUE);			// [+] button
			m_selMode = SEL_JUNCTION;
		}
		m_route.endStationId = endStationId;	/* 終着駅更新 */
		if (m_selMode != SEL_LINE) {
			// 選択リストが「路線の分岐駅一覧」or 「路線の駅一覧」表示中だった場合
			// 「(着駅)」と表示されたリストを更新する為、駅選択リストを更新
			setupForStationlistByLine(IDENT1(pLRoute->GetItemData(numList - 1)), m_curStationId);
		}
	}
	SetDlgItemText(IDC_EDIT_END, dlg.getStationName());		// 着駅表示
	GetDlgItem(IDC_BUTTON_TERM_CLEAR)->EnableWindow(TRUE);
}


// 「路線」／「分岐駅」／「着駅」の選択
//	IDC_BUTTON_SEL [+] button pushed.
//
void Calps_mfcDlg::OnBnClickedButtonSel()
{
	int selIdx;
	int selId;
	int nRoute;
	CString selTitle;
	int curLineId;
	
	int wc;
	int wn;

	CListCtrl* pLRoute = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_ROUTE));
	CListCtrl* pLSel   = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_LINESTATIONS));

	selIdx   = pLSel->GetNextItem(-1, LVNI_ALL | LVNI_SELECTED);
	if ((1 !=  pLSel->GetSelectedCount()) || (-1 == selIdx)) {
		return;		/* Multiselected or non selection. */
	}

	if ((pLSel->GetItemText(selIdx, 0))[0] == _T('-')) {
		SetDlgItemText(IDC_EDIT_STAT, _T("直前乗車路線は指定できません.戻って乗換駅を再選択してください."));
		return;
	}

	nRoute	 = pLRoute->GetItemCount();			// 経路リスト数
	selTitle = pLSel->GetItemText(selIdx, 0);	// 選択 駅／線 名
	selId    = pLSel->GetItemData(selIdx);		//        のId

	ASSERT(0 < selId);

	if (m_selMode == SEL_LINE) {
		// add route list 路線Id
		pLRoute->SetItemText(pLRoute->InsertItem(LVIF_TEXT | LVIF_PARAM, nRoute, selTitle, 0, 0, 0, MAKEPAIR(selId, 0)), 1, _T(""));
		wc = pLRoute->GetColumnWidth(0);
		wn = pLRoute->GetStringWidth(selTitle) + 16;
		if (wc < wn) {
			pLRoute->SetColumnWidth(0, wn);
		}
		GetDlgItem(IDC_BUTTON_BS)->EnableWindow(TRUE);		// Enable [-] button

		m_selMode = SEL_JUNCTION;
		setupForStationlistByLine(selId, m_curStationId);
	} else {
		// add route list 駅Id

		/* 経路追加 */// last line
		curLineId = IDENT1(pLRoute->GetItemData(nRoute - 1));	//(stationId is not yet strage in HIWORD)
		int rslt = m_route.add(curLineId, /*m_curStationId,*/selId);
		if (m_route.isModified()) {
			if (0 < ModifyRouteList()) {		// 経路表示更新
				curLineId = m_route.routeList().back().lineId;
				selId = m_route.routeList().back().stationId;
			} else {
				ResetContent();
				return;
			}
		}
		if (rslt < 0) {
			ASSERT(rslt == -1);		/* -1 以外はバグ(DBエラーか、引数不正) */
			if (-1 != rslt) {
				AfxMessageBox(_T("Fatal error occured."));
				ResetContent();
				return;
			}
			SetDlgItemText(IDC_EDIT_STAT, _T("経路が重複しています."));
			return;
		}
		if (0 == rslt) {	/* fin */
			if (m_route.endStationId != selId) {
				if ((m_selMode != SEL_TERMINATE) &&
				(IDYES != MessageBox(
				_T("経路が片道条件に達しました. 着駅として終了しますか？"), _T("経路終端"),
										MB_YESNO | MB_ICONQUESTION))) {
					m_route.removeTail();
					if (0 < ModifyRouteList()) {		// 経路表示更新
						curLineId = m_route.routeList().back().lineId;
						selId = m_route.routeList().back().stationId;
					} else {
						ResetContent();
					}
					return;
				}
				m_route.end();
				m_route.endStationId = selId;				// 着駅変更
				SetDlgItemText(IDC_EDIT_END, selTitle);
				GetDlgItem(IDC_BUTTON_TERM_CLEAR)->EnableWindow(TRUE);
			}
			setupForLinelistByStation(selId, curLineId);
			routeEnd();
		} else if (1 != rslt) {	// undefine
			ASSERT(FALSE);
			return;
		} else { 				/* rslt == 1 */
			setupForLinelistByStation(selId, curLineId);

			if ((m_selMode == SEL_TERMINATE) || (selId == m_route.endStationId)) {
				/* 着駅指定 */
				if (selId != m_route.endStationId) {
					m_route.endStationId = selId;		/* 着駅:強制書き換え */
					SetDlgItemText(IDC_EDIT_END, selTitle);						// 着駅表示
					GetDlgItem(IDC_BUTTON_TERM_CLEAR)->EnableWindow(TRUE);		// 
				}
				routeEnd();
			} else if ((rslt == 1) && !m_route.isModified()) {	/* OK */
				pLRoute->SetItemText(nRoute - 1, 1, selTitle);					// 経路：分岐駅表示
				pLRoute->SetItemData(nRoute - 1, MAKEPAIR(curLineId, selId));	//経路：分岐駅ID設定

				// カラム幅調整
				wc = pLRoute->GetColumnWidth(1);
				wn = pLRoute->GetStringWidth(selTitle) + 16;
				if (wc < wn) {
					pLRoute->SetColumnWidth(1, wn);
				}
			}
		}
		
		/* 運賃表示 */
		showFare();
		m_curStationId = selId;
		m_selMode = SEL_LINE;	/* for [-] button */
	}
}

//	List double click
//	IDC_LIST_LINESTATIONS [(路線／分岐駅／着駅)] ListCtrl Double clicked.
//
void Calps_mfcDlg::OnNMDblclkListStations(NMHDR *pNMHDR, LRESULT *pResult)
{
	OnBnClickedButtonSel();	// 「路線」/「分岐駅」/「着駅」の選択(IDC_BUTTON_SEL[+]button pushed)	
}

//	分岐駅選択 Radio Button
//	IDC_RADIO_BRANCH_SEL [分岐駅] Radio Button pushed.
//
void Calps_mfcDlg::OnBnClickedRadioBranchSel()
{
	int itemcnt;

	if (m_selMode == SEL_LINE) {
		ASSERT(FALSE);
		return;
	}
	
	if (IDC_RADIO_BRANCH_SEL == GetCheckedRadioButton(IDC_RADIO_BRANCH_SEL, IDC_RADIO_TERMINAL_SEL)) {
		m_selMode = SEL_JUNCTION;
	} else {
		m_selMode = SEL_TERMINATE;
	}

	CListCtrl* pLRoute = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_ROUTE));
	itemcnt = pLRoute->GetItemCount();
	int curLineId = IDENT1(pLRoute->GetItemData(itemcnt - 1));	// current select line

	ASSERT(((pLRoute->GetItemCount() <= 1) && (m_route.routeList().size() == 0) && 
			(m_curStationId == m_route.startStationId())) || 
			((itemcnt < 2) || (m_curStationId == IDENT2(pLRoute->GetItemData(pLRoute->GetItemCount() - 2)))));	// current select line

	if (0 < curLineId) {
		setupForStationlistByLine(curLineId, m_curStationId);
	} else {
		ASSERT(FALSE);
	}
}

//	終着駅指定 Radio button
//	IDC_RADIO_STATION_SEL [着駅] Radio Button pushed.
//
void Calps_mfcDlg::OnBnClickedRadioTerminalSel()
{
	OnBnClickedRadioBranchSel();	// IDC_RADIO_BRANCH_SEL [分岐駅] Radio Button pushed.
}

// delete button(経路の末尾をキャンセル)
//	IDC_BUTTON_BS [-] button pushed.
//
//	enable: IDC_LIST_LINESTATIONS item added for IDC_BUTTON_SEL click or IDC_LIST_LINESTATIONS double click
//	disable: this(self) removed or clear(route_end())
//
void Calps_mfcDlg::OnBnClickedButtonBs()
{
	CListCtrl* pLSel   = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_LINESTATIONS));
	CListCtrl* pLRoute = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_ROUTE));
	int numList;
	int curLineId;

	numList = pLRoute->GetItemCount();
	if (numList < 1) {
		ASSERT(FALSE);
		return;
	}

	if (isComplete()) {
		GetDlgItem(IDC_LIST_LINESTATIONS)->EnableWindow(TRUE);	// 駅/路線 選択リスト
		GetDlgItem(IDC_BUTTON_SEL)->EnableWindow(TRUE);			// [+] button
	}
	if (m_selMode == SEL_LINE) {
		/* 路線リスト表示中 */
		ASSERT(2 <= m_route.routeList().size());
		ASSERT((m_curStationId == m_route.endStationId) || (m_curStationId == IDENT2(pLRoute->GetItemData(numList - 1))));
		if (2 <= numList) {			/* Routeリストに分岐駅は2行以上? */
			m_curStationId = IDENT2(pLRoute->GetItemData(numList - 2)); // 最終行の分岐駅
		} else {
			m_curStationId = m_route.startStationId();		// 発駅
		}
		m_selMode = SEL_JUNCTION;
		m_route.removeTail();

		curLineId = IDENT1(pLRoute->GetItemData(numList - 1));	// last line
		setupForStationlistByLine(curLineId, m_curStationId);

		pLRoute->SetItemText(numList - 1, 1, _T(""));
		pLRoute->SetItemData(numList - 1, MAKEPAIR(curLineId, 0));

		/* 運賃表示 */
		showFare();
	} else {	/* SEL_JUNCTION or SEL_TERMINATE */
		/* 分岐駅／着駅リスト表示中 */
		m_selMode = SEL_LINE;

		if (2 <= numList) {
			curLineId = IDENT1(pLRoute->GetItemData(numList - 2));	// last line
			ASSERT(0 < curLineId);
		} else {
			curLineId = 0;
			GetDlgItem(IDC_BUTTON_BS)->EnableWindow(FALSE);	// Disable [-] button
		}
		setupForLinelistByStation(m_curStationId, curLineId);

		pLRoute->DeleteItem(numList - 1);				// remvoe tail
	}
}

//	発駅、着駅、経路 => 全消去
//	IDC_BUTTON_ALL_CLEAR [X] Button pushed.
//
void Calps_mfcDlg::OnBnClickedButtonAllClear()
{
	if (0 < reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_ROUTE))->GetItemCount()) {
		if (IDYES != CancelRouteQuery()) {
			return;
		}
	}
	ResetContent();
}

//	着駅クリア
//	IDC_BUTTON_TERM_CLEAR [X] button pushed.
//
void Calps_mfcDlg::OnBnClickedButtonTermClear()
{
	CListCtrl* pLRoute = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_ROUTE));
	int numList = pLRoute->GetItemCount();

	if (isComplete()) {
		// 「完了」
		m_route.removeTail();
		if (2 <= numList) {
			m_curStationId = IDENT2(pLRoute->GetItemData(numList - 2));
		} else {
			m_curStationId = m_route.startStationId();		// 発駅
		}
		GetDlgItem(IDC_LIST_LINESTATIONS)->EnableWindow(TRUE);	// 駅/路線 選択リスト
		GetDlgItem(IDC_BUTTON_SEL)->EnableWindow(TRUE);			// [+] button
		m_selMode = SEL_JUNCTION;
	}
	m_route.endStationId = 0;
	if (m_selMode != SEL_LINE) {
		// 「(着駅)」と表示されたリストを更新する為、駅選択リストを更新
		setupForStationlistByLine(IDENT1(pLRoute->GetItemData(numList - 1)), m_curStationId);
	}
	SetDlgItemText(IDC_EDIT_END, _T(""));
	GetDlgItem(IDC_BUTTON_TERM_CLEAR)->EnableWindow(FALSE);
}

//	IDC_BUTTON_AUTOROUTE [最短経路] button pushed
//
void Calps_mfcDlg::OnBnClickedButtonAutoroute()
{
	int rc;
	
	if ((m_route.startStationId ()<= 0) || (m_route.endStationId <= 0)) {
		MessageBox(_T("開始駅、終了駅を指定しないと最短経路は算出しません."),
										_T("確認"), MB_OK | MB_ICONEXCLAMATION);
		return;
	}
	if (m_route.startStationId()== m_route.endStationId) {
		MessageBox(_T("開始駅=終了駅では最短経路は算出しません."),
										_T("確認"), MB_OK | MB_ICONEXCLAMATION);
		return;
	}
	
	rc = m_route.changeNeerest((IDYES == MessageBox(_T("新幹線を含めますか?"),
										_T("確認"), MB_YESNO | MB_ICONQUESTION | MB_DEFBUTTON2)));
	if (0 <= rc) {
		CListCtrl* pLRoute = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_ROUTE));
		int numList = UpdateRouteList();	/* IDC_LIST_ROUTE update view */
		if (0 < numList) {
			ASSERT(m_curStationId == m_route.endStationId);
			//m_selMode = SEL_LINE;				/* for [-] button */
			//int curLineId = IDENT1(pLRoute->GetItemData(numList - 1));	// last line
			//ASSERT(0 < curLineId);
			//setupForLinelistByStation(m_curStationId, curLineId);	// 着駅の所属路線
			//GetDlgItem(IDC_BUTTON_BS)->EnableWindow(TRUE);			// Enable [-] button
			//
			///* 運賃表示 */
			///showFare();
			routeEnd();
			return;				/* success */
		} else {
			ASSERT(FALSE);
		}
	} else if (-100 < rc) {
		MessageBox(_T("経路が重複しているため算出できませんでした."),
				   _T("自動ルート"), MB_OK | MB_ICONEXCLAMATION);
	} else { /* < -1000 */
		MessageBox(_T("算出できませんでした."),
				   _T("確認"), MB_OK | MB_ICONEXCLAMATION);
	}
	if (m_route.isModified()) {
		if (0 < ModifyRouteList()) {		// 経路表示更新
			int curLineId = m_route.routeList().back().lineId;
			int selId = m_route.routeList().back().stationId;
			setupForLinelistByStation(selId, curLineId);
			showFare();
			routeEnd();
		}
	}
}

//	ListView<IDC_LIST_LINESTATIONS>
//	駅の所属路線一覧を表示
//
//	@param [in]				stationId		駅
//	@param [in][optional]	curLineId	選択不可路線(直前乗車路線)
//
void Calps_mfcDlg::setupForLinelistByStation(int stationId, int curLineId /* =0 */)
{
	CListCtrl* pLSel = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_LINESTATIONS));
	LVCOLUMN column;
	int idx;

	pLSel->DeleteAllItems();			// all record clear

	// 分岐駅<->終着駅 選択
	GetDlgItem(IDC_RADIO_BRANCH_SEL)->ShowWindow(SW_HIDE);
	GetDlgItem(IDC_RADIO_TERMINAL_SEL)->ShowWindow(SW_HIDE);

	memset(&column, 0, sizeof(column));

	CRect rc;
	pLSel->GetClientRect(rc);

	column.mask = LVCF_TEXT | LVCF_WIDTH;
	column.pszText = _T("路線");		// List title
	column.cx = rc.Width();
	pLSel->SetColumn(0, &column);
	column.pszText = _T("");
	column.cx = 10;
	pLSel->SetColumn(1, &column);

	// 駅の所属路線をリスト
	DBO dbo = Route::Enum_line_of_stationId(stationId);
	if (!dbo.isvalid()) {
		ASSERT(FALSE);
		return;
	}
	for (idx = 0; dbo.moveNext(); idx++) {
		CString lineName;
		int lineId = dbo.getInt(1);

		/* 前回選択路線は選択不可(行頭に"-") */
		lineName.Format(_T("%s%s"), (lineId == curLineId) ? _T("- ") : _T(""), dbo.getText(0).c_str());

		pLSel->SetItemText(
				pLSel->InsertItem(LVIF_TEXT | LVIF_PARAM, 
								idx, lineName, 0, 0, 0, lineId), 
				1, _T(""));
	}
	ASSERT(1 <= idx);
	SetDlgItemText(IDC_EDIT_STAT, _T("路線を選択してください."));
	SetDlgItemText(IDC_STATIC_LIST_SEL, _T("路線選択"));
}

//	ListView<IDC_LIST_LINESTATIONS>
//	路線内の分岐駅／全駅一覧を表示
//
//	@param [in]				lineId			路線
//	@param [in][optional]	curStationId	選択不可駅
//
void Calps_mfcDlg::setupForStationlistByLine(int lineId, int curStationId /* =0 */)
{
	CListCtrl* pLSel = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_LINESTATIONS));
	LVCOLUMN column;
	int idx;

	GetDlgItem(IDC_RADIO_BRANCH_SEL)->ShowWindow(SW_SHOW);
	GetDlgItem(IDC_RADIO_TERMINAL_SEL)->ShowWindow(SW_SHOW);

	pLSel->DeleteAllItems();			// all record clear

	memset(&column, 0, sizeof(column));

	CRect rc;
	pLSel->GetClientRect(rc);

	column.mask = LVCF_TEXT;

	if (m_selMode == SEL_JUNCTION) {
		CheckRadioButton(IDC_RADIO_BRANCH_SEL, IDC_RADIO_TERMINAL_SEL, IDC_RADIO_BRANCH_SEL);
		column.pszText = _T("分岐駅");
		SetDlgItemText(IDC_EDIT_STAT, _T("乗換駅を選択してください."));
		SetDlgItemText(IDC_STATIC_LIST_SEL, _T("乗換駅選択"));
	} else {
		CheckRadioButton(IDC_RADIO_BRANCH_SEL, IDC_RADIO_TERMINAL_SEL, IDC_RADIO_TERMINAL_SEL);
		column.pszText = _T("駅");
		SetDlgItemText(IDC_EDIT_STAT, _T("着駅を選択してください."));
		SetDlgItemText(IDC_STATIC_LIST_SEL, _T("着駅選択"));
	}
	pLSel->SetColumn(0, &column);

	column.pszText = _T("分岐路線");
	pLSel->SetColumn(1, &column);

	DBO dbo;
	if (m_selMode == SEL_JUNCTION) {
		dbo = Route::Enum_junction_of_lineId(lineId, m_route.endStationId);
	} else if (m_selMode == SEL_TERMINATE) {
		dbo = Route::Enum_station_of_lineId(lineId);
	} else {
		ASSERT(FALSE);
		return;
	}
	if (!dbo.isvalid()) {
		ASSERT(FALSE);
		return;
	}
	
	int width1, width2;		// カラム幅計算用変数
	width1 = width2 = 0;
	
	for (idx = 0; dbo.moveNext(); idx++) {
		CString stationName;
		int stationId = dbo.getInt(1);

		stationName.Format(_T("%s%s"), 
			(stationId == curStationId) ? _T("- ") : ((stationId == m_route.endStationId) ? _T("(着駅)") : _T("")), 
			dbo.getText(0).c_str());

		CString jctLines;
		if (0 != dbo.getInt(2)) { /* 分岐駅 */
			// 分岐駅の乗り入れ路線を'/'で区切り列挙した文字列を作成
			DBO dbo_lines = Route::Enum_line_of_stationId(stationId);
			if (!dbo_lines.isvalid()) {
				ASSERT(FALSE);
			} else {
				while (dbo_lines.moveNext()) {
					if (!BIT_CHK(dbo_lines.getInt(2), BSRJCTSP)) {
						if (jctLines != _T("")) {
							jctLines += _T("/");
						}
						jctLines += dbo_lines.getText(0).c_str();
					}
				}
			}
		}
		pLSel->SetItemText(
			pLSel->InsertItem(LVIF_TEXT | LVIF_PARAM, 
							idx, stationName, 0, 0, 0, stationId), 
			1, jctLines);

		// カラム幅計算
		int w1 = pLSel->GetStringWidth(stationName);
		int w2 = pLSel->GetStringWidth(jctLines);
		if (width1 < w1) {
			width1 = w1;
		}
		if (width2 < w2) {
			width2 = w2;
		}
	}
	pLSel->SetColumnWidth(0, width1 + 16);
	pLSel->SetColumnWidth(1, width2 + 16);
}

//	ルート選択キャンセル(ルート破棄）問い合わせ
//
UINT Calps_mfcDlg::CancelRouteQuery()
{
	return MessageBox(_T("経路選択中ですがすべてキャンセルしてもよろしいですか？"),
										_T("選択経路破棄確認"), MB_YESNO | MB_ICONQUESTION);
}

// "指定した発駅＝着駅の経路は指定不可能です"
//
void Calps_mfcDlg::CantSameStartAndEnd()
{
	MessageBox(_T("指定した発駅＝着駅の経路は指定不可能です"), _T("指定不可発着駅"), MB_ICONEXCLAMATION);
}


//	表示クリア
//	(画面表示の初期化)
//
void Calps_mfcDlg::ResetContent()
{
	CListCtrl* pLSel = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_LINESTATIONS));

	m_route.removeAll();

	m_selMode = SEL_LINE;
	m_curStationId = 0;

	LVCOLUMN column;
	memset(&column, 0, sizeof(LVCOLUMN));

	column.mask = LVCF_TEXT | LVCF_WIDTH;

	column.pszText = _T("路線");
	column.cx = 80;
	pLSel->SetColumn(0, &column);

	column.pszText = _T("");
	column.cx = 200;
	pLSel->SetColumn(1, &column);

	pLSel->DeleteAllItems();			// all record clear

	reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_ROUTE))->DeleteAllItems();

	GetDlgItem(IDC_BUTTON_ENDSEL)->EnableWindow(TRUE); // 着駅選択
	GetDlgItem(IDC_BUTTON_STARTSEL)->EnableWindow(TRUE);

	GetDlgItem(IDC_BUTTON_TERM_CLEAR)->EnableWindow(FALSE);

	GetDlgItem(IDC_LIST_LINESTATIONS)->EnableWindow(FALSE);	// 駅/路線 選択リスト
	GetDlgItem(IDC_BUTTON_SEL)->EnableWindow(FALSE);		// [+]button

	GetDlgItem(IDC_BUTTON_BS)->EnableWindow(FALSE);
	GetDlgItem(IDC_EDIT_STAT)->SetWindowText(_T("発駅選択してください."));

	GetDlgItem(IDC_EDIT_START)->SetWindowText(_T(""));
	GetDlgItem(IDC_EDIT_END)->SetWindowText(_T(""));
	GetDlgItem(IDC_STATIC_LIST_SEL)->SetWindowText(_T("")); // ListView title
	GetDlgItem(IDC_RADIO_BRANCH_SEL)->ShowWindow(SW_HIDE);
	GetDlgItem(IDC_RADIO_TERMINAL_SEL)->ShowWindow(SW_HIDE);

	GetDlgItem(IDC_BUTTON_STARTSEL)->SetFocus();

	SetDlgItemText(IDC_EDIT_RESULT, _T(""));

	CheckDlgButton(IDC_CHECK_RULEAPPLY, BST_CHECKED);	/* [特例適用]ボタン押下げ状態 */
	GetDlgItem(IDC_CHECK_SPECIAL_CITY)->EnableWindow(FALSE);
}

//	着駅までの指定完了
//
//
void Calps_mfcDlg::routeEnd()
{
	/* 終着駅指定 */
	GetDlgItem(IDC_RADIO_BRANCH_SEL)->ShowWindow(SW_HIDE);		// RADIO BUTTON[分岐駅]
	GetDlgItem(IDC_RADIO_TERMINAL_SEL)->ShowWindow(SW_HIDE);	// RADIO BUTTON[終着駅]
	SetDlgItemText(IDC_STATIC_LIST_SEL, _T(""));				// Select List view title
	GetDlgItem(IDC_LIST_LINESTATIONS)->EnableWindow(FALSE);		// [路線/分岐駅/着駅]Select List View
	GetDlgItem(IDC_BUTTON_SEL)->EnableWindow(FALSE);			// [+]
	// 着駅の所属路線の表示の役目として残すことにするためにコンテンツは消去しない
	//reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_LINESTATIONS))
	//->DeleteAllItems();											// all record clear
	SetDlgItemText(IDC_EDIT_STAT, _T("完了"));
}



//	[発駅を単駅に指定／着駅を単駅に指定]
//
void Calps_mfcDlg::OnBnClickedCheckSpecialCity()
{
	showFare();
}

//	[特例適用]チェックボタン
//
void Calps_mfcDlg::OnBnClickedCheckRuleapply()
{
	showFare();
}

//	[リバース]Pushボタン
//	経路を逆転する
//
void Calps_mfcDlg::OnBnClickedButtonReverse()
{
	int rc;
	int endStationId;

	endStationId = m_route.endStationId;

	if (m_route.routeList().size() <= 1) {
		if ((0 < m_route.endStationId) && (0 < m_route.startStationId())) {
			m_route.endStationId = m_route.startStationId();
			m_curStationId = endStationId;
			m_route.add(endStationId);
			GetDlgItem(IDC_EDIT_START)->SetWindowText(Route::StationName(m_route.startStationId()).c_str());	// 発駅表示
			GetDlgItem(IDC_EDIT_END)->SetWindowText(Route::StationName(m_route.endStationId).c_str());	// 着駅表示

			setupForLinelistByStation(m_curStationId);				// 発駅の所属路線一覧の表示
		}
		return;
	}
	
	rc = m_route.reverse();

	if (0 < rc) {
		GetDlgItem(IDC_EDIT_START)->SetWindowText(Route::StationName(m_route.startStationId()).c_str());	// 発駅表示
		UpdateRouteList();
		if (0 < endStationId) {
			if (endStationId == m_route.startStationId()) {
				endStationId = (m_route.routeList().cend() - 1)->stationId;
			}
			m_route.endStationId = endStationId;
			GetDlgItem(IDC_EDIT_END)->SetWindowText(Route::StationName(endStationId).c_str());	// 着駅表示
		}
	} else if (rc < 0) {
		AfxMessageBox(_T("経路が重複しています"));
	}
}


// [経路記録]
//
void Calps_mfcDlg::OnBnClickedButtonRoutecopy()
{
	tstring s = m_route.route_script();

	if (s.empty() || (0 == s.compare(m_lastRouteString))) {
		return;
	}

	CStdioFile file;

	if (file.Open(_T("route.txt"), CFile::modeCreate |CFile::modeReadWrite | CFile::modeNoTruncate)) {
		file.SeekToEnd();
		file.WriteString(s.c_str());
		m_lastRouteString.assign(s);
	} else {
		AfxMessageBox(_T("ファイルオープンエラー"));
	}
}

//	[経路開く]
//
void Calps_mfcDlg::OnBnClickedButtonRouteOpen()
{
	CString s;
	CFileDialog dlg(TRUE);
	HINSTANCE hInst =
	ShellExecute(NULL, _T("open"), _T("route.txt"), NULL, NULL, SW_SHOW);

	if (hInst <= (HINSTANCE)32) {
		s.Format(_T("経路記録ファイルのオープンに失敗しました. %d"), hInst);
		AfxMessageBox(s);
		
		if (IDYES == dlg.DoModal()) {
			ShellExecute(NULL, _T("open"), dlg.GetFileName(), NULL, NULL, SW_SHOW);
		}
	}
}

// [経路入力]
//
void Calps_mfcDlg::OnBnClickedButtonRoutein()
{
	CRouteInputDlg dlg;
	if (IDOK == dlg.DoModal()) {
		parseAndSetupRoute(dlg.routeString);
	}
}

// [結果記録]
//
void Calps_mfcDlg::OnBnClickedButtonResultcopy()
{
	tstring s;
	tstring result_string;
	CStdioFile file;
	int opt;
	int flag;
	bool ui_sel;

	flag = 0;

	/* 単駅選択可能な特定都区市内発着か? */
	opt = m_route.fareCalcOption();
	if ((opt == 1) || (opt == 2)) {
		/* 単駅指定 */
		ui_sel = (BST_CHECKED == IsDlgButtonChecked(IDC_CHECK_SPECIAL_CITY));
		if (((opt == 1) && !ui_sel) || ((opt == 2) && ui_sel)) {
			flag = APPLIED_START;
		}
	}
	/* 規則適用か? */
	flag |=	((BST_CHECKED == IsDlgButtonChecked(IDC_CHECK_RULEAPPLY)) ? RULE_APPLIED : RULE_NO_APPLIED);
	result_string = m_route.showFare(flag).c_str();
	
	int rp;
	do {
		rp = result_string.find(_T("\r\n"));
		if (rp == string::npos) {
			break;
		}
		result_string.replace(rp, 2, _T("\n"));
	} while (true);

	if (result_string.empty() || (0 == result_string.compare(m_lastResultString))) {
		return;
	}
	
	s = result_string + _T("\n------------------------------------------------\n");
	if (file.Open(_T("result.txt"), CFile::modeCreate |CFile::modeReadWrite | CFile::modeNoTruncate)) {
		file.SeekToEnd();
		file.WriteString(s.c_str());
		m_lastResultString.assign(result_string);
	} else {
		AfxMessageBox(_T("ファイルオープンエラー"));
	}
}

//	m_routeの内容でIDC_LIST_ROUTEを作成しなおす
//	@return IDC_LIST_ROUTEの行数を返す
//
int Calps_mfcDlg::UpdateRouteList()
{
	int idx;
	int w0;
	int w1;
	int lineId = 0;
	int stationId = 0;

	CListCtrl* pLRoute = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_ROUTE));

	pLRoute->DeleteAllItems();

	if (m_route.routeList().size() <= 1) {
		return 0;
	}

	vector<RouteItem>::const_iterator pos = m_route.routeList().cbegin();
	w0 = w1 = 0;
	ASSERT((pos->lineId == 0) && (pos->stationId == m_route.startStationId()));
	pos++;
	for (idx = 0; pos != m_route.routeList().cend() ; pos++, idx++) {
		CString lineName;
		CString stationName;
		/* 
		 * retrive line and station
		 *
		 */
		stationId = pos->stationId;
		if (stationId != m_route.endStationId) {
			stationName = Route::StationName(stationId).c_str();
		}
		lineId = pos->lineId;
		lineName = Route::LineName(lineId).c_str();

		pLRoute->SetItemText(
			pLRoute->InsertItem(LVIF_TEXT | LVIF_PARAM, 
								idx, 
								lineName, 0, 0, 0, 
								MAKEPAIR(lineId, stationId)), 
								1, stationName);
								
		// カラム幅計算
		int wn0 = pLRoute->GetStringWidth(lineName) + 16;
		int wn1 = pLRoute->GetStringWidth(stationName) + 16;
		if (w0 < wn0) {
			w0 = wn0;
		}
		if (w1 < wn1) {
			w1 = wn1;
		}
	}
	ASSERT(pLRoute->GetItemCount() == idx);
	
	if (0 < idx) {
		// カラム幅設定
		if (pLRoute->GetColumnWidth(0) < w0) {
			pLRoute->SetColumnWidth(0, w0);
		}
		if (pLRoute->GetColumnWidth(1) < w1) {
			pLRoute->SetColumnWidth(1, w1);
		}

		// UI mode set
		m_selMode = SEL_LINE;				/* for [-] button */
		setupForLinelistByStation(stationId, lineId);	// 着駅の所属路線

		m_curStationId = stationId;

		GetDlgItem(IDC_BUTTON_BS)->EnableWindow(TRUE);			// Enable [-] button

		/* 運賃表示 */
		showFare();
	} else {
		GetDlgItem(IDC_BUTTON_BS)->EnableWindow(FALSE);		// Disnable [-] button
	}
	UpdateWindow();
	return idx;
}

//	m_routeの内容で経路リスト:IDC_LIST_ROUTEを作成しなおす(後ろ3行のみ)
//	@return IDC_LIST_ROUTEの変更行数を返す
//
int Calps_mfcDlg::ModifyRouteList()
{
	int idx;
	int w0;
	int w1;
	int nitem;
	int lineId = 0;
	int stationId = 0;
	DWORD dw;

	w0 = w1 = 0;

	CListCtrl* pLRoute = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_ROUTE));

	nitem = pLRoute->GetItemCount();
	if (nitem < 5) {
		return UpdateRouteList();	// 5行以下なら全更新
	}
	if (m_route.routeList().size() <= 1) {
		ASSERT(FALSE);
		return 0;					// 経路なし
	}
	// Listの後ろ3行を消去
	for (idx = 0; idx < 3; idx++) {
		pLRoute->DeleteItem(nitem - idx - 1);
	}
	idx = nitem - 3 - 1;	// last index
	dw = pLRoute->GetItemData(idx);
	RouteItem ri(IDENT1(dw), IDENT2(dw));	// last item

	vector<RouteItem>::const_reverse_iterator rpos = m_route.routeList().crbegin();
	rpos++;
	// 経路リストを最後より表示のLast Item値と一致するものを得る.
	while (rpos != m_route.routeList().crend()) {
		if (ri == *rpos) {
			break;
		}
		rpos++;
	}
	
	ASSERT(ri == *rpos);
	ASSERT(rpos != m_route.routeList().crend());
	ASSERT(rpos != m_route.routeList().crbegin());
	if (!ri.is_equal(*rpos)) {
		return idx;		// safety >>>>>>>>>>>
	}
	
	do {
		rpos--;		// forward
		idx++;		// forward

		CString lineName;
		CString stationName;
		/* 
		 * retrive line and station
		 *
		 */
		stationId = rpos->stationId;
		if (stationId != m_route.endStationId) {
			stationName = Route::StationName(stationId).c_str();
		}
		lineId = rpos->lineId;
		lineName = Route::LineName(lineId).c_str();

		pLRoute->SetItemText(
			pLRoute->InsertItem(LVIF_TEXT | LVIF_PARAM, 
								idx, 
								lineName, 0, 0, 0, 
								MAKEPAIR(lineId, stationId)), 
								1, stationName);
								
		// カラム幅計算
		int wn0 = pLRoute->GetStringWidth(lineName) + 16;
		int wn1 = pLRoute->GetStringWidth(stationName) + 16;
		if (w0 < wn0) {
			w0 = wn0;
		}
		if (w1 < wn1) {
			w1 = wn1;
		}
	} while (rpos != m_route.routeList().crbegin());

	idx++;
	ASSERT(pLRoute->GetItemCount() == idx);
	
	if (0 < idx) {
		// カラム幅設定
		if (pLRoute->GetColumnWidth(0) < w0) {
			pLRoute->SetColumnWidth(0, w0);
		}
		if (pLRoute->GetColumnWidth(1) < w1) {
			pLRoute->SetColumnWidth(1, w1);
		}

		// UI mode set
		m_selMode = SEL_LINE;				/* for [-] button */
		setupForLinelistByStation(stationId, lineId);	// 着駅の所属路線

		m_curStationId = stationId;

		GetDlgItem(IDC_BUTTON_BS)->EnableWindow(TRUE);			// Enable [-] button

		/* 運賃表示 */
		showFare();
	} else {
		GetDlgItem(IDC_BUTTON_BS)->EnableWindow(FALSE);		// Disnable [-] button
	}
	UpdateWindow();
	return idx;
}

/*	Dialog drag and drop
 *  ファイルをD&Dすることで経路を追加する機能
 *	ファイルは単一テキストファイルのみで1行目1行のみ読み込んで設定
 *	1行のみで, ',', ' ', '|', '/', (tab)などの区切りで"駅、路線、分岐駅、路線、..."の並び
 *
 */
void Calps_mfcDlg::OnDropFiles(HDROP hDropInfo)
{
	TCHAR path[MAX_PATH];
    CString str;

    if (1 != DragQueryFile(hDropInfo, 0xffffffff, NULL, 0)) {
		return;	/* ignore multi file drop */
	}
    
	DragQueryFile(hDropInfo, 0, path, MAX_PATH);
	try {
		CStdioFile fn(path, CFile::modeRead);
		fn.ReadString(str);
		parseAndSetupRoute(str);
	} catch (CFileException *e) {
		e->Delete();
	}
}


/*	運賃表示
 *
 */
void Calps_mfcDlg::showFare()
{
	int opt;
	int flag;
	bool ui_sel;
	
	/*	運賃表示条件フラグ取得 */

	flag = 0;

	/* 単駅選択可能な特定都区市内発着か? */
	opt = m_route.fareCalcOption();
	if ((opt == 1) || (opt == 2)) {
		/* 単駅指定 */
		ui_sel = (BST_CHECKED == IsDlgButtonChecked(IDC_CHECK_SPECIAL_CITY));
		if (((opt == 1) && !ui_sel) || ((opt == 2) && ui_sel)) {
			flag = APPLIED_START;
		}
	}
	/* 規則適用か? */
	flag |=	((BST_CHECKED == IsDlgButtonChecked(IDC_CHECK_RULEAPPLY)) ? RULE_APPLIED : RULE_NO_APPLIED);
	
	SetDlgItemText(IDC_EDIT_RESULT, m_route.showFare(flag).c_str());
	
	opt = m_route.fareCalcOption();
	if ((opt == 1) || (opt == 2)) {
		//case 1:		// 「発駅を単駅に指定」
		//case 2:		// 「着駅を単駅に指定」
		GetDlgItem(IDC_CHECK_SPECIAL_CITY)->EnableWindow(TRUE);
		if (opt == 1) {
			SetDlgItemText(IDC_CHECK_SPECIAL_CITY, _T("発駅を単駅に指定"));
		} else {
			SetDlgItemText(IDC_CHECK_SPECIAL_CITY, _T("着駅を単駅に指定"));
		}
	} else {
		GetDlgItem(IDC_CHECK_SPECIAL_CITY)->EnableWindow(FALSE);
	}
}


//	Dialog Double click
//
//
void Calps_mfcDlg::OnLButtonDblClk(UINT nFlags, CPoint point)
{
#ifdef _DEBUG		//	for TEST
	//int numList;

	//CListCtrl* pLRoute = reinterpret_cast<CListCtrl*>(GetDlgItem(IDC_LIST_ROUTE));

	//test_exec();	// 単体テストを実行(結果はtest_result.txt)
	//numList = UpdateRouteList();	/* IDC_LIST_ROUTE update view */

	//m_curStationId = IDENT2(pLRoute->GetItemData(numList - 1));	// last station
	//m_selMode = SEL_LINE;				/* for [-] button */
	//int curLineId = IDENT1(pLRoute->GetItemData(numList - 1));	// last line
	//ASSERT(0 < curLineId);
	//setupForLinelistByStation(m_curStationId, curLineId);	// 着駅の所属路線

	if (1 < m_route.routeList().size()) {

		vector<RouteItem>::const_iterator pos = m_route.routeList().cbegin();
		TRACE(_T("\nbegin befor: %s\n"), Route::StationName(pos->stationId).c_str());
		for (++pos; pos != m_route.routeList().cend(); pos++) {
			TRACE(_T("%s, %s, %d\n"), Route::LineName(pos->lineId).c_str(), Route::StationName(pos->stationId).c_str(), pos->flag>>31);
		}
		TRACE(_T("\n"));
	
		UpdateRouteList();

		pos = m_route.routeList().cbegin();
		TRACE(_T("\nbegin after: %s\n"), Route::StationName(pos->stationId).c_str());
		for (++pos; pos != m_route.routeList().cend(); pos++) {
			TRACE(_T("%s, %s, %d\n"), Route::LineName(pos->lineId).c_str(), Route::StationName(pos->stationId).c_str(), pos->flag>>31);
		}
		TRACE(_T("\n"));
	} else {
		GetDlgItem(IDC_BUTTON_BS)->EnableWindow(FALSE);		// Disnable [-] button
	}
#endif
	CRouteInputDlg dlg;
	if (IDOK == dlg.DoModal()) {
		parseAndSetupRoute(dlg.routeString);
	}
}


// 文字列で指定した経路を設定する
//
int Calps_mfcDlg::parseAndSetupRoute(LPCTSTR route_str)
{
	int rc;

	ResetContent();

	rc = m_route.setup_route(route_str);

	GetDlgItem(IDC_EDIT_START)->SetWindowText(Route::StationName(m_route.startStationId()).c_str());	// 発駅表示

	switch (rc) {
	case -200:
		AfxMessageBox(_T("駅名不正が含まれています"));
		break;
	case -300:
		AfxMessageBox(_T("線名不正が含まれています"));
		break;
	case -100:
		AfxMessageBox(_T("致命的エラー"));
		break;
	case -1:
		AfxMessageBox(_T("経路が重複しています"));
		break;
	case -2:
		AfxMessageBox(_T("不正な経路指定です"));
		break;
	case 0:
	case 1:
		/* success */
		break;
	default:
		AfxMessageBox(_T("不明なエラー"));
		break;
	}
	if (0 <= rc) {
		UpdateRouteList();
		GetDlgItem(IDC_LIST_LINESTATIONS)->EnableWindow(TRUE);	// 駅/路線 選択リスト選択可
		GetDlgItem(IDC_BUTTON_SEL)->EnableWindow(TRUE);			// [+] button
	} else {
		ResetContent();
	}
	return 0;
}

//	[結果を開く]
//
void Calps_mfcDlg::OnBnClickedButtonRsltopen()
{
	CString s;
	CFileDialog dlg(TRUE);
	HINSTANCE hInst =
	ShellExecute(NULL, _T("open"), _T("result.txt"), NULL, NULL, SW_SHOW);

	if (hInst <= (HINSTANCE)32) {
		s.Format(_T("結果記録ファイルのオープンに失敗しました. %d"), hInst);
		AfxMessageBox(s);
		
		if (IDYES == dlg.DoModal()) {
			ShellExecute(NULL, _T("open"), dlg.GetFileName(), NULL, NULL, SW_SHOW);
		}
	}
}


