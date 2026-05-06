# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  space_station.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/27 18:12:11 by asulon          #+#    #+#               #
#  Updated: 2026/05/06 15:31:45 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional, Annotated


Pourcent = Annotated[float, Field(ge=0, le=100)]


class SpaceStation(BaseModel):
    station_id: Annotated[str, Field(min_length=3, max_length=10)]
    name: Annotated[str, Field(min_length=1, max_length=50)]
    crew_size: Annotated[int, Field(ge=1, le=20)]
    power_level: Pourcent
    oxygen_level: Pourcent
    last_maintenance: datetime
    is_operational: bool = True
    notes: Annotated[Optional[str], Field(max_length=200)] = None


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)

    valid_station = {"station_id": "NOS001",
                     "name": "Nostromo",
                     "crew_size": 8,
                     "power_level": 16,
                     "oxygen_level": 10,
                     "last_maintenance": datetime(2026, 5, 24)}

    invalid_station = {"station_id": "NOS001",
                       "name": "Nostromo",
                       "crew_size": 5353,
                       "power_level": 16,
                       "oxygen_level": 10,
                       "last_maintenance": datetime(2026, 5, 24)}
    try:
        nostromo = SpaceStation(**valid_station)
        print("Valid station created:")
        print(f"ID: {nostromo.station_id}")
        print(f"Name: {nostromo.name}")
        print(f"Crew: {nostromo.crew_size}")
        print(f"Power: {nostromo.power_level}")
        print(f"Oxygen: {nostromo.oxygen_level}")
        print("Status: "
              "Operational" if nostromo.is_operational else "Disfuntionnal")
    except ValidationError as e:
        for err in e.errors():
            field = ".".join(str(x) for x in err["loc"])
            print(f"Field {field}: {err['msg']}")

    print("=" * 40)

    try:
        print("Expected validation error:")
        nostromo = SpaceStation(**invalid_station)
        print("Valid station created:")
        print(f"ID: {nostromo.station_id}")
        print(f"Name: {nostromo.name}")
        print(f"Crew: {nostromo.crew_size}")
        print(f"Power: {nostromo.power_level}")
        print(f"Oxygen: {nostromo.oxygen_level}")
        print("Status: "
              "Operational" if nostromo.is_operational else "Disfuntionnal")
    except ValidationError as e:
        for err in e.errors():
            field = ".".join(str(x) for x in err["loc"])
            print(f"Field {field}: {err['msg']}")


if __name__ == "__main__":
    main()
