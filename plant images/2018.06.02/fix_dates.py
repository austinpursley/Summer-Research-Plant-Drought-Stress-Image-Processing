import os

day = '0602'
time = ['0800]', '1000', '1200', '1400', '1600']
type = ['front', 'top']
vi   = ['', 'visualize_ir']


#dir = '0800/top/visualize_ir/'

for t in time:
    for y in type:
        for v in vi:
            if v == '':
                dir = t + '/' + y + '/'
            elif v == 'visualize_ir':
                dir = t + '/' + y + '/' + v + '/'
            for f in os.listdir(dir):
                if (os.path.splitext(f)[1] == ".pgm") | (os.path.splitext(f)[1] == ".jpg"):
                    old_name = dir + f
                    new_name = dir + day + t + "00" + f[-16:]
                    print old_name
                    print new_name
                    if os.path.isfile(new_name):
                        continue
                    else:
                        print "old name: ", old_name
						print "new name: ", new_name, '/n'
						os.rename(old_name, new_name)