from enum import IntEnum
from tortoise import models
from tortoise import fields
from tortoise import Tortoise, run_async


class AbstractModel(models.Model):
    # 主键，当表里所有属性都没设置pk时，默认生成一个IntField类型 id 的主键
    id = fields.UUIDField(pk=True)

    class Meta:
        # 抽象模型，不生成表
        abstract = True


class MixinTimeFiled:
    # 添加数据时间
    created = fields.DatetimeField(null=True, auto_now_add=True)
    # 修改数据时间
    modified = fields.DatetimeField(null=True, auto_now=True)


class Gender(IntEnum):
    MAN = 0
    WOMAN = 1


class UserModel(AbstractModel, MixinTimeFiled):
    # unique 是否唯一 max—length 数据长度 index 是否索引
    username = fields.CharField(max_length=20, description="描述", unique=True, index=True)
    # null 是否可以为空
    nickname = fields.CharField(max_length=30, description='nickname', null=True, default='777')
    # description 字段备注 ddl展示， 此处入库的为 0 or 1
    gender = fields.IntEnumField(Gender, description='sex', default=Gender.WOMAN)
    # max——digits 小输点左边最大位数，decimal——places 小数点右边最大位数
    balance = fields.DecimalField(max_digits=2, decimal_places=2, description='balance')
    is_admin = fields.BooleanField(default=False)
    job_info = fields.JSONField(default=dict)

    class Meta:
        # 自定义表名，不配置按照类名小写生成
        table = "tableName"
        table_description = "set table ddl desc"

        # 多列设置唯一复合所有
        unique_together = (('gender', 'balance'),)
        # 排序
        ordering = ('is_admin',)
        # 索引
        indexes = ('balance',)


class Test(AbstractModel, MixinTimeFiled):
    description = fields.CharField(max_length=50)


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        # 数据库连接
        db_url='mysql://root:123456@127.0.0.1:3306/asyncsql',
        # 连接mysql pip install aiomysql
        # db_url='mysql://root:123456@127.0.0.1:3306/tortoise',
        # 指定管理的models，__main__ 🈯️当前文件的models.Model
        modules={'models': ['__main__']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

if __name__ == '__main__':

    run_async(init())
