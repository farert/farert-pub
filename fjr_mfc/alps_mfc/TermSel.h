#pragma once



// CTermSel �_�C�A���O

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
class CTermSel : public CDialogEx
{
	DECLARE_DYNAMIC(CTermSel)

public:
	CTermSel(bool bTerm, CWnd* pParent = NULL);   // �W���R���X�g���N�^�[
	virtual ~CTermSel();

// �_�C�A���O �f�[�^
	enum { IDD = IDD_DIALOG_TERM_SEL };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV �T�|�[�g
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
