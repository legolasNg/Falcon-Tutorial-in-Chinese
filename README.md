---
##Falcon-Tutorial-in-Chinese

中文版Falcon官方教程《Falcon Tutorial》([英文原版][1],Falcon版本：0.3.0stable)。

后续会将官方文档《Classes and Functions》([英文原版][2])也进行翻译。

这是个人业余时间的一个尝试，如果有什么问题，欢迎指正。

<wujianye3@163.com>

---
##Falcon安装

###使用PyPi安装

- 如果Cython可用，Falcon使用Cython可以很快编译自身。那么我们首先确保已经安装了最新版的Cython:

```
$ pip install --upgrade cython falcon
```

- 如果你想使其在PyPy上运行，你可以不用安装Cython，只需要输入下面的命令:

```
$ pip install --upgrade falcon
```

**注意事项**
当你使用Cython时，你应该在升级Python之后重新编译一下Falcon。命令如下:

```
$ pip install --force-reinstall --upgrade cython
$ pip install --force-reinstall --upgrade falcon
```

###在OSX上安装Cython

- 想要在带5.1版本Xcode的OS X Mavericks上运行Cython，你首先得配置好Xcode Command Line Tools。使用下面的命令来安装:

```
$ xcode-select --install
```

- 5.1版本Xcode的CLang编译器会将一些无法识别的命令行选项当作错误处理;在Python 2.6下会出现一些问题，例如:

```
clang: error: unknown argument: '-mno-fused-madd' [-Wunused-command-line-argument-hard-error-in-future]
```

我们可以通过设置环境变量来解决一些由未使用的参数导致的问题:

```
$ export CFLAGS=-Qunused-arguments
$ export CPPFLAGS=-Qunused-arguments
$ pip install cython falcon
```

###WSGI服务器

- Falcon依赖于WSGI。如果你想运行你的Falcon应用，你需要一个好的WSGI服务器。Gunicorn和uWSGI是使用最广泛的WSGI服务器，你可以在上面加载应用做任何事情。Gevent是一个异步库，可以很好的和Gunicorn或uWSGI搭配使用:

```
$ pip install --upgrade gevent [gunicorn|uwsgi]
```

###源码

- 为了使源码易于查看、下载、fork，Falcon将源码托管在Github。同时也非常欢迎提交代码！如果您愿意，记得star下我们的项目。

- 只要你从Github上clone或者下载了压缩包，你可以这样安装:

```
$ cd falcon
$ pip install .
```

- 另外，如果你想编辑代码，先从主仓库fork，然后clone这个fork到你的电脑，运行下面的命令使用符号链接去安装。这样，当你修改了fork版本的代码，可以直接在你的应用上生效，而不用去重新安装这个包:

```
$ cd  falcon
$ pip install -e
```

---
##Falcon简介

Falcon 是一个高性能的 Python 框架，用于构建云端 API 和 Web 应用的后端程序。

###1 .设计目标

- Fast
- Light
- Flexible

###2 .特性

- 通过URI模板和资源类可直观的了解路由信息
- 轻松访问请求和响应类来访问header和body信息
- 通过方便的异常类实现对HTTP错误响应的处理
- 通过全局、资源和方法钩子实现DRY请求处理
- 通过WSGI helper和mock实现单元测试
- 使用Cython可提升20%的速度
- 支持Python 2.6,Python 2.7,PyPy和Python 3.3/3.4
- 高性能

官方github主页:<https://github.com/falconry/falcon>

Falcon官网:<http://falconframework.org/index.html>

[1]:http://falcon.readthedocs.org/en/stable/user/tutorial.html
[2]:http://falcon.readthedocs.org/en/stable/api/index.html
