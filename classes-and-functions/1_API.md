# API类

标签： API Falcon

---
Falcon的API类，是一个WSGI类“应用”，你可以将其托管在任何标准兼容的WSGI服务器上。

```python
import falcon

api = application = falcon.API()
```

class falcon.API(media_type='application/json; charset=utf-8', before=None, after=None, request_type=<class 'falcon.request.Request'>, response_type=<class 'falcon.response.Response'>, middleware=None, router=None)
[source][1]

这个类是基于Falcon的应用的主要入口。

每个API实例提供一个可调用的WSGI接口和一个路由引擎。

**警告**

不赞成全局钩子(在kwargs使用前后配置)用于中间件，(全局钩子)在未来版本的框架中将会被移除。

参数:

- media_type (str, optional) - 

- middleware (object or list, optional) –


  [1]: https://github.com/falconry/falcon/blob/0.3.0/falcon/api.py#L29