import aiosqlite
from typing import List, Tuple

from config import DB_PATH


class AsyncDatabase:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name

    async def get_subscriptions(self, user_id: int) -> List[Tuple[int, str, str, str]]:
        """Асинхронно получает активные подписки пользователя из базы данных."""
        query = """
            SELECT id, topic_name, channel_name, last_pub_time
            FROM News
            WHERE user_id = ? AND is_active = '🟢'
        """
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute(query, (user_id,)) as cursor:
                subscriptions = await cursor.fetchall()
        return subscriptions
