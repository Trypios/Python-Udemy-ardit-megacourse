# TRIGGERS VIDEO FROM PC WEBCAM
# TRACKS/LOGS MOTION
# DETECTS FACES

import cv2, time, pandas
from datetime import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource


def trigger_video():
    """opens window for live video capture using PC's webcam"""

    prev_frame = None
    screen = {'mode': ord('1'),
            'tracking': False,
            'activity': [(datetime.now(), 1)]}
    print('q = quit')
    print('1 = normal cam')
    print('2 = grayscale cam')
    print('3 = delta cam')

    # start capturing video, 0 denotes the first webcam on the PC
    video = cv2.VideoCapture(0)

    while True:
        # capture video-frame
        check, frame = video.read()
        motion = False
        prev_key = screen['mode']
        prev_track = screen['tracking']

        # detect faces
        face_cascade = cv2.CascadeClassifier("files/haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.05, minNeighbors=5)
        for x, y, width, height in faces:
            face_frame = cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 3)

        if len(faces):
            motion = True

        # turn running frame to gray, then add blur
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        current_frame = cv2.GaussianBlur(frame_gray, (21, 21), 0)

        # compare previous frame with current frame
        if prev_frame is not None:
            frame_delta = cv2.absdiff(prev_frame, current_frame)
        else:
            prev_frame = current_frame
            continue

        # set motion threshold
        frame_thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
        frame_thresh = cv2.dilate(frame_thresh, None, iterations=2)

        # track motion activity
        screen['tracking'] = motion
        if prev_track and not screen['tracking']:
            screen['activity'].append((datetime.now(), 0))
        if not prev_track and screen['tracking']:
            screen['activity'].append((datetime.now(), 1))

        # press q to exit loop...
        key = cv2.waitKey(1)
        if key == ord('q'):
            screen['activity'].append((datetime.now(), 0))
            break
        # ...or numbers 1 2 3 to change camera mode
        elif key == ord('1'):
            prev_key = screen['mode']
            screen['mode'] = ord('1')
        elif key == ord('2'):
            prev_key = screen['mode']
            screen['mode'] = ord('2')
        elif key == ord('3'):
            prev_key = screen['mode']
            screen['mode'] = ord('3')

        if prev_key != screen['mode']:
            cv2.destroyAllWindows()
            prev_key = screen['mode']
        if screen['mode'] == ord('1'):
            cv2.imshow("Original", frame)
        elif screen['mode'] == ord('2'):
            cv2.imshow("Grayscale", frame_gray)
        elif screen['mode'] == ord('3'):
            cv2.imshow("Delta", frame_delta)
        elif screen['mode'] == ord('4'):
            cv2.imshow("Thresh", frame_thresh)

    # after loop, log activity to a csv file
    df = pandas.DataFrame(columns=["Time", "Status"])
    for time, status in screen['activity']:
        df = df.append({"Time": time, "Status": status}, ignore_index=True)
    df.to_csv('./files/log.csv')

    # then end process and close window(s)
    video.release()
    cv2.destroyAllWindows()


def plot_activity():
    """read the log created after video capture and produce a graph based on motion activity"""

    df = pandas.read_csv("files/log.csv")
    #df['Time'] = df['Time'].dt.strftime("%Y-%m-%d %H:%M:%S")
    #df["Start_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
    x_axis = df['Time']
    y_axis = df['Status']

    #cds = ColumnDataSource(df)

    graph = figure(x_axis_type='datetime', height=200, width=1000)
    graph.title.text = 'Motion Activity'
    graph.title.text_font_style = "bold"
    graph.xaxis.axis_label = "Time" 
    graph.yaxis.axis_label = "Activity"
    graph.line(x_axis, y_axis)
    # graph.yaxis.minor_tick_line_color = None
    # graph.ygrid[0].ticker.desired_num_ticks = 1

    # hover = HoverTool(tooltips=[("Start", "@Start_string"), ("End", "@End_string")])
    # graph.add_tools(hover)

    # graph.quad(left=df['Time'][0], right=df['Time'][-1], bottom=0, top=1, color="green")

    output_file("files/motion-activity.html")
    show(graph)


if __name__ == '__main__':
    trigger_video()
    # plot_activity()
