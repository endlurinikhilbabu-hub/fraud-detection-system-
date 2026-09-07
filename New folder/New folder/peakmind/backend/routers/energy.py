from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List, Dict, Any

from database import get_session
from models import EnergyLog
import sys
import os

# Add parent directory to path to import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.ai_coach import get_energy_suggestion

router = APIRouter(
    prefix="/api/energy",
    tags=["Energy"]
)

@router.get("/", response_model=List[EnergyLog])
def get_energy_logs(user_id: str, session: Session = Depends(get_session)):
    logs = session.exec(select(EnergyLog).where(EnergyLog.user_id == user_id).order_by(EnergyLog.logged_at.desc())).all()
    return logs

@router.post("/")
def log_energy(energy_log: EnergyLog, session: Session = Depends(get_session)):
    session.add(energy_log)
    session.commit()
    session.refresh(energy_log)
    
    # Get AI Suggestion
    suggestion = get_energy_suggestion(energy_log.score, energy_log.mood)
    
    return {
        "log": energy_log,
        "ai_suggestion": suggestion
    }
