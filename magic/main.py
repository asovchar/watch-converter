import os
import glob
import magic.load as load
import magic.colors as colors
import magic.size as size
from magic.filename_tool import find_name


def main():
    print('{:5s}  {:30s} {:30s}'.format('Index', 'Source', 'Result'))
    for idx, img_name in enumerate(glob.glob('./src/*.jpg') + glob.glob('./res/*.png')):
        img_arr = load.load_image(img_name)

        fixed = colors.fix(img_arr)
        colored = colors.invert(fixed)

        screen_ratio = int(os.environ['HEIGHT'])/int(os.environ['WIDTH'])
        borders = size.find_borders(colored)
        cut = size.cut_borders(colored, borders)
        restored = size.restore_ratio(cut, screen_ratio)

        new_name = find_name('./res/watch_img.jpg')
        load.save_image(restored, new_name)
        print('{:5d}  {:30s} {:30s}'.format(idx, img_name, new_name))


if __name__ == '__main__':
    import dotenv
    dotenv.load_dotenv('.env')

    for directory in ('./src/', './res/'):
        try:
            os.mkdir(directory)
            print(f'Directory "{directory}" was created')
        except FileExistsError:
            pass
    main()
