import sql
import handler

def main():
    sql.init_db()
    session = sql.get_session()
    handler.menu(session)
    session.commit()
    session.close()

if __name__ == "__main__":
    main()