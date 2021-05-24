import redis

from django.conf import settings

from shop.models import Product

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class Recommender:

    def get_product_ids(self, products):
        return [p.pk for p in products]

    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    def products_bought(self, products):
        product_ids = self.get_product_ids(products)
        for p_id in product_ids:
            for with_id in product_ids:
                if p_id != with_id:
                    r.zincrby(self.get_product_key(p_id), value=with_id, amount=1)

    def suggest_products_for(self, products, max_results=6):
        product_ids = self.get_product_ids(products)
        if len(product_ids) == 1:
            # сразу получаем список товаров, купленных с этим продуктом,
            # при этом учитываем рейтинг
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]),
                0, -1, desc=True)[:max_results]
        else:
            # формируем временный ключ (tmp_key)
            flat_ids = ''.join(list(map(str, product_ids)))
            tmp_key = 'tmp_{}'.format(flat_ids)

            keys = [self.get_product_key(id) for id in product_ids]

            # суммируем рейтинги для каждого товара, который был куплен вместе
            # с каким-либо переданных в аргументе
            # zunionstore - выполняет объединение множеств по указанным ключам
            # и сохраняет в Redis аггрегированное значение по новому ключу (tmp_key здесь)
            # https://redis.io/commands/zunionstore
            # сохраняем суммы во временном ключе
            r.zunionstore(tmp_key, keys)

            # чтобы товары, которые были переданы в аргумент функции products
            # не попали в рекомендации удаляем их с помощью zrem
            r.zrem(tmp_key, *product_ids)

            # получаем id товаров, отсортированных по рейтингу
            suggestions = r.zrange(tmp_key, 0, -1,
                                   desc=True)[:max_results]
            # удаляем временный ключ
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]

        # получаем рекомендуемые товары и сортируем их
        suggested_products = list(Product.objects.filter(pk__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.pk))
        return suggested_products

    def clear_purchases(self, products):
        for pk in self.get_product_ids(Product.objects.all()):
            r.delete(self.get_product_key(pk))
        ## OR
        # for pk in Product.objects.values_list('pk', flat=True):
        #     r.delete(self.get_product_key(pk))
