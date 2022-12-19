# CRUD Process
import os
import csv

csv_src = os.path.join(os.path.dirname(__file__), 'booksdata-final.csv').replace("\\", "/")
clrscr = lambda : os.system('cls' if os.name == 'nt' else 'clear')

mapper = lambda data, key: list(map(lambda x: (x[f'{key}']) if key != None else int(x), data))
summator = lambda l: float(l[0]) if len(l) == 1 else (l[0]) + summator(l[1:])
meanOf = lambda l: summator(l) / len(l)
medianOf = lambda l: sorted(l)[(len(sorted(l))//2)] if len(sorted(l)) % 2 == 1 else (sorted(l)[((len(sorted(l)))//2)-1]+sorted(l)[(len(sorted(l)))//2])/2
modeOf = lambda l: max(set(l), key = l.count)

class Chain:
    def __init__(self, data):
        self.data = data

    def __call__(self):
        return self.data

    def then(self, function):
        self.data = function(self.data)  
        return self

def Printer(data):
    print(f'''BookID [{data[0]}]
Judul         : {data[1]}
Pencipta      : {data[2]}
Rating        : {data[3]}
ISBN          : {data[4]}
Kode Bahasa   : {data[5]}
Review        : {data[6]}
Tanggal Terbit: {data[7]}
Penerbit      : {data[8]}
''')

def ShowStatistic():
    clrscr()
    with open(csv_src, newline='', encoding='utf-8') as data:
        reader = csv.DictReader(data)
        datas = [row for row in reader]

    print('Data Statistik Saat Ini')
    print('-----------------------')
    RevCount = Chain(map(lambda x: int(x), mapper(datas, 'Review'))).then(enumerate).then(list)
    Title = mapper(datas, 'Judul')
    Rating = list(map(lambda x: float(x), mapper(datas, 'Rating')))
    MaxRevCount = max(RevCount(), key=lambda x: x[1])
    Years = list(map(lambda x: int(x[6:]), mapper(datas, 'Tanggal Terbit')))

    print(f'Author terbanyak (Modus):, {modeOf(mapper(datas, "Penerbit"))}')
    print(f'Buku review terbanyak (Max):, {Title[MaxRevCount[0]]}, {MaxRevCount[1]}')
    print(f'Jumlah Author (Sum):, {len(set(mapper(datas, "Penerbit")))}')
    print(f'Jumlah Buku (Sum): {len(mapper(datas, "ID Buku"))}')
    print(f'Rata-rata rating (Mean): {round(meanOf(Rating), 2)}')
    print(f'Bahasa terbanyak (Modus): {modeOf(mapper(datas, "Kode Bahasa"))}')
    print(f'Median tahun terbit: {int(medianOf(Years))}')
    BackTo(Program)

def ShowBook():
    clrscr()
    with open(csv_src, newline='', encoding='utf-8') as data:
        # books = [row for row in csv.reader(data)]
        books = list(csv.reader(data))

    if (len(books) > 0):
        for data in books[1:]:
            Printer(data)
    else:
        print('Tidak ada data...')
    BackTo(Program)

def InsertBook():
    clrscr()
    with open(csv_src, newline='', encoding='utf-8') as data:
        # books = [row for row in csv.reader(data)]
        books = list(csv.reader(data))

    with open(csv_src, mode='a', newline='') as data:
        fieldnames = books[0]
        writer = csv.DictWriter(data, fieldnames=fieldnames)
        newdata = {}
        for i in fieldnames:
            newdata[f'{i}'] = input(f'Masukkan {i} : ')
        writer.writerow(newdata)
        print('Berhasil disimpan!')
    BackTo(Program)

def ModifyBook(n=None):
    clrscr()
    with open(csv_src, 'r', newline='', encoding='utf-8') as data:
        books = list(csv.reader(data))
        # books = [row for row in csv.reader(data)]
    if n is None:
        bookid = input('[ID Buku >] ')
    else:
        bookid = n

    # found = False
    # for data in books:
    #     if data[0] == bookid:
    #         row = books.index(data)
    #         found = True
    # print(found)
    data = list(map(lambda x: x[0], books))
    found = True if bookid in data else False
    row = data.index(bookid)
    if found:
        Printer(books[row])

        ask = input('Ubah? [y/n] ')
        if ask == 'y':
            clrscr()
            judul = input('Judul : ')
            pencipta = input('Pencipta : ')
            rating = input('Rating : ')
            isbn = input('ISBN : ')
            kodebahasa = input('Kode Bahasa : ')
            review = input('Review : ')
            tanggal = input('Tanggal Terbit: ')
            penerbit = input('Penerbit : ')

            orig = books[row]
            mod = [bookid, judul, pencipta, rating, isbn, kodebahasa, review, tanggal, penerbit]
            moddata = list(map(lambda x, y: y if x == '-' else x, mod, orig))
            newmod = list(map(lambda x: moddata if x[0] == bookid else x, books))

            with open(csv_src, 'w', newline='', encoding='utf-8') as data:
                writer = csv.writer(data, delimiter=",")
                for i in newmod:
                    writer.writerow(i)
            if mod.count("-") == len(mod)-1:
                print('Tidak ada data yang dirubah...')
            else:
                print('Data buku berhasil dirubah!')
            BackTo(Program)

        elif ask == 'n':
            BackTo(Program)
    else:
        print('Data tidak ditemukan, Ulangi...')
        BackTo(ModifyBook)

def DeleteBook():
    clrscr()
    with open(csv_src, 'r', newline='', encoding='utf-8') as data:
        # books = [row for row in csv.reader(data)]
        books = list(csv.reader(data))
    bookid = input('[ID Buku >] ')
    
    data = list(map(lambda x: x[0], books))
    found = True if bookid in data else False
    row = data.index(bookid)
    Printer(books[row])
    if found:
        ask = input('Yakin? [y/n] ')
        if ask == 'y':

            newdata = list(filter(lambda x: True if x[0] != bookid else False, books))

            with open(csv_src, 'w', newline='', encoding='utf-8') as data:
                writer = csv.writer(data, delimiter=",")
                for i in newdata:
                    writer.writerow(i)
            BackTo(Program)
        elif ask == 'n':
            BackTo(Program)
    else:
        print('Data tidak ditemukan, Ulangi...')
        BackTo(DeleteBook)

def SearchBook():
    clrscr()
    with open(csv_src, newline='', encoding='utf-8') as data:
        books = list(csv.reader(data))
        # books = [row for row in csv.reader(data)]
    bookid = input('[ID Buku >] ')
    # found = False
    # for data in books:
    #     if data[0] == bookid:
    #         found = True
    data = list(map(lambda x: x[0], books))
    found = True if bookid in data else False
    row = data.index(bookid)
    if found:
        datas = list(filter(lambda x: True if x[0] == bookid else False, books))[0]
        Printer(datas)
        BackTo(Program)
    else:
        BackTo(SearchBook)

def Program():
    clrscr()
    print('Halo selamat datang di Admin Perpustakaan...')
    print('''
1. Lihat Statistik Buku
2. Masukkan Data Buku
3. Lihat Semua Buku
4. Lihat/Cari Buku
5. Ubah Data Buku
6. Hapus Data Buku
0. Keluar
''')
    opt = input("[>] ")
    if not 0 <= int(opt) <= 6:
        BackTo(Program)
    MainMethods = [ShowStatistic, InsertBook, ShowBook, SearchBook, ModifyBook, DeleteBook, exit]
    Call = MainMethods[int(opt)-1]
    Call()

def BackTo(func):
    print()
    input("[Enter untuk kembali >]")
    func()

if __name__ == "__main__":
    while True:
        Program()