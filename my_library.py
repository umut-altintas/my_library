"""

-Kitap takip uygulaması-

"""

import datetime as dt
import time
import sqlite3
import sys
import os
from typing import Literal

"""CONST"""
#Yazdırma düzeni ve görüntüsü için eklendi.
UNDERLINE = "\033[4m"
RESET = "\033[0m"
HEADER_AUTHOR_ID = 15
HEADER_BOOK_ID = 15
HEADER_AUTHOR_NAME = 30
HEADER_BOOK_NAME = 50
HEADER_BOOK_SCORE = 15
HEADER_BOOK_ADDED_DATE = 35
HEADER_BOOK_FINISHED_DATE = 35
HEADER_BOOK_READING_TIME = 15
HEADER_AUTHOR_SCORE = 20

"""Arrays"""

msg_header = {"author_id":f"{"Yazar No.:":<{HEADER_AUTHOR_ID}}",
             "book_id":f"{"Kitap No.:":<15}",
             "author_name":f"{"Yazar adı:":<30}",
             "book_name":f"{"Kitap adı:":<50}",
             "book_score":f"{"Kitabın puanı:":<15}",
             "book_added_date":f"{"Kitabın eklenme tarihi:":<35}",
             "book_finished_date":f"{"Kitabın bitirilme tarihi:":<35}",
             "book_reading_time":f"{"Kitabın bitirilme süresi":<15}",
             "author_score":f"{"Yazar puanı:":<20}"}

msg_header_keys = Literal["author_id",
                  "book_id",
                  "author_name",
                "book_name",
                "book_score",
                "book_added_date",
                "book_finished_date",
                "book_reading_time",
                "author_score"] #Header fonksiyonunda içeri değer girerken verilere erişme kolaylığı için eklendi.

msg_author_score_types = {"very_liked":"Çok beğenilen yazar",
                          "liked":"Beğenilen yazar",
                          "average":"Vasat yazar",
                          "disliked":"Kötü yazar"}

msg_user_output = {"invalid_input":"Geçersiz tuşlama yaptınız!",
            "invalid_datatype":"Girdiğiniz veri tipi yanlış!",
            "successfully_saved":"başarıyla kaydedildi!",
            "invalid_author_id":"Girdiğiniz numara bir yazara ait değil!",
            "successfully_removed":"başarıyla kaldırıldı!",
            "invalid_book_id":"Girdiğiniz numara bir kitaba ait değil!",
            "invalid_format":"Geçersiz formatta giriş yaptınız!",
            "finished_book_congrats":"kitabını bitirdiniz. Tebrikler!",
            "invalid_rate":"Belirtilen aralıkta puanlama yapınız!",
            "score_to_book":" kitabına puanınız: ",
            "successfully_saved_book_summary":"Kitap özeti başarıyla kaydedildi!",
            "successfully_deleted_book":"listenizden başarıyla kaldırıldı!",
            "successfully_saved_book":"listenize başarıyla kaydedildi!",
            "does_not_exist_book_score":"Henüz bir kitap puanlamadınız!",
            "does_not_exist_book_summary":"Henüz bir kitap özeti eklemediniz!",
            "have_been_added_author":"Bu yazar zaten eklenmiş!",
            "have_been_added_book":"Bu kitap zaten eklenmiş!",
            "does_not_exist_unrated_book":"Puanlanmamış bir kitap bulunmuyor!",
            "does_not_exist_unfinished_book":"Bitirmediğiniz bir kitap bulunmuyor!",
            "does_not_exist_books":"Listenizde hiç kitap bulunmuyor!"}

msg_user_input = {"author_name":"Lütfen yazarın ismini giriniz: ",
                  "author_id":"Lütfen yazarın numarasını giriniz: ",
                  "no_author_in_table":"Listenizde hiç yazar bulunmuyor eklemek ister misiniz?(y/n): ",
                  "to_main_menu":"Ana menüye dönmek için 'q' tuşlayınız: ",
                  "book_name":"Kitap adını giriniz: ",
                  "author_id_book_id_format":"İşleminiz için (yazar numarası, kitap numarası) formatında giriş yapınız: ",
                  "no_book_in_table":"Kütüphanenizde hiç kitap bulunmuyor! Eklemek ister misiniz?(y/n): ",
                  "book_id":"Lütfen kitap numarasını giriniz: ",
                  "rating":"0-100 arası tamsayı bir puan giriniz: ",
                  "menu_choice":"Seçim yapmak istediğiniz menüyü tuşlayınız: ",
                  "exit_question":"Çıkmak istediğinize emin misiniz?(y/n): ",
                  "book_summary":"Kitap özetini giriniz: "}

msg_main_menu = {"author_options":"1. Yazar işlemleri",
             "book_options":"2. Kitap işlemleri",
             "exit":"3. Çıkış yap"}

msg_author_options = {"add_author":"1. Yazar ekle",
                "delete_author":"2. Yazar sil",
                "show_author":"3. Yazarları görüntüle",
                "main_menu":"0. Ana menüye dönüş"}

msg_book_options = {"add_book":"1. Kitap ekle",
                "delete_book":"2. Kitap sil",
                "show_books":"3. Kitapları görüntüle",
                "finished_books":"4. Bitirilen kitap işlemleri",
                "main_menu":"0. Ana menüye dönüş"}

msg_finished_books = {"add_finished_book":"1. Bitirilen kitap ekle",
                  "add_book_score":"2. Kitabı puanla",
                  "add_book_summary":"3. Kitap özeti ekle",
                  "show_book_summary":"4. Kitap özeti görüntüle",
                  "show_book_scores":"5. Kitap puanlarını görüntüle",
                  "main_menu":"0. Ana menüye dönüş"}

"""SQlite"""

con = sqlite3.connect("my_lib.db")
con.execute("PRAGMA foreign_keys = ON")
cur = con.cursor()

def db_tables() -> None:
    db_table_author = """--sql
        CREATE TABLE IF NOT EXISTS authors(
            author_id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_name TEXT UNIQUE,
            author_score TEXT DEFAULT 'Boş'
        )
    """
    db_table_books = """--sql
        CREATE TABLE IF NOT EXISTS books(
            author_id INTEGER NOT NULL,
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_name TEXT UNIQUE,
            book_added_date TEXT,
            FOREIGN KEY(author_id) REFERENCES authors(author_id) ON DELETE CASCADE
        )
    """
    db_table_finished_books = """--sql
        CREATE TABLE IF NOT EXISTS finished_books(
            book_id INTEGER PRIMARY KEY,
            book_read_date TEXT,
            book_reading_time TEXT,
            FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
        )
    """
    db_table_book_scores = """--sql
        CREATE TABLE IF NOT EXISTS book_scores(
            book_id INTEGER PRIMARY KEY,
            book_score INTEGER,
            book_summary TEXT,
            FOREIGN KEY (book_id) REFERENCES finished_books(book_id) ON DELETE CASCADE
        )
    """
    cur.execute(db_table_author)
    con.commit()
    cur.execute(db_table_books)
    con.commit()
    cur.execute(db_table_finished_books)
    con.commit()
    cur.execute(db_table_book_scores)
    con.commit()


QUERIES = {"GET_AUTHORS":"SELECT * FROM authors ORDER BY author_id",
           "COUNT_AUTHORS":"SELECT COUNT(*) FROM authors",
           "COUNT_BOOKS":"SELECT COUNT(*) FROM books",
           "COUNT_FINISHED_BOOKS":"SELECT COUNT(*) FROM finished_books",
           "COUNT_BOOK_SCORES":"SELECT COUNT(*) FROM book_scores",
           "GET_BOOKS":"SELECT * FROM books ORDER BY author_id",
           "GET_AUTHOR_BY_ID":"SELECT author_name FROM authors WHERE author_id = ?",
           "GET_BOOK_NAME_BY_ID":"SELECT book_name FROM books WHERE book_id = ?",
           "GET_BOOK_READ_DATE":"SELECT book_added_date FROM books where book_id = ?",
           "GET_FINISHED_BOOKS":"SELECT * FROM finished_books",
           "GET_BOOK_SCORE_BY_ID":"SELECT book_score FROM book_scores WHERE book_id = ?",
           "GET_UNFINISHED_BOOKS":"SELECT book_id, book_name FROM books WHERE NOT EXISTS(SELECT 1 FROM finished_books WHERE finished_books.book_id = books.book_id)",
           "GET_UNRATED_BOOKS":"SELECT fb.book_id, b.book_name, fb.book_read_date, fb.book_reading_time FROM finished_books AS fb JOIN books AS b ON fb.book_id = b.book_id WHERE NOT EXISTS(SELECT 1 FROM book_scores AS bs WHERE bs.book_id = fb.book_id)",
           "GET_BOOKS_MISSING_SUMMARY":"SELECT bs.book_id, b.book_name FROM book_scores AS bs JOIN books AS b ON bs.book_id = b.book_id WHERE (book_summary IS NULL OR bs.book_summary = '')",
           "GET_BOOKS_MISSING_SUMMARY_BY_ID":"SELECT book_id FROM book_scores WHERE book_id = ? AND (book_summary IS NULL OR book_summary = '')",
           "GET_BOOK_SUMMARY_BY_ID":"SELECT book_summary FROM book_scores WHERE book_id = ?",
           "GET_BOOK_SCORES":"SELECT bs.book_id, b.book_name, bs.book_score FROM book_scores AS bs JOIN books AS b ON bs.book_id = b.book_id",
           "GET_BOOKS_THAT_HAVE_SUMMARY":"SELECT bs.book_id, b.book_name FROM book_scores AS bs JOIN books AS b ON bs.book_id = b.book_id WHERE(bs.book_summary IS NOT NULL)",
           "GET_BOOK_SCORE_BY_ID":"SELECT book_score FROM book_scores WHERE book_id = ?",
           "GET_AUTHOR_ID_BY_BOOK_ID":"SELECT author_id FROM books WHERE book_id = ?",
           "GET_ALL_BOOK_SCORES_BY_AUTHOR_ID": "SELECT bs.book_score FROM book_scores bs INNER JOIN books b ON bs.book_id = b.book_id WHERE b.author_id = ?"}

VALUES = {"INSERT_AUTHOR":"INSERT INTO authors(author_name) VALUES(?)",
          "INSERT_BOOK":"INSERT INTO books(author_id, book_name, book_added_date) VALUES(?,?,?)",
          "INSERT_FINISHED_BOOK":"INSERT INTO finished_books VALUES(?,?,?)",
          "INSERT_BOOK_SCORE":"INSERT INTO book_scores(book_id, book_score) VALUES(?,?)"}

UPDATE = {"UPDATE_BOOK_SUMMARY":"UPDATE book_scores SET book_summary = ? WHERE book_id = ?",
          "UPDATE_AUTHOR_SCORE":"UPDATE authors SET author_score = ? WHERE author_id = ?"}

DELETE = {"DELETE_AUTHOR":"DELETE FROM authors WHERE author_id = ?",
          "DELETE_BOOK":"DELETE FROM books WHERE author_id = ? AND book_id = ?"}


"""os library"""

def clear_screen() -> None:
    # os.name 'nt' ise bilgisayar Windows'tur, değilse macOS/Linux'tur.
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def start_and_clear(function_name) -> None:
    clear_screen()
    function_name()

"""Functions for authors"""

def add_author() -> None:
    user_author_input = input(msg_user_input["author_name"]).strip().title()
    if any(char.isdigit() for char in user_author_input):
        popup(msg_user_output["invalid_datatype"])
    else:
        try:
            cur.execute(VALUES["INSERT_AUTHOR"], [user_author_input])
            con.commit()
            popup(f"{user_author_input} {msg_user_output['successfully_saved']}")
        except:
            popup(msg_user_output["have_been_added_author"])

def delete_author() -> None:
    cur.execute(QUERIES["GET_AUTHORS"])
    header('author_id','author_name')
    for i in cur.fetchall():
        print(f"{i[0]:<{HEADER_AUTHOR_ID}}{i[1]:<{HEADER_AUTHOR_NAME}}")
    delete_author = input(f"\n{msg_user_input["author_id"]}").strip()

    cur.execute(QUERIES["GET_AUTHOR_BY_ID"], [delete_author])
    temp_deleted_author = cur.fetchone()
    cur.execute(DELETE["DELETE_AUTHOR"],[delete_author])
    con.commit()
    if cur.rowcount > 0:
        popup(f"{temp_deleted_author} {msg_user_output['successfully_removed']}")
    else:
        popup(msg_user_output["invalid_author_id"])

def show_authors() -> None:
    cur.execute(QUERIES["COUNT_AUTHORS"])
    if cur.fetchone()[0] == 0:
        temp_choice = input(msg_user_input["no_author_in_table"]).strip().lower()
        if temp_choice == 'y':
            start_and_clear(add_author)
        elif temp_choice == 'n':
            pass
        else:
            popup(f"{msg_user_output['invalid_input']}")
    else:
        cur.execute(QUERIES["GET_AUTHORS"])
        header('author_id','author_name','author_score')
        for i in cur.fetchall():
            print(f"{i[0]:<{HEADER_AUTHOR_ID}}{i[1]:<{HEADER_AUTHOR_NAME}}{i[2]:<{HEADER_AUTHOR_SCORE}}")
        temp_choice = input(f"\n{msg_user_input["to_main_menu"]}").strip().lower()
        if temp_choice == 'q':
            pass
        else:
            popup(f"{msg_user_output['invalid_input']}")
        
"""Functions for books"""

def add_book() -> None:
    cur.execute(QUERIES["GET_AUTHORS"])
    header('author_id','author_name')
    for i in cur.fetchall():
        print(f"{i[0]:<{HEADER_AUTHOR_ID}}{i[1]:<{HEADER_AUTHOR_NAME}}")
    user_author_input = input(f"\n{msg_user_input["to_main_menu"]}\n{msg_user_input['author_id']}").strip().lower()
    todays_date = dt.datetime.now().isoformat()[:19]
    if user_author_input == 'q':
        return
    cur.execute(QUERIES["GET_AUTHOR_BY_ID"], [user_author_input])
    check_id = cur.fetchone()
    if check_id == None:
        popup(msg_user_output["invalid_author_id"])
    else:
        try:
            user_book_input = input(msg_user_input["book_name"]).strip().title()
            cur.execute(VALUES["INSERT_BOOK"], [user_author_input, user_book_input, todays_date])
            con.commit()
            popup(f"{user_book_input}, {msg_user_output['successfully_saved_book']}")
        except:
            popup(msg_user_output["have_been_added_book"])

def delete_book() -> None:
    cur.execute(QUERIES["GET_BOOKS"])
    books = cur.fetchall()
    if len(books)==0:
        popup(msg_user_output['does_not_exist_books'])
    else:
        header('author_id','book_id','book_name','book_added_date')
        for i in books:
            print(f"{i[0]:<{HEADER_AUTHOR_ID}}{i[1]:<{HEADER_BOOK_ID}}{i[2]:<{HEADER_BOOK_NAME}}{i[3]:<{HEADER_BOOK_ADDED_DATE}}")
        try:
            user_id_input = input(f"\n{msg_user_input['to_main_menu']}\n{msg_user_input['author_id_book_id_format']}").strip()
            if user_id_input == 'q':
                return
            else:
                temp_list = user_id_input.split(",")
                splited_input = [item.strip() for item in temp_list]
                author_id = splited_input[0]
                book_id = splited_input[1]
                cur.execute(QUERIES["GET_AUTHOR_BY_ID"], [author_id])
                check_author = cur.fetchone()
                cur.execute(QUERIES["GET_BOOK_NAME_BY_ID"], [book_id])
                check_book = cur.fetchone()
                if check_author == None:
                    popup(msg_user_output["invalid_author_id"])
                    return
                elif check_book == None:
                    popup(msg_user_output["invalid_book_id"])
                    return
                else:
                    cur.execute(QUERIES["GET_BOOK_NAME_BY_ID"], [book_id])
                    book_name = cur.fetchone()[0]
                    cur.execute(DELETE["DELETE_BOOK"], [author_id,book_id])
                    con.commit()
                    update_author_score(int(author_id))
                    popup(f"{book_name}, {msg_user_output['successfully_deleted_book']}")
        except IndexError:
            popup(msg_user_output["invalid_format"])

def show_books() -> None:
    cur.execute(QUERIES["COUNT_BOOKS"])
    if cur.fetchone()[0] == 0:
        temp_choice = input(msg_user_input["no_book_in_table"]).strip().lower()
        if temp_choice == 'y':
            start_and_clear(add_book)
        elif temp_choice == 'n':
            pass
        else:
            popup(msg_user_output["invalid_input"])
    else:
        cur.execute(QUERIES["GET_BOOKS"])
        header('author_id','book_id','book_name','book_added_date')
        for i in cur.fetchall():
            print(f"{i[0]:<{HEADER_AUTHOR_ID}}{i[1]:<{HEADER_BOOK_ID}}{i[2]:<{HEADER_BOOK_NAME}}{i[3]:<{HEADER_BOOK_ADDED_DATE}}")
        temp_choice = input(f"\n{msg_user_input["to_main_menu"]}").strip().lower()
        if temp_choice == 'q':
            pass
        else:
            popup(msg_user_output["invalid_input"])

"""Functions for finished books"""

def add_finished_book() -> None:
    cur.execute(QUERIES['GET_UNFINISHED_BOOKS'])
    books = cur.fetchall()
    if len(books) == 0:
        popup(msg_user_output['does_not_exist_unfinished_book'])
    else:
        header('book_id','book_name')
        for i in books:
            print(f"{i[0]:<{HEADER_BOOK_ID}}{i[1]:<{HEADER_BOOK_NAME}}")
        finished_book_id = input(f"\n{msg_user_input["book_id"]}").strip()
        finished_date_for_calc = dt.datetime.now()
        finished_date_for_table = dt.datetime.now().isoformat()[:19]
        try:
            cur.execute(QUERIES["GET_BOOK_READ_DATE"], [finished_book_id])
            read_date = cur.fetchone()
            read_date_converted = dt.datetime.fromisoformat(read_date[0])
            delta_time = finished_date_for_calc - read_date_converted
            delta_time_for_table =  str(delta_time).split('.')[0]
            try:
                cur.execute(VALUES["INSERT_FINISHED_BOOK"], [finished_book_id, finished_date_for_table, delta_time_for_table])
                con.commit()
                cur.execute(QUERIES['GET_BOOK_NAME_BY_ID'], [finished_book_id])
                popup(f"{cur.fetchone()[0]} {msg_user_output['finished_book_congrats']}")
            except:
                popup(msg_user_output["invalid_input"])
        except TypeError:
            popup(msg_user_output["invalid_book_id"])

def rate_book() -> None:
    cur.execute(QUERIES['GET_UNRATED_BOOKS'])
    books = cur.fetchall()
    if len(books) == 0:
        popup(msg_user_output["does_not_exist_unrated_book"])
    else:
        header('book_id','book_name','book_finished_date','book_reading_time')
        for i in books:
            print(f"{i[0]:<{HEADER_BOOK_ID}}{i[1]:<{HEADER_BOOK_NAME}}{i[2]:<{HEADER_BOOK_FINISHED_DATE}}{i[3]:<{HEADER_BOOK_READING_TIME}}")
        finished_book_id = input(f"\n{msg_user_input["book_id"]}")
        try:
            finished_book_score = int(input(msg_user_input["rating"]))
            if finished_book_score < 0 or finished_book_score > 100:
                popup(msg_user_output["invalid_rate"])
            else:
                try:
                    cur.execute(VALUES["INSERT_BOOK_SCORE"], [finished_book_id, finished_book_score])
                    con.commit()
                    cur.execute(QUERIES["GET_BOOK_NAME_BY_ID"], [finished_book_id])
                    book_name = cur.fetchone()[0]
                    cur.execute(QUERIES["GET_BOOK_SCORE_BY_ID"], [finished_book_id])
                    book_score = cur.fetchone()[0]
                    popup(f"{book_name}{msg_user_output['score_to_book']}{book_score}")
                    cur.execute(QUERIES["GET_AUTHOR_ID_BY_BOOK_ID"], [finished_book_id])
                    author_id = cur.fetchone()[0]
                    update_author_score(int(author_id))
                except:
                    popup(msg_user_output["invalid_input"])
        except ValueError:
            popup(msg_user_output["invalid_datatype"])

def add_book_summary() -> None:
    cur.execute(QUERIES["GET_BOOKS_MISSING_SUMMARY"])
    books = cur.fetchall()
    if len(books) == 0:
        popup(msg_user_output["does_not_exist_book_score"])
    else:
        header('book_id','book_name')
        for i in books:
            print(f"{i[0]:<{HEADER_BOOK_ID}}{i[1]:<{HEADER_BOOK_NAME}}")
        book_id = input(msg_user_input["book_id"]).strip()
        cur.execute(QUERIES["GET_BOOKS_MISSING_SUMMARY_BY_ID"], [book_id])
        _ = cur.fetchone()
        if _ == None:
            popup(msg_user_output["invalid_book_id"])
        else:
            try:
                book_summary = input(f"\n{msg_user_input["book_summary"]}")
                cur.execute(UPDATE['UPDATE_BOOK_SUMMARY'], [book_summary, book_id])
                con.commit()
                popup(msg_user_output["successfully_saved_book_summary"])
            except ValueError:
                popup(msg_user_output["invalid_datatype"])

def show_book_summary() -> None:
    cur.execute(QUERIES['COUNT_BOOK_SCORES'])
    if cur.fetchone()[0] == 0:
        popup(msg_user_output["does_not_exist_book_summary"])
    else:
        cur.execute(QUERIES["GET_BOOKS_THAT_HAVE_SUMMARY"])
        books = cur.fetchall()
        if len(books) == 0:
            popup(msg_user_output["does_not_exist_book_summary"])
        else:
            header('book_id', 'book_name')
            for i in books:
                print(f"{i[0]:<{HEADER_BOOK_ID}}{i[1]:<{HEADER_BOOK_NAME}}")
            
            book_id = input(f"\n{msg_user_input['book_id']}").strip()
            cur.execute(QUERIES["GET_BOOK_SUMMARY_BY_ID"], [book_id])
            book_summary = cur.fetchone() 
            if book_summary is None:
                popup(msg_user_output["invalid_book_id"])
            else:
                print(f"{book_summary[0]}")
                _ = input(msg_user_input["to_main_menu"])

def show_book_scores() -> None:
    cur.execute(QUERIES["COUNT_BOOK_SCORES"])
    if cur.fetchone()[0] == 0:
        popup(msg_user_output['does_not_exist_book_score'])
    else:
        cur.execute(QUERIES["GET_BOOK_SCORES"])
        header('book_id', 'book_name', 'book_score')
        for i in cur.fetchall():
            print(f"{i[0]:<{HEADER_BOOK_ID}}{i[1]:<{HEADER_BOOK_NAME}}{i[2]:<{HEADER_BOOK_SCORE}}")
        _ = input(msg_user_input["to_main_menu"])

"""Misc Functions"""

def avg_book_score_calc(author_id: int) -> int | None:
    cur.execute(QUERIES["GET_ALL_BOOK_SCORES_BY_AUTHOR_ID"], [author_id])
    book_scores = cur.fetchall()
    count = len(book_scores)
    if count == 0:
        return None
    else:
        total_score = 0
        for i in book_scores:
            total_score += int(i[0])
        avg_score = round(total_score / count)
        return avg_score

def update_author_score(author_id: int) -> None:
    avg_score = avg_book_score_calc(author_id)
    if avg_score is None:
        cur.execute(UPDATE["UPDATE_AUTHOR_SCORE"], ['Boş', author_id])
        con.commit()
    else:
        score_text: str = ''
        if 75 < avg_score <= 100:
            score_text = msg_author_score_types["very_liked"]
        elif 50 < avg_score <= 75:
            score_text = msg_author_score_types["liked"]
        elif 25 < avg_score <= 50:
            score_text = msg_author_score_types["average"]
        elif 0 <= avg_score <= 25:
            score_text = msg_author_score_types["disliked"]
            
        cur.execute(UPDATE["UPDATE_AUTHOR_SCORE"], [score_text, author_id])
        con.commit()

def popup(output:str, sleep_time:float = 1.5) -> None:
    print(output)
    time.sleep(sleep_time)

def header(*keys: msg_header_keys) -> None:
    print(f"{UNDERLINE}",end='')
    for i in keys:
        print(msg_header[i], end='')
    print(f"{RESET}\n")

"""Main loop"""

def author_options() -> None:
    for _ in msg_author_options.values():
        print(_)
    temp_choice = input(msg_user_input["menu_choice"]).strip()
    match temp_choice:
        case '0':
            pass
        case '1':
            start_and_clear(add_author)
        case '2':
            start_and_clear(delete_author)
        case '3':
            start_and_clear(show_authors)
        case _:
            popup(msg_user_output["invalid_input"])

def book_options() -> None:
    for _ in msg_book_options.values():
        print(_)
    temp_choice = input(msg_user_input["menu_choice"]).strip()
    match temp_choice:
        case '0':
            pass
        case '1':
            start_and_clear(add_book)
        case '2':
            start_and_clear(delete_book)
        case '3':
            start_and_clear(show_books)
        case '4':
            start_and_clear(finished_book_options)
        case _:
            popup(msg_user_output["invalid_input"])

def finished_book_options() -> None:
    for _ in msg_finished_books.values():
        print(_)
    temp_choice = input(msg_user_input["menu_choice"]).strip()
    match temp_choice:
        case '0':
            pass
        case '1':
            start_and_clear(add_finished_book)
        case '2':
            start_and_clear(rate_book)
        case '3':
            start_and_clear(add_book_summary)
        case '4':
            start_and_clear(show_book_summary)
        case '5':
            start_and_clear(show_book_scores)
        case _:
            popup(msg_user_output["invalid_input"])

def exit() -> None:
    temp_choice = input(msg_user_input["exit_question"]).strip().lower()
    match temp_choice:
        case 'y':
            con.close()
            sys.exit()
        case 'n':
            pass
        case _:
            popup(msg_user_output["invalid_input"])

def main() -> None:
    db_tables()
    while True:
        while True: #Menü temizleme döngüsü. Kısa süre çalışıp kapanıyor.
            clear_screen()
            for _ in msg_main_menu.values():
                print(_)
            break
        temp_choice = input(msg_user_input["menu_choice"]).strip()
        match temp_choice:

            case '1':
                start_and_clear(author_options)

            case '2':
                start_and_clear(book_options)

            case '3':
                start_and_clear(exit)
            case _:
                popup(msg_user_output["invalid_input"])

if __name__ == "__main__":
    main()