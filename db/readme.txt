2013-8-17

How-To-Makeing-db.txt	データベース作成手順書(さらにつづきの詳細はmkdb.batを読むべし)

jr.db			データベースファイル

jrdb.txt		データベース作成元データ

jrdb.xlsx		データベース作成元データの元データ
			jrdb.xlsx ->(手作業でコピペ)-> jrdb.txt ->(mkdb.bat)-> jr.db
			となる。本来、pythonでやりたいところだが、OS依存なので避けている

misc\			昔のファイル(もう使わないゴミ)

mkdb.bat		データベース作成スクリプト(jrdb.txtからjr.dbを生成・作成する)

node_list.txt		データベース作成スクリプトが作成した中間ファイル(使用することはない)

scripts\		データベース操作関連スクリプトやテストコードなどを格納
			実行するときは、現ディレクトリをカレントとして、
			> python scripts\xxx.py
			として実行する（scripts\内をカレントとして実行してもDBが読み込めないので実行失敗する)


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

"""
以上
