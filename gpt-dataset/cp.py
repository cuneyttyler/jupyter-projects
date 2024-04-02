import shutil

for i in range(0,20,1):
    for j in range(20):
        shutil.copyfile(f'custom-3/{i}.txt',f'custom-3/{(i + 1) * 20 + j}.txt')
        #shutil.copyfile(f'custom-3/{i+1}.txt',f'custom-3/{(i+1)*j+1}.txt')
