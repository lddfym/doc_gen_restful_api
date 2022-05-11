import apimd
import json
import os


def json_to_md_string(filename):
    with open(filename, 'r') as f:
        content = f.read()
        api_list = json.loads(content)

    md = apimd.APIToMD()
    content = []
    for api in api_list:
        content.append(md.do(api))
    return "\n\n\n".join(content)


def generate_md(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if not filename.endswith(".json"):
                raise Exception(f"invalid file: {os.path.join(root, filename)}")
            content = json_to_md_string(os.path.join(root, filename))
            with open(os.path.join(output_dir, f"{filename[:-5]}.md"), "w") as f:
                f.write(content)


if __name__ == '__main__':
    generate_md("test_interface", "test_doc")
