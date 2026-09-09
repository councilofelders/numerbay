from contextlib import ExitStack
from typing import Dict, Generator, List, Optional, Tuple
from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app import crud, models
from app.api.dependencies import numerai
from app.schemas import ProductOptionCreate
from app.schemas.product import ProductCreate, ProductUpdate
from app.tests.utils.category import create_random_category
from app.tests.utils.product import get_random_product
from app.tests.utils.user import get_random_user
from app.tests.utils.utils import random_decimal, random_lower_string


def test_create_product(db: Session) -> None:
    name = random_lower_string()
    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, category_id=1, description=description, options=[]
    )
    with get_random_user(db) as user:
        product = crud.product.create_with_owner(
            db=db, obj_in=product_in, owner_id=user.id, sku=sku
        )
        product_option_in = ProductOptionCreate(
            price=price, is_on_platform=False, currency="USD", product_id=product.id
        )
        crud.product_option.create(db, obj_in=product_option_in)
        assert product.name == name
        assert product.description == description
        assert product.owner.id == user.id
        assert product.options[0].price == price  # type: ignore

        crud.product.remove(db=db, id=product.id)


def test_search_product(db: Session) -> None:
    name = random_lower_string()
    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, category_id=1, description=description, options=[]
    )
    with get_random_user(db) as user:
        product = crud.product.create_with_owner(
            db=db, obj_in=product_in, owner_id=user.id, sku=sku
        )
        product_option_in = ProductOptionCreate(
            price=price, is_on_platform=False, currency="USD", product_id=product.id
        )
        crud.product_option.create(db, obj_in=product_option_in)

        stored_product = crud.product.search(db=db, id=product.id)
        assert stored_product
        assert stored_product["total"] == 1
        assert product.name == stored_product["data"][0].name

        stored_product = crud.product.search(db=db, term=name[:5])
        assert stored_product
        assert stored_product["total"] > 0

        stored_product = crud.product.search(db=db, filters={"user": {"in": [user.id]}})
        assert stored_product
        assert stored_product["total"] > 0

        crud.product.remove(db=db, id=product.id)


def test_get_multiple_products(db: Session) -> None:
    name = random_lower_string()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, category_id=1, description=description, options=[]
    )
    with get_random_user(db) as user:
        product = crud.product.create_with_owner(
            db=db, obj_in=product_in, owner_id=user.id, sku=sku
        )
        stored_product = crud.product.get_multi_by_category(db=db, category_id=1)
        assert stored_product
        assert len(stored_product) > 0

        stored_product = crud.product.get_multi_by_owner(db=db, owner_id=user.id)
        assert stored_product
        assert len(stored_product) > 0

        crud.product.remove(db=db, id=product.id)


def test_get_product(db: Session) -> None:
    name = random_lower_string()
    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, category_id=1, description=description, options=[]
    )
    with get_random_user(db) as user:
        product = crud.product.create_with_owner(
            db=db, obj_in=product_in, owner_id=user.id, sku=sku
        )
        product_option_in = ProductOptionCreate(
            price=price, is_on_platform=False, currency="USD", product_id=product.id
        )
        crud.product_option.create(db, obj_in=product_option_in)

        stored_product = crud.product.get(db=db, id=product.id)
        assert stored_product
        assert product.id == stored_product.id
        assert product.name == stored_product.name
        assert product.options[0].price == stored_product.options[0].price  # type: ignore
        assert product.description == stored_product.description
        assert product.owner.id == stored_product.owner_id

        stored_product = crud.product.get_by_sku(db=db, sku=sku)
        assert stored_product
        assert product.id == stored_product.id

        crud.product.remove(db=db, id=product.id)


def test_update_product(db: Session) -> None:
    name = random_lower_string()
    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, category_id=1, description=description, options=[]
    )
    with get_random_user(db) as user:
        product = crud.product.create_with_owner(
            db=db, obj_in=product_in, owner_id=user.id, sku=sku
        )
        product_option_in = ProductOptionCreate(
            price=price, is_on_platform=False, currency="USD", product_id=product.id
        )
        crud.product_option.create(db, obj_in=product_option_in)
        product = crud.product.get(db, id=product.id)  # type: ignore

        description2 = random_lower_string()
        product_update = ProductUpdate(description=description2)
        product2 = crud.product.update(db=db, db_obj=product, obj_in=product_update)
        assert product.id == product2.id
        assert product.name == product2.name
        assert product.options[0].price == product2.options[0].price  # type: ignore
        assert product2.description == description2
        assert product.owner.id == product2.owner_id

        crud.product.remove(db=db, id=product.id)


def test_expire_products(db: Session) -> None:
    name = random_lower_string()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name,
        category_id=1,
        description=description,
        expiration_round=280,
        options=[],
    )
    with get_random_user(db) as user:
        product = crud.product.create_with_owner(
            db=db, obj_in=product_in, owner_id=user.id, sku=sku
        )
        description2 = random_lower_string()
        product_update = ProductUpdate(description=description2)
        product2 = crud.product.update(db=db, db_obj=product, obj_in=product_update)
        assert product.id == product2.id
        assert product.name == product2.name
        assert product.expiration_round == 280
        assert product.is_active

        crud.product.bulk_expire(db, current_round=281)
        product3 = crud.product.get(db, id=product.id)
        assert product3
        assert not product3.is_active

        crud.product.remove(db=db, id=product.id)


def test_delete_product(db: Session) -> None:
    name = random_lower_string()
    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, sku=sku, category_id=1, description=description, options=[]
    )
    with get_random_user(db) as user:
        product = crud.product.create_with_owner(
            db=db, obj_in=product_in, owner_id=user.id, sku=sku
        )
        product_option_in = ProductOptionCreate(
            price=price, is_on_platform=False, currency="USD", product_id=product.id
        )
        crud.product_option.create(db, obj_in=product_option_in)

        product2 = crud.product.remove(db=db, id=product.id)
        product3 = crud.product.get(db=db, id=product.id)
        assert product3 is None
        assert product2.id == product.id
        assert product2.name == name
        assert product2.options[0].price == price  # type: ignore
        assert product2.description == description
        assert product2.owner.id == user.id


@pytest.fixture
def ranking_catalog(db: Session) -> Generator:
    category = create_random_category(db)
    category.tournament = 8
    try:
        with ExitStack() as stack:
            user = stack.enter_context(get_random_user(db))
            products = [
                stack.enter_context(get_random_product(db, owner_id=user.id))
                for _ in range(7)
            ]
            for product in products:
                product.category_id = category.id
            db.commit()
            yield category, products
    finally:
        crud.category.remove(db, id=category.id)


@pytest.mark.parametrize(
    "tournament,weights,sort,expected_order",
    [
        (8, {"corr60": 3, "mmc60": 15}, None, [2, 1, 0, 3, 6, 5, 4]),
        (11, {"alpha": 0.3, "mpc": 0.8}, None, [0, 2, 1, 3, 6, 5, 4]),
        (12, {"corr": 0.1, "mmc": 1}, None, [2, 1, 0, 3, 6, 5, 4]),
        (11, {"neutral_corr": 2, "neutral_mmc": 4}, None, [0, 2, 1, 3, 6, 5, 4]),
        (8, {"corr60": 3, "mmc60": 15}, "payout-score-up", [3, 0, 2, 1, 6, 5, 4]),
        (8, {"corr60": 3, "mmc60": 15}, "payout-score-down", [2, 1, 0, 3, 6, 5, 4]),
    ],
)
def test_payout_sort_orders_before_pagination(
    db: Session,
    monkeypatch: pytest.MonkeyPatch,
    ranking_catalog: Tuple[models.Category, List[models.Product]],
    tournament: int,
    weights: Dict[str, float],
    sort: Optional[str],
    expected_order: List[int],
) -> None:
    category, products = ranking_catalog
    category.tournament = tournament
    first, second = weights
    reputations = [
        {first: 0.4, second: 0},
        {first: 0, second: 0.1},
        {first: 0, second: 0.1},
        {first: -0.1, second: 0},
        {first: 1000},
        {first: 1000, second: None},
        None,
    ]
    for product, reps in zip(products, reputations):
        product.model.tournament = tournament
        product.model.latest_reps = reps
    db.commit()
    config = {"payout_scores": weights}
    fetch = Mock(return_value=config)
    monkeypatch.setattr(numerai, "get_payout_score_config", fetch)
    expected_ids = [products[index].id for index in expected_order]

    result = crud.product.search(db, category_id=category.id, sort=sort)
    assert [p.id for p in result["data"]] == expected_ids
    assert result["ranking"]["config"] == config
    assert result["ranking"]["effective_sort"] == (sort or "payout-score-down")

    pages = []
    for offset in range(0, 7, 2):
        page = crud.product.search(
            db, category_slug=category.slug, sort=sort, skip=offset, limit=2
        )
        assert page["total"] == 7
        pages.extend(p.id for p in page["data"])
    assert pages == expected_ids
    fetch.assert_called_with(tournament)


def test_legacy_sort_keeps_its_formula_without_fetching_config(
    db: Session,
    monkeypatch: pytest.MonkeyPatch,
    ranking_catalog: Tuple[models.Category, List[models.Product]],
) -> None:
    category, products = ranking_catalog
    products[0].model.latest_reps = {"canon_corr": 0.4, "canon_mmc": 0}
    products[1].model.latest_reps = {"canon_corr": 0, "canon_mmc": 0.1}
    db.commit()
    fetch = Mock()
    monkeypatch.setattr(numerai, "get_payout_score_config", fetch)

    result = crud.product.search(
        db, category_id=category.id, sort="0.75corr2.25mmc-down"
    )
    assert result["data"][0].id == products[0].id
    assert result["ranking"]["effective_sort"] == "0.75corr2.25mmc-down"
    fetch.assert_not_called()


@pytest.mark.parametrize("scoped", [True, False])
def test_payout_sort_falls_back_to_latest(
    db: Session,
    monkeypatch: pytest.MonkeyPatch,
    ranking_catalog: Tuple[models.Category, List[models.Product]],
    scoped: bool,
) -> None:
    category, products = ranking_catalog
    fetch = Mock(return_value={})
    monkeypatch.setattr(numerai, "get_payout_score_config", fetch)
    ids = [p.id for p in products]

    result = crud.product.search(
        db,
        category_id=category.id if scoped else None,
        filters={"id": {"in": ids}},
        sort="payout-score-down",
    )
    assert [p.id for p in result["data"]] == list(reversed(ids))
    assert result["ranking"] == {"effective_sort": "latest", "config": {}}
    if scoped:
        fetch.assert_called_once_with(8)
    else:
        fetch.assert_not_called()


@pytest.fixture
def payout_api(monkeypatch: pytest.MonkeyPatch) -> Tuple[Mock, Mock, Dict]:
    monkeypatch.setattr(numerai, "_payout_score_cache", {})
    clock = Mock(return_value=1000.0)
    monkeypatch.setattr(numerai, "monotonic", clock)
    current_round = {
        "number": 1350,
        "roundScoreConfigs": [
            {"displayName": "corr60", "isPayout": True, "defaultMultiplier": 3},
        ],
    }
    response = Mock()
    response.json.return_value = {"data": {"rounds": [current_round]}}
    post = Mock(return_value=response)
    monkeypatch.setattr(numerai.requests, "post", post)
    return post, clock, current_round


def test_payout_config_uses_exact_nonzero_payout_scores(
    payout_api: Tuple[Mock, Mock, Dict],
) -> None:
    post, _, current_round = payout_api
    current_round["roundScoreConfigs"][0]["displayName"] = "neutral_corr"
    current_round["roundScoreConfigs"].extend(
        [
            {"displayName": "canon_corr", "isPayout": False, "defaultMultiplier": 1},
            {"displayName": "unused", "isPayout": True, "defaultMultiplier": 0},
        ]
    )
    config = numerai.get_payout_score_config(11)
    assert config["payout_scores"] == {"neutral_corr": 3}
    assert post.call_args.kwargs["timeout"] == (3, 5)
    assert post.call_args.kwargs["json"]["variables"] == {"tournament": 11}


def test_payout_config_refreshes_after_five_minutes(
    payout_api: Tuple[Mock, Mock, Dict],
) -> None:
    post, clock, current_round = payout_api
    initial = numerai.get_payout_score_config(8)
    clock.return_value = 1299.0
    assert numerai.get_payout_score_config(8) == initial
    assert post.call_count == 1

    clock.return_value = 1300.0
    current_round["number"] = 1351
    current_round["roundScoreConfigs"][0]["displayName"] = "new_score"
    refreshed = numerai.get_payout_score_config(8)
    assert refreshed["round_number"] == 1351
    assert refreshed["payout_scores"] == {"new_score": 3}
    assert post.call_count == 2


@pytest.mark.parametrize("cached", [True, False])
@pytest.mark.parametrize("failure", ["http", "graphql"])
def test_payout_config_retries_failures_without_erasing_cache(
    payout_api: Tuple[Mock, Mock, Dict], cached: bool, failure: str
) -> None:
    post, clock, _ = payout_api
    expected = numerai.get_payout_score_config(8) if cached else {}
    if failure == "http":
        post.side_effect = numerai.requests.RequestException("Unavailable")
    else:
        post.return_value.json.return_value = {"errors": [{"message": "Unavailable"}]}

    clock.return_value = 1300.0
    assert numerai.get_payout_score_config(8) == expected
    attempts = post.call_count
    clock.return_value = 1359.0
    assert numerai.get_payout_score_config(8) == expected
    assert post.call_count == attempts
    clock.return_value = 1360.0
    assert numerai.get_payout_score_config(8) == expected
    assert post.call_count == attempts + 1
