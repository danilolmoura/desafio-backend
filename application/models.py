import enum

from sqlalchemy import Column, ForeignKey, types
from sqlalchemy.dialects import postgresql

from application import db


class EnumBikeTripType(enum.IntEnum):
    TRABALHO = 1
    ATIVIADADE_FISICA = 2
    LAZER = 3
    DESLOCAMENTO = 4


class Trip(db.Model):
    """Define schema for trip table
    """

    id = db.Column(
        db.Integer,
        primary_key=True,
        doc='id da viagem')

    data_inicio = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        index=True,
        default=db.func.now(),
        doc='Data início da viagem')

    data_fim = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        index=True,
        default=db.func.now(),
        doc='Data fim da viagem')

    classificacao = db.Column(
        types.Enum(EnumBikeTripType, name='enum_bike_trip_type'),
        nullable=True,
        doc=u'Classificacão da viagem')

    nota = db.Column(
        db.Integer(),
        nullable=True,
        doc='Nota da viagem')

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False)

    user = db.relationship('User')


class User(db.Model):
    """Define schema for user table
    """

    id = db.Column(
        db.Integer,
        primary_key=True,
        doc='id do usuário')

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        index=True,
        default=db.func.now(),
        doc='Data de criação')

    email = db.Column(
        db.String(),
        nullable=False,
        doc='E-mail do usuário')

    name = db.Column(
        db.String(),
        nullable=False,
        doc='Nome do usuário')

    password = db.Column(
        db.String(),
        nullable=False,
        doc='Senha do usuário')
