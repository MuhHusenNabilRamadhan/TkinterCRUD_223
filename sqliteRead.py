import tkinter as tk
from tkinter import messagebox
import sqlite3

# Membuat koneksi ke database SQLite
conn = sqlite3.connect('nilai_siswa.db')
c = conn.cursor()

# Membuat table nilai_siswa jika belum ada
c.execute('''
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_siswa TEXT,
    biologi INTEGER,
    fisika INTEGER,
    inggris INTEGER,
    prediksi_fakultas TEXT
)
''')
conn.commit()

def submit_nilai():
    try:
        nama = entry_nama.get()
        biologi = int(entry_biologi.get())
        fisika = int(entry_fisika.get())
        inggris = int(entry_inggris.get())

        # Validasi input nama tidak kosong
        if not nama:
            messagebox.showerror("Error", "Nama siswa harus diisi")
            return

        # Menentukan prediksi fakultas berdasarkan nilai tertinggi
        if biologi >= fisika and biologi >= inggris:
            prediksi = "Kedokteran"
        elif fisika >= biologi and fisika >= inggris:
            prediksi = "Teknik"
        else:
            prediksi = "Bahasa"

        # Menyimpan data ke database
        c.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
        ''', (nama, biologi, fisika, inggris, prediksi))
        conn.commit()

        # Menampilkan pesan sukses
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")

        # Membersihkan entry setelah submit
        entry_nama.delete(0, tk.END)
        entry_biologi.delete(0, tk.END)
        entry_fisika.delete(0, tk.END)
        entry_inggris.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Nilai biologi, fisika, dan inggris harus berupa angka")

# Membuat window utama tkinter
root = tk.Tk()
root.title("Prediksi Fakultas Berdasarkan Nilai")

# Label dan Entry untuk nama siswa
tk.Label(root, text="Nama Siswa:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
entry_nama = tk.Entry(root)
entry_nama.grid(row=0, column=1, padx=10, pady=5)

# Label dan Entry untuk nilai Biologi
tk.Label(root, text="Nilai Biologi:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
entry_biologi = tk.Entry(root)
entry_biologi.grid(row=1, column=1, padx=10, pady=5)

# Label dan Entry untuk nilai Fisika
tk.Label(root, text="Nilai Fisika:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
entry_fisika = tk.Entry(root)
entry_fisika.grid(row=2, column=1, padx=10, pady=5)

# Label dan Entry untuk nilai Inggris
tk.Label(root, text="Nilai Inggris:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
entry_inggris = tk.Entry(root)
entry_inggris.grid(row=3, column=1, padx=10, pady=5)

# Button submit untuk menyimpan nilai dan prediksi
btn_submit = tk.Button(root, text="Submit Nilai", command=submit_nilai)
btn_submit.grid(row=4, column=0, columnspan=2, pady=15)

root.mainloop()

# Menutup koneksi saat program selesai (opsional karena tkinter loop)
conn.close()
