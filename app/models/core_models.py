from enum import Enum
from sqlmodel import JSON, Relationship, SQLModel, Field
from typing import List, Optional
from datetime import datetime,timezone

class UserRole(str, Enum):
    ADMIN = "admin"
    AGENT = "agent"
    CASINO = "casino"




class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(nullable=False, unique=True, index=True)
    password_hash: str = Field(nullable=False)
    
    role: UserRole = Field(nullable=False, description="admin, agent, or casino")

    # Only used when role == 'casino'
    casino_id: Optional[int] = Field(default=None, foreign_key="casino.id")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)
    
    # Relationships
    casino: Optional["Casino"] = Relationship(back_populates="user")






class Casino(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Unique username for login (can be email or custom string)
    # username: str = Field(index=True, unique=True, nullable=False, max_length=50)
    
    # # Store password hash (never store plain text password)
    # password_hash: str = Field(nullable=False)
    
    # Commission percentage the casino pays me 30 (e.g., 0.3 for 30%)
    commission_rate: float = Field(default=0.3, description="Commission percentage, e.g., 0.02 for 2%")
    
    # Casino display name (friendly)
    name: str = Field(nullable=False, max_length=100)
    
    # Contact email or phone (optional)
    contact_email: Optional[str] = Field(unique=True,default=None, max_length=25)
    contact_phones: List[str] = Field(default_factory=list, sa_type=JSON)
    
   
    
    # Track creation and update time for auditing
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) ,nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) , nullable=False)
    
    
    # Status flag: active/inactive (for banning or disabling casinos)
    is_active: bool = Field(default=True, description="Is casino active and allowed to play")

    # Relationships
    user: Optional["User"] = Relationship(back_populates="casino")

    tickets: List["Ticket"] = Relationship(back_populates="casino")
    round_profits: List["CasinoProfitPerRound"] = Relationship(back_populates="casino")
    transactions: List["Transaction"] = Relationship(back_populates="casino")









class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign keys
    casino_id: int = Field(foreign_key="casino.id", nullable=False)
    round_id: int = Field(foreign_key="round.id", nullable=False)
    
    casino:Optional["Casino"]=Relationship(back_populates="tickets")
    round: Optional["Round"] = Relationship(back_populates="tickets")




    # Ticket code is unique and tied to round (for fraud prevention)
    ticket_code: str = Field(nullable=False, unique=True, index=True, description="Printed code for validation")

    # Multiplier guess placed by the player
    guessed_multiplier: float = Field(nullable=False, description="The multiplier guessed by the player")

    # Bet amount placed on the ticket
    bet_amount: float = Field(nullable=False, ge=0)

    # Timestamp of when ticket was created
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Computed fields after round ends
    actual_multiplier: Optional[float] = Field(default=None, description="Crash multiplier of the round")
    is_winner: Optional[bool] = Field(default=None, description="True if guessed_multiplier <= actual_multiplier")
    payout_amount: Optional[float] = Field(default=None, ge=0, description="Amount to pay out if winner")
    is_redeemed: bool = Field(default=False, description="Flag to track if payout was claimed")

  






class CasinoProfitPerRound(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign Keys
    casino_id: int = Field(foreign_key="casino.id", nullable=False)
    round_id: int = Field(foreign_key="round.id", nullable=False)

    # Relationships
    casino: Optional["Casino"] = Relationship(back_populates="round_profits")
    round: Optional["Round"] = Relationship(back_populates="casino_profits")

    # Financial fields
    total_bet_amount: float = Field(default=0.0, ge=0.0, description="Total amount bet by players at this casino for this round")
    total_payout_amount: float = Field(default=0.0, ge=0.0, description="Total amount casino should pay to winners")
    profit: float = Field(default=0.0, description="Net profit for this casino for this round")
    commission_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Commission rate (%) to take from profit")
    commission_amount: float = Field(default=0.0, ge=0.0, description="Amount the casino owes to admin")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))



class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    casino_id: int = Field(foreign_key="casino.id", nullable=False)
    casino: Optional["Casino"] = Relationship(back_populates="transactions")

    amount: float = Field(ge=0, description="Amount sent by the casino operator to admin")
    reference_id: Optional[str] = Field(default=None, description="External reference (screenshot ID, payment gateway txn ID, etc.)")
    note: Optional[str] = Field(default=None, description="Optional note like 'payment for round 120–126'")
    
    is_verified: bool = Field(default=False, description="Set True by admin after confirming payment")

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the transaction was submitted")



class Round(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    round_number: int = Field(index=True, unique=True, description="Sequential global round number")

    server_seed: str = Field(description="Server seed used in hash generation")
    commitment_hash: str = Field(description="Hash shared before round starts to prove fairness")
    multiplier: Optional[float] = Field(default=None, ge=1.0, description="Crash multiplier revealed at end")

    state: str = Field(default="pending", description="Round state: pending, running, ended")
    start_time: Optional[datetime] = Field(default=None, description="When round started (UTC)")
    end_time: Optional[datetime] = Field(default=None, description="When round ended (UTC)")

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Time when this round was created"
    )

    # Relationships
    tickets: List["Ticket"] = Relationship(back_populates="round")
    casino_profits: List["CasinoProfitPerRound"] = Relationship(back_populates="round")
    
