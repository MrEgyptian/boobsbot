from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functions.db_models import User,File,Download,Group
import sqlalchemy,logging
from sqlalchemy import text
class Database:
    import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.engine.url import make_url

class Database:
    def __init__(self, database_url):
        self.database_url = database_url
        self._ensure_database_exists()
        self._init_engine()

    def _ensure_database_exists(self):
        url = make_url(self.database_url)
        db_name = url.database

        try:
            # Try connecting to the target DB
            test_engine = create_engine(self.database_url)
            with test_engine.connect():
                pass
        except OperationalError as e:
            if e.code == "e3q8":  # database does not exist
                logging.info(f"Database {db_name} does not exist, creating...")

                # Reconnect without database
                url_no_db = url.set(database="postgres")
                engine_no_db = create_engine(url_no_db)

                with engine_no_db.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
                    conn.execute(text(f'CREATE DATABASE "{db_name}"'))
            else:
                raise

    def _init_engine(self):
        self.engine = create_engine(self.database_url)
        User.metadata.create_all(self.engine)
        File.metadata.create_all(self.engine)
        Download.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


    def get_session(self):
        """Create a new session."""
        return self.Session()
    def get_users(self):
        with self.get_session() as session:
            users=session.query(User).all()
            users=[int(u.telegram_id) for u in users]
            return users
    def get_user_by_id(self, user_id):
        with self.get_session() as session:
            return session.query(User).filter(User.user_id == user_id).first()
    def get_user_by_telegram_id(self, telegram_id):
        with self.get_session() as session:
            return session.query(User).filter(User.telegram_id == telegram_id).first()
    def add_user(self,  telegram_id):
        with self.get_session() as session:
            user = User( telegram_id=telegram_id)
            session.add(user)
            session.commit()
            return user
    def rm_user(self, user_id):
        with self.get_session() as session:
            user = session.query(User).filter(User.telegram_id == user_id).first()
            if user:
                session.delete(user)
                session.commit()
    def white_list_user(self, user_id):
        with self.get_session() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.whitelisted = True
                session.commit()
    def unwhite_list_user(self, user_id):
        with self.get_session() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.whitelisted = False
                session.commit()
    def add_admin(self, user_id):
        with self.get_session() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.is_admin = True
                session.commit()
    def add_admin_by_telegram_id(self, telegram_id):
        with self.get_session() as session:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                user.is_admin = True
                session.commit()
    def remove_admin_by_telegram_id(self, telegram_id):
        with self.get_session() as session:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                user.is_admin = False
                session.commit()
    def ban_user(self,user_id):
        with self.get_session() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.banned = True
                session.commit()
    def unban_user(self,user_id):
        with self.get_session() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.banned = False
                session.commit()
    def get_admins(self):
        with self.get_session() as session:
            return session.query(User).filter(User.is_admin == True).all()
    def get_banned_users(self):
        with self.get_session() as session:
            return session.query(User).filter(User.banned == True).all()
    def remove_admin(self, user_id):
        with self.get_session() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.is_admin = False
                session.commit()
    def get_user_history(self, user_id):
        with self.get_session() as session:
            return session.query(Download).filter(Download.user_id == user_id).all()
    def clear_user_history(self, user_id):
        with self.get_session() as session:
            session.query(Download).filter(Download.user_id == user_id).delete()
            session.commit()
    def add_file(self, file_name, file_path, file_size, file_type,file_tg_id):
        with self.get_session() as session:
            file = File(file_name=file_name, file_path=file_path, file_size=file_size, file_type=file_type,file_tg_id=file_tg_id)
            session.add(file)
            session.commit()
    def rm_file(self, file_id):
        with self.get_session() as session:
            file = session.query(File).filter(File.file_id == file_id).first()
            if file:
                session.delete(file)
                session.commit()
    def clear_file_history(self, file_id):
        with self.get_session() as session:
            session.query(Download).filter(Download.file_id == file_id).delete()
            session.commit()
    def get_bot_users(self):
        with self.get_session() as session:
            return session.query(User).filter(User.whitelisted == True).all()
    def get_bot_users_count(self):
        with self.get_session() as session:
            return session.query(User).filter(User.whitelisted == True).count()
    def get_bot_groups(self):
        with self.get_session() as session:
            return session.query(Group).filter(Group.whitelisted == True).all()
    def add_bot_group(self, telegram_id):
        with self.get_session() as session:
            group = Group(telegram_id=telegram_id)
            session.add(group)
            session.commit()
    def rm_bot_group(self, telegram_id):
        with self.get_session() as session:
            group = session.query(Group).filter(Group.telegram_id == telegram_id).first()
            if group:
                session.delete(group)
                session.commit()
if __name__ == "__main__":
    DATABASE_URL = "postgresql://postgres:1@127.0.0.1:5432/dl_bot"
    db = Database(DATABASE_URL)
    
