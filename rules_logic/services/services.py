import os
import asyncio
import random
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, joinedload,load_only
from sqlalchemy import select, text, and_, func
from models.models import ChessMove, Game,DecisionTree

# Crear un AsyncEngine en lugar del engine normal
engine = create_async_engine(os.getenv('DATABASE_URL'), echo=True, future=True)

# Crear una AsyncSession para manejar las transacciones asíncronas
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Función asincrónica para iniciar el juego
async def start_game(session_id, difficult, winner=None):
    async with async_session() as session:
        try:
            new_game = Game(
                session_id=session_id,
                difficult=difficult,
                winner=winner
            )
            session.add(new_game)
            await session.commit()  # Usar await para commit asíncrono
            return True
        except Exception as e:
            print(e)
            await session.rollback()  # Rollback asíncrono
            return False

# Función asincrónica para registrar un movimiento
async def make_move_Service(session_id, piece, move_from, move_to, turn, player_type):
    async with async_session() as session:
        try:
            new_move = ChessMove(
                session_id=session_id,
                piece=piece,
                move_from=move_from,
                move_to=move_to,
                turn=turn,
                player_type=player_type  # Movimiento del jugador
            )
            session.add(new_move)
            await session.commit()  # Commit asíncrono
            return True
        except Exception as e:
            print(e)
            await session.rollback()  # Rollback asíncrono
            return None

# Función asincrónica para cambiar la dificultad
async def change_difficult(session_id, new_difficult):
    async with async_session() as session:
        try:
            game = await session.get(Game, session_id)
            if game:
                game.difficult = new_difficult
                await session.commit()  # Commit asíncrono
                return True
            return False
        except Exception as e:
            print(e)
            await session.rollback()  # Rollback asíncrono
            return False

async def set_winner(session_id, winner):
    async with async_session() as session:
        try:
            game = await session.get(Game, session_id)
            if game:
                game.winner = winner
                await session.commit()  # Commit asíncrono
                return True
            return False
        except Exception as e:
            print(e)
            await session.rollback()  # Rollback asíncrono
            return False
        
async def get_decision():
    async with async_session() as session:
        try:
         
            total_records = await session.scalar(select(func.count(DecisionTree.id)))
            
            if total_records == 0:
                return None 

            random_id = random.randint(1, total_records)

            result = await session.execute(
                select(DecisionTree)
                .where(DecisionTree.id == random_id)
                .options(load_only(DecisionTree.movimiento_sugerido, DecisionTree.v1, DecisionTree.v2, DecisionTree.v3, DecisionTree.v4, DecisionTree.v5, DecisionTree.v6, DecisionTree.v7, DecisionTree.v8, DecisionTree.v9, DecisionTree.v10))
            )
            decision = result.scalar_one_or_none()

            if decision:
                variables = [decision.v1, decision.v2, decision.v3, decision.v4, decision.v5, decision.v6, decision.v7, decision.v8, decision.v9, decision.v10]
                return {
                    'movimiento_sugerido': decision.movimiento_sugerido,
                    'variables': variables
                }
            else:
                return None

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            await session.rollback()
            return None