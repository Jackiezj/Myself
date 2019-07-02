# 后端接口设计

## 获取图片验证码

- 请求URL

    GET `/verifications/image_codes/(?P<image_code_id>[\w-]+)/`
    
- 请求参数

    image_code_id: 图片验证码id
    
- 响应数据

    image(image/jpeg): 二进制图片

```python
# GET /verification/
```