import sqlite3
import json

DB_PATH = 'movies.db'
JSON_IN_PATH = 'movies.json'
JSON_OUT_PATH = 'exported.json'


def connect_db(db_path: str) -> sqlite3.Connection:
    """連接到 SQLite 資料庫
       並設定 row_factory 以便取得字典格式"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    # 設定查詢結果為字典格式，方便通過欄位名稱取值
    return conn


def create_table(conn):
    """建立 movies 資料表"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            director TEXT NOT NULL,
            genre TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL CHECK(rating >= 1.0 AND rating <= 10.0)
        )
    """)
    conn.commit()


def import_movies(conn: sqlite3.Connection, json_file: str):
    """從 movies.json 檔案匯入電影資料至資料庫"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            movies = json.load(f)  # 載入 JSON 檔案內容為電影資料
        with conn:
            # 將每部電影資料插入資料庫
            for movie in movies:
                conn.execute("""
                    INSERT INTO movies (title, director, genre, year, rating)
                    VALUES (?, ?, ?, ?, ?)
                """, (movie['title'], movie['director'], movie['genre'],
                      movie['year'], movie['rating']))
        print("電影已匯入")  # 匯入成功提示

    except FileNotFoundError:
        print("錯誤: 找不到電影資料檔案！")
        # 當找不到檔案時，顯示錯誤訊息
    except json.JSONDecodeError:
        print("錯誤: JSON 格式錯誤！")
        # 當 JSON 格式錯誤時，顯示錯誤訊息
    except Exception as e:
        print(f'發生其它錯誤: {e}')


def list_movies(conn: sqlite3.Connection):
    """列出電影資料或查詢特定電影"""
    search_all = input("查詢全部電影嗎？(y/n): ").strip().lower()

    if search_all == 'y':
        cursor = conn.execute("SELECT * FROM movies")
        # 查詢所有電影資料
        movies = cursor.fetchall()
        if not movies:
            print("查無資料")
            # 當資料庫中沒有電影時，顯示提示
        else:
            # 設定欄位寬度
            title_width = 15
            director_width = 12
            genre_width = 8
            year_width = 8
            rating_width = 5

            # 顯示電影資料
            # 使用全形空白 chr(12288)
            print(f"{'電影名稱':{chr(12288)}<{title_width}}"
                  f"{'導演':{chr(12288)}<{director_width}}"
                  f"{'類型':{chr(12288)}<{genre_width}}"
                  f"{'上映年份':{chr(12288)}<{year_width}}"
                  f"{'評分':{chr(12288)}<{rating_width}}")
            print("-" * 100)
            # 格式化列出電影資料
            for movie in movies:
                print(f"{movie['title']:{chr(12288)}<{title_width}}"
                      f"{movie['director']:{chr(12288)}<{director_width}}"
                      f"{movie['genre']:{chr(12288)}<{genre_width}}"
                      f"{movie['year']:{chr(12288)}<{year_width}}"
                      f"{movie['rating']:{chr(12288)}<{rating_width}.1f}")
    else:
        title = input("請輸入電影名稱: ")
        # 如果不查詢全部電影，則要求輸入電影名稱
        cursor = conn.execute(
            "SELECT * FROM movies WHERE title LIKE ?",
            (f"%{title}%",)
            )
        # 根據名稱查詢電影
        movies = cursor.fetchall()
        if not movies:
            print("查無資料")
            # 如果沒有查詢到電影，顯示提示
        else:
            # 顯示查詢結果
            # 使用全形空白 chr(12288)
            print(f"{'電影名稱':{chr(12288)}<{title_width}}"
                  f"{'導演':{chr(12288)}<{director_width}}"
                  f"{'類型':{chr(12288)}<{genre_width}}"
                  f"{'上映年份':{chr(12288)}<{year_width}}"
                  f"{'評分':{chr(12288)}<{rating_width}}")
            print("-" * 100)
            # 格式化列出電影資料
            for movie in movies:
                print(f"{movie['title']:{chr(12288)}<{title_width}}"
                      f"{movie['director']:{chr(12288)}<{director_width}}"
                      f"{movie['genre']:{chr(12288)}<{genre_width}}"
                      f"{movie['year']:{chr(12288)}<{year_width}}"
                      f"{movie['rating']:{chr(12288)}<{rating_width}.1f}")


def add_movie(conn: sqlite3.Connection):
    """新增電影資料"""
    title = input("電影名稱: ")
    # 輸入電影名稱
    director = input("導演: ")
    # 輸入電影導演
    genre = input("類型: ")
    # 輸入電影類型
    year = int(input("上映年份: "))
    # 輸入上映年份（轉換為整數）
    rating = float(input("評分 (1.0 - 10.0): "))
    # 輸入評分（轉換為浮點數）
    with conn:
        # 插入新電影資料到資料庫
        conn.execute("""
            INSERT INTO movies (title, director, genre, year, rating)
            VALUES (?, ?, ?, ?, ?)
        """, (title, director, genre, year, rating))
    print("電影已新增")  # 新增成功提示


def modify_movie(conn: sqlite3.Connection):
    """修改電影資料"""
    movie_title = input("請輸入要修改的電影名稱: ")
    # 輸入要修改的電影名稱
    cursor = conn.execute(
        "SELECT * FROM movies WHERE title = ?",
        (movie_title,)
    )
    # 查詢該電影資料
    movie = cursor.fetchone()
    if movie:
        # 顯示該電影資料
        print(f"{'電影名稱':<15}{'導演':<12}{'類型':<8}{'上映年份':<8}{'評分':<5}")
        print("-" * 100)
        print(
            f"{movie['title']:<15}",
            f"{movie['director']:<12}",
            f"{movie['genre']:<8}",
            f"{movie['year']:<8}",
            f"{movie['rating']:<5.1f}"
        )
        # 要修改的欄位
        title = input("請輸入新的電影名稱 (若不修改請直接按 Enter): ")
        director = input("請輸入新的導演 (若不修改請直接按 Enter): ")
        genre = input("請輸入新的類型 (若不修改請直接按 Enter): ")
        year = input("請輸入新的上映年份 (若不修改請直接按 Enter): ")
        rating = input("請輸入新的評分 (若不修改請直接按 Enter): ")

        update_data = []  # 用來儲存修改的欄位
        update_values = []  # 用來儲存修改後的值

        # 根據輸入的資料來組建更新的 movies 資料庫內容
        if title:
            update_data.append("title = ?")
            update_values.append(title)
        if director:
            update_data.append("director = ?")
            update_values.append(director)
        if genre:
            update_data.append("genre = ?")
            update_values.append(genre)
        if year:
            update_data.append("year = ?")
            update_values.append(int(year))
        if rating:
            update_data.append("rating = ?")
            update_values.append(float(rating))

        update_values.append(movie['id'])
        # 將電影 ID 加入更新資料中
        if update_data:
            # 執行更新操作
            with conn:
                conn.execute(f"UPDATE movies SET {', '.join(update_data)} "
                             f"WHERE id = ?", tuple(update_values))
            print("資料已修改")
            # 修改成功提示
        else:
            print("未做任何修改")
            # 如果沒有任何欄位修改，顯示提示
    else:
        print("電影不存在")
        # 如果電影找不到，顯示提示


def delete_movie(conn: sqlite3.Connection):
    """刪除電影資料"""
    delete_all = input("刪除全部電影嗎？(y/n): ").strip().lower()
    if delete_all == 'y':
        # 刪除所有電影資料
        with conn:
            conn.execute("DELETE FROM movies")
        print("所有電影資料已刪除")
        # 刪除成功提示
    else:
        movie_title = input("請輸入要刪除的電影名稱: ")
        # 輸入電影名稱(可用關鍵字)
        cursor = conn.execute(
            "SELECT * FROM movies WHERE title LIKE ?",
            (f"%{movie_title}%",)
        )
        # 查詢該電影資料
        movie = cursor.fetchone()

        if movie:
            print(f"{'電影名稱':<15}{'導演':<12}{'類型':<8}{'上映年份':<8}{'評分':<5}")
            print("-" * 100)
            print(
                f"{movie['title']:<15}",
                f"{movie['director']:<12}",
                f"{movie['genre']:<8}",
                f"{movie['year']:<8}",
                f"{movie['rating']:<5.1f}"
            )

            confirm = input("是否要刪除(y/n): ").strip().lower()
            if confirm == 'y':
                # 執行刪除操作
                with conn:
                    conn.execute(
                        "DELETE FROM movies WHERE id = ?", (movie['id'],)
                    )
                print("電影已刪除")  # 刪除成功提示
        else:
            print("電影不存在")  # 如果電影不存在，顯示提示


def export_movies(conn: sqlite3.Connection, output_file: str):
    """將電影資料匯出到 JSON 檔案"""
    export_all = input("匯出全部電影嗎？(y/n): ").strip().lower()
    if export_all == 'y':
        cursor = conn.execute("SELECT * FROM movies")  # 查詢所有電影資料
        movies = cursor.fetchall()
        movie_list = [{"title": movie['title'], "director": movie['director'],
                       "genre": movie['genre'], "year": movie['year'],
                       "rating": movie['rating']} for movie in movies]
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(movie_list, f, ensure_ascii=False, indent=4)
            # 將電影資料以 JSON 格式寫入檔案
        print(f"電影資料已匯出至 {output_file}")  # 匯出成功提示
    else:
        # 當使用者選擇匯出特定電影
        title = input("請輸入要匯出的電影名稱: ")
        cursor = conn.execute(
            "SELECT * FROM movies WHERE title LIKE ?",
            (f"%{title}%",)
        )
        movies = cursor.fetchall()

    # 檢查是否有符合條件的電影資料
    if not movies:
        print("查無符合條件的電影資料")
        return

    # 將查詢結果轉換成 JSON 格式
    movie_list = [{"title": movie['title'],
                   "director": movie['director'],
                   "genre": movie['genre'],
                   "year": movie['year'],
                   "rating": movie['rating']} for movie in movies]

    # 將電影資料匯出至指定的 JSON 檔案
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(movie_list, f, ensure_ascii=False, indent=4)

    print(f"電影資料已匯出至 {output_file}")
