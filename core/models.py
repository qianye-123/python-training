from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, nickname, password=None, **extra_fields):
        if not nickname:
            raise ValueError('昵称不能为空')
        user = self.model(nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(nickname, password, **extra_fields)


class User(AbstractBaseUser):
    FAMILY_ROLES = [
        ('爸爸', '爸爸'),
        ('妈妈', '妈妈'),
        ('孩子', '孩子'),
        ('长辈', '长辈'),
    ]
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=50, unique=True, verbose_name='昵称')
    password = models.CharField(max_length=128, verbose_name='密码')
    family_role = models.CharField(max_length=20, choices=FAMILY_ROLES, verbose_name='家庭身份')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['family_role']

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'


class UserTaboo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='所属用户')
    taboo_name = models.CharField(max_length=50, verbose_name='忌口食材名称')

    class Meta:
        db_table = 'user_taboo'
        verbose_name = '用户忌口'
        verbose_name_plural = '用户忌口'


class Material(models.Model):
    MATERIAL_TYPES = [
        ('蔬菜', '蔬菜'),
        ('肉类', '肉类'),
        ('水果', '水果'),
        ('干货', '干货'),
    ]
    SEASON_CHOICES = [
        ('春', '春'),
        ('夏', '夏'),
        ('秋', '秋'),
        ('冬', '冬'),
        ('全年', '全年'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, verbose_name='食材名称')
    type = models.CharField(max_length=20, choices=MATERIAL_TYPES, verbose_name='分类')
    season = models.CharField(max_length=20, choices=SEASON_CHOICES, verbose_name='季节')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=5.00, verbose_name='参考单价(元/斤)')
    unit = models.CharField(max_length=20, default='斤', verbose_name='单位')

    class Meta:
        db_table = 'material'
        verbose_name = '食材'
        verbose_name_plural = '食材'

    def __str__(self):
        return self.name


class Dish(models.Model):
    DISH_CATEGORIES = [
        ('素菜', '素菜'),
        ('荤菜', '荤菜'),
        ('汤品', '汤品'),
        ('凉菜', '凉菜'),
        ('小吃', '小吃'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, verbose_name='菜品名称')
    category = models.CharField(max_length=20, choices=DISH_CATEGORIES, verbose_name='分类')
    image = models.CharField(max_length=200, blank=True, null=True, verbose_name='菜品图片存储路径')
    desc = models.TextField(blank=True, null=True, verbose_name='口味、制作步骤描述')

    class Meta:
        db_table = 'dish'
        verbose_name = '菜品'
        verbose_name_plural = '菜品'

    def __str__(self):
        return self.name


class DishMaterial(models.Model):
    UNIT_CHOICES = [
        ('斤', '斤'),
        ('个', '个'),
        ('颗', '颗'),
        ('盒', '盒'),
        ('把', '把'),
    ]
    id = models.AutoField(primary_key=True)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='对应菜品')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='对应食材')
    need_num = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='菜品所需食材数量')
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, verbose_name='单位')

    class Meta:
        db_table = 'dish_material'
        verbose_name = '菜品食材'
        verbose_name_plural = '菜品食材'


class Fruit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, verbose_name='水果名称')
    image = models.CharField(max_length=200, blank=True, null=True, verbose_name='图片路径')
    store_tip = models.TextField(blank=True, null=True, verbose_name='储存建议')
    base_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='基础参考单价')
    is_allergy = models.BooleanField(default=False, verbose_name='是否易过敏')

    class Meta:
        db_table = 'fruit'
        verbose_name = '水果'
        verbose_name_plural = '水果'

    def __str__(self):
        return self.name


class Drink(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, verbose_name='饮品名称')
    spec = models.CharField(max_length=30, blank=True, null=True, verbose_name='规格')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='单品售价')
    is_lactose = models.BooleanField(default=False, verbose_name='是否含乳糖')

    class Meta:
        db_table = 'drink'
        verbose_name = '饮品'
        verbose_name_plural = '饮品'

    def __str__(self):
        return self.name


class Market(models.Model):
    id = models.AutoField(primary_key=True)
    area = models.CharField(max_length=50, verbose_name='所属地区')
    market_name = models.CharField(max_length=50, verbose_name='菜市场名称')
    address = models.TextField(blank=True, null=True, verbose_name='详细地址')

    class Meta:
        db_table = 'market'
        verbose_name = '菜市场'
        verbose_name_plural = '菜市场'

    def __str__(self):
        return self.market_name


class MarketPrice(models.Model):
    id = models.AutoField(primary_key=True)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, verbose_name='所属菜市场')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='对应食材')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='当日零售单价')
    update_date = models.DateField(auto_now_add=True, verbose_name='价格更新日期')

    class Meta:
        db_table = 'market_price'
        verbose_name = '食材市场价'
        verbose_name_plural = '食材市场价'


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='对应食材')
    stock_num = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='剩余库存数量')
    tip = models.CharField(max_length=100, blank=True, null=True, verbose_name='过期备注')
    update_time = models.DateTimeField(auto_now=True, verbose_name='库存更新时间')

    class Meta:
        db_table = 'stock'
        verbose_name = '家庭库存'
        verbose_name_plural = '家庭库存'


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='下单用户')
    order_date = models.DateField(auto_now_add=True, verbose_name='下单日期')
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='采购总花费')
    purchase_text = models.TextField(verbose_name='完整采购清单文本')
    is_finish = models.BooleanField(default=False, verbose_name='是否已采购')

    class Meta:
        db_table = 'order'
        verbose_name = '点餐订单'
        verbose_name_plural = '点餐订单'


class OrderItem(models.Model):
    EAT_TIME_CHOICES = [
        ('早餐', '早餐'),
        ('午餐', '午餐'),
        ('晚餐', '晚餐'),
        ('加餐', '加餐'),
    ]
    GOODS_TYPE_CHOICES = [
        ('dish', '菜品'),
        ('fruit', '水果'),
        ('drink', '饮品'),
    ]
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='所属订单')
    goods_type = models.CharField(max_length=10, choices=GOODS_TYPE_CHOICES, verbose_name='商品类型')
    goods_id = models.IntegerField(verbose_name='对应商品id')
    buy_num = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='购买份数')
    eat_time = models.CharField(max_length=10, choices=EAT_TIME_CHOICES, verbose_name='用餐时段')

    class Meta:
        db_table = 'order_item'
        verbose_name = '订单明细'
        verbose_name_plural = '订单明细'


class UserCollect(models.Model):
    GOODS_TYPE_CHOICES = [
        ('dish', '菜品'),
        ('fruit', '水果'),
        ('drink', '饮品'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='收藏用户')
    goods_type = models.CharField(max_length=10, choices=GOODS_TYPE_CHOICES, verbose_name='商品类型')
    goods_id = models.IntegerField(verbose_name='对应商品id')

    class Meta:
        db_table = 'user_collect'
        verbose_name = '用户收藏'
        verbose_name_plural = '用户收藏'
        unique_together = ('user', 'goods_type', 'goods_id')