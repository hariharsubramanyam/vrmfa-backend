import argparse
import psycopg2

if __name__=="__main__":
    table_name = "images"
    create_table_query_format = '''
    CREATE TABLE %s (url text PRIMARY KEY);
    '''
    parser = argparse.ArgumentParser(description="Recreate the tables")
    parser.add_argument('--dbname', type=str, required=True, help="The name of the PostgreSQL database")
    parser.add_argument('--user', type=str, required=True, help="The name of the PostgreSQL user")

    args = parser.parse_args()
    dbname = args.dbname
    user = args.user
    conn = psycopg2.connect("dbname=%s user=%s" % (dbname, user))
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS %s;" % (table_name,))
    cur.execute(create_table_query_format % (table_name,))
    conn.commit()
    cur.close()
    conn.close()
