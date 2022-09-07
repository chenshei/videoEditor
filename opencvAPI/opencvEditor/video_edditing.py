import cv2 as cv
import json
import numpy as np
import os
from pathlib import Path

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

base_dir = Path(__file__).resolve().parent.parent


def load_json(json_file):
    # JSON file
    with open(json_file, "r") as f:
        # Reading from file
        return json.loads(f.read())


def extract_frames(video):
    frames = []
    video = cv.VideoCapture(video)

    while True:
        read, frame = video.read()
        if not read:
            break
        frames.append(frame)
    return frames


def edit_photo(edited_frame, corners):
    is_closed = True
    color = (0, 255, 0)
    thickness = 2
    np_corners = np.array([corners], np.int32)

    image = cv.polylines(edited_frame, np_corners,
                         is_closed, color, thickness)
    return image


def insert_imgs_on_frames(frames, edit_data, name):
    path = os.path.join(base_dir, 'media\\frames\\' + name)
    if not os.path.exists(path):
        os.mkdir(path)
    for index, edit_instruction in edit_data.items():
        edited_frame = frames[int(index) - 1]
        for polygon_data in edit_instruction.values():
            # print(polygon_data["corners"])
            corners = polygon_data["corners"]
            img = edit_photo(edited_frame, corners)
            frames[int(index) - 1] = img
            cv.imwrite(os.path.join(path, 'frame-{0}.jpg'.format(index)), img)
            print('wrote {0} of {1}'.format(index, len(edit_data)))
    return frames


@api_view(['GET', 'POST'])
def main(request, video):
    print('started!')
    data = load_json(os.path.join(base_dir, "media\\" + video + ".json"))
    polygon_data = data["metadata"]["frames"]
    frames = extract_frames(os.path.join(base_dir, "media\\original\\" + video + ".mp4"))
    name = os.path.basename(video)
    name = os.path.splitext(name)[0].lower()
    edited_frames = insert_imgs_on_frames(frames, polygon_data, name)

    height, width, _ = frames[0].shape
    fourcc = cv.VideoWriter_fourcc(*'mp4v')

    out = cv.VideoWriter(os.path.join(base_dir, 'media\\edited\\' + video + '.mp4'),
                         fourcc, 30.0, (width, height))
    [out.write(f) for f in edited_frames]
    out.release()
    print('done!')
    return Response(status=status.HTTP_201_CREATED)
