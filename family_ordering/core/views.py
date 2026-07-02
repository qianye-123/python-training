import os
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

from .models import (
    User, UserTaboo, Material, Dish, DishMaterial,
    Fruit, Drink, Market, MarketPrice, Stock, Order, OrderItem, UserCollect
)


def get_current_season():
    month = datetime.now().month
    if 3 <= month <= 5:
        return '春'
    elif 6 <= month <= 8:
        return '夏'
    elif 9 <= month <= 11:
        return '秋'
    else:
        return '冬'


def get_all_taboo_names():
    taboos = UserTaboo.objects.all()
    return set(t.taboo_name for t in taboos)


def check_dish_has_taboo(dish):
    taboo_names = get_all_taboo_names()
    dish_materials = DishMaterial.objects.filter(dish=dish)
    for dm in dish_materials:
        if dm.material.name in taboo_names:
            return True, dm.material.name
    return False, None


def check_fruit_has_allergy(fruit, user):
    if fruit.is_allergy:
        user_taboos = UserTaboo.objects.filter(user=user)
        taboo_names = set(t.taboo_name for t in user_taboos)
        if fruit.name in taboo_names:
            return True
    return False


def check_drink_has_lactose(drink, user):
    if drink.is_lactose:
        user_taboos = UserTaboo.objects.filter(user=user)
        taboo_names = set(t.taboo_name for t in user_taboos)
        if '乳糖' in taboo_names:
            return True
    return False


def get_monthly_seasonal_materials():
    month = datetime.now().month
    seasonal_map = {
        1: {'name': '冬', 'materials': ['大白菜', '白萝卜', '土豆', '莲藕', '山药', '香菇', '木耳']},
        2: {'name': '冬', 'materials': ['大白菜', '胡萝卜', '土豆', '冬笋', '南瓜', '香菇', '木耳']},
        3: {'name': '春', 'materials': ['韭菜', '菠菜', '莴笋', '香椿', '春笋', '荠菜', '豌豆']},
        4: {'name': '春', 'materials': ['芹菜', '蒜苗', '芦笋', '香椿', '蚕豆', '枸杞头', '荠菜']},
        5: {'name': '春', 'materials': ['西红柿', '黄瓜', '茄子', '青椒', '豆角', '蒜苔', '洋葱']},
        6: {'name': '夏', 'materials': ['黄瓜', '丝瓜', '苦瓜', '冬瓜', '南瓜', '空心菜', '苋菜']},
        7: {'name': '夏', 'materials': ['豇豆', '扁豆', '毛豆', '茄子', '西红柿', '青椒', '南瓜']},
        8: {'name': '夏', 'materials': ['冬瓜', '苦瓜', '丝瓜', '豇豆', '毛豆', '扁豆', '马齿苋']},
        9: {'name': '秋', 'materials': ['南瓜', '冬瓜', '莲藕', '山药', '芋头', '红薯', '花生']},
        10: {'name': '秋', 'materials': ['大白菜', '萝卜', '土豆', '莲藕', '山药', '芋头', '红薯']},
        11: {'name': '秋', 'materials': ['大白菜', '白萝卜', '胡萝卜', '洋葱', '芹菜', '香菇', '木耳']},
        12: {'name': '冬', 'materials': ['大白菜', '萝卜', '土豆', '莲藕', '山药', '香菇', '木耳']},
    }
    return seasonal_map.get(month, {'name': '全年', 'materials': []})


def index(request):
    seasonal_info = get_monthly_seasonal_materials()
    season = seasonal_info['name']
    seasonal_materials_list = seasonal_info['materials']
    seasonal_materials = Material.objects.filter(name__in=seasonal_materials_list) | Material.objects.filter(season='全年')
    
    if request.user.is_authenticated:
        user_taboos = UserTaboo.objects.filter(user=request.user)
        taboo_names = [t.taboo_name for t in user_taboos]
    else:
        taboo_names = []

    categories = ['素菜', '荤菜', '汤品', '凉菜', '小吃']
    dishes_by_category = {}
    for cat in categories:
        dishes = Dish.objects.filter(category=cat)[:6]
        dishes_with_details = []
        for dish in dishes:
            has_taboo, taboo_name = check_dish_has_taboo(dish)
            dish_materials = DishMaterial.objects.filter(dish=dish)
            materials = []
            for dm in dish_materials:
                materials.append({
                    'name': dm.material.name,
                    'num': dm.need_num,
                    'unit': dm.unit
                })
            dishes_with_details.append({
                'dish': dish,
                'has_taboo': has_taboo,
                'taboo_name': taboo_name,
                'materials': materials
            })
        dishes_by_category[cat] = dishes_with_details

    fruits = Fruit.objects.all()[:8]
    drinks = Drink.objects.all()[:8]
    
    stocks = Stock.objects.all()[:10]

    cart_items = []
    cart = request.session.get('cart', [])
    for item in cart:
        if item['goods_type'] == 'dish':
            obj = Dish.objects.filter(id=item['goods_id']).first()
            has_taboo, taboo_name = check_dish_has_taboo(obj) if obj else (False, None)
        elif item['goods_type'] == 'fruit':
            obj = Fruit.objects.filter(id=item['goods_id']).first()
            has_taboo = False
            taboo_name = None
        elif item['goods_type'] == 'drink':
            obj = Drink.objects.filter(id=item['goods_id']).first()
            has_taboo = False
            taboo_name = None
        if obj:
            cart_items.append({
                'item': item,
                'obj': obj,
                'has_taboo': has_taboo,
                'taboo_name': taboo_name
            })

    if request.user.is_authenticated:
        today = datetime.now().date()
        daily_stats = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            day_orders = Order.objects.filter(user=request.user, order_date=date)
            day_total = sum(order.total_cost for order in day_orders)
            daily_stats.append({
                'date': date.strftime('%m-%d'),
                'total': float(day_total)
            })
    else:
        today = datetime.now().date()
        daily_stats = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            daily_stats.append({
                'date': date.strftime('%m-%d'),
                'total': 0
            })

    user_location = request.session.get('user_location', '')
    
    return render(request, 'index.html', {
        'season': season,
        'seasonal_materials': seasonal_materials,
        'dishes_by_category': dishes_by_category,
        'fruits': fruits,
        'drinks': drinks,
        'taboo_names': taboo_names,
        'stocks': stocks,
        'cart_items': cart_items,
        'daily_stats': daily_stats,
        'user_location': user_location
    })


def register(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        family_role = request.POST.get('family_role')
        taboos = request.POST.getlist('taboos')
        custom_taboo = request.POST.get('custom_taboo')

        if User.objects.filter(nickname=nickname).exists():
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': '昵称已存在'}, status=200)
            messages.error(request, '昵称已存在')
            return redirect('register')
        
        if len(password) < 6:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': '密码长度至少6位'}, status=200)
            messages.error(request, '密码长度至少6位')
            return redirect('register')

        user = User.objects.create_user(
            nickname=nickname,
            password=password,
            family_role=family_role
        )

        for taboo in taboos:
            if taboo:
                UserTaboo.objects.create(user=user, taboo_name=taboo)
        
        if custom_taboo:
            UserTaboo.objects.create(user=user, taboo_name=custom_taboo)

        login(request, user)
        messages.success(request, '注册成功')
        return redirect('index')
    
    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        user = authenticate(request, nickname=nickname, password=password)
        
        if user is None:
            try:
                User.objects.get(nickname=nickname)
                error_msg = '密码错误'
            except User.DoesNotExist:
                error_msg = '昵称不存在'
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': error_msg}, status=200)
            
            messages.error(request, error_msg)
            return redirect('login')

        login(request, user)
        
        if remember:
            request.session.set_expiry(30*24*60*60)
        else:
            request.session.set_expiry(0)

        messages.success(request, '登录成功')
        return redirect('index')
    
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    messages.success(request, '已退出登录')
    return redirect('index')


@login_required
def profile(request):
    user = request.user
    
    if request.method == 'POST':
        action = request.POST.get('action')
        taboo_name = request.POST.get('taboo_name')
        
        if action == 'add_taboo' and taboo_name:
            if not UserTaboo.objects.filter(user=user, taboo_name=taboo_name).exists():
                UserTaboo.objects.create(user=user, taboo_name=taboo_name)
                messages.success(request, '忌口食材已添加')
            else:
                messages.error(request, '该忌口食材已存在')
        
        elif action == 'delete_taboo' and taboo_name:
            UserTaboo.objects.filter(user=user, taboo_name=taboo_name).delete()
            messages.success(request, '忌口食材已删除')
        
        return redirect('profile')
    
    taboos = UserTaboo.objects.filter(user=user)
    orders = Order.objects.filter(user=user).order_by('-order_date')[:10]
    
    order_items = OrderItem.objects.filter(order__in=orders)
    dish_ids = [item.goods_id for item in order_items if item.goods_type == 'dish']
    
    if dish_ids:
        frequency = OrderItem.objects.filter(
            goods_type='dish', goods_id__in=dish_ids
        ).values('goods_id').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        frequent_dishes = []
        for item in frequency:
            try:
                dish = Dish.objects.get(id=item['goods_id'])
                frequent_dishes.append({'dish': dish, 'count': item['count']})
            except:
                pass
    else:
        frequent_dishes = []

    collections = UserCollect.objects.filter(user=user)
    collected_dishes = []
    collected_fruits = []
    collected_drinks = []
    for c in collections:
        try:
            if c.goods_type == 'dish':
                collected_dishes.append(Dish.objects.get(id=c.goods_id))
            elif c.goods_type == 'fruit':
                collected_fruits.append(Fruit.objects.get(id=c.goods_id))
            elif c.goods_type == 'drink':
                collected_drinks.append(Drink.objects.get(id=c.goods_id))
        except:
            pass

    markets = Market.objects.all()[:6]
    
    user_location = request.session.get('user_location', '')
    
    return render(request, 'profile.html', {
        'user': user,
        'taboos': taboos,
        'orders': orders,
        'frequent_dishes': frequent_dishes,
        'collected_dishes': collected_dishes,
        'collected_fruits': collected_fruits,
        'collected_drinks': collected_drinks,
        'markets': markets,
        'user_location': user_location
    })


@login_required
def save_location(request):
    if request.method == 'POST':
        location = request.POST.get('location', '') or request.body.decode('utf-8').split('location=')[1] if 'location=' in request.body.decode('utf-8') else ''
        if location and '{' in location:
            import json
            data = json.loads(location)
            location = data.get('location', '')
        request.session['user_location'] = location
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        new_nickname = request.POST.get('nickname')
        new_password = request.POST.get('password')
        
        if new_nickname and new_nickname != user.nickname:
            if User.objects.filter(nickname=new_nickname).exists():
                messages.error(request, '昵称已存在')
                return redirect('profile')
            user.nickname = new_nickname
            user.save()
        
        if new_password and len(new_password) >= 6:
            user.set_password(new_password)
            user.save()
            login(request, user)
            messages.success(request, '密码修改成功')
        
        messages.success(request, '信息更新成功')
        return redirect('profile')


@login_required
def taboo_manage(request):
    user = request.user
    if request.method == 'POST':
        action = request.POST.get('action')
        taboo_name = request.POST.get('taboo_name')
        
        if action == 'add' and taboo_name:
            if not UserTaboo.objects.filter(user=user, taboo_name=taboo_name).exists():
                UserTaboo.objects.create(user=user, taboo_name=taboo_name)
                messages.success(request, '忌口食材已添加')
            else:
                messages.error(request, '该忌口食材已存在')
        
        elif action == 'delete' and taboo_name:
            UserTaboo.objects.filter(user=user, taboo_name=taboo_name).delete()
            messages.success(request, '忌口食材已删除')
    
    return redirect('profile')


def dish_list(request):
    category = request.GET.get('category', '')
    if category:
        dishes = Dish.objects.filter(category=category)
    else:
        dishes = Dish.objects.all()
    
    dishes_with_taboo = []
    for dish in dishes:
        has_taboo, taboo_name = check_dish_has_taboo(dish)
        dishes_with_taboo.append({
            'dish': dish,
            'has_taboo': has_taboo,
            'taboo_name': taboo_name
        })

    cart_items = []
    cart = request.session.get('cart', [])
    for item in cart:
        if item['goods_type'] == 'dish':
            obj = Dish.objects.filter(id=item['goods_id']).first()
        elif item['goods_type'] == 'fruit':
            obj = Fruit.objects.filter(id=item['goods_id']).first()
        elif item['goods_type'] == 'drink':
            obj = Drink.objects.filter(id=item['goods_id']).first()
        if obj:
            cart_items.append({'item': item, 'obj': obj})

    categories = ['素菜', '荤菜', '汤品', '凉菜', '小吃']
    return render(request, 'dish_list.html', {
        'dishes': dishes_with_taboo,
        'categories': categories,
        'selected_category': category,
        'cart_items': cart_items
    })


def dish_detail(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    has_taboo, taboo_name = check_dish_has_taboo(dish)
    materials = DishMaterial.objects.filter(dish=dish)
    
    is_collected = False
    if request.user.is_authenticated:
        is_collected = UserCollect.objects.filter(
            user=request.user, goods_type='dish', goods_id=pk
        ).exists()

    return render(request, 'dish_detail.html', {
        'dish': dish,
        'materials': materials,
        'has_taboo': has_taboo,
        'taboo_name': taboo_name,
        'is_collected': is_collected
    })


@login_required
def dish_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        desc = request.POST.get('desc')
        
        if Dish.objects.filter(name=name).exists():
            messages.error(request, '菜品名称已存在')
            return redirect('dish_add')

        dish = Dish.objects.create(name=name, category=category, desc=desc)

        if request.FILES.get('image'):
            fs = FileSystemStorage()
            image = request.FILES['image']
            filename = fs.save(f'dishes/{image.name}', image)
            dish.image = filename
            dish.save()

        material_ids = request.POST.getlist('material_id')
        need_nums = request.POST.getlist('need_num')
        units = request.POST.getlist('unit')

        for i in range(len(material_ids)):
            if material_ids[i] and need_nums[i]:
                DishMaterial.objects.create(
                    dish=dish,
                    material_id=material_ids[i],
                    need_num=need_nums[i],
                    unit=units[i]
                )

        messages.success(request, '菜品添加成功')
        return redirect('dish_list')
    
    materials = Material.objects.all()
    categories = ['素菜', '荤菜', '汤品', '凉菜', '小吃']
    return render(request, 'dish_add.html', {
        'materials': materials,
        'categories': categories
    })


@login_required
def dish_edit(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    
    if request.method == 'POST':
        dish.name = request.POST.get('name')
        dish.category = request.POST.get('category')
        dish.desc = request.POST.get('desc')
        
        if request.FILES.get('image'):
            fs = FileSystemStorage()
            image = request.FILES['image']
            filename = fs.save(f'dishes/{image.name}', image)
            dish.image = filename
        
        dish.save()

        DishMaterial.objects.filter(dish=dish).delete()
        
        material_ids = request.POST.getlist('material_id')
        need_nums = request.POST.getlist('need_num')
        units = request.POST.getlist('unit')

        for i in range(len(material_ids)):
            if material_ids[i] and need_nums[i]:
                DishMaterial.objects.create(
                    dish=dish,
                    material_id=material_ids[i],
                    need_num=need_nums[i],
                    unit=units[i]
                )

        messages.success(request, '菜品编辑成功')
        return redirect('dish_detail', pk=pk)
    
    materials = Material.objects.all()
    categories = ['素菜', '荤菜', '汤品', '凉菜', '小吃']
    dish_materials = DishMaterial.objects.filter(dish=dish)
    
    return render(request, 'dish_edit.html', {
        'dish': dish,
        'materials': materials,
        'categories': categories,
        'dish_materials': dish_materials
    })


@login_required
def dish_delete(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    dish.delete()
    messages.success(request, '菜品已删除')
    return redirect('dish_list')


def fruit_list(request):
    fruits = Fruit.objects.all()
    
    fruits_with_allergy = []
    for fruit in fruits:
        has_allergy = False
        if request.user.is_authenticated:
            has_allergy = check_fruit_has_allergy(fruit, request.user)
        fruits_with_allergy.append({
            'fruit': fruit,
            'has_allergy': has_allergy
        })

    return render(request, 'fruit_list.html', {
        'fruits': fruits_with_allergy
    })


def fruit_detail(request, pk):
    fruit = get_object_or_404(Fruit, pk=pk)
    has_allergy = False
    if request.user.is_authenticated:
        has_allergy = check_fruit_has_allergy(fruit, request.user)
    
    is_collected = False
    if request.user.is_authenticated:
        is_collected = UserCollect.objects.filter(
            user=request.user, goods_type='fruit', goods_id=pk
        ).exists()

    return render(request, 'fruit_detail.html', {
        'fruit': fruit,
        'has_allergy': has_allergy,
        'is_collected': is_collected
    })


@login_required
def fruit_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        store_tip = request.POST.get('store_tip')
        base_price = request.POST.get('base_price')
        is_allergy = request.POST.get('is_allergy') == 'on'
        
        if Fruit.objects.filter(name=name).exists():
            messages.error(request, '水果名称已存在')
            return redirect('fruit_add')

        fruit = Fruit.objects.create(
            name=name, store_tip=store_tip, base_price=base_price, is_allergy=is_allergy
        )

        if request.FILES.get('image'):
            fs = FileSystemStorage()
            image = request.FILES['image']
            filename = fs.save(f'fruits/{image.name}', image)
            fruit.image = filename
            fruit.save()

        messages.success(request, '水果添加成功')
        return redirect('fruit_list')
    
    return render(request, 'fruit_add.html')


@login_required
def fruit_edit(request, pk):
    fruit = get_object_or_404(Fruit, pk=pk)
    
    if request.method == 'POST':
        fruit.name = request.POST.get('name')
        fruit.store_tip = request.POST.get('store_tip')
        fruit.base_price = request.POST.get('base_price')
        fruit.is_allergy = request.POST.get('is_allergy') == 'on'
        
        if request.FILES.get('image'):
            fs = FileSystemStorage()
            image = request.FILES['image']
            filename = fs.save(f'fruits/{image.name}', image)
            fruit.image = filename
        
        fruit.save()

        messages.success(request, '水果编辑成功')
        return redirect('fruit_detail', pk=pk)
    
    return render(request, 'fruit_edit.html', {'fruit': fruit})


@login_required
def fruit_delete(request, pk):
    fruit = get_object_or_404(Fruit, pk=pk)
    fruit.delete()
    messages.success(request, '水果已删除')
    return redirect('fruit_list')


def drink_list(request):
    drinks = Drink.objects.all()
    
    drinks_with_lactose = []
    for drink in drinks:
        has_lactose = False
        if request.user.is_authenticated:
            has_lactose = check_drink_has_lactose(drink, request.user)
        drinks_with_lactose.append({
            'drink': drink,
            'has_lactose': has_lactose
        })

    return render(request, 'drink_list.html', {
        'drinks': drinks_with_lactose
    })


def drink_detail(request, pk):
    drink = get_object_or_404(Drink, pk=pk)
    has_lactose = False
    if request.user.is_authenticated:
        has_lactose = check_drink_has_lactose(drink, request.user)
    
    is_collected = False
    if request.user.is_authenticated:
        is_collected = UserCollect.objects.filter(
            user=request.user, goods_type='drink', goods_id=pk
        ).exists()

    return render(request, 'drink_detail.html', {
        'drink': drink,
        'has_lactose': has_lactose,
        'is_collected': is_collected
    })


@login_required
def drink_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        spec = request.POST.get('spec')
        price = request.POST.get('price')
        is_lactose = request.POST.get('is_lactose') == 'on'
        
        if Drink.objects.filter(name=name).exists():
            messages.error(request, '饮品名称已存在')
            return redirect('drink_add')

        Drink.objects.create(
            name=name, spec=spec, price=price, is_lactose=is_lactose
        )

        messages.success(request, '饮品添加成功')
        return redirect('drink_list')
    
    return render(request, 'drink_add.html')


@login_required
def drink_edit(request, pk):
    drink = get_object_or_404(Drink, pk=pk)
    
    if request.method == 'POST':
        drink.name = request.POST.get('name')
        drink.spec = request.POST.get('spec')
        drink.price = request.POST.get('price')
        drink.is_lactose = request.POST.get('is_lactose') == 'on'
        drink.save()

        messages.success(request, '饮品编辑成功')
        return redirect('drink_detail', pk=pk)
    
    return render(request, 'drink_edit.html', {'drink': drink})


@login_required
def drink_delete(request, pk):
    drink = get_object_or_404(Drink, pk=pk)
    drink.delete()
    messages.success(request, '饮品已删除')
    return redirect('drink_list')


@login_required
def add_to_cart(request):
    goods_type = request.POST.get('goods_type')
    goods_id = request.POST.get('goods_id')
    buy_num = request.POST.get('buy_num', 1)
    eat_time = request.POST.get('eat_time', '午餐')

    cart = request.session.get('cart', [])
    
    existing_item = None
    for item in cart:
        if item['goods_type'] == goods_type and item['goods_id'] == int(goods_id):
            existing_item = item
            break
    
    if existing_item:
        existing_item['buy_num'] = float(existing_item['buy_num']) + float(buy_num)
    else:
        cart.append({
            'goods_type': goods_type,
            'goods_id': int(goods_id),
            'buy_num': float(buy_num),
            'eat_time': eat_time
        })
    
    request.session['cart'] = cart
    messages.success(request, '已加入点餐清单')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': len(cart)})
    
    return redirect('cart')


@login_required
def cart(request):
    cart = request.session.get('cart', [])
    cart_items = []
    
    for item in cart:
        if item['goods_type'] == 'dish':
            obj = Dish.objects.filter(id=item['goods_id']).first()
            has_taboo, taboo_name = check_dish_has_taboo(obj) if obj else (False, None)
        elif item['goods_type'] == 'fruit':
            obj = Fruit.objects.filter(id=item['goods_id']).first()
            has_taboo = check_fruit_has_allergy(obj, request.user) if obj else False
            taboo_name = None
        elif item['goods_type'] == 'drink':
            obj = Drink.objects.filter(id=item['goods_id']).first()
            has_taboo = check_drink_has_lactose(obj, request.user) if obj else False
            taboo_name = None
        
        if obj:
            cart_items.append({
                'item': item,
                'obj': obj,
                'has_taboo': has_taboo,
                'taboo_name': taboo_name
            })
    
    return render(request, 'cart.html', {'cart_items': cart_items})


@login_required
def remove_from_cart(request):
    goods_type = request.POST.get('goods_type')
    goods_id = int(request.POST.get('goods_id'))
    
    cart = request.session.get('cart', [])
    cart = [item for item in cart if not (item['goods_type'] == goods_type and item['goods_id'] == goods_id)]
    request.session['cart'] = cart
    
    return redirect('cart')


@login_required
def clear_cart(request):
    request.session['cart'] = []
    messages.success(request, '点餐清单已清空')
    return redirect('cart')


def cart_count(request):
    cart = request.session.get('cart', [])
    return JsonResponse({'count': len(cart)})


@login_required
def summary(request):
    cart = request.session.get('cart', [])
    
    material_needs = {}
    
    for item in cart:
        if item['goods_type'] == 'dish':
            dish = Dish.objects.filter(id=item['goods_id']).first()
            if dish:
                dish_materials = DishMaterial.objects.filter(dish=dish)
                for dm in dish_materials:
                    key = dm.material.id
                    if key not in material_needs:
                        material_needs[key] = {
                            'name': dm.material.name,
                            'unit': dm.unit,
                            'total_need': 0,
                            'material': dm.material
                        }
                    material_needs[key]['total_need'] += float(dm.need_num) * float(item['buy_num'])
    
    stock_map = {}
    stocks = Stock.objects.all()
    for stock in stocks:
        stock_map[stock.material_id] = stock.stock_num
    
    for key in material_needs:
        if key in stock_map:
            material_needs[key]['total_need'] -= float(stock_map[key])
            if material_needs[key]['total_need'] < 0:
                material_needs[key]['total_need'] = 0
    
    need_purchase = {k: v for k, v in material_needs.items() if v['total_need'] > 0}
    
    user_location = request.session.get('user_location', '')
    markets_list = []
    
    if user_location:
        for market_city, markets in MARKET_DATA.items():
            if market_city in user_location or user_location in market_city:
                markets_list.extend(markets)
            else:
                for market in markets:
                    if market['area'] in user_location or user_location in market['area']:
                        markets_list.append(market)
                    elif market['address'] and user_location in market['address']:
                        markets_list.append(market)
    else:
        markets_list = MARKET_DATA.get('北京', [])
    
    markets_list = markets_list[:6]
    
    return render(request, 'summary.html', {
        'material_needs': need_purchase.values(),
        'markets': markets_list,
        'cart': cart,
        'user_location': user_location
    })


@login_required
def generate_purchase_text(request):
    cart = request.session.get('cart', [])
    
    material_needs = {}
    
    for item in cart:
        if item['goods_type'] == 'dish':
            dish = Dish.objects.filter(id=item['goods_id']).first()
            if dish:
                dish_materials = DishMaterial.objects.filter(dish=dish)
                for dm in dish_materials:
                    key = dm.material.id
                    if key not in material_needs:
                        material_needs[key] = {
                            'name': dm.material.name,
                            'unit': dm.unit,
                            'total_need': 0
                        }
                    material_needs[key]['total_need'] += float(dm.need_num) * float(item['buy_num'])
    
    stock_map = {}
    stocks = Stock.objects.all()
    for stock in stocks:
        stock_map[stock.material_id] = stock.stock_num
    
    for key in material_needs:
        if key in stock_map:
            material_needs[key]['total_need'] -= float(stock_map[key])
            if material_needs[key]['total_need'] < 0:
                material_needs[key]['total_need'] = 0
    
    need_purchase = {k: v for k, v in material_needs.items() if v['total_need'] > 0}
    
    text_lines = ["【采购清单】"]
    for v in need_purchase.values():
        text_lines.append(f"{v['name']}: {v['total_need']} {v['unit']}")
    
    fruit_needs = []
    drink_needs = []
    for item in cart:
        if item['goods_type'] == 'fruit':
            fruit = Fruit.objects.filter(id=item['goods_id']).first()
            if fruit:
                fruit_needs.append(f"{fruit.name}: {item['buy_num']}份")
        elif item['goods_type'] == 'drink':
            drink = Drink.objects.filter(id=item['goods_id']).first()
            if drink:
                drink_needs.append(f"{drink.name}: {item['buy_num']}份")
    
    if fruit_needs:
        text_lines.append("\n【水果】")
        text_lines.extend(fruit_needs)
    
    if drink_needs:
        text_lines.append("\n【饮品】")
        text_lines.extend(drink_needs)
    
    purchase_text = "\n".join(text_lines)
    
    request.session['purchase_text'] = purchase_text
    
    return render(request, 'purchase_text.html', {'purchase_text': purchase_text})


@login_required
def calculate_cost(request):
    market_name = request.POST.get('market_id')
    
    market_data = None
    for city_markets in MARKET_DATA.values():
        for market in city_markets:
            if market['market_name'] == market_name:
                market_data = market
                break
        if market_data:
            break
    
    if not market_data:
        market_data = {'market_name': market_name, 'area': '', 'address': ''}
    
    cart = request.session.get('cart', [])
    user_location = request.session.get('user_location', '')
    
    material_needs = {}
    
    for item in cart:
        if item['goods_type'] == 'dish':
            dish = Dish.objects.filter(id=item['goods_id']).first()
            if dish:
                dish_materials = DishMaterial.objects.filter(dish=dish)
                for dm in dish_materials:
                    key = dm.material.id
                    if key not in material_needs:
                        material_needs[key] = {
                            'name': dm.material.name,
                            'unit': dm.unit,
                            'total_need': 0,
                            'material': dm.material
                        }
                    material_needs[key]['total_need'] += float(dm.need_num) * float(item['buy_num'])
    
    stock_map = {}
    stocks = Stock.objects.all()
    for stock in stocks:
        stock_map[stock.material_id] = stock.stock_num
    
    for key in material_needs:
        if key in stock_map:
            material_needs[key]['total_need'] -= float(stock_map[key])
            if material_needs[key]['total_need'] < 0:
                material_needs[key]['total_need'] = 0
    
    need_purchase = {k: v for k, v in material_needs.items() if v['total_need'] > 0}
    
    total_cost = 0
    price_details = []
    
    for key, v in need_purchase.items():
        price_info = get_price_for_location(v['name'], user_location)
        price = price_info['price']
        cost = float(v['total_need']) * float(price)
        total_cost += cost
        price_details.append({
            'name': v['name'],
            'need': v['total_need'],
            'unit': v['unit'],
            'price': price,
            'cost': round(cost, 2)
        })
    
    fruit_cost = 0
    drink_cost = 0
    for item in cart:
        if item['goods_type'] == 'fruit':
            fruit = Fruit.objects.filter(id=item['goods_id']).first()
            if fruit:
                fruit_cost += float(fruit.base_price) * float(item['buy_num'])
        elif item['goods_type'] == 'drink':
            drink = Drink.objects.filter(id=item['goods_id']).first()
            if drink:
                drink_cost += float(drink.price) * float(item['buy_num'])
    
    total_cost += fruit_cost + drink_cost
    
    return render(request, 'cost_calculation.html', {
        'market': market_data,
        'price_details': price_details,
        'fruit_cost': round(fruit_cost, 2),
        'drink_cost': round(drink_cost, 2),
        'total_cost': round(total_cost, 2),
        'cart': cart
    })


@login_required
def submit_order(request):
    total_cost = request.POST.get('total_cost')
    purchase_text = request.session.get('purchase_text', '')
    
    if not purchase_text:
        cart = request.session.get('cart', [])
        material_needs = {}
        for item in cart:
            if item['goods_type'] == 'dish':
                dish = Dish.objects.filter(id=item['goods_id']).first()
                if dish:
                    dish_materials = DishMaterial.objects.filter(dish=dish)
                    for dm in dish_materials:
                        key = dm.material.id
                        if key not in material_needs:
                            material_needs[key] = {
                                'name': dm.material.name,
                                'unit': dm.unit,
                                'total_need': 0
                            }
                        material_needs[key]['total_need'] += float(dm.need_num) * float(item['buy_num'])
        
        stock_map = {}
        stocks = Stock.objects.all()
        for stock in stocks:
            stock_map[stock.material_id] = stock.stock_num
        
        for key in material_needs:
            if key in stock_map:
                material_needs[key]['total_need'] -= float(stock_map[key])
                if material_needs[key]['total_need'] < 0:
                    material_needs[key]['total_need'] = 0
        
        need_purchase = {k: v for k, v in material_needs.items() if v['total_need'] > 0}
        
        text_lines = ["【采购清单】"]
        for v in need_purchase.values():
            text_lines.append(f"{v['name']}: {v['total_need']} {v['unit']}")
        
        purchase_text = "\n".join(text_lines)
    
    order = Order.objects.create(
        user=request.user,
        total_cost=total_cost,
        purchase_text=purchase_text
    )
    
    cart = request.session.get('cart', [])
    for item in cart:
        OrderItem.objects.create(
            order=order,
            goods_type=item['goods_type'],
            goods_id=item['goods_id'],
            buy_num=item['buy_num'],
            eat_time=item['eat_time']
        )
    
    request.session['cart'] = []
    messages.success(request, '订单提交成功')
    
    return redirect('order_detail', pk=order.id)


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = OrderItem.objects.filter(order=order)
    
    items_detail = []
    for item in order_items:
        if item.goods_type == 'dish':
            obj = Dish.objects.filter(id=item.goods_id).first()
        elif item.goods_type == 'fruit':
            obj = Fruit.objects.filter(id=item.goods_id).first()
        elif item.goods_type == 'drink':
            obj = Drink.objects.filter(id=item.goods_id).first()
        items_detail.append({
            'item': item,
            'obj': obj
        })
    
    return render(request, 'order_detail.html', {
        'order': order,
        'items_detail': items_detail
    })


@login_required
def mark_order_finish(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.is_finish = True
    order.save()
    messages.success(request, '订单已标记为已采购')
    return redirect('order_detail', pk=pk)


@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not order.is_finish:
        order.delete()
        messages.success(request, '订单已取消')
    else:
        messages.error(request, '已采购的订单无法取消')
    return redirect('profile')


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'order_list.html', {'orders': orders})


def market_list(request):
    markets = Market.objects.all()
    return render(request, 'market_list.html', {'markets': markets})


MARKET_DATA = {
    '北京': [
        {'market_name': '望京菜市场', 'area': '朝阳区', 'address': '望京街10号'},
        {'market_name': '西单菜市场', 'area': '西城区', 'address': '西单北大街120号'},
        {'market_name': '东单菜市场', 'area': '东城区', 'address': '东单北大街3号'},
        {'market_name': '中关村菜市场', 'area': '海淀区', 'address': '中关村大街27号'},
        {'market_name': '三里屯菜市场', 'area': '朝阳区', 'address': '三里屯路19号'},
        {'market_name': '五道口菜市场', 'area': '海淀区', 'address': '成府路28号'},
    ],
    '上海': [
        {'market_name': '漕河泾菜市场', 'area': '徐汇区', 'address': '漕溪路250号'},
        {'market_name': '静安菜市场', 'area': '静安区', 'address': '南京西路1688号'},
        {'market_name': '浦东菜市场', 'area': '浦东新区', 'address': '张杨路601号'},
        {'market_name': '外滩菜市场', 'area': '黄浦区', 'address': '中山东一路1号'},
        {'market_name': '长宁菜市场', 'area': '长宁区', 'address': '中山公园路88号'},
        {'market_name': '杨浦菜市场', 'area': '杨浦区', 'address': '邯郸路100号'},
    ],
    '广州': [
        {'market_name': '天河菜市场', 'area': '天河区', 'address': '天河路208号'},
        {'market_name': '越秀菜市场', 'area': '越秀区', 'address': '北京路168号'},
        {'market_name': '荔湾菜市场', 'area': '荔湾区', 'address': '上下九路90号'},
        {'market_name': '海珠菜市场', 'area': '海珠区', 'address': '江南西路48号'},
        {'market_name': '番禺菜市场', 'area': '番禺区', 'address': '市桥街繁华路2号'},
        {'market_name': '白云菜市场', 'area': '白云区', 'address': '白云大道北88号'},
    ],
    '青岛': [
        {'market_name': '黄岛菜市场', 'area': '黄岛区', 'address': '钱塘江路369号'},
        {'market_name': '台东菜市场', 'area': '市北区', 'address': '台东三路68号'},
        {'market_name': '李村菜市场', 'area': '李沧区', 'address': '京口路90号'},
        {'market_name': '城阳菜市场', 'area': '城阳区', 'address': '正阳中路168号'},
        {'market_name': '市南菜市场', 'area': '市南区', 'address': '中山路36号'},
        {'market_name': '崂山菜市场', 'area': '崂山区', 'address': '香港东路128号'},
    ],
    '深圳': [
        {'market_name': '罗湖菜市场', 'area': '罗湖区', 'address': '东门老街88号'},
        {'market_name': '福田菜市场', 'area': '福田区', 'address': '深南中路3039号'},
        {'market_name': '南山菜市场', 'area': '南山区', 'address': '南海大道2000号'},
        {'market_name': '宝安菜市场', 'area': '宝安区', 'address': '新安街道前进一路'},
        {'market_name': '龙岗菜市场', 'area': '龙岗区', 'address': '龙城大道88号'},
        {'market_name': '盐田菜市场', 'area': '盐田区', 'address': '深盐路200号'},
    ],
    '成都': [
        {'market_name': '春熙路菜市场', 'area': '锦江区', 'address': '春熙路步行街188号'},
        {'market_name': '武侯菜市场', 'area': '武侯区', 'address': '武侯祠大街231号'},
        {'market_name': '青羊菜市场', 'area': '青羊区', 'address': '人民西路2号'},
        {'market_name': '锦江菜市场', 'area': '锦江区', 'address': '东大街下东大街段'},
        {'market_name': '成华菜市场', 'area': '成华区', 'address': '建设路26号'},
        {'market_name': '金牛菜市场', 'area': '金牛区', 'address': '沙湾路88号'},
    ],
}

def market_nearby(request):
    city = request.GET.get('city', '')
    
    matched_markets = []
    
    if city:
        for market_city, markets in MARKET_DATA.items():
            if market_city in city or city in market_city:
                matched_markets.extend(markets)
            else:
                for market in markets:
                    if market['area'] in city or city in market['area']:
                        matched_markets.append(market)
                    elif market['address'] and city in market['address']:
                        matched_markets.append(market)
    
    if not matched_markets:
        for market_city, markets in MARKET_DATA.items():
            if any(keyword in city for keyword in ['朝阳', '海淀', '东城', '西城', '静安', '浦东', '天河', '越秀', '黄岛', '台东']):
                for market in markets:
                    if any(keyword in market['area'] for keyword in ['朝阳', '海淀', '东城', '西城', '静安', '浦东', '天河', '越秀', '黄岛', '台东']):
                        matched_markets.append(market)
                        break
    
    if not matched_markets:
        matched_markets = MARKET_DATA.get('北京', [])[:3]
    
    return JsonResponse(matched_markets[:6], safe=False)


@login_required
def market_add(request):
    if request.method == 'POST':
        area = request.POST.get('area')
        market_name = request.POST.get('market_name')
        address = request.POST.get('address')
        
        Market.objects.create(area=area, market_name=market_name, address=address)
        messages.success(request, '菜市场添加成功')
        return redirect('market_list')
    
    return render(request, 'market_add.html')


@login_required
def market_edit(request, pk):
    market = get_object_or_404(Market, pk=pk)
    
    if request.method == 'POST':
        market.area = request.POST.get('area')
        market.market_name = request.POST.get('market_name')
        market.address = request.POST.get('address')
        market.save()
        messages.success(request, '菜市场编辑成功')
        return redirect('market_list')
    
    return render(request, 'market_edit.html', {'market': market})


@login_required
def market_delete(request, pk):
    market = get_object_or_404(Market, pk=pk)
    market.delete()
    messages.success(request, '菜市场已删除')
    return redirect('market_list')


def price_list(request):
    material_id = request.GET.get('material_id')
    materials = Material.objects.all()
    
    if material_id:
        prices = MarketPrice.objects.filter(material_id=material_id).order_by('-update_date')
        material = Material.objects.get(pk=material_id)
    else:
        prices = MarketPrice.objects.all().order_by('-update_date')[:20]
        material = None
    
    return render(request, 'price_list.html', {
        'materials': materials,
        'prices': prices,
        'selected_material': material
    })


def price_by_location(request):
    location = request.GET.get('location', '')
    material_name = request.GET.get('material_name', '')
    
    if material_name:
        price_info = get_price_for_location(material_name, location)
        return JsonResponse(price_info)
    else:
        all_prices = {}
        for name in BASE_MATERIAL_PRICES.keys():
            all_prices[name] = get_price_for_location(name, location)
        return JsonResponse(all_prices)


@login_required
def price_add(request):
    if request.method == 'POST':
        market_id = request.POST.get('market_id')
        material_id = request.POST.get('material_id')
        price = request.POST.get('price')
        
        MarketPrice.objects.create(
            market_id=market_id,
            material_id=material_id,
            price=price
        )
        messages.success(request, '价格录入成功')
        return redirect('price_list')
    
    markets = Market.objects.all()
    materials = Material.objects.all()
    return render(request, 'price_add.html', {
        'markets': markets,
        'materials': materials
    })


def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'stock_list.html', {'stocks': stocks})


@login_required
def stock_add(request):
    if request.method == 'POST':
        material_id = request.POST.get('material_id')
        stock_num = request.POST.get('stock_num')
        tip = request.POST.get('tip')
        
        Stock.objects.create(
            material_id=material_id,
            stock_num=stock_num,
            tip=tip
        )
        messages.success(request, '库存录入成功')
        return redirect('stock_list')
    
    materials = Material.objects.all()
    return render(request, 'stock_add.html', {'materials': materials})


@login_required
def stock_edit(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    
    if request.method == 'POST':
        stock.material_id = request.POST.get('material_id')
        stock.stock_num = request.POST.get('stock_num')
        stock.tip = request.POST.get('tip')
        stock.save()
        messages.success(request, '库存编辑成功')
        return redirect('stock_list')
    
    materials = Material.objects.all()
    return render(request, 'stock_edit.html', {
        'stock': stock,
        'materials': materials
    })


@login_required
def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    stock.delete()
    messages.success(request, '库存已删除')
    return redirect('stock_list')


def material_list(request):
    materials = Material.objects.all()
    seasons = ['春', '夏', '秋', '冬', '全年']
    current_season = get_current_season()
    
    return render(request, 'material_list.html', {
        'materials': materials,
        'seasons': seasons,
        'current_season': current_season
    })


BASE_MATERIAL_PRICES = {
    '大白菜': {'price': 1.5, 'unit': '斤'},
    '白萝卜': {'price': 1.2, 'unit': '斤'},
    '胡萝卜': {'price': 1.8, 'unit': '斤'},
    '土豆': {'price': 2.0, 'unit': '斤'},
    '莲藕': {'price': 4.5, 'unit': '斤'},
    '山药': {'price': 6.0, 'unit': '斤'},
    '香菇': {'price': 8.0, 'unit': '斤'},
    '木耳': {'price': 15.0, 'unit': '斤'},
    '西红柿': {'price': 3.5, 'unit': '斤'},
    '黄瓜': {'price': 2.8, 'unit': '斤'},
    '茄子': {'price': 3.0, 'unit': '斤'},
    '青椒': {'price': 4.0, 'unit': '斤'},
    '豆角': {'price': 3.5, 'unit': '斤'},
    '蒜苔': {'price': 5.0, 'unit': '斤'},
    '洋葱': {'price': 2.5, 'unit': '斤'},
    '冬瓜': {'price': 1.0, 'unit': '斤'},
    '苦瓜': {'price': 4.0, 'unit': '斤'},
    '丝瓜': {'price': 3.5, 'unit': '斤'},
    '南瓜': {'price': 1.8, 'unit': '斤'},
    '毛豆': {'price': 5.0, 'unit': '斤'},
    '扁豆': {'price': 4.5, 'unit': '斤'},
    '空心菜': {'price': 2.0, 'unit': '斤'},
    '菠菜': {'price': 3.0, 'unit': '斤'},
    '油菜': {'price': 2.5, 'unit': '斤'},
    '韭菜': {'price': 4.0, 'unit': '斤'},
    '香菜': {'price': 5.0, 'unit': '把'},
    '莴笋': {'price': 2.5, 'unit': '斤'},
    '春笋': {'price': 8.0, 'unit': '斤'},
    '豌豆': {'price': 6.0, 'unit': '斤'},
    '芹菜': {'price': 3.0, 'unit': '斤'},
    '蒜苗': {'price': 4.0, 'unit': '斤'},
    '芦笋': {'price': 12.0, 'unit': '斤'},
    '香椿': {'price': 30.0, 'unit': '斤'},
    '蚕豆': {'price': 7.0, 'unit': '斤'},
    '枸杞头': {'price': 15.0, 'unit': '斤'},
    '荠菜': {'price': 10.0, 'unit': '斤'},
    '豇豆': {'price': 4.0, 'unit': '斤'},
    '苋菜': {'price': 3.0, 'unit': '斤'},
    '马齿苋': {'price': 8.0, 'unit': '斤'},
    '芋头': {'price': 3.5, 'unit': '斤'},
    '红薯': {'price': 2.0, 'unit': '斤'},
    '花生': {'price': 8.0, 'unit': '斤'},
    '五花肉': {'price': 18.0, 'unit': '斤'},
    '瘦肉': {'price': 22.0, 'unit': '斤'},
    '排骨': {'price': 25.0, 'unit': '斤'},
    '鸡翅': {'price': 15.0, 'unit': '斤'},
    '鸡腿': {'price': 12.0, 'unit': '斤'},
    '牛肉': {'price': 45.0, 'unit': '斤'},
    '羊肉': {'price': 50.0, 'unit': '斤'},
    '鸡蛋': {'price': 6.5, 'unit': '斤'},
    '鲫鱼': {'price': 15.0, 'unit': '斤'},
    '草鱼': {'price': 12.0, 'unit': '斤'},
}

CITY_PRICE_RATIOS = {
    '北京': 1.3,
    '上海': 1.35,
    '广州': 1.2,
    '深圳': 1.4,
    '成都': 0.95,
    '青岛': 0.9,
    '杭州': 1.25,
    '武汉': 0.95,
    '西安': 0.85,
    '重庆': 0.9,
    '南京': 1.15,
    '苏州': 1.15,
    '天津': 1.1,
    '郑州': 0.9,
    '长沙': 0.95,
    '东莞': 1.1,
    '佛山': 1.05,
    '宁波': 1.15,
    '无锡': 1.1,
    '厦门': 1.2,
}

CITY_ALIASES = {
    '朝阳': '北京', '海淀': '北京', '东城': '北京', '西城': '北京', '丰台': '北京', '石景山': '北京',
    '静安': '上海', '浦东': '上海', '徐汇': '上海', '黄浦': '上海', '长宁': '上海', '虹口': '上海',
    '天河': '广州', '越秀': '广州', '荔湾': '广州', '海珠': '广州', '番禺': '广州',
    '福田': '深圳', '罗湖': '深圳', '南山': '深圳', '宝安': '深圳', '龙岗': '深圳',
    '锦江': '成都', '武侯': '成都', '青羊': '成都', '金牛': '成都',
    '黄岛': '青岛', '市南': '青岛', '市北': '青岛', '李沧': '青岛', '崂山': '青岛',
    '西湖': '杭州', '上城': '杭州', '滨江': '杭州',
    '武昌': '武汉', '汉口': '武汉', '汉阳': '武汉',
    '雁塔': '西安', '碑林': '西安',
    '渝中': '重庆', '江北': '重庆', '南岸': '重庆',
    '玄武': '南京', '秦淮': '南京',
    '姑苏': '苏州', '工业园区': '苏州',
    '和平': '天津', '南开': '天津',
    '中原': '郑州', '金水': '郑州',
    '芙蓉': '长沙', '天心': '长沙',
    '莞城': '东莞', '虎门': '东莞',
    '禅城': '佛山', '南海': '佛山',
    '鄞州': '宁波', '海曙': '宁波',
    '梁溪': '无锡', '滨湖': '无锡',
    '思明': '厦门', '湖里': '厦门',
}

def get_city_from_location(location):
    if not location:
        return '北京'
    
    for alias, city in CITY_ALIASES.items():
        if alias in location:
            return city
    
    for city in CITY_PRICE_RATIOS.keys():
        if city in location:
            return city
    
    return '北京'

def get_price_for_location(material_name, location):
    city = get_city_from_location(location)
    ratio = CITY_PRICE_RATIOS.get(city, 1.0)
    
    if material_name in BASE_MATERIAL_PRICES:
        base_info = BASE_MATERIAL_PRICES[material_name]
        return {
            'price': round(base_info['price'] * ratio, 2),
            'unit': base_info['unit'],
            'city': city,
            'ratio': ratio
        }
    return {'price': 5.0, 'unit': '斤', 'city': city, 'ratio': ratio}

@login_required
def material_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        type = request.POST.get('type')
        season = request.POST.get('season')
        price = request.POST.get('price', 5.0)
        unit = request.POST.get('unit', '斤')
        
        if Material.objects.filter(name=name).exists():
            messages.error(request, '食材名称已存在')
            return redirect('material_add')
        
        Material.objects.create(name=name, type=type, season=season, price=price, unit=unit)
        messages.success(request, '食材添加成功')
        return redirect('material_list')
    
    types = ['蔬菜', '肉类', '水果', '干货']
    seasons = ['春', '夏', '秋', '冬', '全年']
    return render(request, 'material_add.html', {
        'types': types,
        'seasons': seasons
    })


@login_required
def material_edit(request, pk):
    material = get_object_or_404(Material, pk=pk)
    
    if request.method == 'POST':
        material.name = request.POST.get('name')
        material.type = request.POST.get('type')
        material.season = request.POST.get('season')
        material.save()
        messages.success(request, '食材编辑成功')
        return redirect('material_list')
    
    types = ['蔬菜', '肉类', '水果', '干货']
    seasons = ['春', '夏', '秋', '冬', '全年']
    return render(request, 'material_edit.html', {
        'material': material,
        'types': types,
        'seasons': seasons
    })


@login_required
def material_delete(request, pk):
    material = get_object_or_404(Material, pk=pk)
    material.delete()
    messages.success(request, '食材已删除')
    return redirect('material_list')


@login_required
def ai_recommend(request):
    season = get_current_season()
    
    user_requirement = request.session.get('user_requirement', '')
    
    if request.method == 'POST':
        if request.POST.get('clear_requirement'):
            user_requirement = ''
            request.session['user_requirement'] = ''
        else:
            user_requirement = request.POST.get('user_requirement', '')
            request.session['user_requirement'] = user_requirement
    
    all_taboos = get_all_taboo_names()
    
    taboo_materials = Material.objects.filter(name__in=all_taboos)
    taboo_material_ids = set(taboo_materials.values_list('id', flat=True))
    
    dishes_with_taboos = DishMaterial.objects.filter(material_id__in=taboo_material_ids).values_list('dish_id', flat=True)
    safe_dishes = Dish.objects.exclude(id__in=dishes_with_taboos)
    
    seasonal_dishes = []
    for dish in safe_dishes:
        dish_materials = DishMaterial.objects.filter(dish=dish)
        for dm in dish_materials:
            if dm.material.season in [season, '全年']:
                seasonal_dishes.append(dish)
                break
    
    stock_materials = Stock.objects.filter(stock_num__gt=0).values_list('material_id', flat=True)
    stock_dishes = []
    for dish in safe_dishes:
        dish_materials = DishMaterial.objects.filter(dish=dish)
        for dm in dish_materials:
            if dm.material_id in stock_materials:
                stock_dishes.append(dish)
                break
    
    combined_dishes = list(set(seasonal_dishes + stock_dishes))
    
    if user_requirement:
        user_requirement_lower = user_requirement.lower()
        
        keywords = {
            '清淡': ['素菜', '汤品'],
            '辣': ['荤菜', '素菜'],
            '肉': ['荤菜'],
            '素菜': ['素菜'],
            '荤菜': ['荤菜'],
            '汤': ['汤品'],
            '凉菜': ['凉菜'],
            '小吃': ['小吃'],
            '早餐': ['小吃', '素菜'],
            '午餐': ['荤菜', '素菜', '汤品'],
            '晚餐': ['荤菜', '素菜', '凉菜'],
        }
        
        preferred_categories = []
        for kw, cats in keywords.items():
            if kw in user_requirement_lower:
                preferred_categories.extend(cats)
        
        if preferred_categories:
            combined_dishes = [d for d in combined_dishes if d.category in preferred_categories]
    
    breakfast_dishes = [d for d in combined_dishes if d.category in ['小吃', '素菜']]
    lunch_dishes = [d for d in combined_dishes if d.category in ['荤菜', '素菜', '汤品']]
    dinner_dishes = [d for d in combined_dishes if d.category in ['荤菜', '素菜', '凉菜', '汤品']]
    
    import random
    
    def pick_dishes(dishes_list, count=2):
        shuffled = random.sample(dishes_list, min(len(dishes_list), count * 2))
        return shuffled[:count]
    
    recommendation = {
        'breakfast': pick_dishes(breakfast_dishes, 2),
        'lunch': pick_dishes(lunch_dishes, 3),
        'dinner': pick_dishes(dinner_dishes, 3)
    }
    
    all_recommended_dishes = []
    for meals in recommendation.values():
        all_recommended_dishes.extend(meals)
    
    materials_summary = {}
    for dish in all_recommended_dishes:
        dish_materials = DishMaterial.objects.filter(dish=dish)
        for dm in dish_materials:
            key = dm.material.id
            if key not in materials_summary:
                materials_summary[key] = {
                    'name': dm.material.name,
                    'unit': dm.unit,
                    'total': 0
                }
            materials_summary[key]['total'] += float(dm.need_num)
    
    return render(request, 'ai_recommend.html', {
        'recommendation': recommendation,
        'materials_summary': materials_summary.values(),
        'user_requirement': user_requirement
    })


@login_required
def add_recommend_to_cart(request):
    breakfast_ids = request.POST.getlist('breakfast')
    lunch_ids = request.POST.getlist('lunch')
    dinner_ids = request.POST.getlist('dinner')
    
    cart = request.session.get('cart', [])
    
    for dish_id in breakfast_ids:
        existing = False
        for item in cart:
            if item['goods_type'] == 'dish' and item['goods_id'] == int(dish_id):
                item['buy_num'] = float(item['buy_num']) + 1
                existing = True
                break
        if not existing:
            cart.append({
                'goods_type': 'dish',
                'goods_id': int(dish_id),
                'buy_num': 1,
                'eat_time': '早餐'
            })
    
    for dish_id in lunch_ids:
        existing = False
        for item in cart:
            if item['goods_type'] == 'dish' and item['goods_id'] == int(dish_id):
                item['buy_num'] = float(item['buy_num']) + 1
                existing = True
                break
        if not existing:
            cart.append({
                'goods_type': 'dish',
                'goods_id': int(dish_id),
                'buy_num': 1,
                'eat_time': '午餐'
            })
    
    for dish_id in dinner_ids:
        existing = False
        for item in cart:
            if item['goods_type'] == 'dish' and item['goods_id'] == int(dish_id):
                item['buy_num'] = float(item['buy_num']) + 1
                existing = True
                break
        if not existing:
            cart.append({
                'goods_type': 'dish',
                'goods_id': int(dish_id),
                'buy_num': 1,
                'eat_time': '晚餐'
            })
    
    request.session['cart'] = cart
    messages.success(request, '推荐菜品已加入点餐清单')
    
    return redirect('cart')


@login_required
def statistics(request):
    mode = request.GET.get('mode', 'month')
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))
    week = int(request.GET.get('week', datetime.now().isocalendar()[1]))
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    today = datetime.now().date()
    
    if mode == 'week':
        d = datetime(year, 1, 1)
        if (d.weekday() > 3):
            d += timedelta(7 - d.weekday())
        else:
            d -= timedelta(d.weekday())
        delta = timedelta(days=(week - 1) * 7)
        start_date = (d + delta).strftime('%Y-%m-%d')
        end_date = (d + delta + timedelta(days=6)).strftime('%Y-%m-%d')
    elif mode == 'month':
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"
    elif mode == 'year':
        start_date = f"{year}-01-01"
        end_date = f"{year + 1}-01-01"
    elif not start_date or not end_date:
        start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
    
    orders = Order.objects.filter(
        user=request.user,
        order_date__gte=start_date,
        order_date__lte=end_date
    ).order_by('order_date')
    
    years = list(range(2023, datetime.now().year + 2))
    months = list(range(1, 13))
    weeks = list(range(1, 53))
    
    total_cost = sum(order.total_cost for order in orders)
    
    eat_time_stats = {}
    for time in ['早餐', '午餐', '晚餐', '加餐']:
        eat_time_stats[time] = 0
    
    order_items = OrderItem.objects.filter(order__in=orders)
    for item in order_items:
        item_cost = 0
        if item.goods_type == 'dish':
            dish = Dish.objects.filter(id=item.goods_id).first()
            if dish:
                item_cost = float(item.buy_num) * 15
        elif item.goods_type == 'fruit':
            fruit = Fruit.objects.filter(id=item.goods_id).first()
            if fruit and hasattr(fruit, 'base_price'):
                item_cost = float(item.buy_num) * float(fruit.base_price)
        elif item.goods_type == 'drink':
            drink = Drink.objects.filter(id=item.goods_id).first()
            if drink and hasattr(drink, 'price'):
                item_cost = float(item.buy_num) * float(drink.price)
        
        eat_time = item.eat_time if item.eat_time in eat_time_stats else '午餐'
        eat_time_stats[eat_time] += item_cost
    
    daily_stats = []
    current_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    while current_date <= end_date_obj:
        day_orders = orders.filter(order_date=current_date)
        day_total = sum(order.total_cost for order in day_orders)
        daily_stats.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'total': float(day_total)
        })
        current_date += timedelta(days=1)
    
    category_stats = {
        '食材采购': 0,
        '水果开销': 0,
        '饮品开销': 0
    }
    
    for item in order_items:
        if item.goods_type == 'dish':
            category_stats['食材采购'] += float(item.buy_num) * 15
        elif item.goods_type == 'fruit':
            fruit = Fruit.objects.filter(id=item.goods_id).first()
            if fruit and hasattr(fruit, 'base_price'):
                category_stats['水果开销'] += float(item.buy_num) * float(fruit.base_price)
        elif item.goods_type == 'drink':
            drink = Drink.objects.filter(id=item.goods_id).first()
            if drink and hasattr(drink, 'price'):
                category_stats['饮品开销'] += float(item.buy_num) * float(drink.price)
    
    avg_daily_cost = round(total_cost / max(len(daily_stats), 1), 2)
    
    return render(request, 'statistics.html', {
        'total_cost': total_cost,
        'eat_time_stats': eat_time_stats,
        'daily_stats': daily_stats,
        'category_stats': category_stats,
        'start_date': start_date,
        'end_date': end_date,
        'orders': orders,
        'mode': mode,
        'year': year,
        'month': month,
        'week': week,
        'years': years,
        'months': months,
        'weeks': weeks,
        'avg_daily_cost': avg_daily_cost
    })


@login_required
def collect(request):
    goods_type = request.POST.get('goods_type')
    goods_id = request.POST.get('goods_id')
    
    if UserCollect.objects.filter(user=request.user, goods_type=goods_type, goods_id=goods_id).exists():
        UserCollect.objects.filter(user=request.user, goods_type=goods_type, goods_id=goods_id).delete()
        messages.success(request, '已取消收藏')
    else:
        UserCollect.objects.create(user=request.user, goods_type=goods_type, goods_id=goods_id)
        messages.success(request, '收藏成功')
    
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)