# 后端接口设计

## 获取图片验证码

- 请求URL

    GET `/verifications/image_codes/(?P<image_code_id>[\w-]+)/`
    
- 请求参数

    image_code_id: 图片验证码id
    
- 响应数据

    image(image/jpeg): 二进制图片

## 短信验证码接口设计

- 业务流程
    1. 根据图片验证码, 判定正确与否
    2. 正确: 发送短信,返回json
    3. 错误: 返回json

- 请求URL

    GET `/verifications/sms_codes/(?P<mobile>1[3-9]\d{9})/`
    
- 请求参数

    - image_code: 查询参数,图片验证码
    - image_code_id: 查询参数,图片验证码id
    
- 响应数据

    - celery异步任务发送短信
    - (json) message OK 
    
