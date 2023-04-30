from infrastructure.repositories import MySqlProductRepository


class GetProductsQuery:
    def __init__(self, page, per_page):
        self.page = page
        self.per_page = per_page

    def execute(self):
        repository = MySqlProductRepository()
        products = repository.get_all(self.page, self.per_page)
        return products
