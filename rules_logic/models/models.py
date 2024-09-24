from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv
import asyncio

# Cargar las variables de entorno
load_dotenv()

# Crear la base declarativa
Base = declarative_base()

# Tabla de Piezas (pieces)
class Piece(Base):
    __tablename__ = 'pieces'
    id = Column(String(10), primary_key=True)  # El id será el identificador de la pieza, e.g., 'Pb', 'Rn'
    name = Column(String(50), nullable=False)  # Descripción de la pieza, e.g., 'Peón Blanco'
    value = Column(Integer, nullable=False)  # Valor de la pieza, e.g., 1 para peón blanco, -90 para rey negro

    # Relación con movimientos (ChessMove)
    moves = relationship('ChessMove', back_populates='piece_')  # Relación inversa a ChessMove

# Tabla de juegos (games)
class Game(Base):
    __tablename__ = 'games'
    
    session_id = Column(String(255), primary_key=True, nullable=False)  # session_id como clave primaria
    difficult = Column(String(10), nullable=False)  # dificultad (e.g., 'Facil', 'Normal', 'Dificil')
    timestamp = Column(DateTime, default=datetime.now, nullable=False)  # Marca de tiempo
    winner = Column(String(255), nullable=True)  # Ganador (puede empezar vacío)

    # Relación con los movimientos de ajedrez (ChessMove)
    moves = relationship('ChessMove', back_populates='game', cascade='all, delete')

# Tabla de movimientos de ajedrez (chess_moves)
class ChessMove(Base):
    __tablename__ = 'chess_moves'
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), ForeignKey('games.session_id'), nullable=False)
    piece = Column(String(10), ForeignKey('pieces.id'), nullable=True)  # Clave foránea referenciando 'pieces.id'
    move_from = Column(String(10), nullable=False)
    move_to = Column(String(10), nullable=False)
    turn = Column(Boolean, nullable=False)  # True para el jugador, False para la IA
    player_type = Column(String(10), nullable=False)  # 'true' para jugador, 'false' para IA

    # Relación con la tabla 'pieces'
    piece_ = relationship('Piece', back_populates='moves')  # Relación con la tabla 'pieces'
    game = relationship('Game', back_populates='moves')  # Relación con la tabla 'games'

# Crear el motor asincrónico
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_async_engine(DATABASE_URL, echo=True)

# Crear la sesión asincrónica
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Función asíncrona para crear las tablas
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Método para poblar la tabla pieces con las piezas y sus valores
async def populate_pieces():
    async with async_session() as session:
        try:
            async with session.begin():
                # Definir las piezas y sus valores
                pieces_data = [
                    {'id': 'Pb', 'name': 'Peón Blanco', 'value': 1},
                    {'id': 'Pn', 'name': 'Peón Negro', 'value': -1},
                    {'id': 'Cb', 'name': 'Caballo Blanco', 'value': 3},
                    {'id': 'Cn', 'name': 'Caballo Negro', 'value': -3},
                    {'id': 'Ab', 'name': 'Alfil Blanco', 'value': 3},
                    {'id': 'An', 'name': 'Alfil Negro', 'value': -3},
                    {'id': 'Tb', 'name': 'Torre Blanca', 'value': 5},
                    {'id': 'Tn', 'name': 'Torre Negra', 'value': -5},
                    {'id': 'RNb', 'name': 'Reina Blanca', 'value': 9},
                    {'id': 'RNn', 'name': 'Reina Negra', 'value': -9},
                    {'id': 'Rb', 'name': 'Rey Blanco', 'value': 90},
                    {'id': 'Rn', 'name': 'Rey Negro', 'value': -90}
                ]

                # Insertar las piezas en la base de datos
                for piece_data in pieces_data:
                    piece = Piece(id=piece_data['id'], name=piece_data['name'], value=piece_data['value'])
                    session.add(piece)

            await session.commit()
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            await session.rollback()

# Ejecutar la creación de tablas y poblar las piezas
async def main():
    await create_tables()
    await populate_pieces()

asyncio.run(main())
