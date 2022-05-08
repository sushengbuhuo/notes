import itchat,os
from math import sqrt
from PIL import Image
path = os.getcwd() + '\\wechat_pics\\'
numbers = input('公众号苏生不惑提示你，请输入要下载的微信好友头像数量，默认为500：')
if numbers == '':
	numbers = 500
# print(path) core.loginInfo['wxsid'] = core.loginInfo['BaseRequest']['Sid'] = cookies["wxsid"]
def save_avatar(path):
	if not os.path.exists(path):
		os.mkdir(path)
	itchat.auto_login(hotReload=False, enableCmdQR=2)
	num = 0
	for friend in itchat.get_friends(update=True)[0:]:
		if num > int(numbers):
			break
		print(friend['NickName'])
		img = itchat.get_head_img(userName=friend["UserName"])
		img_path = path + friend['NickName'] + "_" + friend['RemarkName'] + ".jpg"
		try:
			with open(img_path,'wb') as f:
				f.write(img)
				num+=1
		except Exception as e:
			print('error')
	print("微信好友头像下载完成")
def joint_avatar(path):	
	pathList = []
	for item in os.listdir(path):
	    imgPath = os.path.join(path,item)
	    pathList.append(imgPath)
	total = len(pathList)
	line = int(sqrt(total))
	NewImage = Image.new('RGB', (128*line,128*line))
	x = y = 0
	for item in pathList:
	    try:
	        img = Image.open(item)
	        img = img.resize((128,128),Image.ANTIALIAS)
	        NewImage.paste(img, (x * 128 , y * 128))
	        x += 1
	    except IOError:
	        print("图片读取失败:%s" % (item))
	        x -= 1
	    if x == line:
	        x = 0
	        y += 1
	    if (x+line*y) == line*line:
	        break
	NewImage.save("wechat_friends.jpg")
	print("微信好友头像拼接完成")
save_avatar(path)
joint_avatar(path)