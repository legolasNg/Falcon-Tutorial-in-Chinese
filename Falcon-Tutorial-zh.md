# Falcon教程
[Falcon Tutorial(英文链接)][1]

标签： REST Falcon Python

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

```
$touch app.py
```

打开app.py，加入下面的内容:

```python
import falcon

api = application = falcon.API()
```

这样就创建了一个WSGI应用，并且设置别名为`api`。我们可以使用任何变量名，Gunicorn希望我们默认使用`application`。

WSGI应用只是一个可调用的明确定义的签名，你可以在任何支持[WSGI协议][2]的web server上托管你的应用。下面我们来看falcon.API类。 

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

现在，image资源对**GET**请求作出响应：`200 ok`和一个`JSON`对象。Falcon默认是`application/json`作为互联网媒体类型，但是你可以设置成任何你想使用的类型。例如，你可以使用[MessagePack][3]或者其他序列化格式。
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

现在关联上resource，看其运行得如何。回到`app.py`，并且将其修改成下面的形式:

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

接下来，我们可以在images资源中添加`on_get`响应器，这样做对于比较简单的resource是可行的，但是这种方法会导致一个问题--当同一个HTTP方法(例如GET)需要作出不同的响应。所以具体取决于使用者想要处理一系列的事件还是单个事件。
按照这个思路，如果我们要处理多张图片，除了表示单张图片资源的类以外，还需要新建一个类。我们可以在新的类中添加`on_get`响应器。

我们按照下面这样，继续编辑`images.py`：

```python
import os
import time
import uuid

import falcon


def _media_type_to_ext(media_type):
    # 剥离'/images/'前缀
    return media_type[6:]

def _ext_to_media_type(ext):
    return 'image/' + ext

def _generate_id():
    return str(uuid.uuid4())
    
    
class Collection(object):
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def on_post(self, req, resp):
        image_id = _generate_id()
        ext = _media_type_to_ext(req.content_type)
        filename = image_id + '.' + ext

        image_path = os.path.join(self.storage_path, filename)

        with open(image_path, 'wb') as image_file:
            while True:
                chunk = req.stream.read(4096)
                if not chunk:
                    break

                image_file.write(chunk)

        resp.status = falcon.HTTP_201
        resp.location = '/images/' + filename


class Item(object):

    def __init__(self, storage_path):
        self.storage_path = storage_path
    
    def on_get(self, req, resp, name):
        ext = os.path.splitext(name)[1][1:]
        resp.content_type = _ext_to_media_type(ext)
        
        image_path = os.path.join(self.storage_path, name)
        resp.st以一个空行开始，以一个空行结束，中间的就是一个段落。ream = open(image_path, 'rb')
        resp.stream_len = os.path.getsize(image_path)
```

可以看到，刚才我们将`Resource`重命名为`Collection`，并且添加了一个`Item`类去表示单张图片资源。还有，我们需要注意到`on_get`响应器中的`name`参数。任何在路由中指定的URL参数都将被转换成对应的kwargs参数，同时传递到目标响应器(responder)中。之后，将会讲解如何指定URL参数。
在`on_get`响应器中，我们按照文件名扩展去设置内容类型的header，然后通过打开文件操作来直接以数据流形式输出图片。还有需要注意`resp.stream_len`的用法。每当我们使用`resp.stream`来代替`resp.body`或`resp.data`的时候，我们必须给数据流指定一个预期的长度，以便web客户端知道从响应(response)中读取的数据有多大。

**Tips**

如果你事先不知道数据流的大小，你可以通过使用分块编码，这个用法超过该教程范围。

如果`resp.status`没有明确地设定，其默认值为`200 OK`，确切的说，这应该是我们应该在`on_get`响应器去做的。

现在我们将事件关联上，然后尝试运行一下。首先按照下面的例子来编辑`app.py`:

```python
import falcon

import images


api = application = falcon.API()

storage_path = '/usr/local/var/look'

image_collection = images.Collection(storage_path)
image = image.Item(storage_path)

api.add_route('/images', image_collection)
api.add_route('/images/(name)', image)
```

可见，我们定义了一个新的路由`/images/{name}`。这会让Falcon将所有的对应的响应器(responder)和获取的`name`参数关联起来。

**Tips**

Falcon还支持更加复杂的参数化路径段(包含多个值)。例如，类Grasshopper(GH-like,可以通过参数的调整直接改变模型形态)的API能够使用下面的模板为两个分支添加一个路由。

```
/repo/{org}/{repo}/compare/{usr0}:{branch0}...{usr1}:{branch1}
```

然后，我们重启gunicorn，并且post并一张图片给service:

```
$  http POST localhost:8000/images Content-type:image/jpeg < test.jpg
```

记下在Location header中返回的路径，然后使用该路径去GET这张图片:

```
$ http localhost:8000/images/6daa465b7b.jpeg
```

HTTPie默认不会下载图片，但是我们可以看到响应(response)的header被设置好了。更有趣的是，我们可以继续在浏览器中输入刚才的URL，图片会被正确的显示出来。

##7. “钩子”简介(Introducing Hooks)

看到这里，我们应该对Falcon基础API有了较好的理解。在教程结束前，我们需要花费一点时间去整理代码，并且加上一些错误处理。

第一步，当接收到一个POST请求时，检查输入的媒体类型(incoming media type)去确认是否为通用图像类型。我们可以通过使用Falcon的`before`钩子来完成。
 @wjy 2015-12-22 18:26 字数 8599 阅读 22 
首先，我们需要定义一个service接收的媒体类型列表。将这些常量定义放在代码顶部，也就是`images.py`文件的import声明后面。

```python
ALLOWED_IMAGE_TYPES = (
    'image/gif',
    'image/jpeg',
    'image/png',
)
```

这样声明只接收GIF、JPEG、PNG图像格式，当然你也可以添加你想要的其它格式。

接下来，在每个请求post消息前创建一个钩子。并且在`ALLOWED_IMAGE_TYPES`下面添加该方法:

```python
def validate_image_type(req, resp, params):
    if req.content_type not in ALLOWED_IMAGE_TYPES:
        msg = 'Image type not allowed. Must be PNG, JPEG, or GIF'
        raise falcon.HTTPBadRequest('Bad request', msg)
```

然后将这个钩子附加在`on_post`响应器上，如下:

```python
@falcon.before(validate_image_type)
def on_post(self, req, resp):
```

这样，每当这个`on_post`响应器被调用前，Falcon将先执行(invoke)`validate_image_type`这个方法。除了必须接受三个参数外，该方法并没有什么特别的。对于每个钩子，会引用传递进对应响应器(responder)的`req`和`reqsp`对象，作为前2个参数。第三个参数，习惯上被称作`params`，引用自Falcon为每个request创建的kwarg字典。如果`params`存在的话，将包含路由的URL模板参数及其对应的值。

由此可见，我们可以使用`req`去获得关于传入的请求的相关信息。而且需要的话，我们也可以使用`resp`去操作HTTP响应，为了避免重复代码(in a DRY way)我们甚至可以给响应器(responder)添加额外的kwarg，例如:
```python
def extract_project_id(req, resp, params):
    """
    为所有响应器的params添加'project_id'。
    意味着将在'before'钩子中被使用
    """
    params['project_id'] = req.get_header('X-PROJECT-ID')
```

现在我们可以想象，这样的一个钩子应该适用于一个资源(resource)的所有响应器(responder)，甚至可以适用于全局范围内的所有资源。我们还可以将钩子应用到整个资源上，如下:

```python
@falcon.before(extract_project_id)
class Message(object):

    #...
```

而且，在API类初始化时将钩子作为参数传递进去，我们可以全局应用:

```python
falcon.API(before=[extract_project_id])
```

如果想对钩子(hooks)进一步了解，可以查阅`API`类的帮助文档，也有装饰器`falcon.before`和`falcon.after`的帮助文档。

至此，我们已经添加了一个钩子--在图像被POST时确认媒体类型。你可以实际操作一下，比如传入一些邪恶的东西，看看发生什么:

```
$ http POST localhost:8000/images Content-Type:image/jpx < test.jpx
```

不出意外，会返回`400 Bad Request`状态和结构分明的错误body。当出现错误时，我们通常想给用户一些信息，来帮助他们解决问题。这个规则有个例外，用户请求访问未授权的东西时产生的错误。这种情况，我们应该希望去仅仅返回一个`404 Not Found`的空body，防止恶意用户想要获得一些能帮助他们破解我们API的信息。

**Tip**

可以关注一下我们的姊妹项目--[Talcons][4]，由社区贡献的一些游泳的Falcon钩子。如果你创建了一些有趣的钩子，同时你认为别人也需要，可以考虑贡献到该项目。

##8. 错误处理(Error Handling)

通常来讲，Falcon假定资源的响应器(on_get,on_post等)在大部分情况下能正确运作。也就是说，Falcon在保护响应器代码上没有做太多工作。

(通常)这样可以减少多余的检查，Falcon可以专注运行一些核心代码，使得框架更高效。在这种理念下，利用Falcon构建一个高质量的API需要:

1.资源响应器将响应变量设置为完整值
2.大部分代码易于测试
3.错误应该是可预见、易查明，并且能在每个响应器中做作相应处理。

**Tip**

除非已经注册自定义处理这种情况的程序,不要继承`falcon.HTTPError`，否则Falcon将会重新抛出错误。(详情请见：[falcon.API][5])

谈到错误处理，当发生一些可怕的(轻度的)错误，我们可以手动设置错误状态、合适的响应header、甚至是一个使用`resp`对象的错误body。然而，Falcon通过提供一套在错误发生时可能抛出的异常，使得处理更加容易。事实上，如果Falcon捕获到(catch)继承自`falcon.HTTPError`的响应器(responder)抛出的任何异常，框架会将异常转换成对应的HTTP错误响应。

你可以抛出`falcon.HTTPError`的实例，或者使用一些预定义的错误类--尝试做一些正确的事情去设置header和body。查阅下面的文档，你可以获得横多关于在你的API中如何使用的信息：

```python
falcon.HTTPBadGateway
falcon.HTTPBadRequest
falcon.HTTPConflict
falcon.HTTPError
falcon.HTTPForbidden
falcon.HTTPInternalServerError
falcon.HTTPLengthRequired
falcon.HTTPMethodNotAllowed
falcon.HTTPNotAcceptable
falcon.HTTPNotFound
falcon.HTTPPreconditionFailed
falcon.HTTPRangeNotSatisfiable
falcon.HTTPServiceUnavailable
falcon.HTTPUnauthorized
falcon.HTTPUnsupportedMediaType
falcon.HTTPUpgradeRequired
```

例如，你可以这样处理没找到的图片:

```python
try:
    resp.stream = open(image_path, 'rb')
except IOError:
    raise falcon.HTTPNotFound()
```

或者你也可以这样处理一个假冒的文件名:

```python
VALID_IMAGE_NAME = re.compile(r'[a-f0-9]{10}\.(jpeg|gif|png)$')

#...

class Item(object):

    def __init__(self, storage_path):
        self.storage_path = storage_path
        
    def on_get(self, req, resp, name):
        if not VALID_IMAGE_NAME.match(name):
            raise falcon.HTTPNotFound()
```

有时候你可能对获取抛出异常的类型没有太多把握。为了解决这个问题，Falcon允许创建解决任何错误类型的自定义处理程序。例如，如果数据库抛出继承自清楚的数据库错误(NiftyDBError)异常，我们可以设置一个特殊的错误处理程序去处理对应的数据库错误(NiftyDBError),但是你不必跨多个响应器(respondee)去粘贴复制你的错误处理代码。

查阅关于`falcon.API.add_error_handler`的文档，获取更多这些特性的信息，使你的代码尽可能精简漂亮：

```
In [7]: help(falcon.API.add_error_handler)
```


##9. 现在该怎么做？

我们友好的社区可以回答你的问题，帮助你解决棘手的问题。

参照:[获取帮助][6]

之前有提到，Falcon的文档覆盖面是相当广的。所以通过Python交互式解释器(REPL,例如IPython、bpython)查阅Falcon的模块，你可以学到很多。

同时，千万不要吝啬将Github上的Falcon源代码pull下来，并用你喜欢的编辑器去查看Falcon代码。开发团队已经尽可能将代码写的简洁明了、高可读性;文档可能会有些不足，但是代码基本上不会出错的。


  [1]: http://falcon.readthedocs.org/en/stable/user/tutorial.html
  [2]: http://legacy.python.org/dev/peps/pep-3333/
  [3]: http://msgpack.org/
  [4]: https://github.com/talons/talons
  [5]: http://falcon.readthedocs.org/en/stable/api/api.html#api
  [6]: http://falcon.readthedocs.org/en/stable/community/help.html#help