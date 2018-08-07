from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible

import markdown
from django.utils.html import strip_tags

# 分类
class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

# 标签
class Tag(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Post(models.Model):
	title = models.CharField(max_length=70)
	# 文章标题

	body = models.TextField()
	# 文章正文

	created_time = models.DateTimeField()    # 创建时间
	modified_time = models.DateTimeField()   # 最后修改时间
	# 文章创建时间和最后修改时间

	excerpt = models.CharField(max_length=200, blank=True)
	# 文章摘要， 指定CharField的blank=True参数值后就可以允许空值，因为默认为必须存入数据

	category = models.ForeignKey(Category)
	# 这文章对应的数据库表和分类、标签对应的数据表关联

	tags = models.ManyToManyField(Tag, blank=True)   # 多对多
	author = models.ForeignKey(User)                 # 一对多 

	def save(self, *args, **kwargs):
		# 如果没有填写摘要
		if not self.excerpt:
			# 首先实例化一个 Markdown 类，用于渲染 body 的文本
			md = markdown.Markdown(extensions=[
				'markdown.extensions.extra',
				'markdown.extensions.codehilite',
				])
			# 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
			self.excerpt = strip_tags(md.convert(self.body))[:100]

		# 调用父类的 save 方法将数据保存到数据库中
		super(Post, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:detail', kwargs={'pk': self.pk})


	class Meta:
		ordering = ['-created_time']


	# 新增 views 字段记录阅读量
	views = models.PositiveIntegerField(default=0)

	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])

