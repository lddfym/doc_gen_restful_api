import atomd as md
import dictmd
import json


class APIToMD(object):
    """
    api 接口的 字典描述 转 markdown描述
    """
    def __init__(self):
        self.analyze = dictmd.DictToTableMD()
        self.title1 = 2
        self.title2 = 3

        self.analyze.title_level = self.title2

    def do(self, api):
        """
        生成接口文档
        :param api: 接口 dict
        :return: markdown string
        """
        items = [self._illustrate(api), self._base_info(api)]

        if "query" in api["request"] and api["request"]["query"]:
            info = self.analyze.table("URL参数", api["request"]["query"])
            items.append(info)

        if "header" in api["request"] and api["request"]["header"]:
            info = self.analyze.table("请求头", api["request"]["header"])
            items.append(info)
        if "body" in api["request"] and api["request"]["body"]:
            info = self.analyze.table("请求参数", api["request"]["body"])
            items.append(info)

        if "header" in api["response"] and api["response"]["header"]:
            info = self.analyze.table("响应头", api["response"]["header"])
            items.append(info)
        if "body" in api["response"] and api["response"]["body"]:
            info = self.analyze.table("响应参数", api["response"]["body"])
            items.append(info)

        info = self._code_example(api)
        items.append(info)
        return md.next_row().join(items)

    def _illustrate(self, api):
        """
        接口基本信息
        :param api: 接口
        :return: markdown string
        """

        headline = ""
        explain = ""

        if "headline" in api and api["headline"] != "":
            headline = md.title(self.title1, api["headline"])
        if "explain" in api and api["explain"] != "":
            explain = md.title(self.title2, "接口说明") + md.next_row() + api["explain"]

        if explain:
            return headline + md.next_row() + explain
        return headline

    def _base_info(self, api):
        """
        接口基本信息
        :param api: 接口
        :return: markdown string
        """
        title = md.title(self.title2, "基本信息")
        address = md.bold("接口URL:") + api["request"]["address"]
        method = md.bold("请求方式:") + api["request"]["method"]
        return title + md.next_row() + address + md.next_row() + method

    def _code_example(self, api):
        """
        接口示例代码：HTTP 描述
        :param api: 接口 dict
        :return: markdown string
        """
        api = self.analyze.clear_format(api)

        url = api["request"]["address"]
        param = []
        if "query" in api["request"]:
            for key, value in api["request"]["query"].items():
                param.append(f'{key}={value}')
            if param:
                param = '?' + '&'.join(param)

        if param:
            if url.endswith('/'):
                url = url[:len(url) - 1] + param
            else:
                url += param

        request_line = f'{api["request"]["method"]} {url} HTTP/1.1\n'
        request_header = ""
        request_body = ""
        if "header" in api["request"]:
            header = []
            for key, value in api["request"]["header"].items():
                header.append(f"{key}: {value}")
            request_header = "\n".join(header) + "\n"
        if "body" in api["request"]:
            request_body = json.dumps(obj=api["request"]["body"], indent=2)

        response_line = f'HTTP/1.1 200 OK\n'
        response_header = ""
        response_body = ""
        if "header" in api["response"]:
            header = []
            for key, value in api["response"]["header"].items():
                header.append(f"{key}: {value}")
            response_header = "\n".join(header) + "\n"
        if "body" in api["response"]:
            response_body = json.dumps(obj=api["response"]["body"], indent=2)

        request = "请求:\n" + request_line + request_header + "\n" + request_body
        response = "响应:\n" + response_line + response_header + "\n" + response_body
        code = request + "\n\n" + response

        code = md.code("", code)
        return md.title(3, "示例代码") + md.next_row() + code


if __name__ == '__main__':
    data = {
        "headline": "查询信息",
        "explain": "可以测试",
        "request": {
            "method": "POST",
            "address": "http://hostname/query",
            "query": {},
            "header": {
                "Content-Type": "application/json",
                "VERSION": 3
            },
            "body": {
                "timestamp": "123456|number|时间戳",
                "a": 5,
            }
        },
        "response": {
            "header": {},
            "body": {
                "err_no": 0,
                "err_msg": "success",
                "log_id": "123456",
                "data": {
                    "a": 1,
                    "b": 5,
                    "case": [
                        {
                            "case_id": 1,
                            "name": "base_case",
                            "size": 1024,
                            "address": "url",
                            "md5": "zxcv"
                        }
                    ]
                }
            }
        }
    }
    m = APIToMD()
    print(m.do(data))
