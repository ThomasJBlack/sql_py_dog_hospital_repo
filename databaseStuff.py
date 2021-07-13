import pymysql
db = pymysql.connect(
    host="freetrainer.cryiqqx3x1ub.us-west-2.rds.amazonaws.com",
    user="thomas",
    password="changeme"
)
cursor = db.cursor()

# READS
sql = "SELECT * FROM Thomas_Black.dog_table LIMIT 10"
cursor.execute(sql)
while True:
    row = cursor.fetchone()
    if row == None:
        break
    print(row)

# WRITES
sql = "INSERT X INTO table_X"
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()

db.close()
