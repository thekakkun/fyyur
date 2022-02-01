"""empty message

Revision ID: 714c99ea6d9d
Revises: abd556a4da34
Create Date: 2022-01-18 14:54:44.017975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '714c99ea6d9d'
down_revision = 'abd556a4da34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist_genre', sa.Column('genre_name', sa.String(length=120), nullable=False))
    op.drop_constraint('artist_genre_genre_id_fkey', 'artist_genre', type_='foreignkey')

    op.create_foreign_key(None, 'artist_genre', 'genre', ['genre_name'], ['name'])
    op.execute('''
        UPDATE artist_genre
        SET genre_name = (
            SELECT name FROM genre WHERE artist_genre.genre_id = genre.id
        );
    ''')

    op.drop_column('artist_genre', 'genre_id')
    # op.drop_constraint('genre_name_key', 'genre', type_='unique')

    op.add_column('venue_genre', sa.Column('genre_name', sa.String(length=120), nullable=False))
    op.drop_constraint('venue_genre_genre_id_fkey', 'venue_genre', type_='foreignkey')
    
    op.create_foreign_key(None, 'venue_genre', 'genre', ['genre_name'], ['name'])
    op.execute('''
        UPDATE venue_genre
        SET genre_name = (
            SELECT name FROM genre WHERE venue_genre.genre_id = genre.id
        );
    ''')
    op.drop_column('venue_genre', 'genre_id')

    op.drop_column('genre', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue_genre', sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'venue_genre', type_='foreignkey')
    op.create_foreign_key('venue_genre_genre_id_fkey', 'venue_genre', 'genre', ['genre_id'], ['id'])
    op.drop_column('venue_genre', 'genre_name')
    op.add_column('genre', sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('genre_id_seq'::regclass)"), autoincrement=True, nullable=False))
    op.create_unique_constraint('genre_name_key', 'genre', ['name'])
    op.add_column('artist_genre', sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'artist_genre', type_='foreignkey')
    op.create_foreign_key('artist_genre_genre_id_fkey', 'artist_genre', 'genre', ['genre_id'], ['id'])
    op.drop_column('artist_genre', 'genre_name')
    # ### end Alembic commands ###
