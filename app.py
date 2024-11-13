# 執行檔/選單選擇與互動

from lib import (
    connect_db,
    create_table,
    import_movies,
    list_movies,
    add_movie,
    modify_movie,
    delete_movie,
    export_movies
)


def show_menu():
    print("\n----- 電影管理系統 -----")
    print("1. 匯入電影資料檔")
    print("2. 查詢電影")
    print("3. 新增電影")
    print("4. 修改電影")
    print("5. 刪除電影")
    print("6. 匯出電影")
    print("7. 離開系統")
    print("------------------------")


def main():
    DB_PATH = 'movies.db'
    JSON_IN_PATH = 'movies.json'
    JSON_OUT_PATH = 'exported.json'

    # 連接資料庫
    conn = connect_db(DB_PATH)
    # 初始化資料表（確保資料表存在）
    create_table(conn)

    while True:
        show_menu()
        choice = int(input("請選擇操作功能: "))
        try:
            if choice == 1:
                import_movies(conn, JSON_IN_PATH)
            elif choice == 2:
                list_movies(conn)
            elif choice == 3:
                add_movie(conn)
            elif choice == 4:
                modify_movie(conn)
            elif choice == 5:
                delete_movie(conn)
            elif choice == 6:
                export_movies(conn, JSON_OUT_PATH)
            else:
                print("系統已退出!")
                break
        except ValueError:
            print("請輸入有效的數字選項！")
        except Exception as e:
            print(f"發生錯誤: {e}")

    # 關閉資料庫連線
    conn.close()


if __name__ == '__main__':
    main()
