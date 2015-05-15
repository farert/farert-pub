
// alps_mfcDlg.h : �w�b�_�[ �t�@�C��
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

���̃v���O�����̓t���[�\�t�g�E�F�A�ł��B���Ȃ��͂�����A�t���[�\�t�g�E�F
�A���c�ɂ���Ĕ��s���ꂽ GNU ��ʌ��O���p�����_��(�o�[�W����3���A��
�]�ɂ���Ă͂���ȍ~�̃o�[�W�����̂����ǂꂩ)�̒�߂�����̉��ōĔЕz
�܂��͉��ς��邱�Ƃ��ł��܂��B

���̃v���O�����͗L�p�ł��邱�Ƃ�����ĔЕz����܂����A*�S���̖��ۏ�* 
�ł��B���Ɖ\���̕ۏ؂����̖ړI�ւ̓K�����́A���O�Ɏ����ꂽ���̂���
�ߑS�����݂��܂���B�ڂ�����GNU ��ʌ��O���p�����_�񏑂��������������B
 
���Ȃ��͂��̃v���O�����Ƌ��ɁAGNU ��ʌ��O���p�����_�񏑂̕��������ꕔ
�󂯎�����͂��ł��B�����󂯎���Ă��Ȃ���΁A�t���[�\�t�g�E�F�A���c��
�Ő������Ă�������

#endif

#pragma once

#include "../lib/alps/alpdb.h"



// Calps_mfcDlg �_�C�A���O
class Calps_mfcDlg : public CDialogEx
{
// �R���X�g���N�V����
public:
	Calps_mfcDlg(CWnd* pParent = NULL);	// �W���R���X�g���N�^�[

// �_�C�A���O �f�[�^
	enum { IDD = IDD_ALPS_MFC_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV �T�|�[�g


// ����
protected:
	HICON m_hIcon;

	// �������ꂽ�A���b�Z�[�W���蓖�Ċ֐�
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

