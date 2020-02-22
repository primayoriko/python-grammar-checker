# python-grammar-checker-uwuw

## The Godfather
--------------------------------------
Cara penggunaan :

1. Pastikan grammar yang dipakai dalam bentuk cnf, dan diberi nama cnf.txt
2. Format grammar CNF :
   [Non-terminal] -> [Prod1] | [Prod2] | dst.
3. Buat file python yang ingin dicompile dan save.
4. Jalankan program di terminal dengan format :
   python main.py [nama file yang ingin diuji termasuk dengan extensinya]
5. Jika file valid muncul tulisan 'ACCEPTED', namun jika tidak muncul
   pesan kesalahan syntax error beserta dengan baris error