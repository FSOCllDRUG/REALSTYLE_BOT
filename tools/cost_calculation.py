from decimal import Decimal

from tools.config_manager import read_config


async def calculate_cost(price: Decimal, category: str) -> Decimal:
    """
    Calculate the cost based on the price and category.

    Args:
    price (Decimal): The price of the item.
    category (str): The category of the item. Can be "L", "M", "S", or "XS".

    Returns:
    Decimal: The calculated cost.
    """
    # Load config from json file
    cfg = await read_config()

    # Get rate from config
    rate = Decimal(cfg["rate"])

    # Get insurance and redemption from config
    insurance_redemption = Decimal(cfg["insurance_redemption"])

    # Get ship and margin from config based on category
    ship = Decimal(cfg[f"ship_{category}"])
    margin = Decimal(cfg[f"margin_{category}"])

    # Calculate cost
    cost = price * rate * ((100 + insurance_redemption) / 100) + ship + margin

    return cost
