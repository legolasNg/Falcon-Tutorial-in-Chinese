# Falcon教程
[Falcon Tutorial(英文链接)][1]

tags:`REST` `Falcon` `Python`

---

##1. 整体架构(The Big Picture)
![架构图](http://falcon.readthedocs.org/en/stable/_images/my-web-app.gif)

##2. 开始(First Steps)

在开始之前，先得保证falcon已经安装。然后创建一个新的project目录“look”，然后切换到该目录:
```
$ mkdir look
$ cd look
```
然后，创建一个新文件app.py作为应用入口:
$touch app.py
    打开app.py，加入下面的内容:
```python
import falcon

api = application = falcon.API()
```
这样就创建了一个WSGI应用，并且设置别名为`api`。我们可以使用任何变量名，Gunicorn希望我们默认使用`application`。WSGI应用只是一个具有明确定义的签名，你可以在任何支持WSGI协议的web server上托管你的应用。下面我们来看falcon.API类。

首先安装IPython，并且启动它:
```
$ pip install ipython
$ ipython
```
然后，输入下面的命令来查看falcon.API的调用
```
In [1]: import falcon
In [2]: falcon.API.__call__？
```
或者，你可以使用内建的`help`函数去查看:
```
In [3]: help(falcon.API.__call__)
```
注意method签名。`env`和`start_response`是标准WSGI参数。Falcon在这些参数上层添加了少许抽象，所以我们不必直接去操作它们。
Falcon框架包含大量的内联文档，你可以通过使用上面介绍的技巧来查询。经过Falcon团队对文档可读性的大量优化，我们可以很快浏览和查找我们需要的。

**Tip**
bpython是另一个非常给力的REPL(交互式解释器)，可以加入我们的工具箱，以便以后浏览新的library(库)。

##3. 托管应用(Hosting Your App)

现在我们已经创建了一个简单的Falcon应用，我们可以让它运行在WSGI server上。Python包含一个自托管的参考server，但是我们还是使用实际部署时使用的server。
```
$ pip install gunicorn
$ gunicorn app
```
现在我们使用curl尝试查询它:
```
$ curl localhost:8000 -v
```
你将会获取到404。这很正常，因为我们没有设定任何路由(route)。Falcon包含默认的404响应处理(response handler)，用来处理没有匹配到任何路由的请求地址。
使用curl可能会有点蛋疼，我们可以安装HTTPie，从今以后就使用它了。
```
$ pip install --upgrade httpie
$ http localhoost:8000
```

##4. 创建资源(Creating Resources)

Falcon从`REST架构风格`引入了一些术语，如果你熟悉REST概念，那么对Falcon应该会比较熟悉。不过，就算完全不懂`REST`，也不用担心。Falcon的设计理念是，尽可能直观地让所有人理解HTTP基本原理。
在Falcon中，我们可以把传入的请求(incoming requests)称为`资源`(Resources)。`资源`只是一个常规class，包含一些遵循一定命名规则的方法(method)。每个方法对应一个动作(API客户端为了获取或转换资源，去请求执行的动作)。
假设我们在构建一个图片分享API，那我们可以创建一个`image`资源。在我们的项目目录中，创建一个`image.py`的文件，可以在里面添加下面的代码:
```python
import falcon


class Resource(object):
    
    def on_get(self, req, resp):
        resp.body = '{"message":"Hello woeld!"}'
        resp.status = falcon.HTTP_200
```
可见,`Resource`只是一个很常规的class，类名可以任意取。Falcon使用`duck-typing`，所以不需要继承任何特定的基类。
上面的image资源定义了单一方法`on_get`。对于resource想要支持的任何HTTP方法，只需要简单在resource上加`on_x`类方法(class method)，`x`可以是标准HTTP方法中的任何一个，例如`on_get`,`on_put`,`on_head`(小写)等等。
我们将这些著名的方法称作`responders`(响应器)。每个`responder`至少需要两个参数，一个代表HTTP请求，另一个代表对应请求的HTTP响应。根据习惯，我们一般写作`req`和`resp`。route(路由)模板和hooks(钩子)可以添加一些额外的参数，在后面将会讲到。
现在，image资源对**GET**请求作出响应：`200 ok`和一个`JSON`对象。Falcon默认是`application/json`作为互联网媒体类型，但是你可以设置成任何你想使用的类型。例如，你可以使用[MessagePack][2]或者其他序列化格式。
如果你想在上面的例子中使用`MessagePack`，你需要为Python安装序列化/反序列化。通过运行`pip install msgpack-python`，然后更新你的responder中相应的响应数据(response data)和内容类型(content_type):
```python
import falcon

import msgpack


class Resource(object):

    def on_get(self, req, resp):
        resp.data = msgpack.packb({'message':'Hello world!'})
        resp.content_type  = 'application/msgpack'
        resp.status = falcon.HTTP_200
```
注意，使用`resp.data`代替`resp.body`。如果你给后者`resp.body`指定一个bytestring，Falcon也能处理，但是通过直接指定`resp.data`你将获得一些性能提升。
现在让我们看resource运行得如何。回到`app.py`，并且将其修改成下面的形式:
```python
import falcon

import images


api = application = falcon.API()

images = images.Resource()
api.add_route('/images', images)
```
现在，如果传入一个“/images”的请求，Falcon请会调用images的资源中的响应器(responder)--对应所需要的HTTP方法。
重启gunicorn，并且尝试向resource(资源)发送一个**GET**请求:
```
$ http GET localhost:8000/images
```
**Tip**
`duck-typing`:动态类型的一种风格。在这种风格中，一个对象有效的语义，不是由继承自特定的类或实现特定的接口，而是由当前方法和属性的集合决定。在duck typing中，关注的不是对象的类型本身，而是它是如何使用的。

##5. 请求对象和响应对象(Request and Response Objects)

资源(resource)中的每个响应器(responder)接收一个请求对象(request oject)--可以被用作读取headers、查询参数和请求的body。你可以使用我们之前提到的`help`函数去列举Request类的成员:
```
In [1]: import falcon
In [2]: help(falcon.Request)
```
每个响应器(responder)也能接收一个响应对象(response object)--可以被用作设置HTTP状态码、headers和响应的body。你可以通过使用同样的技巧来列举Response的类成员:
```
In [3]: help(falcon.Response)
```
让我们探究一下他们如何运作。当客户端(client)**POSTs**到images集合(collection)时，我们要创建一个新的image资源。首先，我们需要指定images保存在什么地方(对于真实的service，你将需要使用一个对象储存服务，例如Cloud Files 或者Amazon S3)。
编辑你的`images.py`文件，添加下列代码到resource:
```python
def __init__(self, storage_path)
    self.storage_path = storage_path
```
然后，编辑`app.py`，然后传入一个path参数到resource的初始化器。
最后，实现**POST**响应器(responder):
```python
import os
import time
import uuid

import falcon


def _media_type_to_ext(media_type):
    #剥离'/images/'前缀
    return media_type[6:]
    

def _generate_id():
    return str(uuid.uuid4())


class Resource(object):

    def __init__(self, storage_path):
        self.storage_path = storage_path
    
    def on_post(self, req, resp):
        image_id = _generate_id()
        ext = _media_type_to_ext(req.content_type)
        filename = image_id + '.' + ext
        
        image_path = os.path.join(self.storage_path, filename)
        with open(image_path, 'wb') as image_file:
            while True:
                chunk  = req.stream.read(4096)
                if not chunk:
                    break
                
                image_file.write(chunk)
        
        resp.status = falcon.HTTP_201
        resp.location = '/images/' + image_id
```
正如我们所看见的，我们给新图片生成了一个唯一的ID和文件名，然后从`req.stream`读取出来，再写入文件。调用`stream`而不是`body`去强调事实--你确实正在从输入流读取;Falcon不会输出(spool)或解码(decode)请求数据(request data)，而是让你直接访问由WSGI server提供的二进制输入流(incoming binary stream)。
注意，我们将`HTTP response status code`设置为“201 Created”。预定义的状态字符清单，我们可以通过对`falcon.status_codes`调用`help`函数来查看:
```
In [4]: help(falcon.status_codes)
```
在`on_post`响应器的最后一行，给新创建的资源设置Location Header。(我们很快就给该路径(path)创建一个了路由(route))注意，Request类和Response类包含一些读取和设置通用header的便利属性，但是通过声明`req.get_header`和`resp.set_header`方法，我们总是可以使用任何header.
重启gunicorn，然后尝试给resource发送一个**POST**请求(可以将test.jpg替换成任何你想操作的JPEG文件的路径)
```
$ http POST localhost:8000/images Content-type:image/jpeg < test.jpg
```
如果现在去查看你储存目录，将会包含你刚才POST的图片的复制品。

##6. 提供图片(Serving Images)##
我们现在已经可以上传图片到服务了，我们还要能获取他们。我们要做的就是，通过带有路径的请求，让服务器返回一张图片到Location header，就像这样:
```
$ http GET localhost:8000/images/87db45ff42
```
接下来，我们可以在images资源中添加`on_get`响应器，这样做对于比较简单的resource是可行的，但是
  [1]: http://falcon.readthedocs.org/en/stable/user/tutorial.html
  [2]: http://msgpack.org/
