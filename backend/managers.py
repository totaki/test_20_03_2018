import sqlalchemy as sa
from aiomysql.sa import create_engine
from sqlalchemy.dialects.mysql import insert
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from aiomysql.sa import Engine


metadata = sa.MetaData()

tbl = sa.Table(
    'words', metadata,
    sa.Column('hash', sa.CHAR(64), primary_key=True),
    sa.Column('word', sa.Text(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False)
)


class WordsManager:

    tbl = tbl

    def __init__(self, engine: 'Engine'):
        self._engine = engine

    async def upgrade_records(self, values) -> None:
        async with self._engine.acquire() as conn:
            # First get existing
            existing_rows = await conn.execute(sa.select([self.tbl.c.hash, self.tbl.c.count]).where(
                self.tbl.c.hash.in_([v['hash'] for v in values])
            ))
            existing = {r.hash: r.count for r in await existing_rows.fetchall()}

            # Update value
            for v in values:
                exists = existing.get(v['hash'])
                if exists:
                    v['count'] = v['count'] + exists

            # Inset or update
            insert_stmt = insert(self.tbl).values(values)
            on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
                count=insert_stmt.inserted.count
            )
            await conn.execute(on_duplicate_key_stmt)

    async def get_records(self) -> List[dict]:
        async with self._engine.acquire() as conn:
            rows = await conn.execute(self.tbl.select().order_by(self.tbl.c.count.desc()))
            result = await rows.fetchall()
            return [dict(r) for r in result]

    @classmethod
    async def create(cls, host: str, db: str, user: str, password: str, loop) -> 'WordsManager':
        engine = await create_engine(
            user=user, password=password, db=db, host=host,  autocommit=True, loop=loop
        )
        return cls(engine)

    async def stop(self):
        self._engine.close()
        self._engine.wait_closed()
