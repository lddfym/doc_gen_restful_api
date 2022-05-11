import json

Empty_Element = {
    "headline": "",
    "explain": "",
    "request": {
        "method": "",
        "address": "",
        "query": {
        },
        "header": {
        },
        "body": {
        }
    },
    "response": {
        "header": {
        },
        "body": {
        }
    }
}


def template(count, filename, element_filename=None):
    if element_filename is None:
        element = Empty_Element
    else:
        with open(element_filename, 'r') as f:
            content = f.read()
            element = json.loads(content)

    content = []
    for i in range(count):
        content.append(element)

    doc = json.dumps(obj=content, indent=2)
    with open(filename, 'w') as f:
        f.write(doc)


def empty_element(filename):
    doc = json.dumps(obj=Empty_Element, indent=2)
    with open(filename, 'w') as f:
        f.write(doc)


if __name__ == '__main__':
    element_file = 'element_get.json'

    output = 'backend_get.json'
    api_num = 3
    template(api_num, output, element_file)
