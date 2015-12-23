# API类

标签： API Falcon

---
Falcon的API类，是一个WSGI类“应用”，你可以将其托管在任何标准兼容的WSGI服务器上。

```python
import falcon

api = application = falcon.API()
```

class falcon.API()
==================

class falcon.API(media_type='application/json; charset=utf-8', before=None, after=None, request_type=<class 'falcon.request.Request'>, response_type=<class 'falcon.response.Response'>, middleware=None, router=None)
[source][1]

这个类是基于Falcon的应用的主要入口。

每个API实例提供一个可调用的WSGI接口和一个路由引擎。

**警告**

*不赞成全局钩子(在kwargs使用前后配置)用于中间件，(全局钩子)在未来版本的框架中将会被移除。*

参数:

- `media_type (str, optional)` - 默认媒体类型用来设置响应的内容类型的header(默认值是'application/json')

- `middleware (object or list, optional)` – 实现以下中间件组件接口的单个或多个对象(实例化的类):

```python
class ExampleComponent(object):
    def process_request(self, req, resp):
        """在构建路由前处理请求
        参数:
            req: 最终关联对应on_*响应器方法的请求对象(request object)。
            resp: 关联到on_*响应器的响应对象(response object)。
        """
        
    def process_resource(self, req, resp, resource):
        """在构建路由后处理请求和资源
        参数:
            req: 最终关联对应on_*响应器方法的请求对象(request object)。
            resp: 关联到on_*响应器的响应对象(response object)。
            resource: 关联到请求(request)的资源对象(resource object)。如果请求没有对应路由，则没有资源对象。
        """
        
    def process_response(self, req, resp, resource)
        """响应的后续处理 (在构建路由后).
        参数:
            req: 请求对象。
            resp: 响应对象。
            resource: 关联到请求(request)的资源对象(resource object)。如果请求没有对应路由，则没有资源对象。
        """
```

详情见[Middleware][2]

- `request_type (Request, optional)` - 与`Request`类似的类，用来取代Falcon的默认类。尤其，该特性允许继承`falcon.request.Request`，去重写`context_type`类的变量。(默认值是`falcon.request.Request`)

- `response_type (Response, optional)` - 与`Response`类似的类，用来取代Falcon的默认类。(默认值是`falcon.response.Response`)

- `router (object, optional)` – 一个自定义路由的实例，用来代替默认引擎。详情见：[Routing][3]。

##req_options##
    请求选项(RequestOptions)
    
    一组与传入请求相关连的操作选项
    
##__call__(env, start_response)##
[source][4]

WSGI应用方法

使调用自WSGI服务器的API实例化。可以用来托管API或者在测试API时直接调用去模拟请求。

详情见:PEP 3333

参数:

- `env (dict)` - WSGI环境的字典

- `start_response (callable)` - WSGI帮助函数，用来在响应中设置状态和header。

##add_error_handler(exception, handler=None)##
[source][5]

给给定的异常的错误类型注册一个处理程序。

参数:

- `exception (type)` – 在处理一个异常(exception)类实例的请求(request)时，无论什么时候出现错误，关联的处理程序都会被调用

- `handler (callable)` – 一个具有`func(ex, req, resp, params)`形式的函数或者可调用对象;

如果没有明确指定，处理程序会被默认置为`exception.handle`，`exception`是上面指定的错误类型，并且`handle`是一个接受了和之前相同参数的静态方法(也就是说，用@staticmethod装饰)。

例如:

```python
class CustomException(CustomBaseException):

    @staticmethod
    def handle(ex, req, resp, params):
        # :将错误记录到日志
        # 转换成falcon.HTTPError的一个实例
        raise falcon.HTTPError(falcon.HTTP_792)
```

**注意事项**

*处理程序也能抛出`HTTPError`实例或者手动修改为了传递客户端问题信息的响应(resp)*

##add_route(uri_template, resource)##
[source][6]

将资源(resource)关联到一个模板化的URL路径。

一个资源是一个定义了各种“响应器(responder)”方法、资源允许的每个HTTP方法的类的实例。响应器命名以on_开始，以他们处理的HTTP方法的名字结尾，例如on_get、on_post、on_put等。

如果我们的资源不支持一个特定的HTTP方法，仅仅是忽略对应的响应器，方法如果曾经被请求过Falcon将会返回一个“405 Method not allowed”(405 方法不被准许)

响应器必须总是定义至少2个参数，去分别接收请求和相应对象。例如:

```python
def on_post(self, req, resp):
    pass
```

除此之外，如果路由模板包含字段表达式(field expression)，任何想要接收该路由请求的响应器必须接收定义以模板中对应字段命名的参数。字段表达式由括号括起来的字段名组成。

例如，给定下面的模板:

```
/user/{name}
```

“/user/kgriffs”的PUT请求会被关联到:

```
def on_put(self, req, resp, name):
    pass
```

个别的路径段可能包含一个或多个字段表达式，例如:

```
/repos/{org}/{repo}/compare/{user0}:{branch0}...{user1}:{branch1}
```

参数:

- `uri_template (str)` - 模板化的URI(Uniform Resource Identifier统一资源标识符)。如果模板被注册，必须小心去确认模板不会覆盖任何sink模式(详情见`add_sink`)。

- `resource (instance)` - 表示一个REST资源的对象。Falcon会将“GET”请求传递给on_get，将“PUT”请求传递给on_put，依次类推。如果所有HTTP方法不被你的资源支持，仅仅没有定义对应的请求处理，那么Falcon会接手。

##add_sink(sink, prefix='/')##
[source][7]

给API注册一个sink方法。

如果没有路由匹配到请求，但是被请求的URL的路径匹配到一个sink前缀，Falcon会将处理传递到对应的sink，而不管被请求的HTTP方法。

当创建静态资源和响应器可能不太适用时，通过使用sink我们可以批量、动态处理大量的路由。例如，你可以使用sink去创建一个智能代理将请求发送到一个或多个后台服务。

参数:

- sink (callable) – 一个`func(req, resp)`形式的可调用函数

- prefix (str) – 正则表达式字符串，通常以'/'开始，如果匹配到请求URL的部分路径，将会处罚sink。字符串和预编译的正则表达式对象都需要指定。从URL路径的头部的字符开始匹配。

**注意事项**

*被声明的组会被转化为kwargs，然后传递到sink*

**警告**

*如果前缀和已注册的路由模板重复了，将会优先处理路由模板，并且覆盖sink(详情见`add_route`)*

##set_error_serializer(serializer)##
[source][8]

重写HTTPError实例的默认序列化器。

当响应器抛出一个HTTPError实例，Falcon会自动将它转换成一个HTTP响应。默认的序列化器支持JSON和XML，但是为了支持其他媒体类型可以使用一个自定义的序列化器来重写。

`falcon.HTTPError`类包括helper方法，例如to_json()和to_dict()，能在自定义的序列化器中使用，例如:

```python
def my_serializer(req, exception):
    representation = None
    
    preferred = req.client_prefers(('application/x-yaml',                              'application/json'))
    
    if preferred is not None:
        if preferred == 'application/json':
            representation = exception.to_json()
        else:
            representation = yaml.dump(exception.to_dict(), encoding=None)

    return (preferred, representation)
```

**注意事项**
*如果自定义的媒体类型被使用，并且包括“+json”或“+xml”后缀，默认的序列化器会将错误对应地转化为JSON或XML。如果这样仍然不满意，使用一个自定义的错误序列化器来重写这个行为*

参数:

- `serializer (callable)` - `func(req, exception)`形式的函数，req是被传递进响应器方法的请求对象，exception是一个`falcon.HTTPError`实例。如果客户端不支持任何可用的媒体类型，这个函数必须返回一个的(media_type，representation)形式的`tuple`或(`None`,`None`)

class falcon.RequestOptions
===========================
[source][9]

该类是`Request`选项的一个容器。

##keep_blank_qs_values##

bool类型

设置为`True`，可以在查询字符串参数时保留空值(默认值为False)

  [1]: https://github.com/falconry/falcon/blob/0.3.0/falcon/api.py#L29
  [2]: https://github.com/wujianye3/Falcon-Tutorial-in-Chinese/blob/master/classes-and-functions/6_Middleware_Components.md
  [3]: https://github.com/wujianye3/Falcon-Tutorial-in-Chinese/blob/master/classes-and-functions/8_Routing.md
  [4]: https://github.com/falconry/falcon/blob/0.3.0/falcon/api.py#L138
  [5]: https://github.com/falconry/falcon/blob/0.3.0/falcon/api.py#L359
  [6]: https://github.com/falconry/falcon/blob/0.3.0/falcon/api.py#L250
  [7]: https://github.com/falconry/falcon/blob/0.3.0/falcon/api.py#L318
  [8]: https://github.com/falconry/falcon/blob/0.3.0/falcon/api.py#L403
  [9]: https://github.com/falconry/falcon/blob/0.3.0/falcon/request.py#L1021