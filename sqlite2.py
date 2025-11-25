import sqlite3
from tkinter import *
from tkinter import messagebox

# Database setup
conn = sqlite3.connect('prodiScore.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        biologi INTEGER,
        fisika INTEGER,
        inggris INTEGER,
        prediksi TEXT
    )
''')
conn.commit()

# Fungsi prediksi prodi
def get_prediksi(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Belum bisa diprediksi"

# Submit data
def submit_data():
    nama = entry_nama.get()
    try:
        biologi = int(entry_biologi.get())
        fisika = int(entry_fisika.get())
        inggris = int(entry_inggris.get())
    except:
        messagebox.showerror("Error", "Nilai harus berupa angka!")
        return

    if not nama:
        messagebox.showerror("Error", "Nama tidak boleh kosong!")
        return

    prediksi = get_prediksi(biologi, fisika, inggris)
    cursor.execute("INSERT INTO scores (nama, biologi, fisika, inggris, prediksi) VALUES (?, ?, ?, ?, ?)",
                   (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    messagebox.showinfo("Sukses", f"Data disimpan! Prediksi Prodi: {prediksi}")
    load_data()
    clear_input()

# Search data
def search_data():
    search_id = entry_search.get()
    if not search_id:
        messagebox.showerror("Error", "Masukkan ID untuk mencari!")
        return

    cursor.execute("SELECT * FROM scores WHERE id=?", (search_id,))
    row = cursor.fetchone()
    if row:
        entry_nama.delete(0, END)
        entry_nama.insert(0, row[1])
        entry_biologi.delete(0, END)
        entry_biologi.insert(0, row[2])
        entry_fisika.delete(0, END)
        entry_fisika.insert(0, row[3])
        entry_inggris.delete(0, END)
        entry_inggris.insert(0, row[4])
        label_id.config(text=row[0])
    else:
        messagebox.showerror("Error", "ID tidak ditemukan!")

# Update data
def update_data():
    record_id = label_id.cget("text")
    if record_id == "-":
        messagebox.showerror("Error", "ID tidak ditemukan!")
        return

    nama = entry_nama.get()
    try:
        biologi = int(entry_biologi.get())
        fisika = int(entry_fisika.get())
        inggris = int(entry_inggris.get())
    except:
        messagebox.showerror("Error", "Nilai harus berupa angka!")
        return

    prediksi = get_prediksi(biologi, fisika, inggris)
    cursor.execute("""
        UPDATE scores
        SET nama=?, biologi=?, fisika=?, inggris=?, prediksi=?
        WHERE id=?
    """, (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
    load_data()
    clear_input()

# Delete data
def delete_data():
    record_id = label_id.cget("text")
    if record_id == "-":
        messagebox.showerror("Error", "ID tidak ditemukan!")
        return

    cursor.execute("DELETE FROM scores WHERE id=?", (record_id,))
    conn.commit()
    messagebox.showinfo("Sukses", "Data berhasil dihapus!")
    load_data()
    clear_input()

# Load tabel list
def load_data():
    listbox.delete(0, END)
    cursor.execute("SELECT * FROM scores")
    rows = cursor.fetchall()

    # Lebar tiap kolom (jumlah karakter)
    col_id   = 10
    col_nama = 18
    col_bio  = 12
    col_fis  = 12
    col_eng  = 12
    col_pred = 20

    # Header tabel
    header = (
        f"{'ID'.ljust(col_id)}"
        f"{'Nama'.ljust(col_nama)}"
        f"{'Biologi'.ljust(col_bio)}"
        f"{'Fisika'.ljust(col_fis)}"
        f"{'English'.ljust(col_eng)}"
        f"{'Prediksi'.ljust(col_pred)}"
    )
    listbox.insert(END, header)
    listbox.insert(END, "-" * (col_id + col_nama + col_bio + col_fis + col_eng + col_pred))

    # Isi data
    for row in rows:
        line = (
            f"{str(row[0]).ljust(col_id)}"
            f"{row[1].ljust(col_nama)}"
            f"{str(row[2]).ljust(col_bio)}"
            f"{str(row[3]).ljust(col_fis)}"
            f"{str(row[4]).ljust(col_eng)}"
            f"{row[5].ljust(col_pred)}"
        )
        listbox.insert(END, line)

# Clear input
def clear_input():
    entry_nama.delete(0, END)
    entry_biologi.delete(0, END)
    entry_fisika.delete(0, END)
    entry_inggris.delete(0, END)
    entry_search.delete(0, END)
    label_id.config(text="-")

# UI SETUP
root = Tk()
root.title("Input Nilai Siswa")

Label(root, text="Nama Siswa").grid(row=0, column=0)
entry_nama = Entry(root)
entry_nama.grid(row=0, column=1)

Label(root, text="Nilai Biologi").grid(row=1, column=0)
entry_biologi = Entry(root)
entry_biologi.grid(row=1, column=1)

Label(root, text="Nilai Fisika").grid(row=2, column=0)
entry_fisika = Entry(root)
entry_fisika.grid(row=2, column=1)

Label(root, text="Nilai English").grid(row=3, column=0)
entry_inggris = Entry(root)
entry_inggris.grid(row=3, column=1)

Button(root, text="Submit", width=15, command=submit_data).grid(row=4, column=0, pady=5)
Button(root, text="Update", width=15, command=update_data).grid(row=4, column=1)
Button(root, text="Delete", width=15, command=delete_data).grid(row=4, column=2)

Label(root, text="Cari berdasarkan ID:").grid(row=5, column=0)
entry_search = Entry(root)
entry_search.grid(row=5, column=1)
Button(root, text="Search", command=search_data).grid(row=5, column=2)

Label(root, text="ID Data Aktif:").grid(row=6, column=0)
label_id = Label(root, text="-", fg="red")
label_id.grid(row=6, column=1)

listbox = Listbox(root, width=90)
listbox.grid(row=7, column=0, columnspan=3, padx=5, pady=10)

load_data()
root.mainloop()
conn.close()
