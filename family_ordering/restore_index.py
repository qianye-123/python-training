content = '''{% extends 'base.html' %}

{% block content %}
<section id="top" class="py-12" style="background: linear-gradient(135deg, #FFF8EF 0%, #FFFFFF 100%);">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <h1 class="text-4xl font-bold text-[#4A403A] mb-4">
                    <span class="text-[#F7A072]">家味</span> - 让买菜做饭更简单
                </h1>
                <p class="text-lg text-[#88807A] mb-6">
                    一站式家庭智能点餐与食材采购核算系统，帮您轻松管理三餐，智能搭配菜谱，精准计算采购清单，让家的味道更温暖。
                </p>
                <div class="d-flex gap-3 flex-wrap">
                    <a href="#dishes" class="btn btn-primary px-6 py-3">
                        <i class="bi bi-utensils"></i> 浏览菜品
                    </a>
                    {% if user.is_authenticated %}
                    <a href="#ai-recommend" class="btn btn-outline-primary px-6 py-3">
                        <i class="bi bi-brain"></i> AI智能配餐
                    </a>
                    {% else %}
                    <a href="#register" class="btn btn-outline-primary px-6 py-3">
                        <i class="bi bi-person-plus"></i> 立即注册
                    </a>
                    {% endif %}
                </div>
            </div>
            <div class="col-lg-6 text-center">
                <div class="food-placeholder" style="height: 300px; font-size: 5rem;">
                    🍳🥗🍎
                </div>
            </div>
        </div>
    </div>
</section>

<section id="seasonal" class="py-8" style="background-color: #94B49F;">
    <div class="container">
        <div class="row">
            <div class="col-lg-8">
                <h3 class="text-white font-bold flex items-center gap-2">
                    <i class="bi bi-leaf"></i>
                    {{ season }}季时令食材推荐
                </h3>
                <div class="flex flex-wrap gap-2 mt-2">
                    {% for material in seasonal_materials %}
                    <span class="bg-white/20 text-white px-3 py-1 rounded-full text-sm">
                        {{ material.name }}
                    </span>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</section>

<section id="dishes" class="py-12">
    <div class="container">
        <h2 class="section-title">
            <i class="bi bi-utensils"></i> 菜品库
        </h2>
        {% for category, dishes in dishes_by_category.items %}
        {% if dishes %}
        <div class="mb-8">
            <h3 class="h4 font-bold text-[#4A403A] mb-4">{{ category }}</h3>
            <div class="row row-cols-1 col-md-2 col-lg-3 col-xl-4 g-4">
                {% for item in dishes %}
                {% with dish=item.dish %}
                <div class="card h-100">
                    <div class="food-placeholder">
                        {% if dish.category == '素菜' %}🥬
                        {% elif dish.category == '荤菜' %}🍖
                        {% elif dish.category == '汤品' %}🍲
                        {% elif dish.category == '凉菜' %}🥗
                        {% else %}🍟{% endif %}
                    </div>
                    <div class="card-body">
                        <div class="d-flex justify-between items-start mb-2">
                            <h5 class="font-bold text-[#4A403A]">{{ dish.name }}</h5>
                            <span class="text-[#F7A072] font-bold">¥{{ dish.base_price }}</span>
                        </div>
                        {% if item.materials %}
                        <div class="mb-3">
                            <p class="text-xs text-[#88807A] mb-1">食材组成：</p>
                            <div class="flex flex-wrap">
                                {% for mat in item.materials %}
                                <span class="material-tag">{{ mat.name }} {{ mat.num }}{{ mat.unit }}</span>
                                {% endfor %}
                            </div>
                        </div>
                        {% endif %}
                        {% if user.is_authenticated %}
                        <form action="{% url 'add_to_cart' %}" method="post" class="d-flex gap-2">
                            {% csrf_token %}
                            <input type="hidden" name="goods_type" value="dish">
                            <input type="hidden" name="goods_id" value="{{ dish.id }}">
                            <select name="eat_time" class="form-select form-select-sm flex-1">
                                <option value="早餐">早餐</option>
                                <option value="午餐">午餐</option>
                                <option value="晚餐">晚餐</option>
                                <option value="加餐">加餐</option>
                            </select>
                            <input type="number" name="buy_num" value="1" min="1" class="form-control form-control-sm w-16">
                            <button type="submit" class="btn btn-primary btn-sm"><i class="bi bi-plus"></i></button>
                        </form>
                        {% else %}
                        <button class="btn btn-outline-primary btn-sm w-full" disabled>登录后可点餐</button>
                        {% endif %}
                    </div>
                </div>
                {% endwith %}
                {% endfor %}
            </div>
        </div>
        {% endif %}
        {% endfor %}
    </div>
</section>

<section id="fruits" class="py-12" style="background-color: #FFF8EF;">
    <div class="container">
        <h2 class="section-title"><i class="bi bi-apple"></i> 水果专区</h2>
        <div class="row row-cols-1 col-md-2 col-lg-3 col-xl-4 g-4">
            {% for fruit in fruits %}
            <div class="card h-100">
                <div class="food-placeholder">
                    {% if fruit.name == '苹果' %}🍎
                    {% elif fruit.name == '香蕉' %}🍌
                    {% elif fruit.name == '橙子' %}🍊
                    {% elif fruit.name == '葡萄' %}🍇
                    {% elif fruit.name == '芒果' %}🥭
                    {% elif fruit.name == '草莓' %}🍓
                    {% elif fruit.name == '西瓜' %}🍉
                    {% elif fruit.name == '桃子' %}🍑
                    {% else %}🍒{% endif %}
                </div>
                <div class="card-body">
                    <div class="d-flex justify-between items-start mb-2">
                        <h5 class="font-bold text-[#4A403A]">{{ fruit.name }}</h5>
                        <span class="text-[#F7A072] font-bold">¥{{ fruit.base_price }}/斤</span>
                    </div>
                    {% if user.is_authenticated %}
                    <form action="{% url 'add_to_cart' %}" method="post" class="d-flex gap-2">
                        {% csrf_token %}
                        <input type="hidden" name="goods_type" value="fruit">
                        <input type="hidden" name="goods_id" value="{{ fruit.id }}">
                        <select name="eat_time" class="form-select form-select-sm flex-1">
                            <option value="早餐">早餐</option>
                            <option value="午餐">午餐</option>
                            <option value="晚餐">晚餐</option>
                            <option value="加餐">加餐</option>
                        </select>
                        <input type="number" name="buy_num" value="1" min="1" class="form-control form-control-sm w-16">
                        <button type="submit" class="btn btn-primary btn-sm"><i class="bi bi-plus"></i></button>
                    </form>
                    {% else %}
                    <button class="btn btn-outline-primary btn-sm w-full" disabled>登录后可点餐</button>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<section id="drinks" class="py-12">
    <div class="container">
        <h2 class="section-title"><i class="bi bi-cup-soda"></i> 饮品专区</h2>
        <div class="row row-cols-1 col-md-2 col-lg-3 col-xl-4 g-4">
            {% for drink in drinks %}
            <div class="card h-100">
                <div class="food-placeholder">
                    {% if drink.name == '豆浆' %}🥛
                    {% elif drink.name == '纯牛奶' %}🥛
                    {% elif drink.name == '酸奶' %}🥛
                    {% elif drink.name == '咖啡' %}☕
                    {% elif drink.name == '橙汁' %}🧃
                    {% elif drink.name == '可乐' %}🥤
                    {% elif drink.name == '茉莉花茶' %}🍵
                    {% elif drink.name == '奶茶' %}🧋
                    {% else %}🥤{% endif %}
                </div>
                <div class="card-body">
                    <div class="d-flex justify-between items-start mb-2">
                        <h5 class="font-bold text-[#4A403A]">{{ drink.name }}</h5>
                        <span class="text-[#F7A072] font-bold">¥{{ drink.price }}</span>
                    </div>
                    {% if user.is_authenticated %}
                    <form action="{% url 'add_to_cart' %}" method="post" class="d-flex gap-2">
                        {% csrf_token %}
                        <input type="hidden" name="goods_type" value="drink">
                        <input type="hidden" name="goods_id" value="{{ drink.id }}">
                        <select name="eat_time" class="form-select form-select-sm flex-1">
                            <option value="早餐">早餐</option>
                            <option value="午餐">午餐</option>
                            <option value="晚餐">晚餐</option>
                            <option value="加餐">加餐</option>
                        </select>
                        <input type="number" name="buy_num" value="1" min="1" class="form-control form-control-sm w-16">
                        <button type="submit" class="btn btn-primary btn-sm"><i class="bi bi-plus"></i></button>
                    </form>
                    {% else %}
                    <button class="btn btn-outline-primary btn-sm w-full" disabled>登录后可点餐</button>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

{% if user.is_authenticated %}
<section id="ai-recommend" class="py-12" style="background-color: #FFF8EF;">
    <div class="container">
        <h2 class="section-title"><i class="bi bi-brain"></i> AI智能三餐推荐</h2>
        <div class="card">
            <div class="card-body">
                <div class="row">
                    <div class="col-lg-8">
                        <p class="text-[#88807A] mb-4">AI将根据全家忌口、家中库存和时令食材，智能搭配一日三餐方案</p>
                    </div>
                    <div class="col-lg-4 text-right">
                        <a href="{% url 'ai_recommend' %}" class="btn btn-primary">
                            <i class="bi bi-lightbulb"></i> 生成推荐方案
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<section id="cart" class="py-12">
    <div class="container">
        <h2 class="section-title"><i class="bi bi-cart"></i> 点餐清单</h2>
        {% include 'cart.html' %}
    </div>
</section>

<section id="stocks" class="py-12" style="background-color: #FFF8EF;">
    <div class="container">
        <h2 class="section-title"><i class="bi bi-box-seam"></i> 食材库存</h2>
        <div class="card">
            <div class="card-header d-flex justify-between align-items-center">
                <span>当前库存列表</span>
                <a href="{% url 'stock_list' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus"></i> 管理库存</a>
            </div>
            <div class="card-body">
                {% if stocks %}
                <table class="table">
                    <thead><tr><th>食材名称</th><th>库存数量</th><th>状态</th><th>更新时间</th></tr></thead>
                    <tbody>
                        {% for stock in stocks %}
                        <tr>
                            <td>{{ stock.material.name }}</td>
                            <td>{{ stock.stock_num }}</td>
                            <td>{% if stock.tip == '临近过期' %}<span class="badge badge-danger">{{ stock.tip }}</span>{% else %}<span class="badge badge-success">库存充足</span>{% endif %}</td>
                            <td>{{ stock.update_time|date:'m-d H:i' }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p class="text-center text-[#88807A] py-4">暂无库存数据</p>
                {% endif %}
            </div>
        </div>
    </div>
</section>

<section id="markets" class="py-12">
    <div class="container">
        <h2 class="section-title"><i class="bi bi-shop"></i> 菜市场比价</h2>
        <div class="card">
            <div class="card-header d-flex justify-between align-items-center">
                <span>周边菜市场</span>
                <a href="{% url 'market_list' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus"></i> 管理市场</a>
            </div>
            <div class="card-body">
                {% if markets %}
                <div class="row row-cols-1 col-md-2 col-lg-4 g-4">
                    {% for market in markets %}
                    <div style="background-color: #FFF8EF; border-radius: 12px; padding: 16px;">
                        <h5 class="font-bold text-[#4A403A]">{{ market.market_name }}</h5>
                        <p class="text-sm text-[#88807A]">{{ market.area }}</p>
                    </div>
                    {% endfor %}
                </div>
                {% else %}
                <p class="text-center text-[#88807A] py-4">暂无菜市场数据</p>
                {% endif %}
            </div>
        </div>
    </div>
</section>

<section id="statistics" class="py-12" style="background-color: #FFF8EF;">
    <div class="container">
        <h2 class="section-title"><i class="bi bi-bar-chart"></i> 消费统计</h2>
        <div class="card">
            <div class="card-body">
                <a href="{% url 'statistics' %}" class="btn btn-primary"><i class="bi bi-calendar"></i> 查看详细统计</a>
            </div>
        </div>
    </div>
</section>

<section id="profile" class="py-12">
    <div class="container">
        <h2 class="section-title"><i class="bi bi-person"></i> 个人中心</h2>
        <div class="card">
            <div class="card-body">
                {% if user.is_authenticated %}
                <div class="row">
                    <div class="col-md-4 text-center">
                        <div class="w-24 h-24 bg-[#F7A072] rounded-full mx-auto flex items-center justify-center text-white text-3xl">{{ user.nickname|first }}</div>
                        <h4 class="font-bold mt-3">{{ user.nickname }}</h4>
                        <p class="text-[#88807A]">{{ user.family_role }}</p>
                    </div>
                    <div class="col-md-8">
                        <div class="row">
                            <div class="col-4"><a href="{% url 'user_center' %}" class="btn btn-outline-primary w-full"><i class="bi bi-gear"></i> 修改资料</a></div>
                            <div class="col-4"><a href="{% url 'my_collections' %}" class="btn btn-outline-primary w-full"><i class="bi bi-heart"></i> 我的收藏</a></div>
                            <div class="col-4"><a href="{% url 'order_list' %}" class="btn btn-outline-primary w-full"><i class="bi bi-list"></i> 历史订单</a></div>
                        </div>
                    </div>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</section>
{% endif %}

<section id="login" class="py-12" style="background-color: #FFF8EF;">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-5">
                <div class="card">
                    <div class="card-header text-center"><h3 class="font-bold text-[#4A403A]">登录</h3></div>
                    <div class="card-body">
                        {% if not user.is_authenticated %}
                        <form action="{% url 'login' %}" method="post">
                            {% csrf_token %}
                            <div class="mb-3"><label class="form-label">昵称</label><input type="text" name="nickname" class="form-control" required></div>
                            <div class="mb-3"><label class="form-label">密码</label><input type="password" name="password" class="form-control" required></div>
                            <button type="submit" class="btn btn-primary w-full">登录</button>
                        </form>
                        <p class="text-center mt-3 text-[#88807A]">还没有账号？<a href="#register" class="text-[#F7A072]">立即注册</a></p>
                        {% else %}
                        <p class="text-center text-[#88807A]">您已登录</p>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<section id="register" class="py-12">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-6">
                <div class="card">
                    <div class="card-header text-center"><h3 class="font-bold text-[#4A403A]">注册</h3></div>
                    <div class="card-body">
                        {% if not user.is_authenticated %}
                        <form action="{% url 'register' %}" method="post">
                            {% csrf_token %}
                            <div class="mb-3"><label class="form-label">昵称</label><input type="text" name="nickname" class="form-control" required></div>
                            <div class="mb-3"><label class="form-label">密码（至少6位）</label><input type="password" name="password" class="form-control" required></div>
                            <div class="mb-3"><label class="form-label">家庭身份</label>
                                <select name="family_role" class="form-select">
                                    <option value="爸爸">爸爸</option>
                                    <option value="妈妈">妈妈</option>
                                    <option value="孩子">孩子</option>
                                    <option value="长辈">长辈</option>
                                </select>
                            </div>
                            <button type="submit" class="btn btn-primary w-full">注册</button>
                        </form>
                        <p class="text-center mt-3 text-[#88807A]">已有账号？<a href="#login" class="text-[#F7A072]">立即登录</a></p>
                        {% else %}
                        <p class="text-center text-[#88807A]">您已登录，无需注册</p>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}'''

with open(r'D:\Python\python-training-main\family_ordering\templates\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Index.html restored successfully')