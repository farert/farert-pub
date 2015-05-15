#pragma once


// CRouteInputDlg ダイアログ

class CRouteInputDlg : public CDialogEx
{
	DECLARE_DYNAMIC(CRouteInputDlg)

public:
	CRouteInputDlg(CWnd* pParent = NULL);   // 標準コンストラクター
	virtual ~CRouteInputDlg();

// ダイアログ データ
	enum { IDD = IDD_ROUTE_INPUT };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV サポート

	DECLARE_MESSAGE_MAP()
public:
//	CString routeString;
	CString routeString;
	virtual BOOL OnInitDialog();
	afx_msg void OnBnClickedButtonExplorer();
};
