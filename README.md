# doc_gen_restful_api

RESTFUL API 接口文档生成工具

## JSON格式
```json
[
    {
    "headline": "创建资源",
    "request": {
      "method": "POST",
      "address": "http://hostname/resource/create",
      "header": {
        "Content-Type": "application/json",
        "Cookie": ""
      },
      "body": {
        "name": "test||名字",
        "size": "1024|number|大小",
        "address": "http://path.zip||url地址",
        "md5": "abc||md5",
        "version": "1|number|版本"
      }
    },
    "response": {
      "body": {
        "err_no": "0|number|错误码",
        "err_msg": "success||错误描述",
        "log_id": "123456||日志id",
        "data": {
          "id": "1|number|资源id"
        }
      }
    }
  }
]
```

## 接口文档

```markdown
## 创建资源  

### 基本信息  

**接口URL:** http://hostname/resource/create  

**请求方式:** POST  

### 请求头  

| 参数名          | 示例值              | 类型     | 必填项 | 描述  |
|--------------|------------------|--------|-----|-----|
| Content-Type | application/json | String | 是   |     |
| Cookie       |                  | String | 是   |     |  

### 请求参数  

| 参数名     | 示例值             | 类型     | 必填项 | 描述    |
|---------|-----------------|--------|-----|-------|
| name    | test            | String | 是   | 名字    |
| size    | 1024            | Number | 是   | 大小    |
| address | http://path.zip | String | 是   | url地址 |
| md5     | abc             | String | 是   | md5   |
| version | 1               | Number | 是   | 版本    |  

### 响应参数  

| 参数名     | 示例值     | 类型     | 必填项 | 描述   |
|---------|---------|--------|-----|------|
| err_no  | 0       | Number | 是   | 错误码  |
| err_msg | success | String | 是   | 错误描述 |
| log_id  | 123456  | String | 是   | 日志id |
| data    |         | Object | 是   |      |
| data.id | 1       | Number | 是   | 资源id |  

### 示例代码  

\```
请求:
POST http://hostname/resource/create HTTP/1.1
Content-Type: application/json
Cookie: 

{
  "name": "test",
  "size": 1024,
  "address": "http://path.zip",
  "md5": "abc",
  "version": 1
}

响应:
HTTP/1.1 200 OK

{
  "err_no": 0,
  "err_msg": "success",
  "log_id": "123456",
  "data": {
    "id": 1
  }
}
\```
```
