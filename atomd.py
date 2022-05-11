

def table(head, lines):
    """
    3行5列的表格
    |     |     |     |     |     |
    | --- | --- | --- | --- | --- |
    |     |     |     |     |     |
    |     |     |     |     |     |

    :param head: 表头 ["",...]
    :param lines: 表格内容 [["",...]...]
    :return: markdown string
    """
    if len(head) == 0 or len(lines) == 0:
        raise Exception("table's param is invalid")
    if len(head) != len(lines[0]):
        raise Exception("table's head and line are not consistency")

    # 统一列宽
    column = [0 for _ in range(len(head))]
    for i, cell in enumerate(head):
        if len(cell) > column[i]:
            column[i] = len(cell)
    column[-1] += 1  # 最后一列多加一个空格

    for line in lines:
        for i, cell in enumerate(line):
            if len(cell) > column[i]:
                column[i] = len(cell)
    column = [i + 2 for i in column]

    for i in range(len(head)):
        head[i] = " " + head[i] + " "
        head[i] += " "*(column[i] - len(head[i]))
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            lines[i][j] = " " + lines[i][j] + " "
            lines[i][j] += " "*(column[j] - len(lines[i][j]))

    # 表头
    hmd = "|" + "|".join(head) + "|\n"
    # 分割线
    split = "|" + "|".join(["-"*i for i in column]) + "|\n"
    # 表数据
    lmd = ["" for _ in range(len(lines))]
    for i, line in enumerate(lines):
        lmd[i] = "|" + "|".join(line) + "|"

    return hmd + split + "\n".join(lmd)


def title(level, name):
    """
    标题
    :param level: 标题等级
    :param name: 标题名
    :return: markdown string
    """
    if level < 1:
        raise Exception("title's param is invalid")

    return "".join(["#" for _ in range(level)]) + " " + name


def bold(text):
    """
    字体加粗
    :param text: 文本
    :return:
    """
    return f"**{text}** "


def next_row():
    """
    换行
    :return: markdown string
    """
    # 如流识知库仅支持空行，不支持换行，所以此处在markdown换行符后增加了一个\n
    return "  \n\n"


def code(code_type, content):
    """
    内嵌代码
    :param code_type: 代码类型
    :param content: 代码内容
    :return: markdown string
    """
    return f"```{code_type}\n{content}\n```"


if __name__ == '__main__':
    h = ["a", "b", "c"]
    l = [
        ["1", "2", "3"],
        ["4", "5", "6"]
    ]
    res = table(h, l)
    print(res)
    print(title(5, "标题"))
    print(code("python", "import"))

