from PIL import Image
import numpy as np

# np.set_printoptions(threshold=np.inf)


def get_small_modes(img,background=None):
    img = img.convert('L')
    box1 = (10, 4, 150, 36)
    img1 = img.crop(box1)
    mode = np.array(img1)
    if background:
        mode = np.where(mode < 100, 0, background)
    else:
        mode = np.where(mode < 100, 0, 1)
    return mode


def mode_to_img(mode,background=None):
    if background:
        mode = np.where(mode < 1, 0, background)
    array_mode = np.array(mode).astype('uint8')
    return Image.fromarray(array_mode).convert('RGB')


def is_white_column(column):
    return all(c != 0 for c in column)

def cut_from_rect(rect, start, end):
    # print("cut from %s to %s" % (start, end))
    return rect[:, start:end]
# 返回分割后的numpy矩阵
def vertical_cut(rect):
    max_width = 35
    last_position = 0
    # print(rect)
    width = rect.shape[1]

    result = []
    bools = []
    for x in range(width):
        c_position = x
        bools.append(is_white_column(rect[:, c_position]))
        if not bools[c_position] and c_position == 0:
            continue

        if not bools[c_position] and bools[c_position - 1]:
            last_position = c_position - 1
            continue

        if (bools[c_position] and not bools[c_position - 1]):
            # 开始截取, 从last_position到c_position
            delta = c_position - last_position
            if delta <= 1: # 像这样到肯定有问题，直接跳过
                continue

            bit = float(delta)/float(max_width)

            point_right = bit - int(bit)
            if point_right > 0.3:
                npart = int(bit) + 1
                interval = int(delta/npart)
                for i in range(npart):
                    if i == npart - 1:
                        # 考虑到整数运算会有误差，所以到最后一步就直接 last_position + inpart : c_position
                        result.append(cut_from_rect(rect, last_position, c_position))
                        last_position = c_position
                    else:
                        # 取last_position + i*npart : last_position + (i+1)*npart
                        result.append(cut_from_rect(rect, last_position, (last_position+(i+1)*interval)))
                        last_position += interval



    # for x in range(width):
    #     c_position = x
    #     bools.append(is_white_column(rect[:, x]))        
    #     if bools[-1] and (bools[-2] if bools.__len__() > 2 else True):
    #         last_position = c_position
    #     if bools[-1] and (not bools[-2] if bools.__len__() > 2 else True):
    #         if c_position - last_position >= 35:
    #             x1 = last_position
    #             x2 = int((c_position + last_position)/2)
    #             x3 = c_position
    #             # print(x1, x2, x3)
    #             result.extend([rect[:, x1:x2], rect[:, x2:x3]])
    #         else:
    #             # print(last_position, c_position)
    #             result.append(rect[:, last_position:c_position+1])
    #         last_position = c_position
    # result.pop(0)
    # result.pop(0)
    return result


def cut_img(img,max_width):
    my_mode = get_small_modes(img)
    li = vertical_cut(my_mode)
    for k,i in enumerate(li):
        its_height = np.shape(i)[0]
        its_width = np.shape(i)[1]
        # 当长度超过预计时，切割中间预计的部分
        if its_width > max_width:
            d = its_width - max_width
            li[k] = i[:,int(d/2):-int(d/2)-d%2]
        # 当长度小于预计的时候，两边填充全为1的列
        if its_width < max_width:
            d = max_width - its_width
            if d == 1:
                one_column1 = np.ones(its_height).reshape(its_height,1).astype('uint8')
                li[k] = np.hstack((i,one_column1))
            else:
                one_column = np.ones(its_height*int(d/2))\
                .reshape(its_height,int(d/2)).astype('uint8')
                one_column1 = np.ones(its_height*(int(d/2)+d%2))\
                .reshape(its_height,int(d/2)+d%2).astype('uint8')
                # print(i.shape)
                # print(one_column.shape)
                new_mode = np.hstack((one_column,i))
                li[k] = np.hstack((new_mode,one_column1))
        
        # img = mode_to_img(i,255)
        # img.show()
    return li




# img = Image.open(open('de_crook_imgs/2.png', 'rb'))
# lis = cut_img(img, 30)
# for i in lis:
#     mode_to_img(i,255).show()

# cut_img(img, 30)