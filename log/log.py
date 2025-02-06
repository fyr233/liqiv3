import asyncio
import aiosqlite
import sqlite3
import os
import pickle

LOG_ROOT = os.path.dirname(os.path.abspath(__file__))
print(__file__, 'LOG_ROOT', LOG_ROOT)

class Logger:
    def __init__(self):
        pass

    def init_db(self):
        self.message_path = LOG_ROOT + '/message/db.sqlite'
        print('message db', self.message_path)
        self.setu_path = LOG_ROOT + '/setu/db.sqlite'
        print('setu db', self.setu_path)

        with sqlite3.connect(self.message_path) as db:
            db.execute('''
            CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            type TEXT DEFAULT 'unknown',
            user_id TEXT,
            group_id TEXT,
            content TEXT
            )
            ''')
            db.commit()

        with sqlite3.connect(self.setu_path) as db:
            db.execute('''
            CREATE TABLE IF NOT EXISTS setu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            type TEXT,
            user_id TEXT,
            group_id TEXT,
            file TEXT,
            message TEXT
            )
            ''')
            db.commit()

    async def log_message(self, type, user_id, group_id, content):
        async with aiosqlite.connect(self.message_path) as db:
            await db.execute('''
            INSERT INTO messages (type, user_id, group_id, content)
            VALUES (?, ?, ?, ?)
            ''', (type, user_id, group_id, content))
            await db.commit()

    async def log_setu(self, type, user_id, group_id, file, message):
        async with aiosqlite.connect(self.setu_path) as db:
            await db.execute('''
            INSERT INTO setu (type, user_id, group_id, file, message)
            VALUES (?, ?, ?, ?, ?)
            ''', (type, user_id, group_id, file, message))
            await db.commit()

    async def get_messages(self, query_str, query_params):
        async with aiosqlite.connect(self.setu_path) as db:
            async with db.execute(query_str, query_params) as cursor:
                return await cursor.fetchall()

# logger
logger = Logger()

# 使用示例
async def _main():

    # 初始化数据库（通常只需在第一次运行时执行）
    await logger.init_db()

    # 假设这是从群聊中接收到的消息
    message_content = '这是一条群聊消息'

    # 记录消息
    await logger.log_message(type='recv_msg', user_id='123', group_id='456', content=message_content)

    # 查询消息（根据需要）
    messages = await logger.get_messages(query_str='SELECT * FROM messages WHERE group_id = ?', query_params=('456',))
    for message in messages:
        print(message)


if __name__ == '__main__':
    asyncio.run(_main())