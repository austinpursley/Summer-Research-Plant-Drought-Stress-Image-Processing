import os
import time

day = '0601'
times = ['1040', '1210', '1340', '1520']
type = ['front', 'top']
vi   = ['', 'visualize_ir']

#dir = '0800/top/visualize_ir/'

for t in times:
    for y in type:
        for v in vi:
            if v == '':
                dir = t + '/' + y + '/'
            elif v == 'visualize_ir':
                dir = t + '/' + y + '/' + v + '/'
            for f in os.listdir(dir):
                old_name = dir + f
                new_name = ''
                if os.path.splitext(f)[1] == ".jpg":
                    if v == '':
                        new_name = dir + f[:11] + day + t + "00.jpg"
                    elif v == 'visualize_ir':
                        new_name = dir + f[:11] + "_" + day + t + "00.jpg"
                elif os.path.splitext(f)[1] == ".pgm":
                    new_name = dir + f[:11] + "_" + day + t + "00.pgm"
                else:
                    continue
                if os.path.isfile(new_name):
                    continue
                else:
                    print "old name: ", old_name
                    print "new name: ", new_name, '/n'
                    os.rename(old_name, new_name)