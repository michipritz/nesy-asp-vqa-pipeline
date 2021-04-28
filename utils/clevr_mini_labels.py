import json
import pycocotools.mask as mask

size_dict = {
    'large': 'La',
    'small': 'Sm'
}

shape_dict = {
    'cylinder': 'Cy',
    'sphere': 'Sp',
    'cube': 'Cu'
}

color_dict = {
    'gray': 'Gra',
    'blue': 'Bl',
    'brown': 'Br',
    'yellow': 'Ye',
    'red': 'Re',
    'green': 'Gre',
    'purple': 'Pu',
    'cyan': 'Cy'
}

material_dict = {
    'metal': 'Me',
    'rubber': 'Ru'
}


def get_width_and_height_from_bit_mask(m):
    img_width = len(m[0])
    img_height = len(m)

    min_hor_start_pos = img_width
    max_hor_end_pos = 0
    min_vert_start_pos = img_height
    max_vert_end_pos = 0

    for row_num, row_val in enumerate(m):
        hor_start_pos = img_width
        hor_end_pos = 0
        hor_obj_detected = False

        vert_start_pos = img_height
        vert_end_pos = 0
        vert_obj_detected = False

        for col_num, col_val in enumerate(row_val):
            if col_val != 0 and hor_obj_detected is False:
                hor_start_pos = col_num
                hor_end_pos = col_num
                hor_obj_detected = True
            elif col_val != 0:
                hor_end_pos = col_num

            if col_val != 0 and vert_obj_detected is False:
                vert_start_pos = row_num
                vert_end_pos = row_num
                vert_obj_detected = True
            elif col_val != 0:
                vert_end_pos = row_num

        if hor_start_pos < min_hor_start_pos:
            min_hor_start_pos = hor_start_pos

        if hor_end_pos > max_hor_end_pos:
            max_hor_end_pos = hor_end_pos

        if vert_start_pos < min_vert_start_pos:
            min_vert_start_pos = vert_start_pos

        if vert_end_pos > max_vert_end_pos:
            max_vert_end_pos = vert_end_pos

    width = 0.0
    height = 0.0

    if not (min_hor_start_pos == img_width and max_hor_end_pos == 0):
        width = max_hor_end_pos - min_hor_start_pos + 1

    if not (min_vert_start_pos == 0 and max_vert_end_pos == 0):
        height = max_vert_end_pos - min_vert_start_pos + 1

    return width, height


def get_category_from_obj(o):
    category_str = ''
    category_str += size_dict[o['size']]
    category_str += color_dict[o['color']]
    category_str += material_dict[o['material']]
    category_str += shape_dict[o['shape']]
    return category_str


def get_category_dict():
    category_id_dict = {}
    category_id = 0
    for size in size_dict:
        for color in color_dict:
            for material in material_dict:
                for shape in shape_dict:
                    category_str = ''
                    category_str += size_dict[size]
                    category_str += color_dict[color]
                    category_str += material_dict[material]
                    category_str += shape_dict[shape]
                    category_id_dict[category_str] = category_id
                    category_id += 1

    return category_id_dict


if __name__ == '__main__':
    with open('../data/clevr_mini/CLEVR_mini_coco_anns.json') as scenes_file:
        scenes = json.load(scenes_file)['scenes']

    scene_count = len(scenes)
    for i, scene in enumerate(scenes):
        print('Scene %d/%d' % (i, scene_count))

        out_file_name = 'CLEVR_mini_%06d.txt' % scene['image_index']
        out_file = open('../data/clevr_mini/labels/' + out_file_name, 'w')
        scene_labels = ''
        for obj in scene['objects']:
            bit_mask = mask.decode(obj['mask'])
            img_height = len(bit_mask)
            img_width = len(bit_mask[0])

            x = obj['pixel_coords'][0] / img_width
            y = obj['pixel_coords'][1] / img_height

            width, height = get_width_and_height_from_bit_mask(bit_mask)
            width /= img_width
            height /= img_height

            category = get_category_from_obj(obj)

            category_dict = get_category_dict()

            scene_labels += '%d %f %f %f %f\n' % (category_dict[category], x, y, width, height)

        out_file.write(scene_labels[:-1])
        out_file.close()
