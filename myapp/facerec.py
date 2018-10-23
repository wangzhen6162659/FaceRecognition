# -*- coding: UTF-8 -*-
import sys,os,dlib,glob,numpy
from skimage import io

def getFace(arr,file):
    if len(arr) != 4:
         print("请检查参数是否正确")
         exit()
     #1.人脸关键点检测器
    predictor_path = arr[0]
    # 2.人脸识别模型
    face_rec_model_path = arr[1]
    # 3.候选人脸文件夹
    descriptors = arr[2]
    # 4.需识别的人脸
    id_labels = arr[3]
    # 1.加载正脸检测器
    detector = dlib.get_frontal_face_detector()
    # 2.加载人脸关键点检测器
    sp = dlib.shape_predictor(predictor_path)
    # 3. 加载人脸识别模型
    facerec = dlib.face_recognition_model_v1(face_rec_model_path)

    # win = dlib.image_window()

    # 候选人脸描述子list

    # 对文件夹下的每一个人脸进行:
    # 1.人脸检测
    # 2.关键点检测
    # 3.描述子提取

    # names = glob.glob(faces_folder_path+ '*.jpg')
    # print(names)
    # for x in names:
    #     id_labels.append(x[x.rfind('\\')+1:x.rfind('.')])
    # for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
    #     print("Processing file: {}".format(f))
    #     img = io.imread(f)
    #     #win.clear_overlay()
    #     #win.set_image(img)
    #
    #     # 1.人脸检测
    #     dets = detector(img, 1)
    #     print("Number of faces detected: {}".format(len(dets)))
    #
    #     for k, d in enumerate(dets):
    #     # 2.关键点检测
    #         shape = sp(img, d)
    #     # 画出人脸区域和和关键点
    #     # win.clear_overlay()
    #     # win.add_overlay(d)
    #     # win.add_overlay(shape)
    #
    #     # 3.描述子提取，128D向量
    #     face_descriptor = facerec.compute_face_descriptor(img, shape)
    #
    #     # 转换为numpy array
    #     v = numpy.array(face_descriptor)
    #     descriptors.append(v)

    # 对需识别人脸进行同样处理
    # 提取描述子，不再注释
    # img = io.imread(img_path)
    img = io.imread(file)
    dets = detector(img, 1)
    if len(dets) == 0:
        return [];

    dist = []
    d_test = []
    for k, d in enumerate(dets):
        shape = sp(img, d)
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        d_test = numpy.array(face_descriptor)

        # 计算欧式距离

        for i in descriptors:
            dist_ = numpy.linalg.norm(i-d_test)
            dist.append(dist_)

    # fobj = open('C://Users//Administrator//Desktop//boke_main1.txt', 'w')
    # for a in d_test:
    #     fobj.write(str(a))
    #     fobj.write(',')
    # fobj.close()
    # 候选人名单

    candidate = id_labels
     # 候选人和距离组成一个dict
    c_d = dict(zip(candidate,dist))
    cd_sorted = sorted(c_d.items(), key=lambda d:d[1])
    return cd_sorted
    # dlib.hit_enter_to_continue()