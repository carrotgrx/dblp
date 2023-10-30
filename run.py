# -*- coding: UTF-8 -*-
import sys


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Usage: python run.py input.txt")
        sys.exit(1)
    file_path = sys.argv[1]
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()

    # 分割数据
    lines = file_contents.split('\n')
    attributes = {}
    current_attribute = ""

    total_groups = 0
    empty_attribute_groups = 0

    for line in lines:
        line = line.strip()
        if line:
            if ':' in line:
                attribute_name, attribute_value = map(str.strip, line.split(':', 1))
                current_attribute = attribute_name
                attributes[current_attribute] = attribute_value
            elif current_attribute:
                attributes[current_attribute] += "\n" + line
        else:
            if current_attribute:
                total_groups += 1
                if any(value.strip() == '' for value in attributes.values()):
                    empty_attribute_groups += 1
            attributes = {}

    # 处理最后一组
    if current_attribute:
        total_groups += 1
        if any(value.strip() == '' for value in attributes.values()):
            empty_attribute_groups += 1

    print(f"总组数: {total_groups}")
    print(f"包含空值的组数: {empty_attribute_groups}")
    print(f"完整度: {(total_groups - empty_attribute_groups) / total_groups * 100:.2f}%")
