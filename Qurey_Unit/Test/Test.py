import cx_Oracle
import ssh
conn = cx_Oracle.connect("ops$aims/quilt1@10.99.1.24:1521/AIMS")
print (conn.version)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM STUDENT")
count = cursor.fetchall()[0][0]
print (count)
cursor.close()
conn.close()

