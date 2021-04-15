import pymysql
conn = pymysql.connect(host='localhost', user='root', password='1234',
                        db='testdb', charset='utf8')
curs = conn.cursor()



def search_service(cop): # 회사별로 서비스하는 영화들이 달라서 회사이름을 매개변수로 cop 받아옴
    while True:
        print("\n영화 이름을 조회하는 창입니다.\n--------------------------\n1.심의등급으로 조회\n2.극장개봉연도로 조회 \n3.감독이름으로 조회\n4.조회수 순위로 조회(범위지정)\n5.국가로 조회\n6.회사 다시 선택하기\n--------------------------\n")
        search_kinds = input("조회 유형을 정해주세요: ")
        if search_kinds == "1":
            rate = input("\n원하시는 심의등급(12세, 15세, 전체관람가, 청소년관람불가)을 입력해주세요: ")
            sql = "select rating, movie_name from Cine where rating like '%{0}%' and {1} != 0".format(rate,cop) #cop로 어느 회사 사용자인지 알수있음.
            curs.execute(sql)
            rows = curs.fetchall()
            if len(rows) == 0: #예외처리 rows의 타입이 튜플이고 검색에 일치하는 결과가 없을때는 rows의 길이가 0 
                print("\n잘못 입력하셨거나 존재하지 않는 심의등급입니다.")
            else:
                print("\n   심의등급      영화")
                print("---------------------------------------------")
                for row in rows:
                    print("{0:>4} | {1:>2}".format(row[0], row[1]),end="\n---------------------------------------------\n") # 심의등급       영화
                info_reply() # 부가정보 조회 선택창으로 넘어감                                                            12세이상관람가  | 영화 형태로 출력
                
        if search_kinds == "2":
            open_date = input("\n극장개봉연도를 입력해주세요.(예시:2020): ")
            sql = "select movie_name from Cine where convert(opendate, char) like '{0}%'".format(open_date) #opendate 필드의 데이터 타입이 int이므로 문자열 데이터 타입으로 컨버트
            curs.execute(sql)
            rows = curs.fetchall()
            if len(rows) == 0:
                print("\n잘못 입력하셨거나 {0}년에는 개봉한 영화가 없습니다.".format(open_date))
            else:
                print("\n{0}년 개봉영화".format(open_date))
                print("--------------------------------")
                for row in rows:
                    print(row[0],end="\n--------------------------------\n") #  2020년 개봉영화
                info_reply()                                                  #영화 이름 형태로 출력

        if search_kinds == "3":
            dit_name = input("\n감독이름을 입력해주세요(예시:봉준호): ")
            sql = "select director, movie_name from Cine where director like '%{0}%'".format(dit_name)
            curs.execute(sql)
            rows = curs.fetchall()
            if len(rows) == 0:
                print("\n잘못 입력하셨거나 {0} 감독의 영화가 없습니다.".format(dit_name))
            else:
                print("\n----------------------------------------")
                for row in rows:
                    print("{0} | {1:>2}".format(row[0],row[1]),end="\n----------------------------------------\n") #감독 | 영화 형태로 출력
                info_reply()

        if search_kinds == "4":
            rank = list(map(int, input("\n순위의 범위(300위까지)를 정해주세요.(예시:(1 300)형태로 입력): ").split()))
            if rank[0] < 1 or rank[1] > 300: #순위의 범위가 1에서 300을 넘어가버릴때
                print("\n잘못 입력하셨습니다. 1에서 300까지의 범위로 정해주세요.")
            sql = "select ranking, movie_name from Cine where ranking between {0} and {1} and {2} != 0".format(rank[0], rank[1], cop) #between 범위지정 cop가 0일때 마다 순위에 1을 빼줌
            curs.execute(sql)
            rows = curs.fetchall()
            print("\n  순위   영화")
            print("--------------------------------")
            for row in rows:
                print("{0:>4}위 | {1:>2}".format(row[0],row[1]),end="\n--------------------------------\n") #순위와 영화를 (1위 | 영화이름) 형태로 출력
            info_reply()

        if search_kinds == "5":
            country = input("원하시는 국가를 입력해주세요(한국, 미국, 중국, 일본 등등): ") 
            sql = "select movie_name from Cine where country like'%{0}%' and {1} != 0".format(country, cop)
            curs.execute(sql)
            rows = curs.fetchall()
            if len(rows) == 0:
                print("\n{0} 나라의 영화가 서비스중이지 않거나 존재하지 않는 나라입니다.".format(country))
            else:
                print("\n             {0}".format(country)) #나라 출력
                print("--------------------------------")
                for row in rows:
                    print("{0:>5}".format(row[0]),end="\n--------------------------------\n") # 미국
                info_reply()                                                 # 영화이름 형태로 출력

        if search_kinds == "6":
            print("\n회사 선택창으로 돌아갑니다.")
            break #다시 회사 선택하는 창으로 돌아감


def info_reply():
    while True:
        print("\n1.예\n2.아니오\n")
        reply = input("부가기능으로 영화의 정보를 조회하시겠습니까?: ")
        if reply == "1":
            info_inquiry()
        if reply == "2":
            print("\n")
            break #아니오를 선택하면 다시 조회창으로 돌아감


def info_inquiry():
    while True:
        movie = input("\n영화를 입력해주세요.(예시:기생충):") # 영화 입력
        sql = "select count(movie_name) from Cine where movie_name like '%{0}%'".format(movie)
        curs.execute(sql)
        rows = curs.fetchone() #영화 제목이 비슷한 것들을 카운트 정확하면 rows[0]이 1이 되고 근접하면 1보다 커짐
        
        if rows[0] > 1: #제목이 근접하게 일치할때
            sql = "select movie_name from Cine where movie_name like '%{0}%'".format(movie)
            curs.execute(sql)
            rows = curs.fetchall()
            print("\n---------------------------------------------------------------")
            print("#제목과 근접한 영화 목록입니다. 영화 제목을 정확히 입력해주세요")
            print("---------------------------------------------------------------\n\n--------------------------------")
            for row in rows:
                print("{0}".format(row[0]),end="\n--------------------------------\n")
            continue

        if rows[0] == 1: #제목이 정확하게 일치할때
            while True:
                print("\n부가 정보를 조회하는 창입니다.\n--------------------------\n1.주연배우\n2.제작연도\n3.영화의 전체매출\n4.{0}서비스의 1월 조회수\n5.영화 입력창으로 돌아가기\n6.프로그램 종료\n--------------------------\n".format(cop))
                info = input("어떤 정보를 조회하시겠습니까?: ")
                if info == "1":
                    sql = "select movie_name, actor from Cine where movie_name like '%{0}%'".format(movie)
                    curs.execute(sql)
                    rows = curs.fetchall()
                    print("\n---------------------------------------------------------------------")
                    for row in rows:
                        print("{0}의 주연배우들은 {1} 입니다.".format(row[0],row[1]))
                    print("---------------------------------------------------------------------\n")    
                    continue
                
                if info == "2": # 제작연도
                    sql = "select movie_name, prd_year from Cine where movie_name like '%{0}%'".format(movie)
                    curs.execute(sql)
                    rows = curs.fetchall()
                    print("\n------------------------------------------")
                    for row in rows:
                        print("{0}의 제작연도는 {1}년도입니다.".format(row[0],row[1]))
                    print("------------------------------------------\n")
                    continue

                if info == "3":  # 전체 매출 
                    sql = "select movie_name, total_price from Cine where movie_name like '%{0}%'".format(movie)
                    curs.execute(sql)
                    rows = curs.fetchall()
                    print("\n------------------------------------------")
                    for row in rows:
                        print("{0}의 전체매출은 {1}원 입니다.".format(row[0],row[1]))
                    print("------------------------------------------\n")
                    continue
                
                if info == "4": # 1월 조회수
                    sql = "select movie_name, {0} from Cine where movie_name like '%{1}%'".format(cop, movie)
                    curs.execute(sql)
                    rows = curs.fetchall()
                    print("\n------------------------------------------")
                    for row in rows:
                        print("{0}의 2021년 1월 {1}서비스 조회수는 {2}회 입니다.".format(row[0], cop, row[1]))
                    print("------------------------------------------\n")
                    continue

                if info == "5":
                    print("\n영화 입력창으로 돌아갑니다.\n")
                    break  #while문을 한번더 썼기 때문에 break를 걸어주면 처음 while문으로 돌아감 97
                
                if info == "6":
                    print("\n프로그램을 종료합니다.\n")
                    exit()

while True:
    print("\n----------------------\n1.KT\n2.LG\n3.SK\n4.홈초이스\n5.프로그램 종료\n----------------------\n")
    cop = input("어느 회사 IPTV를 사용중이신가요?: ")
    if cop == "1":
        print("\nKT를 선택하셨습니다.")
        cop = "kt" # cop를 회사에 맞는 필드명으로 변경 회사마다 서비스하지 않는 영화들이 있음
        search_service(cop)
    if cop == "2":
        print("\nLG를 선택하셨습니다.")
        cop = "lg"
        search_service(cop)
    if cop == "3":
        print("\nSK를 선택하셨습니다.")
        cop = "sk"
        search_service(cop)
    if cop == "4":
        print("\n홈초이스를 선택하셨습니다.")
        cop = "homechoice"
        search_service(cop)
    if cop == "5":
        print("\n프로그램을 종료합니다.")
        break

conn.close()

