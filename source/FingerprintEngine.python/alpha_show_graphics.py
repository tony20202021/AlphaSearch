import numpy as np
import matplotlib.pyplot as plt
import pylab
import cv2

# import matplotlib
# print(matplotlib.__version__)

def show_diff(bright, bright_diff):
    plt.figure(figsize=(9, 9))

    total_subplots = 6
    plt.subplot(total_subplots, 1, 1)
    bright_plot = bright[0]
    plt.bar(np.arange(bright_plot.size), bright_plot, color="red")

    plt.subplot(total_subplots, 1, 2)
    bright_plot = bright[1]
    bright_diff_plot = bright_diff[1]
    plt.bar(np.arange(bright_plot.size), bright_plot, color="green")
    plt.plot(np.arange(bright_diff_plot.size), bright_diff_plot, color="red")

    plt.subplot(total_subplots, 1, 3)
    bright_plot = bright[2]
    bright_diff_plot = bright_diff[2]
    plt.bar(np.arange(bright_plot.size), bright_plot, color="blue")
    plt.plot(np.arange(bright_diff_plot.size), bright_diff_plot, color="green")

    plt.subplot(total_subplots, 1, 4)
    bright_plot = bright[3]
    bright_diff_plot = bright_diff[3]
    plt.bar(np.arange(bright_plot.size), bright_plot, color="black")
    plt.plot(np.arange(bright_diff_plot.size), bright_diff_plot, color="blue")

    plt.subplot(total_subplots, 1, 5)
    bright_plot = bright[4]
    bright_diff_plot = bright_diff[4]
    plt.bar(np.arange(bright_plot.size), bright_plot, color="yellow")
    plt.plot(np.arange(bright_diff_plot.size), bright_diff_plot, color="black")

    plt.subplot(total_subplots, 1, 6)
    bright_plot = bright[5]
    bright_diff_plot = bright_diff[5]
    plt.bar(np.arange(bright_plot.size), bright_plot, color="cyan")
    plt.plot(np.arange(bright_diff_plot.size), bright_diff_plot, color="yellow")

    plt.show()


def show_time_line(time_lines_all, title):

    # def frames2seconds(x):
    #     return x * time_lines_all[i]['duration'] / time_lines_all[i]['frames']
    #
    # def seconds2frames(x):
    #     return x * time_lines_all[i]['frames'] / time_lines_all[i]['duration']

    plt.figure(figsize=(15, 9))
    plt.gcf().canvas.set_window_title(title)

    ax1 = None
    ax2 = None
    group_ax_shared = None

    group = None
    group_index = 0
    groups = [time_line['group'] for time_line in time_lines_all]
    count_groups = len(np.unique(groups))

    count_plots = len(time_lines_all)
    for i in range(count_plots):
        # plt.subplot(count_plots, 1, 1)
        # plt.title('value')
        # plt.grid(True)

        # x = [line['frame_index'] * time_lines_all['duration'] / time_lines_all['frames'] for line in time_lines_all['details']]
        # y = [line['value'] for line in time_lines_all['details']]
        # plt.plot(x, y, marker='o', label=time_lines_all['name'] + '(' + str(len(time_lines_all['details'])) + ')')
        # plt.legend()

        # y = np.repeat(diff_threshold_sum, len(bright_time_line))
        # plt.plot(x, y, "r--")

        if (group is None) or (group != time_lines_all[i].get('group', 2)):
            group = time_lines_all[i].get('group', 2)
            group_index += 1

            ax1 = plt.subplot(count_groups, 1, group_index, sharex=group_ax_shared)
            if group_ax_shared is None:
                group_ax_shared = ax1

            plt.title(time_lines_all[i]['subplot_name'])
            ax1.grid(True)
            ax1.set_xlabel('time(seconds)', x=0, horizontalalignment='left')

            # ax2 = ax1.secondary_xaxis('top', functions=(frames2seconds, seconds2frames))
            # ax2.set_xlabel('frames(number), fps={:.1f}'.format(time_lines_all[i]['frames'] / time_lines_all[i]['duration']), x=0, horizontalalignment="left")

        label = time_lines_all[i].get('plot_label', '') + '(values: ' + str(len(time_lines_all[i]['values'])) + ')'
        markersize = time_lines_all[i].get('markersize', 2)
        linewidth = time_lines_all[i].get('linewidth', 1)
        width = time_lines_all[i].get('width', 0.5)
        shift = time_lines_all[i].get('shift', 0.0)

        x = [shift + line['x'] for line in time_lines_all[i]['values']]
        y = [line['y'] for line in time_lines_all[i]['values']]

        if time_lines_all[i].get('plot_type', 'plot') == 'plot':
            ax1.plot(x, y, marker='o', markersize=markersize, linewidth=linewidth, label=label)
        elif time_lines_all[i].get('plot_type') == 'bar':
            ax1.bar(x, y, width=width, label=label)
        else:
            assert(False)

        plt.legend()

    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.5, wspace=1.65)
    plt.show(block=True)

def show_image_cv(image, title='image'):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_gray_cv(image, height, width, title='image'):
    gray = image[:height * width].reshape([height, width])
    gray3 = np.stack((gray, gray, gray), axis=-1)

    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, gray3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_image_pylab(image, height, width, title='image'):
    gray = image[:height * width].reshape([height, width])
    gray3 = np.stack((gray, gray, gray), axis=-1)

    pylab.imshow(gray3)
    pylab.gcf().canvas.set_window_title(title)

    plt.show(block=True)
