# 上海公交API

#### 1. 公交线路查询接口
**接口地址**：/bus/<router_name>
**请求方式**：GET
**请求参数**：

| 名称 | 位置 | 类型 | 说明 |
| --- | --- | --- |
| router_name | url | string | 公交线路名称，如：1路、2路 |
| direction | query string |  | 公交行驶方向，上行：0，下行：1 |

**返回参数**：

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| from | string | 公交起点站名称 |
| to | string | 公交终点站名称 |
| direction | int | 公交行驶方向，上行：0，下行：1 |
| stops | array | 公交站点列表 |
| stop_id | string | 公交站点的数字代号 |
| stop_name | string |  公交站点名称 |

#### 2.公交到站信息查询接口
**接口地址**：/bus/<router_name>/stop/<stop_id>
**请求方式**：GET
**请求参数**：

| 名称 | 位置 | 类型 | 说明 |
| --- | --- | --- |
| router_name | url | string | 公交线路名称，如：1路、2路 |
| stop_id | string | url | 公交站点的数字代号 |
| direction | query string |  | 公交行驶方向，上行：0，下行：1 |

**返回参数**：

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| router_name | string | 公交线路名称 |
| direction | int | 公交行驶方向，上行：0，下行：1 |
| plate_number | string | 公交车车牌号 |
| stop_at | int | 当前公交车到达站点的数字代号 |
| distance | int | 当前公交车到达本站的距离 |
| time | int | 当前公交车到达本站的时间（秒） |