content = '''{% extends 'base.html' %}

{% block content %}
<style>
    .wood-texture {
        background-image: 
            repeating-linear-gradient(90deg, transparent, transparent 50px, rgba(139, 90, 43, 0.03) 50px, rgba(139, 90, 43, 0.03) 51px),
            repeating-linear-gradient(0deg, transparent, transparent 30px, rgba(139, 90, 43, 0.02) 30px, rgba(139, 90, 43, 0.02) 31px);
    }
    
    .food-card {
        transition: all 0.3s ease;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        width: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .food-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 30px rgba(247,160,114,0.2);
    }
    
    .food-image-container {
        height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        background: linear-gradient(135deg, rgba(247,160,114,0.1) 0%, rgba(148,180,159,0.1) 100%);
        position: relative;
        overflow: hidden;
        flex-shrink: 0;
    }
    
    .food-image-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .food-image-container::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
        transition: left 0.6s ease;
    }
    
    .food-card:hover .food-image-container::after {
        left: 100%;
    }
    
    .material-chip {
        display: inline-block;
        padding: 3px 10px;
        background-color: rgba(148, 180, 159, 0.15);
        color: #4A7C59;
        font-size: 0.75rem;
        border-radius: 12px;
        margin: 2px;
    }
    
    .price-tag {
        background: linear-gradient(135deg, #F7A072 0%, #E88F5D 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 15px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1.5rem;
    }
    
    .section-title-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #F7A072 0%, #E88F5D 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.2rem;
    }
    
    .season-card {
        background: linear-gradient(135deg, #94B49F 0%, #7BA385 100%);
        border-radius: 20px;
        padding: 1.5rem;
        color: white;
    }
    
    .season-tag {
        display: inline-block;
        padding: 4px 14px;
        background-color: rgba(255,255,255,0.2);
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 4px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .season-tag:hover {
        background-color: rgba(255,255,255,0.3);
        transform: scale(1.05);
    }
    
    .category-tabs {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 1rem;
    }
    
    .category-tab {
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }
    
    .category-tab.active {
        background: linear-gradient(135deg, #F7A072 0%, #E88F5D 100%);
        color: white;
    }
    
    .category-tab:not(.active) {
        background-color: rgba(247,160,114,0.1);
        color: #4A403A;
    }
    
    .category-tab:not(.active):hover {
        background-color: rgba(247,160,114,0.2);
    }
    
    .stock-item {
        background-color: #FFF8EF;
        border-radius: 12px;
        padding: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .stock-status {
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 10px;
    }
    
    .stock-status.sufficient {
        background-color: rgba(148, 180, 159, 0.2);
        color: #4A7C59;
    }
    
    .stock-status.warning {
        background-color: rgba(224, 114, 114, 0.2);
        color: #B04646;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #FFF8EF 0%, #FFFFFF 100%);
        padding: 4rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .hero-decoration {
        position: absolute;
        font-size: 10rem;
        opacity: 0.03;
        animation: float 8s ease-in-out infinite;
    }
    
    .hero-decoration.f1 { top: 5%; right: 5%; animation-delay: 0s; }
    .hero-decoration.f2 { bottom: 10%; left: 3%; animation-delay: 2s; }
    .hero-decoration.f3 { top: 40%; right: 15%; animation-delay: 4s; }
    .hero-decoration.f4 { top: 15%; left: 10%; animation-delay: 6s; }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-30px) rotate(8deg); }
    }
    
    .hero-icon-container {
        position: relative;
        height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        perspective: 1000px;
    }
    
    .hero-food-icon {
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        filter: drop-shadow(0 4px 12px rgba(0,0,0,0.1));
    }
    
    .hero-food-icon:nth-child(1) { 
        font-size: 5rem; 
        top: 10%; 
        left: 10%; 
        animation: floatHero 5s ease-in-out infinite; 
        z-index: 1;
    }
    .hero-food-icon:nth-child(2) { 
        font-size: 3.5rem; 
        top: 65%; 
        left: 20%; 
        animation: floatHero 5s ease-in-out infinite 0.8s; 
        z-index: 2;
    }
    .hero-food-icon:nth-child(3) { 
        font-size: 6rem; 
        top: 25%; 
        left: 55%; 
        animation: floatHero 5s ease-in-out infinite 1.6s; 
        z-index: 5;
    }
    .hero-food-icon:nth-child(4) { 
        font-size: 3rem; 
        top: 75%; 
        left: 70%; 
        animation: floatHero 5s ease-in-out infinite 2.4s; 
        z-index: 3;
    }
    .hero-food-icon:nth-child(5) { 
        font-size: 4.5rem; 
        top: 15%; 
        left: 80%; 
        animation: floatHero 5s ease-in-out infinite 3.2s; 
        z-index: 4;
    }
    
    @keyframes floatHero {
        0%, 100% { 
            transform: translateY(0) rotate(0deg) scale(1); 
            z-index: 1;
            opacity: 0.7;
        }
        25% { 
            transform: translateY(-30px) rotate(5deg) scale(1.1); 
            z-index: 3;
            opacity: 0.9;
        }
        50% { 
            transform: translateY(-50px) rotate(-3deg) scale(1.3); 
            z-index: 10;
            opacity: 1;
        }
        75% { 
            transform: translateY(-20px) rotate(3deg) scale(1.05); 
            z-index: 3;
            opacity: 0.85;
        }
    }
    
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 3000;
        display: none;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(5px);
    }
    
    .modal-overlay.show {
        display: flex;
    }
    
    .modal-content {
        background-color: white;
        border-radius: 20px;
        width: 90%;
        max-width: 450px;
        max-height: 85vh;
        overflow-y: auto;
        animation: modalIn 0.3s ease;
        display: flex;
        flex-direction: column;
    }
    
    .modal-content::-webkit-scrollbar {
        display: none;
    }
    
    @keyframes modalIn {
        from { opacity: 0; transform: scale(0.9) translateY(20px); }
        to { opacity: 1; transform: scale(1) translateY(0); }
    }
    
    .modal-header {
        background: linear-gradient(135deg, #F7A072 0%, #E88F5D 100%);
        padding: 1.25rem 1.5rem;
        text-align: center;
        color: white;
        border-radius: 20px 20px 0 0;
        position: relative;
        flex-shrink: 0;
    }
    
    .modal-header h3 {
        font-size: 1.25rem;
        margin-bottom: 0.25rem;
    }
    
    .modal-header p {
        font-size: 0.85rem;
        margin: 0;
    }
    
    .modal-close {
        position: absolute;
        right: 0.75rem;
        top: 0.75rem;
        background: rgba(255,255,255,0.2);
        border: none;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        font-size: 1rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
    }
    
    .modal-close:hover {
        background: rgba(255,255,255,0.3);
    }
    
    .modal-body {
        padding: 1.5rem;
        flex: 1;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
    }
    
    .modal-body .form-label {
        font-size: 0.9rem;
        font-weight: 500;
        color: #4A403A;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .modal-body .form-control,
    .modal-body .form-select {
        font-size: 0.9rem;
        padding: 0.75rem;
        border-radius: 10px;
        border: 1px solid rgba(74, 64, 58, 0.1);
        margin-bottom: 1rem;
        width: 100%;
        box-sizing: border-box;
    }
    
    .modal-body .btn-primary {
        width: 100%;
        padding: 0.75rem;
        font-size: 0.95rem;
        font-weight: 500;
        border-radius: 20px;
        margin-top: 0.5rem;
    }
    
    .modal-body .text-sm {
        font-size: 0.85rem;
        color: #88807A;
        margin-top: 1rem;
        text-align: center;
    }
    
    .modal-error {
        background-color: rgba(224, 114, 114, 0.1);
        color: #E07272;
        padding: 0.75rem;
        border-radius: 10px;
        font-size: 0.85rem;
        margin-bottom: 1rem;
        display: none;
    }
    
    .responsive-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 24px;
    }
    
    .navbar {
        position: fixed !important;
        top: 0;
        left: 0;
        right: 0;
        z-index: 9999 !important;
        width: 100%;
    }
    
    main {
        padding-top: 80px;
    }
    
    .toast-notification {
        position: fixed;
        top: 100px;
        right: 20px;
        background: linear-gradient(135deg, #F7A072 0%, #E88F5D 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(247,160,114,0.3);
        z-index: 10000;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    
    .toast-notification.show {
        opacity: 1;
        transform: translateX(0);
    }
    
    .cart-summary {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        padding: 12px 20px;
        z-index: 9998;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.3s ease;
    }
    
    .cart-summary:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(247,160,114,0.2);
    }
    
    .cart-count {
        background: linear-gradient(135deg, #F7A072 0%, #E88F5D 100%);
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .location-btn {
        background: linear-gradient(135deg, #94B49F 0%, #7BA385 100%);
        color: white;
        border: none;
        padding: 6px 14px;
        border-radius: 12px;
        font-size: 0.85rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 6px;
        transition: all 0.2s ease;
    }
    
    .location-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 2px 10px rgba(148,180,159,0.3);
    }
    
    .location-btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
    }
</style>

<section class="hero-section" id="top">
    <div class="container">
        <div class="hero-decoration f1">🍳</div>
        <div class="hero-decoration f2">🥗</div>
        <div class="hero-decoration f3">🍎</div>
        <div class="hero-decoration f4">🥕</div>
        
        <div class="row align-items-center">
            <div class="col-lg-6">
                <div class="mb-4">
                    <span style="display: inline-block; padding: 6px 18px; background: rgba(247,160,114,0.15); border-radius: 20px; font-size: 0.9rem; color: #F7A072; font-weight: 500;">
                        <i class="bi bi-heart"></i> 让家更温暖
                    </span>
                </div>
                <h1 class="text-4xl font-bold text-[#4A403A] mb-4">
                    <span class="text-[#F7A072]">家味</span> - 让买菜做饭更简单
                </h1>
                <p class="text-lg text-[#88807A] mb-6">
                    一站式家庭智能点餐与食材采购核算系统，帮您轻松管理三餐，智能搭配菜谱，精准计算采购清单。
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
                    <button onclick="showModal('register')" class="btn btn-outline-primary px-6 py-3">
                        <i class="bi bi-person-plus"></i> 立即注册
                    </button>
                    {% endif %}
                </div>
            </div>
            <div class="col-lg-6">
                <div class="hero-icon-container">
                    <span class="hero-food-icon">🍳</span>
                    <span class="hero-food-icon">🥗</span>
                    <span class="hero-food-icon">🍎</span>
                    <span class="hero-food-icon">🥕</span>
                    <span class="hero-food-icon">🥦</span>
                </div>
            </div>
        </div>
    </div>
</section>

<section id="seasonal" class="py-8" style="background-color: #94B49F;">
    <div class="container">
        <div class="season-card">
            <div class="row align-items-center">
                <div class="col-lg-8">
                    <h3 class="text-xl font-bold flex items-center gap-3 mb-3">
                        <i class="bi bi-leaf"></i>
                        {{ season }}季时令食材推荐
                    </h3>
                    <p class="text-white/80 text-sm mb-3">
                        根据季节变化，为您精选当季新鲜食材，营养丰富，价格实惠
                    </p>
                    <div class="flex flex-wrap" id="seasonal-carousel">
                        {% for material in seasonal_materials %}
                        <span class="season-tag">{{ material.name }}</span>
                        {% endfor %}
                    </div>
                </div>
                <div class="col-lg-4 text-center">
                    <div style="font-size: 3rem;">🥬🍅🌶️</div>
                </div>
            </div>
        </div>
    </div>
</section>

<section id="dishes" class="py-12 wood-texture">
    <div class="container">
        <div class="section-header">
            <div class="section-title-icon"><i class="bi bi-utensils"></i></div>
            <div>
                <h2 class="text-2xl font-bold text-[#4A403A]">菜品库</h2>
                <p class="text-sm text-[#88807A]">精选家常菜谱，让每一餐都充满家的味道</p>
            </div>
        </div>

        <div class="category-tabs">
            {% for category, dishes in dishes_by_category.items %}
            {% if dishes %}
            <div class="category-tab active" onclick="showCategory('{{ category }}')">{{ category }}</div>
            {% endif %}
            {% endfor %}
        </div>

        {% for category, dishes in dishes_by_category.items %}
        {% if dishes %}
        <div id="category-{{ category }}" class="category-content">
            <div class="responsive-grid">
                {% for item in dishes %}
                {% with dish=item.dish %}
                <div class="food-card card h-100">
                    <div class="food-image-container">
                        {% if dish.image %}
                        <img src="{{ dish.image }}" alt="{{ dish.name }}">
                        {% else %}
                        {% if dish.category == '素菜' %}🥬
                        {% elif dish.category == '荤菜' %}🍖
                        {% elif dish.category == '汤品' %}🍲
                        {% elif dish.category == '凉菜' %}🥗
                        {% else %}🍟{% endif %}
                        {% endif %}
                    </div>
                    <div class="card-body p-4 flex-grow">
                        <div class="d-flex justify-between items-start mb-2">
                            <h5 class="font-bold text-[#4A403A]">{{ dish.name }}</h5>
                            <span class="price-tag">¥{{ dish.base_price }}</span>
                        </div>
                        {% if item.materials %}
                        <div class="mb-3">
                            <p class="text-xs text-[#88807A] mb-1 font-medium">食材组成：</p>
                            <div style="display: flex; flex-wrap: wrap;">
                                {% for mat in item.materials %}
                                <span class="material-chip">{{ mat.name }} {{ mat.num }}{{ mat.unit }}</span>
                                {% endfor %}
                            </div>
                        </div>
                        {% endif %}
                        {% if item.has_taboo %}
                        <div class="mb-3 p-2 bg-[#E07272]/10 rounded-lg">
                            <p class="text-xs text-[#E07272]"><i class="bi bi-exclamation-circle"></i> 含忌口食材：{{ item.taboo_name }}</p>
                        </div>
                        {% endif %}
                        {% if user.is_authenticated %}
                        <form action="{% url 'add_to_cart' %}" method="post" class="cart-form" style="display: flex; gap: 4px;">
                            {% csrf_token %}
                            <input type="hidden" name="goods_type" value="dish">
                            <input type="hidden" name="goods_id" value="{{ dish.id }}">
                            <select name="eat_time" class="form-select form-select-sm" style="flex: 1; font-size: 0.8rem;">
                                <option value="早餐">早餐</option>
                                <option value="午餐">午餐</option>
                                <option value="晚餐">晚餐</option>
                                <option value="加餐">加餐</option>
                            </select>
                            <input type="number" name="buy_num" value="1" min="1" class="form-control form-control-sm" style="width: 40px;">
                            <button type="submit" class="btn btn-primary btn-sm" style="width: 36px; height: 36px; padding: 0;"><i class="bi bi-plus"></i></button>
                        </form>
                        {% else %}
                        <button onclick="showModal('login')" class="btn btn-outline-primary btn-sm w-full">登录后可点餐</button>
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
        <div class="section-header">
            <div class="section-title-icon"><i class="bi bi-apple"></i></div>
            <div>
                <h2 class="text-2xl font-bold text-[#4A403A]">水果专区</h2>
                <p class="text-sm text-[#88807A]">新鲜水果，补充每日维生素</p>
            </div>
        </div>
        <div class="responsive-grid">
            {% for fruit in fruits %}
            <div class="food-card card h-100">
                <div class="food-image-container">
                    {% if fruit.image %}
                    <img src="{{ fruit.image }}" alt="{{ fruit.name }}">
                    {% else %}
                    {% if fruit.name == '苹果' %}🍎
                    {% elif fruit.name == '香蕉' %}🍌
                    {% elif fruit.name == '橙子' %}🍊
                    {% elif fruit.name == '葡萄' %}🍇
                    {% elif fruit.name == '芒果' %}🥭
                    {% elif fruit.name == '草莓' %}🍓
                    {% elif fruit.name == '西瓜' %}🍉
                    {% elif fruit.name == '桃子' %}🍑
                    {% else %}🍒{% endif %}
                    {% endif %}
                </div>
                <div class="card-body p-4 flex-grow">
                    <div class="d-flex justify-between items-start mb-2">
                        <h5 class="font-bold text-[#4A403A]">{{ fruit.name }}</h5>
                        <span class="price-tag">¥{{ fruit.base_price }}/斤</span>
                    </div>
                    {% if fruit.is_allergy %}
                    <div class="mb-3 p-2 bg-[#E07272]/10 rounded-lg">
                        <p class="text-xs text-[#E07272]"><i class="bi bi-exclamation-circle"></i> 易过敏水果</p>
                    </div>
                    {% endif %}
                    {% if user.is_authenticated %}
                    <form action="{% url 'add_to_cart' %}" method="post" class="cart-form" style="display: flex; gap: 4px;">
                        {% csrf_token %}
                        <input type="hidden" name="goods_type" value="fruit">
                        <input type="hidden" name="goods_id" value="{{ fruit.id }}">
                        <select name="eat_time" class="form-select form-select-sm" style="flex: 1; font-size: 0.8rem;">
                            <option value="早餐">早餐</option>
                            <option value="午餐">午餐</option>
                            <option value="晚餐">晚餐</option>
                            <option value="加餐">加餐</option>
                        </select>
                        <input type="number" name="buy_num" value="1" min="1" class="form-control form-control-sm" style="width: 40px;">
                        <button type="submit" class="btn btn-primary btn-sm" style="width: 36px; height: 36px; padding: 0;"><i class="bi bi-plus"></i></button>
                    </form>
                    {% else %}
                    <button onclick="showModal('login')" class="btn btn-outline-primary btn-sm w-full">登录后可点餐</button>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<section id="drinks" class="py-12 wood-texture">
    <div class="container">
        <div class="section-header">
            <div class="section-title-icon"><i class="bi bi-cup-soda"></i></div>
            <div>
                <h2 class="text-2xl font-bold text-[#4A403A]">饮品专区</h2>
                <p class="text-sm text-[#88807A]">清爽饮品，开启美好一天</p>
            </div>
        </div>
        <div class="responsive-grid">
            {% for drink in drinks %}
            <div class="food-card card h-100">
                <div class="food-image-container">
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
                <div class="card-body p-4 flex-grow">
                    <div class="d-flex justify-between items-start mb-2">
                        <h5 class="font-bold text-[#4A403A]">{{ drink.name }}</h5>
                        <span class="price-tag">¥{{ drink.price }}</span>
                    </div>
                    {% if drink.is_lactose %}
                    <div class="mb-3 p-2 bg-[#E07272]/10 rounded-lg">
                        <p class="text-xs text-[#E07272]"><i class="bi bi-exclamation-circle"></i> 含乳糖</p>
                    </div>
                    {% endif %}
                    {% if user.is_authenticated %}
                    <form action="{% url 'add_to_cart' %}" method="post" class="cart-form" style="display: flex; gap: 4px;">
                        {% csrf_token %}
                        <input type="hidden" name="goods_type" value="drink">
                        <input type="hidden" name="goods_id" value="{{ drink.id }}">
                        <select name="eat_time" class="form-select form-select-sm" style="flex: 1; font-size: 0.8rem;">
                            <option value="早餐">早餐</option>
                            <option value="午餐">午餐</option>
                            <option value="晚餐">晚餐</option>
                            <option value="加餐">加餐</option>
                        </select>
                        <input type="number" name="buy_num" value="1" min="1" class="form-control form-control-sm" style="width: 40px;">
                        <button type="submit" class="btn btn-primary btn-sm" style="width: 36px; height: 36px; padding: 0;"><i class="bi bi-plus"></i></button>
                    </form>
                    {% else %}
                    <button onclick="showModal('login')" class="btn btn-outline-primary btn-sm w-full">登录后可点餐</button>
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
        <div class="section-header">
            <div class="section-title-icon"><i class="bi bi-brain"></i></div>
            <div>
                <h2 class="text-2xl font-bold text-[#4A403A]">AI智能三餐推荐</h2>
                <p class="text-sm text-[#88807A]">基于AI算法，为您定制专属一日三餐方案</p>
            </div>
        </div>
        <div class="card food-card">
            <div class="card-body p-6">
                <div class="row align-items-center">
                    <div class="col-lg-8">
                        <div class="mb-3" style="font-size: 3rem;">🤖</div>
                        <h3 class="h4 font-bold text-[#4A403A] mb-2">智能配餐助手</h3>
                        <p class="text-[#88807A] text-sm">
                            AI将根据全家忌口、家中库存和时令食材，智能搭配营养均衡的一日三餐方案。让您不再为吃什么而烦恼！
                        </p>
                        {% if taboo_names %}
                        <div class="mt-3 p-3 bg-[#E07272]/10 rounded-lg">
                            <p class="text-xs text-[#E07272]"><i class="bi bi-exclamation-circle"></i> 已识别忌口：{{ taboo_names|join:', ' }}</p>
                        </div>
                        {% endif %}
                    </div>
                    <div class="col-lg-4 text-center">
                        <a href="{% url 'ai_recommend' %}" class="btn btn-primary px-6 py-3">
                            <i class="bi bi-lightbulb"></i> 生成推荐方案
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<section id="cart" class="py-12 wood-texture">
    <div class="container">
        <div class="section-header">
            <div class="section-title-icon"><i class="bi bi-cart"></i></div>
            <div>
                <h2 class="text-2xl font-bold text-[#4A403A]">点餐清单</h2>
                <p class="text-sm text-[#88807A]">查看您的点餐清单，准备采购食材</p>
            </div>
        </div>
        {% include 'cart.html' %}
    </div>
</section>

<section id="stocks" class="py-12" style="background-color: #FFF8EF;">
    <div class="container">
        <div class="section-header">
            <div class="section-title-icon"><i class="bi bi-box-seam"></i></div>
            <div>
                <h2 class="text-2xl font-bold text-[#4A403A]">食材库存</h2>
                <p class="text-sm text-[#88807A]">实时管理家中食材库存，避免浪费</p>
            </div>
        </div>
        <div class="card">
            <div class="card-header d-flex justify-between align-items-center" style="background-color: rgba(247,160,114,0.05); border-radius: 16px 16px 0 0;">
                <span class="font-bold text-[#4A403A]">当前库存列表</span>
                <a href="{% url 'stock_list' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus"></i> 管理库存</a>
            </div>
            <div class="card-body">
                {% if stocks %}
                <div class="responsive-grid">
                    {% for stock in stocks %}
                    <div class="stock-item">
                        <div>
                            <h5 class="font-bold text-[#4A403A] text-sm">{{ stock.material.name }}</h5>
                            <p class="text-xs text-[#88807A]">库存：{{ stock.stock_num }}</p>
                        </div>
                        <span class="stock-status {% if stock.tip == '临近过期' %}warning{% else %}sufficient{% endif %}">
                            {% if stock.tip == '临近过期' %}临近过期{% else %}充足{% endif %}
                        </span>
                    </div>
                    {% endfor %}
                </div>
                {% else %}
                <div class="text-center py-8">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📦</div>
                    <p class="text-[#88807A]">暂无库存数据</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</section>

<section id="markets" class="py-12 wood-texture">
    <div class="container">
        <div class="section-header">
            <div class="section-title-icon"><i class="bi bi-shop"></i></div>
            <div class="d-flex align-items-center gap-3">
                <div>
                    <h2 class="text-2xl font-bold text-[#4A403A]">菜市场比价</h2>
                    <p class="text-sm text-[#88807A]">周边菜市场价格对比，省钱又省心</p>
                </div>
                <button id="locate-btn" class="location-btn" onclick="getLocation()">
                    <i class="bi bi-geo-alt"></i> 定位
                </button>
            </div>
        </div>
        <div id="location-info" class="mb-4 p-3 bg-[#94B49F]/10 rounded-lg" style="display: none;">
            <p class="text-sm text-[#4A7C59]"><i class="bi bi-geo-alt"></i> 当前位置：<span id="location-text">定位中...</span></p>
        </div>
        <div class="card">
            <div class="card-header d-flex justify-between align-items-center" style="background-color: rgba(247,160,114,0.05); border-radius: 16px 16px 0 0;">
                <span class="font-bold text-[#4A403A]">周边菜市场</span>
                <a href="{% url 'market_list' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus"></i> 管理市场</a>
            </div>
            <div class="card-body">
                {% if markets %}
                <div class="responsive-grid">
                    {% for market in markets %}
                    <div class="food-card p-4 text-center">
                        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🏪</div>
                        <h5 class="font-bold text-[#4A403A]">{{ market.market_name }}</h5>
                        <p class="text-xs text-[#88807A]">{{ market.area }}</p>
                        <p class="text-xs text-[#F7A072]">{{ market.address }}</p>
                    </div>
                    {% endfor %}
                </div>
                {% else %}
                <div class="text-center py-8">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🛒</div>
                    <p class="text-[#88807A]">暂无菜市场数据</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</section>

<section id="statistics" class="py-12" style="background-color: #FFF8EF;">
    <div class="container">
        <div class="section-header">
            <div class="section-title-icon"><i class="bi bi-bar-chart"></i></div>
            <div>
                <h2 class="text-2xl font-bold text-[#4A403A]">消费统计</h2>
                <p class="text-sm text-[#88807A]">可视化分析家庭消费情况</p>
            </div>
        </div>
        <div class="card food-card">
            <div class="card-body p-6 text-center">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h3 class="h4 font-bold text-[#4A403A] mb-2">消费统计中心</h3>
                <p class="text-[#88807A] text-sm mb-4">查看月度消费趋势、食材采购分析和家庭餐饮统计报告</p>
                <a href="{% url 'statistics' %}" class="btn btn-primary px-6 py-3">
                    <i class="bi bi-calendar"></i> 查看详细统计
                </a>
            </div>
        </div>
    </div>
</section>

<section id="profile" class="py-12 wood-texture">
    <div class="container">
        <div class="section-header">
            <div class="section-title-icon"><i class="bi bi-person"></i></div>
            <div>
                <h2 class="text-2xl font-bold text-[#4A403A]">个人中心</h2>
                <p class="text-sm text-[#88807A]">管理您的账户信息和偏好设置</p>
            </div>
        </div>
        <div class="card">
            <div class="card-body p-6">
                {% if user.is_authenticated %}
                <div class="row">
                    <div class="col-md-4 text-center">
                        <div class="w-24 h-24 bg-gradient-to-br from-[#F7A072] to-[#E88F5D] rounded-full mx-auto flex items-center justify-center text-white text-3xl mb-3">
                            {{ user.nickname|first }}
                        </div>
                        <h4 class="font-bold text-[#4A403A]">{{ user.nickname }}</h4>
                        <p class="text-sm text-[#88807A]">{{ user.family_role }}</p>
                    </div>
                    <div class="col-md-8">
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
                            <a href="{% url 'profile' %}" class="btn btn-outline-primary w-full p-3">
                                <i class="bi bi-gear"></i>
                                <br><span class="text-xs">修改资料</span>
                            </a>
                            <a href="{% url 'collect' %}" class="btn btn-outline-primary w-full p-3">
                                <i class="bi bi-heart"></i>
                                <br><span class="text-xs">我的收藏</span>
                            </a>
                            <a href="{% url 'order_list' %}" class="btn btn-outline-primary w-full p-3">
                                <i class="bi bi-list"></i>
                                <br><span class="text-xs">历史订单</span>
                            </a>
                        </div>
                    </div>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</section>
{% endif %}

<div id="login-modal" class="modal-overlay">
    <div class="modal-content">
        <div class="modal-header">
            <button class="modal-close" onclick="hideModal('login')">&times;</button>
            <h3>欢迎回家</h3>
            <p>登录您的家味账户</p>
        </div>
        <div class="modal-body">
            {% if not user.is_authenticated %}
            <div id="login-error" class="modal-error"></div>
            <form id="login-form" action="{% url 'login' %}" method="post">
                {% csrf_token %}
                <label class="form-label">昵称</label>
                <input type="text" name="nickname" class="form-control" required>
                
                <label class="form-label">密码</label>
                <input type="password" name="password" class="form-control" required>
                
                <button type="submit" class="btn btn-primary">登录</button>
            </form>
            <p class="text-sm">还没有账号？<button onclick="switchModal('register')" class="text-[#F7A072] font-medium bg-transparent border-none cursor-pointer">立即注册</button></p>
            {% else %}
            <div class="text-center py-6">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">✅</div>
                <p class="text-[#88807A]">您已登录</p>
            </div>
            {% endif %}
        </div>
    </div>
</div>

<div id="register-modal" class="modal-overlay">
    <div class="modal-content">
        <div class="modal-header">
            <button class="modal-close" onclick="hideModal('register')">&times;</button>
            <h3>加入家味</h3>
            <p>创建您的家庭账户</p>
        </div>
        <div class="modal-body">
            {% if not user.is_authenticated %}
            <div id="register-error" class="modal-error"></div>
            <form id="register-form" action="{% url 'register' %}" method="post">
                {% csrf_token %}
                <label class="form-label">昵称</label>
                <input type="text" name="nickname" class="form-control" required>
                
                <label class="form-label">密码（至少6位）</label>
                <input type="password" name="password" class="form-control" required>
                
                <label class="form-label">家庭身份</label>
                <select name="family_role" class="form-select">
                    <option value="爸爸">爸爸</option>
                    <option value="妈妈">妈妈</option>
                    <option value="孩子">孩子</option>
                    <option value="长辈">长辈</option>
                </select>
                
                <button type="submit" class="btn btn-primary">注册</button>
            </form>
            <p class="text-sm">已有账号？<button onclick="switchModal('login')" class="text-[#F7A072] font-medium bg-transparent border-none cursor-pointer">立即登录</button></p>
            {% else %}
            <div class="text-center py-6">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">✅</div>
                <p class="text-[#88807A]">您已登录，无需注册</p>
            </div>
            {% endif %}
        </div>
    </div>
</div>

<div id="toast" class="toast-notification">已加入点餐清单</div>

{% if user.is_authenticated %}
<div class="cart-summary" id="cart-summary">
    <div class="cart-count" id="cart-count">0</div>
    <span class="text-sm font-medium text-[#4A403A]">点餐清单</span>
    <i class="bi bi-cart" style="color: #F7A072;"></i>
</div>
{% endif %}

<script>
    function showCategory(category) {
        document.querySelectorAll('.category-tab').forEach(tab => tab.classList.remove('active'));
        document.querySelector(`[onclick="showCategory('${category}')"]`).classList.add('active');
        
        document.querySelectorAll('.category-content').forEach(content => {
            content.style.display = 'none';
        });
        document.getElementById(`category-${category}`).style.display = 'block';
    }
    
    function showModal(type) {
        const modal = document.getElementById(`${type}-modal`);
        if (modal) {
            modal.classList.add('show');
            document.body.style.overflow = 'hidden';
        }
    }
    
    function hideModal(type) {
        const modal = document.getElementById(`${type}-modal`);
        if (modal) {
            modal.classList.remove('show');
            document.body.style.overflow = '';
        }
    }
    
    function switchModal(type) {
        document.querySelectorAll('.modal-overlay').forEach(modal => modal.classList.remove('show'));
        setTimeout(() => {
            showModal(type);
        }, 100);
    }
    
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('show');
                document.body.style.overflow = '';
            }
        });
    });
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    const seasonalTags = document.querySelectorAll('.season-tag');
    let tagIndex = 0;
    setInterval(() => {
        seasonalTags.forEach(tag => tag.style.transform = 'scale(1)');
        tagIndex = (tagIndex + 1) % seasonalTags.length;
        if (seasonalTags[tagIndex]) {
            seasonalTags[tagIndex].style.transform = 'scale(1.1)';
        }
    }, 2000);
    
    document.getElementById('register-form')?.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const errorDiv = document.getElementById('register-error');
        
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                return response.text();
            }
        })
        .then(data => {
            if (data) {
                try {
                    const result = JSON.parse(data);
                    if (result.error) {
                        errorDiv.textContent = result.error;
                        errorDiv.style.display = 'block';
                    }
                } catch (e) {
                    window.location.href = window.location.pathname;
                }
            }
        })
        .catch(error => {
            errorDiv.textContent = '注册失败，请重试';
            errorDiv.style.display = 'block';
        });
    });
    
    document.getElementById('login-form')?.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const errorDiv = document.getElementById('login-error');
        
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                return response.text();
            }
        })
        .then(data => {
            if (data) {
                try {
                    const result = JSON.parse(data);
                    if (result.error) {
                        errorDiv.textContent = result.error;
                        errorDiv.style.display = 'block';
                    }
                } catch (e) {
                    window.location.href = window.location.pathname;
                }
            }
        })
        .catch(error => {
            errorDiv.textContent = '登录失败，请重试';
            errorDiv.style.display = 'block';
        });
    });
    
    document.querySelectorAll('.cart-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast('已加入点餐清单');
                    updateCartCount(data.cart_count);
                    
                    const cartSection = document.getElementById('cart');
                    if (cartSection) {
                        cartSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }
                }
            })
            .catch(error => {
                console.error('Add to cart failed:', error);
            });
        });
    });
    
    function showToast(message) {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 2000);
    }
    
    function updateCartCount(count) {
        const cartCount = document.getElementById('cart-count');
        if (cartCount) {
            cartCount.textContent = count;
        }
    }
    
    function getLocation() {
        const locateBtn = document.getElementById('locate-btn');
        const locationInfo = document.getElementById('location-info');
        const locationText = document.getElementById('location-text');
        
        locateBtn.disabled = true;
        locateBtn.innerHTML = '<i class="bi bi-geo-alt"></i> 定位中...';
        locationInfo.style.display = 'block';
        locationText.textContent = '定位中...';
        
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
                    
                    fetch(`https://api.map.baidu.com/geocoder/reverse?location=${latitude},${longitude}&output=json&ak=您的百度地图AK`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.result && data.result.addressComponent) {
                            const address = data.result.addressComponent;
                            locationText.textContent = `${address.city || address.province} ${address.district || ''}`;
                        } else {
                            locationText.textContent = `${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
                        }
                        locateBtn.disabled = false;
                        locateBtn.innerHTML = '<i class="bi bi-geo-alt"></i> 重新定位';
                    })
                    .catch(error => {
                        locationText.textContent = `${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
                        locateBtn.disabled = false;
                        locateBtn.innerHTML = '<i class="bi bi-geo-alt"></i> 重新定位';
                    });
                },
                function(error) {
                    locationText.textContent = '定位失败，请手动选择城市';
                    locateBtn.disabled = false;
                    locateBtn.innerHTML = '<i class="bi bi-geo-alt"></i> 重新定位';
                },
                { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
            );
        } else {
            locationText.textContent = '浏览器不支持定位';
            locateBtn.disabled = false;
            locateBtn.innerHTML = '<i class="bi bi-geo-alt"></i> 定位';
        }
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        fetch('{% url "cart_count" %}')
        .then(response => response.json())
        .then(data => {
            updateCartCount(data.count);
        });
    });
</script>
{% endblock %}'''

with open(r'D:\Python\python-training-main\family_ordering\templates\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Index.html updated successfully')