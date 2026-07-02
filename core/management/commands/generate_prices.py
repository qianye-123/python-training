import random
from datetime import date
from django.core.management.base import BaseCommand
from core.models import Material, Market, MarketPrice


class Command(BaseCommand):
    help = 'AI自动生成食材市场价（结合位置信息）'

    def handle(self, *args, **options):
        price_ranges = {
            '西红柿': (3.5, 5.5), '土豆': (2.0, 4.0), '黄瓜': (3.0, 5.0),
            '茄子': (3.5, 6.0), '青椒': (4.0, 7.0), '豆角': (4.5, 7.5),
            '大白菜': (1.5, 3.0), '萝卜': (1.8, 3.5), '莲藕': (5.0, 9.0),
            '山药': (6.0, 10.0), '香菇': (8.0, 15.0), '木耳': (15.0, 25.0),
            '韭菜': (4.0, 8.0), '菠菜': (3.0, 6.0), '莴笋': (2.5, 5.0),
            '香椿': (15.0, 30.0), '春笋': (8.0, 15.0), '荠菜': (6.0, 12.0),
            '豌豆': (5.0, 10.0), '蒜苔': (4.0, 8.0), '洋葱': (2.0, 4.5),
            '冬瓜': (1.5, 3.5), '苦瓜': (3.0, 6.0), '丝瓜': (3.0, 6.0),
            '南瓜': (2.0, 4.5), '毛豆': (5.0, 10.0), '扁豆': (4.0, 8.0),
            '空心菜': (2.5, 5.0), '芋头': (4.0, 8.0), '红薯': (2.0, 4.0),
            '花生': (6.0, 12.0), '猪肉': (25.0, 35.0), '牛肉': (45.0, 65.0),
            '羊肉': (50.0, 75.0), '鸡肉': (15.0, 25.0), '鸡蛋': (5.0, 8.0),
            '豆腐': (2.0, 4.0), '粉条': (8.0, 15.0), '大米': (3.0, 5.0),
            '面粉': (2.5, 4.5), '食用油': (50.0, 80.0), '酱油': (10.0, 20.0),
            '醋': (8.0, 15.0), '盐': (2.0, 5.0), '糖': (4.0, 8.0),
            '料酒': (8.0, 15.0), '葱姜蒜': (3.0, 6.0),
        }

        area_factors = {
            '朝阳区': 1.15, '海淀区': 1.10, '东城区': 1.20, '西城区': 1.18,
            '丰台区': 1.05, '朝阳区': 1.15, '通州区': 0.95, '顺义区': 0.98,
            '昌平区': 0.92, '房山区': 0.88, '大兴区': 1.00, '密云区': 0.85,
            '延庆区': 0.82, '石景山区': 1.08, '门头沟区': 0.90,
        }

        month_factor = {
            1: 1.2, 2: 1.25, 3: 1.1, 4: 1.05, 5: 1.0, 6: 0.95,
            7: 0.9, 8: 0.92, 9: 1.0, 10: 1.05, 11: 1.15, 12: 1.2,
        }

        materials = Material.objects.all()
        markets = Market.objects.all()

        current_month = date.today().month
        m_factor = month_factor.get(current_month, 1.0)

        for market in markets:
            area_factor = area_factors.get(market.area, 1.0)
            for material in materials:
                base_range = price_ranges.get(material.name, (3.0, 10.0))
                base_price = random.uniform(*base_range)
                final_price = round(base_price * area_factor * m_factor, 2)
                MarketPrice.objects.update_or_create(
                    market=market, material=material,
                    defaults={'price': final_price, 'update_date': date.today()}
                )

        self.stdout.write(self.style.SUCCESS('AI食材定价已成功生成！'))