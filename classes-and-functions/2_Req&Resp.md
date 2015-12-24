#请求/响应

标签： Falcon req resp

---

请求和响应类的实例被传入到响应器(responder)，分别作为第二和第三个参数。

```python
import falcon


class Resource(object):

    def on_get(self, req, resp):
        resp.body = '{"message": "Hello world!"}'
        resp.status = falcon.HTTP_200

```

##请求(request)

###class falcon.Request(env, options=None)
[source][1]

表示客户端的HTTP请求。

**注意事项**

*Request并不意味着要被响应器(responder)直接实例化*

参数:

- `env (dict)` – 从服务器传入的WSGI环境的字典，详情见:PEP-3333

- `options (dict)` - 从API处理程序传入的全局选项集合

####protocol

####method

####host

####subdomain

####user_agent

####app

####env

####context

####context_type

####uri

####url

####relative_uri

####path

####query_string

####accept

####auth

####client_accepts_json

####client_accepts_msgpack

####client_accepts_xml

####content_type

####content_length

####stream

####date

####expect

####range

####if_match

####if_none_match

####if_modified_since

####if_unmodified_since

####if_range

####headers

####params

####options

####cookies

####client_accepts(media_type)
source

####client_prefers(media_types)
source

####get_header(name, required=False)
source

####get_header_as_datetime(header, required=False)
source

####get_param(name, required=False, store=None, default=None)
source

####get_param_as_bool(name, required=False, store=None, blank_as_true=False)
source

####get_param_as_date(name, format_string='%Y-%m-%d', required=False, store=None)
source

####get_param_as_int(name, required=False, min=None, max=None, store=None)
source

####get_param_as_list(name, transform=None, required=False, store=None)
source

####log_error(message)
source

##响应(response)

###class falcon.Response
source

**注意事项**

**

####status

####body

####body_encoded

####data

####stream

####stream_len

####add_link(target, rel, title=None, title_star=None, anchor=None, hreflang=None, type_hint=None)
source

**注意事项**

**

**注意事项**

**

#####参数:

- target (str)

- rel (str)

#####Kwargs:

######title (str):

######title_star (tuple of str):

######anchor (str):

######hreflang (str or iterable):

######type_hint(str):

####append_header(name, value)
source

####cache_control

####content_location

####content_range

####content_type

####etag

####last_modified

####location

####retry_after

####set_cookie(name, value, expires=None, max_age=None, domain=None, path=None, secure=True, http_only=True)
source

#####参数

- name (str)

- value (str) 

- expires (datetime)

- max_age (int)

- domain (str)

- path (str)

- secure (bool)

- http_only (bool)

#####抛出(Raise)

- KeyError

- ValueError

####set_header(name, value)
source

#####参数

- name (str)

- value (str)

####set_headers(headers)
source

#####参数

- headers (dict or list)

#####抛出(Raise)

- ValueError

####set_stream(stream, stream_len)
source

####unset_cookie(name)
source

####vary



  [1]: https://github.com/falconry/falcon/blob/master/falcon/request.py#L58