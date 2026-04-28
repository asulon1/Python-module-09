# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  space_crew.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/28 02:41:17 by asulon          #+#    #+#               #
#  Updated: 2026/04/28 03:33:34 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from datetime import datetime
from enum import Enum
from typing import Annotated, Self
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(Enum):
    CADER = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: Annotated[str, Field(min_length=3, max_length=10)]
    name: Annotated[str, Field(min_length=2, max_length=50)]
    rank: Rank
    age: Annotated[int, Field(ge=18, le=80)]
    specialization: Annotated[str, Field(min_length=3, max_length=30)]
    years_experience: Annotated[int, Field(ge=0, le=50)]
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: Annotated[str, Field(min_length=5, max_length=15)]
    mission_name: Annotated[str, Field(min_length=3, max_length=100)]
    destination: Annotated[str, Field(min_length=3, max_length=50)]
    launch_date: datetime
    duration_days: Annotated[int, Field(ge=1, le=3650)]
    crew: Annotated[list[CrewMember], Field(min_length=1, max_length=12)]
    mission_status: Annotated[str, Field()] = "planned"
    budget_millions: Annotated[float, Field(ge=1, le=10000)]

    @model_validator(mode="after")
    def validation_after(self: Self) -> Self:
        valid_rank = False
        experimented_member = 0
        if not self.mission_id.startswith('M'):
            raise ValueError("Mission ID must start with 'M'")
        for member in self.crew:
            if not member.is_active:
                raise ValueError("All members of the crew must be active")
            if member.rank == Rank.COMMANDER or member.rank == Rank.CAPTAIN:
                valid_rank = True
            if member.years_experience >= 5:
                experimented_member += 1
        if not valid_rank:
            raise ValueError("Crew needs a Captain or a Commander")
        if (self.duration_days > 365 and
                experimented_member < len(self.crew) / 2):
            raise ValueError(
                "Need more experimented members for long mission")

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 40)

    travelers = []
    try:
        travelers: list[CrewMember] = [
            CrewMember(member_id="CPT_001",
                       name="Solanum",
                       rank=Rank.COMMANDER,
                       age=18,
                       specialization="Quantic explorer",
                       years_experience=50,
                       is_active=True),
            CrewMember(member_id="PSN_001",
                       name="Feldspath",
                       rank=Rank.CADER,
                       age=40,
                       specialization="Pilot",
                       years_experience=2,
                       is_active=True)]
    except ValidationError as e:
        for err in e.errors():
            field = ".".join(str(x) for x in err["loc"])
            print(f"Field {field}: {err['msg']}")

    valid_mission = {
        "mission_id": "M1900_EOTE",
        "mission_name": "Echoes of the eye",
        "destination": "Eye of the universe",
        "launch_date": datetime(1900, 1, 1),
        "duration_days": 3640,
        "crew": travelers,
        "budget_millions": 10000
    }
    invalid_mission = {}
    try:
        print("Expected validation error:")
        valid = SpaceMission(**valid_mission)
        print(f"Mission: {valid.mission_name}")
        print(f"ID: {valid.mission_id}")
        print(f"Destination {valid.destination}")
        print(f"Duration: {valid.duration_days} days")
        print(f"Budget: ${valid.budget_millions:.1f}M")
        print(f"Crew size: {len(valid.crew)}")
        print("Crew members")
        for member in valid.crew:
            print(
                f" - {member.name} ({member.rank.value}) - "
                f"{member.specialization}"
            )
    except ValidationError as e:
        for err in e.errors():
            field = ".".join(str(x) for x in err["loc"])
            print(f"Field {field}: {err['msg']}")


if __name__ == "__main__":
    main()
