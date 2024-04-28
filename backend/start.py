from flask import Flask, request, jsonify, Blueprint
import sqlite3
from sqlite3 import Error
import json
from flask_cors import CORS

# 创建一个 Blueprint 实例
api_v1 = Blueprint('api_v1', __name__)

# 数据库文件位置
DATABASE = 'dbsqlite3.db'


# 连接数据库
def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(e)


@api_v1.route('/profile/shopping1', methods=['GET'])
def get_shopping_data():
    conn = get_db_connection()
    cur = conn.cursor()

    # 查询所有分组数据
    cur.execute('SELECT * FROM entries ORDER BY group_id, id')
    entries_rows = cur.fetchall()

    # 组织数据以返回所有分组
    entries = {}
    for row in entries_rows:
        group_id = row['group_id']
        entry = {'name': row['name'], 'image': row['image']}
        if group_id not in entries:
            entries[group_id] = [entry]
        else:
            entries[group_id].append(entry)

    # 将字典转换为列表，保持JSON格式
    entries_list = [entries[group_id] for group_id in sorted(entries)]

    cur.close()
    conn.close()

    return jsonify({'entries': entries_list})


@api_v1.route('/profile/filter1', methods=['GET'])
def get_filter_data():
    conn = get_db_connection()
    cur = conn.cursor()

    # 查询 navTab 数据
    cur.execute('SELECT * FROM navTab')
    navTab = [dict(ix) for ix in cur.fetchall()]

    # 查询 sortBy 数据
    cur.execute('SELECT * FROM sortBy')
    sortBy = [dict(ix) for ix in cur.fetchall()]

    # 查询 screenBy 和 screenByOptions 数据
    cur.execute('SELECT * FROM screenBy')
    rows = cur.fetchall()

    screenBy = []
    for row in rows:
        screenBy.append({
            'id': row['id'],
            'title': row['title'],
            # Assuming data is stored in valid JSON format
            'data': json.loads(row['data'])
        })

    cur.close()
    conn.close()

    return jsonify({'navTab': navTab, 'sortBy': sortBy, 'screenBy': screenBy})


@api_v1.route('/profile/restaurants', methods=['GET'])
def get_restaurants():
    # 从请求中获取分页参数和排序规则参数
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    sortruler = request.args.get('sortParamsData')
    # 计算OFFSET值，从第1页开始
    offset = (page - 1) * size

    conn = get_db_connection()
    cur = conn.cursor()

    if sortruler == "distance":
        # 按distance属性排序，并分页
        cur.execute(
            'SELECT * FROM restaurants ORDER BY distance LIMIT ? OFFSET ?', (size, offset))
        print("按距离排序成功")
    elif sortruler == "is_premium":
        # 按distance属性排序，并分页
        cur.execute(
            'SELECT * FROM restaurants where is_premium=1 LIMIT ? OFFSET ?', (size, offset))
        print("按品牌排序成功")
    elif sortruler == "rating":
        # 按distance属性排序，并分页
        cur.execute(
            'SELECT * FROM restaurants ORDER BY rating desc LIMIT ? OFFSET ?', (size, offset))
        print("按评分排序成功")
    elif sortruler == "recent_order_num":
        # 按distance属性排序，并分页
        cur.execute(
            'SELECT * FROM restaurants ORDER BY recent_order_num desc LIMIT ? OFFSET ?', (size, offset))
        print("按销量排序成功")
    elif sortruler == "float_minimum_order_amount":
        # 按distance属性排序，并分页
        cur.execute(
            'SELECT * FROM restaurants ORDER BY float_minimum_order_amount LIMIT ? OFFSET ?', (size, offset))
        print("按起送价排序成功")
    elif sortruler == "order_lead_time":
        # 按distance属性排序，并分页
        cur.execute(
            'SELECT * FROM restaurants ORDER BY order_lead_time LIMIT ? OFFSET ?', (size, offset))
        print("按配送最快排序成功")
    elif sortruler == "float_delivery_fee":
        # 按distance属性排序，并分页
        cur.execute(
            'SELECT * FROM restaurants ORDER BY float_delivery_fee LIMIT ? OFFSET ?', (size, offset))
        print("按配送费最低排序成功")
    else:
        # 正常分页查询
        cur.execute('SELECT * FROM restaurants LIMIT ? OFFSET ?',
                    (size, offset))
        print("未排序")

    restaurants_rows = cur.fetchall()

    # 将查询结果转换为字典列表
    restaurants = [dict(ix) for ix in restaurants_rows]

    cur.close()
    conn.close()

    return jsonify({'restaurants': restaurants})


@api_v1.route('/profile/search', methods=['GET'])
def search_restaurants():
    key_word = request.args.get('key_word')  # 从查询参数中获取关键字
    if not key_word:
        return jsonify({'error': '缺少key_word参数'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # 执行跨表搜索的 SQL 查询
        cur.execute('''SELECT DISTINCT r.* FROM restaurants r
                       LEFT JOIN restaurants_menus rm ON r.id = rm.restaurant_id
                       LEFT JOIN restaurants_menus_foods rmf ON rm.id = rmf.menu_id
                       WHERE r.name LIKE ? OR rmf.name LIKE ?''',
                    ('%' + key_word + '%', '%' + key_word + '%'))
        matched_restaurants = cur.fetchall()
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    if matched_restaurants:
        # 将查询结果转换为列表字典
        restaurants_list = [dict(restaurant)
                            for restaurant in matched_restaurants]
        return jsonify({'restaurants': restaurants_list})
    else:
        return jsonify({'error': '没有匹配的结果'}), 404


@api_v1.route('/profile/restaurants_detail', methods=['GET'])
def get_restaurant_detail():
    shop_id = request.args.get('shop_id')  # 从查询参数获取shop_id
    if not shop_id:
        return jsonify({"error": "Missing 'shop_id' query parameter."}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # 根据shop_id查询店铺详情
    cur.execute('SELECT * FROM restaurants WHERE id = ?', (shop_id,))
    restaurant = cur.fetchone()

    if restaurant is None:
        return jsonify({"error": "Restaurant not found."}), 404

    # 将查询结果转换为字典
    restaurant_detail = dict(restaurant)

    cur.close()
    conn.close()

    return jsonify(restaurant_detail)


@api_v1.route('/profile/restaurants_menus', methods=['GET'])
def get_restaurant_menus():
    shop_id = request.args.get('shop_id')  # 从查询参数获取shop_id
    if not shop_id:
        return jsonify({"error": "Missing 'shop_id' query parameter."}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # 根据shop_id查询该店铺的所有菜单
    cur.execute(
        'SELECT * FROM restaurants_menus WHERE restaurant_id = ?', (shop_id,))
    menus_rows = cur.fetchall()

    if menus_rows is None:
        return jsonify({"error": "Menus not found."}), 404

    # 将查询结果转换为字典列表
    menus = [dict(menu) for menu in menus_rows]

    cur.close()
    conn.close()

    return jsonify({'menus': menus})


@api_v1.route('/profile/restaurants_menus_foods', methods=['GET'])
def get_menu_foods():
    menu_id = request.args.get('menu_id')  # 从查询参数获取menu_id
    if not menu_id:
        return jsonify({"error": "Missing 'menu_id' query parameter."}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # 根据menu_id查询该菜单下的所有食物
    cur.execute(
        'SELECT * FROM restaurants_menus_foods WHERE menu_id = ?', (menu_id,))
    foods_rows = cur.fetchall()

    if foods_rows is None:
        return jsonify({"error": "Foods not found."}), 404

    # 将查询结果转换为字典列表
    foods = [dict(food) for food in foods_rows]

    cur.close()
    conn.close()

    return jsonify({'foods': foods})


@api_v1.route('/profile/restaurants_foods_details', methods=['GET'])
def get_food_details():
    food_id = request.args.get('food_id')
    if not food_id:
        return jsonify({'error': 'Missing food_id parameter'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # 尝试获取与food_id匹配的食物详细信息
    cur.execute('SELECT * FROM restaurants_menus_foods WHERE id = ?', (food_id,))
    food_details = cur.fetchone()

    cur.close()
    conn.close()

    if food_details:
        # 将结果从sqlite3.Row对象转换为字典
        food_details_dict = dict(food_details)
        return jsonify({'food_details': food_details_dict})
    else:
        return jsonify({'error': 'Food not found'}), 404


@api_v1.route('/profile/comments_restaurants', methods=['GET'])
def get_comments_by_restaurant():
    restaurant_id = request.args.get('restaurant_id')  # 从查询参数获取restaurant_id
    if not restaurant_id:
        return jsonify({"error": "Missing 'restaurant_id' query parameter."}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM comments_restaurants WHERE restaurant_id = ?',
                (restaurant_id,))
    comments = cur.fetchall()

    if comments is None or len(comments) == 0:
        return jsonify({"error": "Comments not found for the given restaurant ID."}), 404

    # 将查询结果转换为指定的列表格式
    comments_list = []
    for comment in comments:
        comment_data = {
            "id": comment["id"],
            "rating_package_score": comment["rating_package_score"],
            "rating_rider_score": comment["rating_rider_score"],
            "rating_shop_score": comment["rating_shop_score"],
            "rating_taste_score": comment["rating_taste_score"],
            "tags": comment["tags"]
        }
        comments_list.append(comment_data)

    cur.close()
    conn.close()

    return jsonify(comments_list)


@api_v1.route('/profile/comments_consumers', methods=['GET'])
def get_comments_consumers():
    restaurant_id = request.args.get('restaurant_id')
    if not restaurant_id:
        return jsonify({"error": "Missing 'restaurant_id' query parameter."}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database."}), 500

    cur = conn.cursor()

    # 查询comments_consumers信息，需要连接到comments_restaurants表以根据restaurant_id过滤
    query = """
    SELECT * FROM comments_consumers
    WHERE restaurants_id = ?
    """
    cur.execute(query, (restaurant_id,))
    comments = cur.fetchall()

    comments_list = [dict(comment) for comment in comments]

    cur.close()
    conn.close()

    return jsonify(comments_list)


@api_v1.route('/profile/seller_info', methods=['GET'])
def get_seller_info():
    restaurant_id = request.args.get('restaurant_id')
    if not restaurant_id:
        return jsonify({"error": "Missing 'restaurant_id' query parameter."}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database."}), 500

    cur = conn.cursor()

    # 查询seller_info表中匹配的商家信息
    cur.execute('SELECT * FROM seller_info WHERE restaurant_id = ?',
                (restaurant_id,))
    seller_infos = cur.fetchall()

    if seller_infos is None or len(seller_infos) == 0:
        return jsonify({"error": "Seller info not found for the given restaurant ID."}), 404

    # 构建信息列表
    seller_info_list = []
    for info in seller_infos:
        info_data = {
            "id": info["id"],
            "header_image": info["header_image"],
            "title": info["title"],
            "brief": info["brief"],
            "restaurant_id": info["restaurant_id"]
        }
        seller_info_list.append(info_data)

    cur.close()
    conn.close()

    return jsonify(seller_info_list)


@api_v1.route('/profile/add_orders', methods=['POST'])
def add_orders():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing order data"}), 400

    # return jsonify({"message": "Order added successfully"}), 201
    user_id = data.get('user_id')
    order_info = data.get('orderInfo')
    total_price = data.get('totalPrice')
    address_info = data.get('addressInfo')
    remark_info = data.get('remarkInfo')
    created_at = data.get('created_at')
    user_addresses_phone = data.get('user_addresses_phone')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('INSERT INTO orders (user_id, order_info, total_price, address_info, remark_info, created_at, user_addresses_phone) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (user_id, json.dumps(order_info), total_price, json.dumps(address_info), json.dumps(remark_info), created_at, user_addresses_phone,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Order added successfully"}), 201


@api_v1.route('/profile/order_list', methods=['GET'])
def get_order_list():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing 'user_id' query parameter."}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:

        cur.execute(' SELECT * FROM orders o left JOIN users_addresses ua ON o.user_addresses_phone = ua.phone WHERE o.user_id = ? and ua.user_id= ? ', (user_id, user_id,))
        orders = cur.fetchall()
        orders_list = [dict(order) for order in orders]

        return jsonify(orders_list)
    except Error as e:
        print(e)
        return jsonify({"error": "Database error."}), 500
    finally:
        cur.close()
        conn.close()


@api_v1.route('/profile/user_address', methods=['GET'])
def get_user_addresses():
    user_id = request.args.get('user_id')  # 从查询参数中获取user_id
    if not user_id:
        return jsonify({'error': 'Missing user_id parameter'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # 根据user_id查询所有匹配的用户地址
    cur.execute('SELECT * FROM users_addresses WHERE user_id = ?', (user_id,))
    addresses_rows = cur.fetchall()

    cur.close()
    conn.close()

    if addresses_rows:
        # 将所有行转换为字典列表
        addresses = [dict(row) for row in addresses_rows]
        return jsonify({'addresses': addresses})
    else:
        return jsonify({'error': 'No addresses found for the given user_id'}), 404


@api_v1.route('/profile/add_address', methods=['POST'])
def add_address():
    data = request.get_json()

    if not all(key in data for key in ('user_id', 'address', 'houseNumber', 'name', 'phone', 'sex', 'tag')):
        return jsonify({'error': 'Missing data for one or more fields'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users_addresses (user_id, address, houseNumber, name, phone, sex, tag) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (data['user_id'], data['address'], data['houseNumber'], data['name'], data['phone'], data['sex'], data['tag']))
        conn.commit()
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'success': 'Address added successfully'}), 201


@api_v1.route('/profile/edit_address', methods=['POST'])
def edit_address():
    data = request.json  # 从请求的body中获取JSON数据
    # 确保所有必需的字段都在JSON数据中，包括地址ID
    required_fields = ['id', 'user_id', 'address',
                       'houseNumber', 'name', 'phone', 'sex', 'tag']
    if not all(key in data for key in required_fields):
        return jsonify({'error': 'Missing data for one or more fields'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # 更新地址信息，根据地址ID
        cur.execute('''UPDATE users_addresses SET user_id = ?, address = ?, houseNumber = ?, 
                       name = ?, phone = ?, sex = ?, tag = ? WHERE id = ?''',
                    (data['user_id'], data['address'], data['houseNumber'],
                     data['name'], data['phone'], data['sex'], data['tag'], data['id']))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({'error': 'Address not found or no update made'}), 404
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'success': 'Address updated successfully'}), 200


@api_v1.route('/profile/delete_address', methods=['POST'])
def delete_address():
    data = request.json  # 从请求的 body 中获取 JSON 数据
    address_id = data.get('id')  # 获取要删除的地址 ID

    if not address_id:
        return jsonify({'error': 'Missing address ID'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # 根据地址 ID 删除地址信息
        cur.execute('DELETE FROM users_addresses WHERE id = ?', (address_id,))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({'error': 'Address not found'}), 404
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'success': 'Address deleted successfully'}), 200


# 创建 Flask 应用并注册 Blueprint
app = Flask(__name__)
CORS(app)
app.register_blueprint(api_v1, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
