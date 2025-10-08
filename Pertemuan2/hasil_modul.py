from pembagian import bagi
from perkalian import kali
from penjumlahan import tambah
from pengurangan import kurang

angka1 = int(input("Masukkan angka pertama: "))
angka2 = int(input("Masukkan angka kedua: "))

print("Hasil penjumlahan dari", angka1, "dan", angka2, "adalah", tambah(angka1, angka2))
print("Hasil pengurangan dari", angka1, "dan", angka2, "adalah", kurang(angka1, angka2))
print("Hasil perkalian dari", angka1, "dan", angka2, "adalah", kali(angka1, angka2))
print("Hasil pembagian dari", angka1, "dan", angka2, "adalah", bagi(angka1, angka2))