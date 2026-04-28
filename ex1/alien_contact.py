# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  alien_contact.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/28 01:41:46 by asulon          #+#    #+#               #
#  Updated: 2026/04/28 02:40:40 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from typing import Optional, Annotated, Self
from enum import Enum


class ContactType(Enum):
    RADIO = "radio",
    VISUAL = "visual",
    PHYSICAL = "physical",
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: Annotated[str, Field(min_length=5, max_length=15)]
    timestamp: datetime
    location: Annotated[str, Field(min_length=3, max_length=100)]
    contact_type: ContactType
    signal_strength: Annotated[float, Field(ge=0, le=10.0)]
    duration_minutes: Annotated[int, Field(ge=1, le=1440)]
    witness_count: Annotated[int, Field(ge=1, le=100)]
    message_received: Annotated[Optional[str], Field(max_length=500)]
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_after(self: Self) -> Self:
        if not self.contact_id.startswith("AC"):
            raise ValueError("contact_id field must start with 'AC'")
        if (self.contact_type == ContactType.PHYSICAL and
                not self.is_verified):
            raise ValueError("Physical contact must be verified")
        if (self.contact_type == ContactType.TELEPATHIC and
                self.witness_count < 3):
            raise ValueError(
                "witness_count must be greater or equal than 3")
        if (self.message_received and
                len(self.message_received.strip()) > 0 and
                self.signal_strength <= 7):
            raise ValueError(
                "signal_strength must be stronger than 7")

        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 40)

    valid_report = {
        "contact_id": "AC_2026_01",
        "timestamp": datetime(2026, 5, 24),
        "location": "Area 51, Nevada",
        "contact_type": ContactType.TELEPATHIC,
        "signal_strength": 8.5,
        "duration_minutes": 45,
        "witness_count": 5,
        "message_received": "Greetings from Zeta Reticuli",
        "is_verified": False
    }
    invalid_report = {
        "contact_id": "DE_2026_01",
        "timestamp": datetime(2026, 5, 24),
        "location": "Ar",
        "contact_type": ContactType.TELEPATHIC,
        "signal_strength": 18.5,
        "duration_minutes": 11145,
        "witness_count": 0,
        "message_received": "Greetings from Zeta Reticuli",
        "is_verified": False
    }
    try:
        print("Valid contact report:")
        valid = AlienContact(**valid_report)
        print(f"ID: {valid.contact_id}")
        print(f"Type: {valid.contact_type.value}")
        print(f"Location {valid.location}")
        print(f"Signal: {valid.signal_strength}/10")
        print(f"Duration: {valid.duration_minutes} minutes")
        print(f"Witnnes: {valid.witness_count}")
        print(f"Message: '{valid.message_received}'\n")
    except ValidationError as e:
        for err in e.errors():
            field = ".".join(str(x) for x in err["loc"])
            print(f"Field {field}: {err["msg"]}")

    print("=" * 40)
    try:
        print("Expected validation error:")
        invalid = AlienContact(**invalid_report)
        print(f"ID: {invalid.contact_id}")
        print(f"Type: {invalid.contact_type.value}")
        print(f"Location {invalid.location}")
        print(f"Signal: {invalid.signal_strength}/10")
        print(f"Duration: {invalid.duration_minutes} minutes")
        print(f"Witnnes: {invalid.witness_count}")
        print(f"Message: '{invalid.message_received}'")
    except ValidationError as e:
        for err in e.errors():
            field = ".".join(str(x) for x in err["loc"])
            print(f"Field {field}: {err["msg"]}")


if __name__ == "__main__":
    main()
