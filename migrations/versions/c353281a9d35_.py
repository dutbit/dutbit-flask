"""empty message

Revision ID: c353281a9d35
Revises: 42f2541a6329
Create Date: 2023-09-11 11:06:35.905374

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c353281a9d35'
down_revision = '42f2541a6329'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('enroll_candidates', sa.Column('politic', sa.String(length=20), server_default='群众', nullable=False))
    op.add_column('enroll_candidates', sa.Column('major', sa.Text(), nullable=True))
    op.add_column('enroll_candidates', sa.Column('major_class', sa.Text(), nullable=True))
    op.add_column('enroll_candidates', sa.Column('advantage', sa.Text(), nullable=True))
    op.add_column('enroll_candidates', sa.Column('other_advantage', sa.Text(), nullable=True))
    op.add_column('enroll_candidates', sa.Column('birth_date', sa.Text(), nullable=True))
    op.add_column('enroll_candidates', sa.Column('role', sa.Text(), nullable=True))
    op.add_column('enroll_candidates', sa.Column('student_exp', sa.Text(), nullable=True))
    op.alter_column('media_list', 'media_id',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_general_ci', length=1024),
               comment='视频ID',
               existing_comment='视频ID, 姓名的md5',
               existing_nullable=False)
    op.drop_column('media_list', 'uuid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('media_list', sa.Column('uuid', mysql.VARCHAR(collation='utf8mb4_general_ci', length=24), nullable=False))
    op.alter_column('media_list', 'media_id',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_general_ci', length=1024),
               comment='视频ID, 姓名的md5',
               existing_comment='视频ID',
               existing_nullable=False)
    op.drop_column('enroll_candidates', 'student_exp')
    op.drop_column('enroll_candidates', 'role')
    op.drop_column('enroll_candidates', 'birth_date')
    op.drop_column('enroll_candidates', 'other_advantage')
    op.drop_column('enroll_candidates', 'advantage')
    op.drop_column('enroll_candidates', 'major_class')
    op.drop_column('enroll_candidates', 'major')
    op.drop_column('enroll_candidates', 'politic')
    # ### end Alembic commands ###
