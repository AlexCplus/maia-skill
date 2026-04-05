import uuid
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class FilledOrder:
    order_id: str
    symbol: str
    side: Literal["buy", "sell"]
    quantity: float
    price: float
    fee: float
    notional: float
    status: Literal["filled"] = "filled"


class PaperBroker:
    def submit_market_order(
        self,
        symbol: str,
        side: Literal["buy", "sell"],
        quantity: float,
        price: float,
        fee: float,
    ) -> FilledOrder:
        notional = quantity * price
        return FilledOrder(
            order_id=f"paper-{uuid.uuid4().hex[:12]}",
            symbol=symbol.upper(),
            side=side,
            quantity=quantity,
            price=price,
            fee=fee,
            notional=notional,
        )

