import atomd as md


class DictToTableMD(object):
    def __init__(self):
        self.opt = "_"
        self.opt_yes = "是"
        self.opt_no = "否"
        self.seg = "|"
        self.title_level = 3

    def _parse_format_key(self, key):
        """
        解析指定格式的键值

            key = "_id"
        解析结果：
            "id","否"

        :param key: format_string
        :return: key, opt
        """
        if key.startswith(self.opt):
            return key[len(self.opt):], self.opt_no
        return key, self.opt_yes

    def _parse_format_value(self, value):
        """
        解析指定格式的值

            value = "1|number|数量"
        解析结果：
            "1","Number","数量"

        :param value: format_string
        :return: value, type, desc
        """
        if isinstance(value, int) or isinstance(value, float):
            return value, "Number", " "
        if isinstance(value, list):
            return " ", "Array", " "
        if isinstance(value, dict):
            return " ", "Object", " "

        if isinstance(value, str):
            v_split = value.split(self.seg)

            v, t, d = " ", "String", " "
            if len(v_split) > 0:
                v = v_split[0] if v_split[0] != "" else " "  # 某些markdown渲染器无法渲染"",只能识别到" "

            if len(v_split) > 1:
                if v_split[1].lower() == "number":
                    t = "Number"
                elif v_split[1] == "":
                    t = "String"
                else:
                    raise Exception("invalid value type")

            if len(v_split) > 2:
                d = v_split[2]

            return v, t, d

        raise Exception("can not parse value")

    def table(self, title, obj):
        """
        字典信息
        :param title:标题
        :param obj:字典内容
        :return:markdown string
        """
        head = ["参数名", "示例值", "类型", "必填项", "描述"]
        # lines = self._dict_parse_root(obj)
        lines = self._parse(obj)
        return md.title(self.title_level, title) + md.next_row() + md.table(head, lines)

    def _parse(self, obj):
        """
        解析信息

            data = {"a": "1|number|数量"}
        解析结果：
            [["a","1","Number","是","数量"]]

        :param obj: int or float or str or dict or list
        :return: [[name, value, type, opt, desc]...]
        """
        comment = []
        if isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, str):
            v, t, d = self._parse_format_value(obj)
            comment.append(["", str(v), t, "", d])

        if isinstance(obj, list):
            for value in obj:
                for item in self._parse(value):
                    comment.append(item)

        if isinstance(obj, dict):
            for key, value in obj.items():
                name, opt = self._parse_format_key(key)
                v, t, d = self._parse_format_value(value)
                comment.append([name, str(v), t, opt, d])

                if isinstance(value, int) or isinstance(value, float) or isinstance(value, str):
                    continue

                # value is dict or list
                for item in self._parse(value):
                    if item[0] != "":
                        item[0] = f"{name}.{item[0]}"
                    else:
                        item[0] = f"{name}.[]"
                    comment.append(item)

        return comment

    def clear_format(self, obj):
        """
        清除格式
        :param obj: int or float or str or dict or list
        :return: obj
        """
        if isinstance(obj, int) or isinstance(obj, float):
            return obj

        if isinstance(obj, str):
            v_split = obj.split(self.seg)
            new_value = v_split[0]
            if len(v_split) > 1:
                if v_split[1].lower() == "number":
                    new_value = int(v_split[0]) if "." not in v_split[0] else float(v_split[0])
            return new_value

        if isinstance(obj, list):
            new_value = []
            for item in obj:
                v = self.clear_format(item)
                new_value.append(v)
            return new_value

        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                new_key = key if not key.startswith(self.opt) else key[len(self.opt):]
                new_value = self.clear_format(value)
                new_obj[new_key] = new_value
            return new_obj


if __name__ == '__main__':
    data = {
        "err_no": "0|number|错误码",
        "err_msg": "success||错误描述",
        "_data": {
            "pages": "1|number|总页数",
            "rows": "10|number|总行数",
            "acc": [
                {
                    "id": "1|number|配饰id",
                    "address": "http://www.baidu.com||URL",
                    "model_id": ["1|number|模型id"]
                }
            ]
        }
    }

    dm = DictToTableMD()
    m = dm.table("测试", data)
    print(m)

    raw = dm.clear_format(data)
    print(raw)

