"""initial

Revision ID: 0001
Revises:
Create Date: 2026-03-27

"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'monthly_energy',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('solar', sa.Float(), nullable=False, server_default='0'),
        sa.Column('load', sa.Float(), nullable=False, server_default='0'),
        sa.Column('grid_import', sa.Float(), nullable=False, server_default='0'),
        sa.Column('grid_export', sa.Float(), nullable=False, server_default='0'),
        sa.Column('battery_charge', sa.Float(), nullable=True),
        sa.Column('battery_discharge', sa.Float(), nullable=True),
        sa.Column('source', sa.String(), nullable=False, server_default='ha_sync'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('year', 'month', name='uq_monthly_energy_year_month'),
    )

    op.create_table(
        'cost',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(), nullable=False, server_default='RON'),
        sa.Column('operating_life_years', sa.Integer(), nullable=False, server_default='25'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'saving_offset',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False, server_default='0'),
        sa.Column('currency', sa.String(), nullable=False, server_default='RON'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'grid_price',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('price_per_kwh', sa.Float(), nullable=False),
        sa.Column('is_peak', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('currency', sa.String(), nullable=False, server_default='RON'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('year', 'month', 'is_peak', name='uq_grid_price_year_month_peak'),
    )

    op.create_table(
        'prosumer_pricing',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('import_price', sa.Float(), nullable=False),
        sa.Column('export_price', sa.Float(), nullable=False),
        sa.Column('fixed_tariff', sa.Float(), nullable=False, server_default='0'),
        sa.Column('tax', sa.Float(), nullable=False, server_default='0'),
        sa.Column('currency', sa.String(), nullable=False, server_default='RON'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('year', 'month', name='uq_prosumer_pricing_year_month'),
    )

    op.create_table(
        'app_config',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('location_name', sa.String(), nullable=False, server_default='My Home'),
        sa.Column('currency', sa.String(), nullable=False, server_default='RON'),
        sa.Column('language', sa.String(), nullable=False, server_default='ro'),
        sa.Column('sensor_solar', sa.String(), nullable=True),
        sa.Column('sensor_load', sa.String(), nullable=True),
        sa.Column('sensor_grid_import', sa.String(), nullable=True),
        sa.Column('sensor_grid_export', sa.String(), nullable=True),
        sa.Column('sensor_battery_charge', sa.String(), nullable=True),
        sa.Column('sensor_battery_discharge', sa.String(), nullable=True),
        sa.Column('last_sync', sa.DateTime(timezone=True), nullable=True),
        sa.Column('sync_enabled', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('app_config')
    op.drop_table('prosumer_pricing')
    op.drop_table('grid_price')
    op.drop_table('saving_offset')
    op.drop_table('cost')
    op.drop_table('monthly_energy')
