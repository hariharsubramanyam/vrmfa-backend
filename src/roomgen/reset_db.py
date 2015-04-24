import argparse
from room_persist import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbname", type=str, required=True)
    parser.add_argument("--user", type=str, required=True)

    args = parser.parse_args()
    dbname = args.dbname
    user = args.user

    rp = RoomPersist(dbname, user)
    rp.start()
    rp.create_tables()
    rp.finish()
