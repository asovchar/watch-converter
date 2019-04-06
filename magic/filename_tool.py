import os


def find_name(file_name):
    if os.path.isfile(file_name):
        idx = 1
        while True:
            *_, body, ext = file_name.split(".")
            new_file_name = f'.{body}_{idx}.{ext}'
            if not os.path.isfile(new_file_name):
                break
            idx += 1
    else:
        new_file_name = file_name
    return new_file_name


if __name__ == '__main__':
    a = find_name('./res/test.jpg')
    print(a)
