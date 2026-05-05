from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas


router = APIRouter(
    prefix="/interactions",
    tags=["Interactions"]
)

@router.post("/", response_model=schemas.InteractionResponse)
def create_interaction(
    interaction: schemas.InteractionCreate,
    db: Session = Depends(get_db)
):
    new_interaction = models.Interaction(**interaction.model_dump())

    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)

    return new_interaction

@router.get("/{interaction_id}", response_model=schemas.InteractionResponse)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    interaction = db.query(models.Interaction).filter(
        models.Interaction.id == interaction_id
    ).first()

    if not interaction:
        return {"error": "Interaction not found"}

    return interaction


@router.put("/{interaction_id}", response_model=schemas.InteractionResponse)
def update_interaction(
    interaction_id: int,
    updated_data: schemas.InteractionCreate,
    db: Session = Depends(get_db)
):
    interaction = db.query(models.Interaction).filter(
        models.Interaction.id == interaction_id
    ).first()

    if not interaction:
        return {"error": "Interaction not found"}

    for key, value in updated_data.model_dump().items():
        setattr(interaction, key, value)

    db.commit()
    db.refresh(interaction)

    return interaction


@router.patch("/{interaction_id}", response_model=schemas.InteractionResponse)
def update_interaction(
    interaction_id: int,
    updated_data: schemas.InteractionUpdate,
    db: Session = Depends(get_db)
):
    interaction = db.query(models.Interaction).filter(
        models.Interaction.id == interaction_id
    ).first()

    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    update_fields = updated_data.model_dump(exclude_unset=True)

    for key, value in update_fields.items():
        setattr(interaction, key, value)

    db.commit()
    db.refresh(interaction)

    return interaction


@router.get("/")
def get_interactions(db: Session = Depends(get_db)):
    interactions = db.query(models.Interaction).all()
    return interactions


# @router.get("/")
# def get_interactions():
#     return {
#         "message": "Interactions route working",
#         "data": []
#     }