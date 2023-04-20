# On Off On switch 

import sensor, image, time, math, tv, pyb

# Set GPIO input
switchColorOne = pyb.Pin("P9", pyb.Pin.IN, pyb.Pin.PULL_UP)
switchColorTwo = pyb.Pin("P7", pyb.Pin.IN, pyb.Pin.PULL_UP)
#switchBlob = pyb.Pin("P7", pyb.Pin.IN, pyb.Pin.PULL_UP)

# Set threshold_list by switch
if switchColorOne.value() == 0 | switchColorTwo.value() == 0:
    # Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
    threshold_list = [( 70, 100,  -30,   40,   20,  100)]
else:
    # Color Tracking Thresholds (Grayscale Min, Grayscale Max)
    threshold_list = [(220, 255)]

print("Resetting Lepton...")
# These settings are applied on reset
sensor.reset()
print("Lepton Res (%dx%d)" % (sensor.ioctl(sensor.IOCTL_LEPTON_GET_WIDTH),
                              sensor.ioctl(sensor.IOCTL_LEPTON_GET_HEIGHT)))
print("Radiometry Available: " + ("Yes" if sensor.ioctl(sensor.IOCTL_LEPTON_GET_RADIOMETRY) else "No"))

# Set color palette by switch
if switchColorOne.value() == 0:
    sensor.set_color_palette(sensor.PALETTE_IRONBOW)
    sensor.set_pixformat(sensor.RGB565)
elif switchColorTwo.value() == 0:
    sensor.set_pixformat(sensor.GRAYSCALE)
else:
    sensor.set_pixformat(sensor.RGB565)


sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=5000)
sensor.set_hmirror(True)
clock = time.clock()

tv.init(triple_buffer=False) # Initialize the tv.
tv.channel(8) # For wireless video transmitter shield

# Flip image 180 degrees

sensor.set_vflip(True)

while(True):
    clock.tick()
    img = sensor.snapshot()
    #if switchBlob.value() != 0:
        # Set pixels_threshold and area_threshold higher (200) if picking up too many blobs
        #for blob in img.find_blobs(threshold_list, pixels_threshold=65, area_threshold=65, merge=True):
            #img.draw_rectangle(blob.rect(), color=127)
            #img.draw_cross(blob.cx(), blob.cy(), color=127)
    #else:
        #break
    tv.display(sensor.snapshot()) # Take a picture and display the image.
    #print(clock.fps())
