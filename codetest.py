import random
import MySQLdb

def database():
    db = MySQLdb.connect(host='localhost',
                         user='root',
                         password='',
                         db='api_db',
                         charset='utf8')
    cursor = db.cursor()
    return db, cursor

db, cursor = database()


c = ['台中', '高雄', '嘉義', '台南', '桃園', '新竹', '苗栗']
a = ['西屯區', '鳳山區', '中區', '東區', '中壢區', '北埔區', '頭份']
p = ['2000', '5000', '10000', '12000', '15000', '18000', '22000']


for n in range(48):
    co = random.choice(c)
    ar = random.choice(a)
    po = random.choice(p)
    cursor.execute(f"INSERT INTO `country`(`country`, `area`, `population`) VALUES ('{co}', '{ar}', '{po}')")
    db.commit()