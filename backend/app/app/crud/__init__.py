from .crud_artifact import artifact
from .crud_category import category
from .crud_favorite import favorite
from .crud_globals import globals
from .crud_item import item
from .crud_model import model
from .crud_order import order
from .crud_poll import poll
from .crud_product import product
from .crud_product_option import product_option
from .crud_review import review
from .crud_user import user

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
