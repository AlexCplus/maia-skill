from sqlalchemy.orm import Session

from src.data.models import Order, Portfolio, Position, Transaction


def list_portfolios(db: Session, owner_id: int) -> list[Portfolio]:
    return db.query(Portfolio).filter(Portfolio.owner_id == owner_id).order_by(Portfolio.id.asc()).all()


def create_portfolio(db: Session, owner_id: int, name: str, base_currency: str) -> Portfolio:
    portfolio = Portfolio(owner_id=owner_id, name=name, base_currency=base_currency)
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


def get_portfolio(db: Session, portfolio_id: int, owner_id: int) -> Portfolio | None:
    return db.query(Portfolio).filter(Portfolio.id == portfolio_id, Portfolio.owner_id == owner_id).first()


def list_positions(db: Session, portfolio_id: int) -> list[Position]:
    return (
        db.query(Position)
        .filter(Position.portfolio_id == portfolio_id)
        .order_by(Position.id.asc())
        .all()
    )


def create_position(
    db: Session,
    portfolio_id: int,
    symbol: str,
    quantity: float,
    avg_cost: float,
    asset_class: str,
) -> Position:
    position = Position(
        portfolio_id=portfolio_id,
        symbol=symbol.upper(),
        quantity=quantity,
        avg_cost=avg_cost,
        asset_class=asset_class,
    )
    db.add(position)
    db.commit()
    db.refresh(position)
    return position


def list_transactions(db: Session, portfolio_id: int) -> list[Transaction]:
    return (
        db.query(Transaction)
        .filter(Transaction.portfolio_id == portfolio_id)
        .order_by(Transaction.id.asc())
        .all()
    )


def create_transaction(
    db: Session,
    portfolio_id: int,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    fee: float,
) -> Transaction:
    transaction = Transaction(
        portfolio_id=portfolio_id,
        symbol=symbol.upper(),
        side=side.lower(),
        quantity=quantity,
        price=price,
        fee=fee,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def get_position_by_symbol(db: Session, portfolio_id: int, symbol: str) -> Position | None:
    return (
        db.query(Position)
        .filter(Position.portfolio_id == portfolio_id, Position.symbol == symbol.upper())
        .first()
    )


def upsert_position_after_fill(
    db: Session,
    portfolio_id: int,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    asset_class: str,
) -> Position | None:
    position = get_position_by_symbol(db, portfolio_id=portfolio_id, symbol=symbol)
    normalized_side = side.lower()
    normalized_symbol = symbol.upper()
    if normalized_side == "buy":
        if position is None:
            position = Position(
                portfolio_id=portfolio_id,
                symbol=normalized_symbol,
                quantity=quantity,
                avg_cost=price,
                asset_class=asset_class,
            )
            db.add(position)
        else:
            prev_qty = position.quantity
            new_qty = prev_qty + quantity
            position.avg_cost = ((prev_qty * position.avg_cost) + (quantity * price)) / new_qty
            position.quantity = new_qty
            position.asset_class = asset_class
    else:
        if position is None:
            return None
        if quantity > position.quantity:
            return None
        new_qty = position.quantity - quantity
        if new_qty == 0:
            db.delete(position)
            db.commit()
            return None
        position.quantity = new_qty
    db.commit()
    if position is not None:
        db.refresh(position)
    return position


def create_order(
    db: Session,
    order_id: str,
    portfolio_id: int,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    fee: float,
    notional: float,
    status: str,
) -> Order:
    order = Order(
        order_id=order_id,
        portfolio_id=portfolio_id,
        symbol=symbol.upper(),
        side=side.lower(),
        quantity=quantity,
        price=price,
        fee=fee,
        notional=notional,
        status=status,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def list_orders(db: Session, owner_id: int, portfolio_id: int | None = None) -> list[Order]:
    query = db.query(Order).join(Portfolio, Portfolio.id == Order.portfolio_id).filter(Portfolio.owner_id == owner_id)
    if portfolio_id is not None:
        query = query.filter(Order.portfolio_id == portfolio_id)
    return query.order_by(Order.id.asc()).all()


def list_orders_for_portfolio(db: Session, portfolio_id: int, owner_id: int) -> list[Order]:
    return (
        db.query(Order)
        .join(Portfolio, Portfolio.id == Order.portfolio_id)
        .filter(Order.portfolio_id == portfolio_id, Portfolio.owner_id == owner_id)
        .order_by(Order.executed_at.asc())
        .all()
    )

