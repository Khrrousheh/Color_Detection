import pandas as pd
import cv2

# Define paths of color data frame and image we will use
img_path = 'pic3.jpg'
csv_path = 'colors.csv'

# Read image and resize it into 800*600
img = cv2.imread(img_path)
img = cv2.resize(img, (800, 600))

# Read color dataframe
df_header = ['Color', 'Color_name', 'hexCode', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=df_header, header=None)

# Main parameters
clicked = False
r = g = b = x_pos = y_pos = 0


def get_color_name(red, green, blue):
    minimum = 1000
    for i in range(len(df)):
        d = abs(red - int(df.loc[i, 'R'])) + abs(green - int(df.loc[i, 'G'])) + abs(blue - int(df.loc[i, 'B']))
        if d <= minimum:
            minimum = d
            color_name = df.loc[i, 'Color_name']

    return color_name


def get_tracked_color(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


# Create Windows
cv2.namedWindow("Image")
cv2.setMouseCallback('Image', get_tracked_color)

while True:
    cv2.imshow('Image', img)
    if clicked:
        # cv2.rectangle(image, start point, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (600, 60), (b, g, r), -1)

        # Creating text string to display( Color name and RGB values )
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
