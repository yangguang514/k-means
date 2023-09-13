# -*- coding: utf-8 -*-
import psycopg2
import matplotlib.pyplot as plt
from shapely.wkb import loads


# 连接到 PostgreSQL 数据库
conn = psycopg2.connect(database="shi", user="postgres", password="yangguang821.", host="localhost", port="5432")
cur = conn.cursor()

Zmin11 = ['永州市', '郴州市', '赣州市', '河源市', '汕尾市', '梅州市', '揭阳市', '汕头市', '抚州市', '上饶市', '九江市', '岳阳市', '益阳市', '娄底市', '湘潭市', '衡阳市', '长沙市', '株洲市', '怀化市', '湘西土家族苗族自治州', '重庆市', '南平市', '宁德市', '温州市', '台州市', '福州市', '萍乡市', '常德市', '贺州市', '梧州市', '玉林市', '鹰潭市', '潮州市', '柳州市', '河池市', '百色市', '曲靖市', '昭通市', '凉山彝族自治州', '乐山市', '甘孜藏族自治州', '楚雄彝族自治州', '普洱市', '迪庆藏族自治州', '眉山市', '丽江市', '红河哈尼族彝族自治州', '六盘水市', '雅安市', '莆田市', '玉溪市', '吉安市', '遂宁市', '绵阳市', '广元市', '大理白族自治州', '保山市', '黔南布依族苗族自治州', '贵阳市', '攀枝花市', '肇庆市', '桂林市', '宜春市', '德宏傣族景颇族自治州', '云浮市', '三明市', '南昌市', '自贡市', '钦州市', '韶关市', '广州市', '湛江市', '茂名市', '邵阳市', '清远市', '黔东南苗族侗族自治州', '阳江市', '南充市', '安顺市', '贵港市', '泉州市', '厦门市', '东莞市', '深圳市', '西双版纳傣族自治州', '昆明市', '南宁市', '佛山市', '惠州市', '江门市', '中山市', '来宾市', '文山壮族苗族自治州', '新余市', '张家界市', '漳州市', '防城港市', '珠海市', '龙岩市', '黔西南布依族苗族自治州', '崇左市', '宜宾市', '北海市', '安康市', '商洛市', '资阳市', '广安市', '临沧市', '内江市', '昌都市', '泸州市', '遵义市', '十堰市', '铜仁市', '怒江傈僳族自治州', '达州市', '神农架林区', '恩施土家族苗族自治州', '巴中市', '毕节市']
Zmin22 = ['平顶山市', '南阳市', '许昌市', '郑州市', '焦作市', '济源市', '运城市', '漯河市', '三门峡市', '新乡市', '鹤壁市', '安阳市', '邯郸市', '濮阳市', '泰安市', '开封市', '济宁市', '枣庄市', '洛阳市', '济南市', '淄博市', '信阳市', '六安市', '合肥市', '马鞍山市', '南京市', '常州市', '无锡市', '苏州市', '泰州市', '盐城市', '淮南市', '嘉兴市', '宁波市', '镇江市', '阜阳市', '蚌埠市', '淮北市', '周口市', '临沂市', '潍坊市', '烟台市', '驻马店市', '扬州市', '湖州市', '德州市', '青岛市', '芜湖市', '沧州市', '天津市', '北京市', '承德市', '保定市', '石家庄市', '大同市', '朔州市', '忻州市', '菏泽市', '邢台市', '商丘市', '阳泉市', '日照市', '秦皇岛市', '滁州市', '南通市', '葫芦岛市', '锦州市', '沈阳市', '抚顺市', '鞍山市', '丹东市', '大连市', '辽源市', '吉林市', '延边朝鲜族自治州', '牡丹江市', '七台河市', '佳木斯市', '哈尔滨市', '绥化市', '营口市', '鹤岗市', '双鸭山市', '长春市', '大庆市', '辽阳市', '鸡西市', '通化市', '盘锦市', '威海市', '宿州市', '本溪市', '徐州市', '廊坊市', '伊春市', '亳州市', '四平市', '晋中市', '绍兴市', '衡水市', '聊城市', '松原市', '朝阳市', '铁岭市', '齐齐哈尔市', '白城市', '黑河市', '金华市', '铜陵市', '安庆市', '呼和浩特市', '包头市', '唐山市', '滨州市', '池州市', '呼伦贝尔市', '张家口市', '连云港市', '赤峰市', '淮安市', '阜新市', '白山市', '宿迁市', '通辽市', '鄂尔多斯市', '银川市', '吴忠市', '乌海市', '石嘴山市', '大兴安岭地区', '阿拉善盟', '兴安盟', '宣城市', '锡林郭勒盟', '东营市', '衢州市', '黄冈市', '鄂州市', '太原市', '上海市', '舟山市', '乌兰察布市', '杭州市', '巴彦淖尔市', '黄石市', '丽水市', '景德镇市', '孝感市', '天门市', '仙桃市', '潜江市', '荆门市', '荆州市', '宜昌市', '黄山市', '武汉市', '襄阳市', '咸宁市', '随州市']
Zmin33 = ['平凉市', '庆阳市', '中卫市', '固原市', '白银市', '武威市', '咸阳市', '渭南市', '海东市', '海南藏族自治州', '甘南藏族自治州', '定西市', '海北藏族自治州', '兰州市', '临夏回族自治州', '西宁市', '果洛藏族自治州', '玉树藏族自治州', '西安市', '天水市', '张掖市', '阿坝藏族羌族自治州', '成都市', '酒泉市', '临汾市', '长治市', '陇南市', '金昌市', '嘉峪关市', '晋城市', '铜川市', '宝鸡市', '巴音郭楞蒙古自治州', '阿里地区', '乌鲁木齐市', '阿克苏地区', '喀什地区', '图木舒克市', '伊犁哈萨克自治州', '可克达拉市', '阿勒泰地区', '北屯市', '阿拉尔市', '吐鲁番市', '克孜勒苏柯尔克孜自治州', '博尔塔拉蒙古自治州', '双河市', '胡杨河市', '五家渠市', '日喀则市', '拉萨市', '林芝市', '昌吉回族自治州', '石河子市', '塔城地区', '哈密市', '山南市', '克拉玛依市', '海西蒙古族藏族自治州', '德阳市', '榆林市', '吕梁市', '和田地区', '昆玉市', '延安市', '铁门关市', '汉中市', '黄南藏族自治州', '那曲市']
print(len(Zmin11))
print(len(Zmin22))
print(len(Zmin33))

# 查询Zmin1聚类中心的几何信息
cur.execute("SELECT city_name, ST_AsBinary(geom) FROM cities WHERE city_name IN %s", (tuple(Zmin11),))
cluster_centers_data_zmin1 = cur.fetchall()

# 查询Zmin2聚类中心的几何信息
cur.execute("SELECT city_name, ST_AsBinary(geom) FROM cities WHERE city_name IN %s", (tuple(Zmin22),))
cluster_centers_data_zmin2 = cur.fetchall()

cur.execute("SELECT city_name, ST_AsBinary(geom) FROM cities WHERE city_name IN %s", (tuple(Zmin33),))
cluster_centers_data_zmin3 = cur.fetchall()


# 解析几何信息并绘制Zmin1聚类中心
for data in cluster_centers_data_zmin1:
    city_name, geom_binary = data
    geom = loads(bytes(geom_binary))
    if geom.geom_type == 'MultiPolygon':
        for polygon in geom:
            x, y = polygon.exterior.xy
            plt.plot(x, y, color='red', marker='x', label='Cluster Center: ' + city_name)
    else:
        x, y = geom.exterior.xy
        plt.plot(x, y, color='red', marker='x', label='Cluster Center: ' + city_name)

# 解析几何信息并绘制Zmin2空间单元
for data in cluster_centers_data_zmin2:
    city_name, geom_binary = data
    geom = loads(bytes(geom_binary))
    if geom.geom_type == 'MultiPolygon':
        for polygon in geom:
            x, y = polygon.exterior.xy
            plt.plot(x, y, color='blue', label='Space Unit: ' + city_name)
    else:
        x, y = geom.exterior.xy
        plt.plot(x, y, color='blue', label='Space Unit: ' + city_name)

# 解析几何信息并绘制Zmin2空间单元
for data in cluster_centers_data_zmin3:
    city_name, geom_binary = data
    geom = loads(bytes(geom_binary))
    if geom.geom_type == 'MultiPolygon':
        for polygon in geom:
            x, y = polygon.exterior.xy
            plt.plot(x, y, color='green', label='Space Unit: ' + city_name)
    else:
        x, y = geom.exterior.xy
        plt.plot(x, y, color='green', label='Space Unit: ' + city_name)

# # 设置图例
# plt.legend()

# 设置坐标轴标签
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# 显示图形
plt.show()

# 关闭数据库连接
cur.close()
conn.close()
