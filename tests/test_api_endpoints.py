from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_all_machine_test_api_requirements():
    prefix = f"pytest-{uuid4().hex[:8]}"
    created_category_ids: list[int] = []
    created_product_ids: list[int] = []

    with TestClient(app) as client:
        try:
            health_response = client.get("/health")
            assert health_response.status_code == 200
            assert health_response.json() == {"status": "ok"}

            category_payload = {
                "name": f"{prefix}-category-main",
                "description": "Category created by automated pytest",
            }
            category_response = client.post("/api/categories", json=category_payload)
            assert category_response.status_code == 201
            category = category_response.json()
            created_category_ids.append(category["id"])
            assert category["name"] == category_payload["name"]

            get_category_response = client.get(f"/api/categories/{category['id']}")
            assert get_category_response.status_code == 200
            assert get_category_response.json()["id"] == category["id"]

            update_category_payload = {
                "name": f"{prefix}-category-updated",
                "description": "Updated by automated pytest",
            }
            update_category_response = client.put(
                f"/api/categories/{category['id']}",
                json=update_category_payload,
            )
            assert update_category_response.status_code == 200
            assert update_category_response.json()["name"] == update_category_payload["name"]

            extra_category_ids = []
            for index in range(12):
                response = client.post(
                    "/api/categories",
                    json={
                        "name": f"{prefix}-page-category-{index}",
                        "description": "Pagination category",
                    },
                )
                assert response.status_code == 201
                extra_category_ids.append(response.json()["id"])
            created_category_ids.extend(extra_category_ids)

            paged_categories_response = client.get("/api/categories?page=3&limit=5")
            assert paged_categories_response.status_code == 200
            assert isinstance(paged_categories_response.json(), list)
            assert len(paged_categories_response.json()) <= 5

            product_payload = {
                "name": f"{prefix}-product-main",
                "description": "Product created by automated pytest",
                "price": "299.99",
                "quantity": 10,
                "category_id": category["id"],
            }
            product_response = client.post("/api/products", json=product_payload)
            assert product_response.status_code == 201
            product = product_response.json()
            created_product_ids.append(product["id"])
            assert product["category"]["id"] == category["id"]

            get_product_response = client.get(f"/api/products/{product['id']}")
            assert get_product_response.status_code == 200
            product_detail = get_product_response.json()
            assert product_detail["id"] == product["id"]
            assert product_detail["category"]["id"] == category["id"]
            assert product_detail["category"]["name"] == update_category_payload["name"]

            update_product_payload = {
                "name": f"{prefix}-product-updated",
                "description": "Updated by automated pytest",
                "price": "349.50",
                "quantity": 4,
                "category_id": category["id"],
            }
            update_product_response = client.put(
                f"/api/products/{product['id']}",
                json=update_product_payload,
            )
            assert update_product_response.status_code == 200
            updated_product = update_product_response.json()
            assert updated_product["name"] == update_product_payload["name"]
            assert updated_product["category"]["id"] == category["id"]

            for index in range(7):
                response = client.post(
                    "/api/products",
                    json={
                        "name": f"{prefix}-page-product-{index}",
                        "description": "Pagination product",
                        "price": "10.00",
                        "quantity": index,
                        "category_id": category["id"],
                    },
                )
                assert response.status_code == 201
                created_product_ids.append(response.json()["id"])

            paged_products_response = client.get("/api/products?page=2&limit=3")
            assert paged_products_response.status_code == 200
            assert isinstance(paged_products_response.json(), list)
            assert len(paged_products_response.json()) <= 3

            delete_product_response = client.delete(f"/api/products/{product['id']}")
            assert delete_product_response.status_code == 204
            created_product_ids.remove(product["id"])

            deleted_product_response = client.get(f"/api/products/{product['id']}")
            assert deleted_product_response.status_code == 404

            delete_category_response = client.delete(f"/api/categories/{category['id']}")
            assert delete_category_response.status_code == 204
            created_category_ids.remove(category["id"])

            deleted_category_response = client.get(f"/api/categories/{category['id']}")
            assert deleted_category_response.status_code == 404

        finally:
            for product_id in created_product_ids:
                client.delete(f"/api/products/{product_id}")
            for category_id in created_category_ids:
                client.delete(f"/api/categories/{category_id}")
