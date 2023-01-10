from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pymysql

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123123', db='待办事项',
                     charset='utf8')
cursor = db.cursor()


class Item(BaseModel):
    id: int
    title: Optional[str] = None
    content: Optional[str] = None
    statuss: Optional[str] = None
    starttime: Optional[str] = None
    endtime: Optional[int] = None


app = FastAPI()


class SearchMenu(BaseModel):
    type: str
    id: Optional[int] = None
    keyword: Optional[str] = None
    page: Optional[int] = None


@app.post("/add")
async def add(item: Item):
    item_dict = item.dict()
    addsql = """
            INSERT INTO todolist(id, title, content, statuss, starttime, endtime)
            VALUES ({0}, "{1}", "{2}", "{3}", {4}, {5});
            """

    try:
        cursor.execute(addsql.format(item.id, item.title, item.content, item.statuss, item.starttime, item.endtime))
        db.commit()
        searchsql = """
                    SELECT * FROM todolist
                    WHERE id = {0};
                    """
        cursor.execute(searchsql.format(item.id))
        data = cursor.fetchone()
        result = {}
        result["code"] = 200
        result["msg"] = "success"
        result["data"] = data
        return result
    except:
        db.rollback()
        result = {}
        result["code"] = 404
        result["msg"] = "该id已存在!"
        return result


@app.post("/delete")
async def delete(searchmenu: SearchMenu):
    if searchmenu.type == "id":
        deletesql = """
                    DELETE FROM todolist WHERE id = {0};
                    """
        cursor.execute(deletesql.format(searchmenu.id))
        db.commit()
        result = {}
        result["code"] = 200
        result["msg"] = "success"
        return result
    if searchmenu.type == "删除所有事项":
        deletesql = """
                    DELETE FROM todolist;
                    """
        cursor.execute(deletesql.format(searchmenu.id))
        db.commit()
        result = {}
        result["code"] = 200
        result["msg"] = "success"
        return result
    if searchmenu.type == "删除所有已完成":
        deletesql = """
                    DELETE FROM todolist WHERE statuss = "已完成";
                    """
        cursor.execute(deletesql.format(searchmenu.id))
        db.commit()
        result = {}
        result["code"] = 200
        result["msg"] = "success"
        return result
    if searchmenu.type == "删除所有待办":
        deletesql = """
                    DELETE FROM todolist WHERE statuss = "待完成";
                    """
        cursor.execute(deletesql.format(item.id))
        db.commit()
        result = {}
        result["code"] = 200
        result["msg"] = "success"
        return result
    else:
        result = {}
        result["code"] = 404
        result["msg"] = "该活动不存在"
        return result


@app.post("/update")
async def update(item: Item):
    if item.statuss != None:
        updatesql = """
                    UPDATE todolist SET statuss="{0}"
                    WHERE id = "{1}";
                    """
        cursor.execute(updatesql.format(item.statuss, item.id))
        db.commit()
        searchsql = """
                            SELECT * FROM todolist
                            WHERE id = {0};
                            """
        cursor.execute(searchsql.format(item.id))
        data = cursor.fetchone()
        result = {}
        result["code"] = 200
        result["msg"] = "success"
        result["data"] = data
        return result
    else:
        result = {}
        result["code"] = 404
        result["msg"] = "该活动不存在"
        return result


@app.post("/search")
async def search(searchmenu: SearchMenu):
    if searchmenu.type == "查询所有事项":
        searchsql = """
                    SELECT * FROM todolist
                    LIMIT {1},5
                    """
        cursor.execute(searchsql.format(searchmenu.keyword,(searchmenu.page-1)*5))
        data = cursor.fetchall()
        result = {}
        result["code"] = 200
        result["msg"] = "success"
        if len(data) != 0:
            result["data"] = data
        else:
            result["data"] = "搜索成功,但是一个To-do都没有qwq"
        return result

    if searchmenu.type == "查询所有已完成":
        searchsql = """
                    SELECT * FROM todolist
                    WHERE statuss = "已完成"
                    LIMIT {1},5
                    """
        cursor.execute(searchsql.format(searchmenu.keyword,(searchmenu.page-1)*5))
        data = cursor.fetchall()
        result = {}
        result["code"] = 200
        result["msg"] = "success"
        if len(data) != 0:
            result["data"] = data
        else:
            result["data"] = "搜索成功,一个已完成的都没有>_<"
        return result

    if searchmenu.type == "查询所有待办":
        searchsql = """
                    SELECT * FROM todolist
                    WHERE statuss = "待完成"
                    LIMIT {1},5
                    """
        cursor.execute(searchsql.format(searchmenu.keyword,(searchmenu.page-1)*5))
        data = cursor.fetchall()
        result = {}
        result["code"] = 200
        result["msg"] = "success"
        if len(data) != 0:
            result["data"] = data
        else:
            result["data"] = "搜索成功,所有To-do都完成了捏~"
        return result

    if searchmenu.type == "关键字查询":
        searchsql = """
                    SELECT * FROM todolist 
                    WHERE title LIKE "%{0}%"
                    LIMIT {1},5
                    """
        cursor.execute(searchsql.format(searchmenu.keyword,(searchmenu.page-1)*5))
        data = cursor.fetchall()
        result = {}
        result["code"] = 200
        result["msg"] = "success"
        if len(data) != 0:
            result["data"] = data
        else:
            result["data"] = "搜索成功,但是没有关于" + searchmenu.keyword + "的To-do"
        return result

    if searchmenu.type == "id查询":
        searchsql = """
                        SELECT * FROM todolist
                        WHERE id = {0};
                        """
        cursor.execute(searchsql.format(searchmenu.id))
        data = cursor.fetchall()
        result = {}
        result["code"] = 200
        result["msg"] = "success"
        if len(data) != 0:
            result["data"] = data
        else:
            result["data"] = "该id下没有To-do!"
        return result
    else:
        result = {}
        result["code"] = 404
        result["msg"] = "该活动不存在"
        return result
