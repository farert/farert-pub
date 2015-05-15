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

// alps_mfc.cpp : アプリケーションのクラス動作を定義します。
//

#include "stdafx.h"
#include "alps_mfc.h"
#include "alps_mfcDlg.h"

/*!	@file alps_mfc.cpp application main.
 *	Copyright(c) sutezo9@me.com 2012.
 */

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

extern "C" int rd(unsigned char* buffer, unsigned enclen);
static bool res2tmpfile(LPCTSTR destFile, LPBYTE p_src, DWORD dwSize);

// Calps_mfcApp

BEGIN_MESSAGE_MAP(Calps_mfcApp, CWinApp)
	ON_COMMAND(ID_HELP, &CWinApp::OnHelp)
END_MESSAGE_MAP()


int g_tax;	// global

// Calps_mfcApp コンストラクション

Calps_mfcApp::Calps_mfcApp()
{
	// 再起動マネージャーをサポートします
	m_dwRestartManagerSupportFlags = AFX_RESTART_MANAGER_SUPPORT_RESTART;

	// TODO: この位置に構築用コードを追加してください。
	// ここに InitInstance 中の重要な初期化処理をすべて記述してください。
}


// 唯一の Calps_mfcApp オブジェクトです。

Calps_mfcApp theApp;


// Calps_mfcApp 初期化

BOOL Calps_mfcApp::InitInstance()
{
	_tsetlocale(LC_ALL, _T(""));	// tstring

	// アプリケーション マニフェストが visual スタイルを有効にするために、
	// ComCtl32.dll Version 6 以降の使用を指定する場合は、
	// Windows XP に InitCommonControlsEx() が必要です。さもなければ、ウィンドウ作成はすべて失敗します。
	INITCOMMONCONTROLSEX InitCtrls;
	InitCtrls.dwSize = sizeof(InitCtrls);
	// アプリケーションで使用するすべてのコモン コントロール クラスを含めるには、
	// これを設定します。
	InitCtrls.dwICC = ICC_WIN95_CLASSES;
	InitCommonControlsEx(&InitCtrls);

	CWinApp::InitInstance();


	LPTSTR opt = _tcsstr(m_lpCmdLine, _T("-tax"));
	if (NULL != opt) {
		g_tax = _ttoi(opt + 4);
		if (g_tax <= 0) {
			g_tax = DEFAULT_TAX;
		}
	} else {
		g_tax = DEFAULT_TAX;	/* default */
	}

	AfxEnableControlContainer();

	// ダイアログにシェル ツリー ビューまたはシェル リスト ビュー コントロールが
	// 含まれている場合にシェル マネージャーを作成します。
	//CShellManager *pShellManager = new CShellManager;

	// 標準初期化
	// これらの機能を使わずに最終的な実行可能ファイルの
	// サイズを縮小したい場合は、以下から不要な初期化
	// ルーチンを削除してください。
	// 設定が格納されているレジストリ キーを変更します。
	// TODO: 会社名または組織名などの適切な文字列に
	// この文字列を変更してください。
	// SetRegistryKey(_T("アプリケーション ウィザードで生成されたローカル アプリケーション"));

	setlocale(LC_ALL, "");
	
	do {
		HRSRC hRc = FindResource(m_hInstance, MAKEINTRESOURCE(IDR_DB), _T("DB"));
		if (hRc) {
			HGLOBAL hGlbl = LoadResource(m_hInstance, hRc);
			if (hGlbl) {
				DWORD dwDbEncSize = SizeofResource(m_hInstance, hRc);
				if (dwDbEncSize) {
					LPVOID p = LockResource(hGlbl);
					if (p) {
						TCHAR impdbfn[MAX_PATH];
						
							// restore(decrypt)
						dwDbEncSize = rd((unsigned char*)p, dwDbEncSize);
						
						GetTempPath(MAX_PATH, impdbfn);
						GetTempFileName(impdbfn, _T("@~~"), 0, impdbfn);
						res2tmpfile(impdbfn, (LPBYTE)p, dwDbEncSize);
						
						bool b = DBS::getInstance()->open(impdbfn);
						DeleteFile(impdbfn);
						if (b) {
							break;	/* success */
						}
					}
				}
			}
		}

		AfxMessageBox(_T("データが開けません."));
		return FALSE;

	} while (0);
	

	Calps_mfcDlg dlg;
	m_pMainWnd = &dlg;
	INT_PTR nResponse = dlg.DoModal();
	if (nResponse == IDOK)
	{
		// TODO: ダイアログが <OK> で消された時のコードを
		//  記述してください。
	}
	else if (nResponse == IDCANCEL)
	{
		// TODO: ダイアログが <キャンセル> で消された時のコードを
		//  記述してください。
	}

	// 上で作成されたシェル マネージャーを削除します。
	//if (pShellManager != NULL)
	//{
	//	delete pShellManager;
	//}

	// ダイアログは閉じられました。アプリケーションのメッセージ ポンプを開始しないで
	//  アプリケーションを終了するために FALSE を返してください。
	return FALSE;
}

// create tempolary file for sqlite3 database engine.
//
static bool res2tmpfile(LPCTSTR destFile, LPBYTE p_src, DWORD dwSize)
{
	HANDLE hFile;
	DWORD dwWritten;

	hFile = CreateFile(destFile, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_TEMPORARY, NULL);
	if (hFile == INVALID_HANDLE_VALUE) {
		TRACE("Can't create file: %d\n", GetLastError());
		return false;
	}
	dwWritten = 0;
	if (!WriteFile(hFile, p_src, dwSize, &dwWritten, NULL) || dwSize != dwWritten) {
		TRACE("Can't write file: %d(write size=%u)\n", GetLastError(), dwWritten);
		return false;
	}
	CloseHandle(hFile);
	return true;
}


