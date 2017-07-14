# 上海公交API

#### 1. 公交线路查询接口
**接口地址**：
``` url
/bus/<router_name>
```

**请求方式**：GET

**请求参数**：

| 名称 | 位置 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- | --- |
| router_name | url | string | 是 | 公交线路名称，如：1路、2路 |
| direction | query string | int | 否 | 公交行驶方向，上行：0（默认），下行：1 |

**返回参数**：

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| from | string | 公交起点站名称 |
| to | string | 公交终点站名称 |
| start_at | string | 首班公交发车时间 |
| end_at | string | 末班公交发车时间 |
| direction | int | 公交行驶方向，上行：0，下行：1 |
| stops | array | 公交站点列表 |
| stop_id | string | 公交站点的数字代号 |
| stop_name | string |  公交站点名称 |

---

#### 2.公交到站信息查询接口
**接口地址**：
``` url
/bus/<router_name>/stop/<stop_id>
```

**请求方式**：GET

**请求参数**：

| 名称 | 位置 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- | --- |
| router_name | url | string | 是 | 公交线路名称，如：1路、2路 |
| stop_id | url | int | 是 | 公交站点的数字代号 |
| direction | query string | int | 否 | 公交行驶方向，上行：0（默认），下行：1 |

**返回参数**：

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| router_name | string | 公交线路名称 |
| direction | int | 公交行驶方向，上行：0，下行：1 |
| plate_number | string | 公交车车牌号 |
| stop_interval | int | 公交车到达本站的站数 |
| distance | int | 当前公交车到达本站的距离 |
| time | int | 当前公交车到达本站的时间（秒） |
| status | string | 公交车状态，waiting：等待发车；running：运行中 |

---

#### 3.公交线路详情查询接口
**接口地址**：
``` url
/bus/<router_name>/details
```

**请求方式**：GET

**请求参数**：

| 名称 | 位置 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- | --- |
| router_name | url | string | 是 | 公交线路名称，如：1路、2路 |
| direction | query string | int | 否 | 公交行驶方向，上行：0（默认），下行：1 |

**返回参数**：

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| from | string | 公交起点站名称 |
| to | string | 公交终点站名称 |
| start_at | string | 首班公交发车时间 |
| end_at | string | 末班公交发车时间 |
| direction | int | 公交行驶方向，上行：0，下行：1 |
| stops | array | 公交站点列表 |
| stop_id | string | 公交站点的数字代号 |
| stop_name | string |  公交站点名称 |
| plate_number | string | 公交车车牌号 |
| stop_interval | int | 公交车到达本站的站数 |
| distance | int | 当前公交车到达本站的距离 |
| time | int | 当前公交车到达本站的时间（秒） |
| status | string | 公交车状态，waiting：等待发车；running：运行中 |

---

#### 错误响应

**返回参数**：

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| error | string | 错误代码 |
| error_msg | string | 错误说明 |

##### 400 Bad Request
``` json
{
  "error": "router_not_exists",
  "error_msg": "不存在该公交线路"
}
```

##### 404 Not Found
``` json
{
  "error": "page_not_found",
  "error_msg": "页面不存在"
}
```

##### 500 Internal Server Error
``` json
{
  "error": "internal_server_error",
  "error_msg": "服务器内部错误"
}
```

#### 依赖库
- flask
- pymysql
- sqlalchemy
- bs4
