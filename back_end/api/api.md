TODO: PUT，DELETE
方法|路径|说明|
---|---|---|
GET | /user  | 获得当前用户信息,需要登录
POST |/user | 登录用户，返回token
GET | /user/posts | 当前用户的帖子,需要登录
GET| /users/<user_id>/posts | 指定用户的帖子
POST | /users | 新增用户
GET | /posts | 所有帖子列表
GET | /posts/<post_id> | 指定帖子详情
POST | /posts | 新增帖子