# Blog
- 这是我的一个仿照CSDN的博客网站
# 技术细节
- 前端技术：
  * Bootstrap：页面的基本样式搭建
  * jQuery：简化ajax请求
  * wangEditor：搭建富文本编辑器
  * highlight：语法高亮效果的实现
- 后端技术：
  * Django5
- 数据库：
  * MySQL
# 使用说明
- 配置my_database.cnf
  * ```database```：你项目对应的数据库名称
  * ```user```：数据库的使用用户名
  * ```password```：数据库的密码
- 配置验证码的发送邮箱，这里以QQ邮箱为例
  * ```EMAIL_HOST_USER```：配置发送验证码的邮箱
  * ```EMAIL_HOST_PASSWORD```：配置QQ邮箱的授权码
  * ```DEFAULT_FROM_EMAIL```：配置默认的发送邮箱
- 生成相关的表单，按顺序执行以下命令
  * ```python manage.py makemigrations```
  * ```python manage.py migrate```