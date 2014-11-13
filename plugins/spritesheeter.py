#!/usr/bin/python

import os
import Image

# All related files are in subfolder \emoti\
# Use icon_map.txt and enter name_of_emoti:file.png per line. All files must be the same resolution (24x24px in our case).

def emoti():

    script_dir = os.path.dirname(__file__)
    rel_path = "emoti/icon_map.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    iconMapFile = open(abs_file_path)
    iconMap = sorted( line.rstrip().split(':') for line in iconMapFile.readlines()
                      if line.rstrip())
    iconMapFile.close()

    images = [Image.open(os.path.join(script_dir, "emoti/%s" % (filename))) for cssClass, filename in iconMap]

    print "%d images will be combined." % len(images)

    image_width, image_height = images[0].size

    print "all images assumed to be %d by %d." % (image_width, image_height)

    master_width = image_width
    master_height = (image_height * len(images))
    print "the master image will by %d by %d" % (master_width, master_height)
    print "creating image...",
    master = Image.new(
        mode='RGBA',
        size=(master_width, master_height),
        color=(0,0,0,0))

    print "created."

    for count, image in enumerate(images):
        location = image_height*count
        print "adding %s at %d..." % (iconMap[count][1], location),
        master.paste(image,(0,location))
        print "added."
    print "done adding icons."

    print "saving master.gif...",
    master.save((os.path.join(script_dir, "emoti/master.gif")), transparency=0 )
    print "saved!"

    print "saving master.png...",
    master.save((os.path.join(script_dir, "emoti/master.png")))
    print "saved!"


    cssTemplate = '''a[href="/%s"] {
        background-position: 0px -%dpx;
    }
    '''

    for format in ['png','gif']:
        print 'saving icons_%s.css...' % format,
        iconCssFile = open((os.path.join(script_dir, "emoti/icons_%s.css" % format )),'w')
        for count, pair in enumerate(iconMap):
            cssClass, filename = pair
            location = image_height*count
            iconCssFile.write( cssTemplate % (cssClass, location) )
        iconCssFile.close()
        print 'created!'

if __name__ == '__main__':
    emoti()