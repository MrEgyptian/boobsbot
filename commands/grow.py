import random
from datetime import datetime, timedelta

from functions.db_models import User, GrowthHistory  # ✅ Import models directly


async def execute(event, client, strings):
    user_tg_id = str(event.sender_id)

    with client.db.get_session() as session:
        user = session.query(User).filter_by(telegram_id=user_tg_id).first()

        # Create if missing
        if not user:
            user = User(telegram_id=user_tg_id, boob_size=0, last_growth=None)
            session.add(user)
            session.commit()
            session.refresh(user)

        # Check cooldown (12 hours)
        now = datetime.utcnow()
        print(user.last_growth)
        if user.last_growth and now - user.last_growth < timedelta(hours=12):
            remaining = timedelta(hours=12) - (now - user.last_growth)
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            await event.reply(
                f"⏳ You already grew recently! Try again in **{hours}h {minutes}m**."
            )
            return

        # Random growth between -2 and +10 cm
        growth = random.randint(-2, 10)
        user.boob_size = (user.boob_size or 0) + growth
        user.last_growth = now

        # Save history
        history = GrowthHistory(
            user_id=user.user_id,
            growth_amount=growth,
            total_size=user.boob_size,
        )
        session.add(history)

        session.commit()
        new_size = user.boob_size

    # Build reply
    print(growth)
    if growth >= 0:
        msg = f"✨ You grew **+{growth} cm** today! Your new size is **{new_size} cm** 🎉"
    else:
        msg = f"💔 Oh no! You shrank **{growth} cm**... Your new size is **{new_size} cm** 😢"

    await event.reply(msg)
