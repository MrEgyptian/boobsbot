import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.engine.url import make_url

from functions.db_models import User, Group, GrowthHistory, Settings, Base


class Database:
    def __init__(self, database_url: str):
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
            #if getattr(e.orig, "pgcode", None) == "3D000":  # invalid_catalog_name (DB does not exist)
            if e.code=='e3q8':
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
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        """Create a new session."""
        return self.Session()

    # ─── USER MANAGEMENT ────────────────────────────────
    def add_user(self, telegram_id: str):
        with self.get_session() as session:
            user = User(telegram_id=telegram_id)
            session.add(user)
            session.commit()
            return user

    def get_user_by_id(self, user_id: int):
        with self.get_session() as session:
            return session.query(User).filter(User.user_id == user_id).first()

    def get_user_by_telegram_id(self, telegram_id: str):
        with self.get_session() as session:
            return session.query(User).filter(User.telegram_id == telegram_id).first()

    def get_users(self):
        with self.get_session() as session:
            return session.query(User).all()

    def rm_user(self, telegram_id: str):
        with self.get_session() as session:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                session.delete(user)
                session.commit()

    def ban_user(self, user_id: int):
        with self.get_session() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.banned = True
                session.commit()

    def unban_user(self, user_id: int):
        with self.get_session() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.banned = False
                session.commit()

    def whitelist_user(self, user_id: int):
        with self.get_session() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.whitelisted = True
                session.commit()

    def unwhitelist_user(self, user_id: int):
        with self.get_session() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.whitelisted = False
                session.commit()

    def add_admin(self, telegram_id: str):
        with self.get_session() as session:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                user.is_admin = True
                session.commit()

    def remove_admin(self, telegram_id: str):
        with self.get_session() as session:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                user.is_admin = False
                session.commit()

    def get_admins(self):
        with self.get_session() as session:
            return session.query(User).filter(User.is_admin == True).all()

    # ─── GROUP MANAGEMENT ───────────────────────────────
    def add_group(self, telegram_id: str):
        with self.get_session() as session:
            group = Group(telegram_id=telegram_id)
            session.add(group)
            session.commit()
            return group

    def get_group_by_id(self, group_id: int):
        with self.get_session() as session:
            return session.query(Group).filter(Group.group_id == group_id).first()

    def get_group_by_telegram_id(self, telegram_id: str):
        with self.get_session() as session:
            return session.query(Group).filter(Group.telegram_id == telegram_id).first()

    def rm_group(self, telegram_id: str):
        with self.get_session() as session:
            group = session.query(Group).filter(Group.telegram_id == telegram_id).first()
            if group:
                session.delete(group)
                session.commit()

    def get_whitelisted_groups(self):
        with self.get_session() as session:
            return session.query(Group).filter(Group.whitelisted == True).all()

    # ─── GROWTH HISTORY ────────────────────────────────
    def add_growth_entry(self, user_id: int, growth_amount: int, total_size: int):
        with self.get_session() as session:
            entry = GrowthHistory(user_id=user_id, growth_amount=growth_amount, total_size=total_size)
            session.add(entry)
            session.commit()
            return entry

    def get_user_history(self, user_id: int):
        with self.get_session() as session:
            return session.query(GrowthHistory).filter(GrowthHistory.user_id == user_id).all()

    def clear_user_history(self, user_id: int):
        with self.get_session() as session:
            session.query(GrowthHistory).filter(GrowthHistory.user_id == user_id).delete()
            session.commit()
    def get_bot_users_count(self, include_banned: bool = False):
        """Return the total number of users in the bot."""
        with self.get_session() as session:
            query = session.query(User)
            if not include_banned:
                query = query.filter(User.banned == False)
            return query.count()

if __name__ == "__main__":
    DATABASE_URL = "postgresql://postgres:1@127.0.0.1:5432/boobs_bot"
    db = Database(DATABASE_URL)
    print("✅ Database initialized!")
