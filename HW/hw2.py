import json
import urllib.request

userlist = []
nextuser = input('Введите следующего пользователя. Чтобы закончить вводить список, введите пустую строку: ')
while nextuser != '':
	userlist.append(nextuser)
	userlist = input('Введите следующего пользователя. Чтобы закончить вводить список, введите пустую строку: ')

token = input('Введите свой токен для доступа к API: ')

def findpagenum(user, token):
	page = 1
	check = True
	while check: 
		url = 'https://api.github.com/users/%s/repos?access_token=%s?page=%s&per_page=100' % (user, token, page)  
		response = urllib.request.urlopen(url)
		text = response.read().decode('utf-8')
		data = json.loads(text)
		if len(data) > 0:
			page += 1
		else:
			return page-1
# функция, которая определяет число страниц, 
# которые необходимо рассмотреть, чтобы перебрать все репозитории

def name_and_desc(user, token):
	print('Вот список его репозиториев:')
	for i in range(1, maxpage+1):
		url = 'https://api.github.com/users/%s/repos?access_token=%s?page=%s&per_page=100' % (user, token, i)  
		response = urllib.request.urlopen(url)
		text = response.read().decode('utf-8')
		data = json.loads(text)
		for j in data:
			print(str(j["name"]) + ' : ' + str(j["description"]))

def create_dic(user, token):
	dic_lang = {}
	for i in range(1, maxpage+1):
		url = 'https://api.github.com/users/%s/repos??access_token=%spage=%s&per_page=100' % (user, token, i)  
		response = urllib.request.urlopen(url)
		text = response.read().decode('utf-8')
		data = json.loads(text)
		for j in data:
			if j["language"] not in dic_lang:
				dic_lang[j["language"]] = 1
			else:
				dic_lang[j["language"]] += 1
	return dic_lang

def language(dic_lang, user):
	keys = list(dic_lang.keys())
	values = list(dic_lang.values())
	print('Список используемых языков: ' + keys)
	for i in range(len(dic_lang)):
		print('Язык ' + str(keys[i]) + ' используется в количестве репозиториев: ' + str(values[i]))

def max_rep(userlist, token):
	lenlist = []
	maxim = 0
	maxim_ind = 0
	for user in userlist:
		sum_len = 0
		for i in range(1, maxpage+1):
			url = 'https://api.github.com/users/%s/repos??access_token=%spage=%s&per_page=100' % (user, token, i)  
			response = urllib.request.urlopen(url)
			text = response.read().decode('utf-8')
			data = json.loads(text)
			sum_len += len(data)
		lenlist.append(sum_len)
	for i in range(len(lenlist)):
		if lenlist[i] > maxim:
			maxim_ind = i
	print('Больше всего репозиториев у пользователя ' + str(userlist[i]))

def pop_lang(userlist, token):
	dic_poplang = {}
	for user in userlist:
		dic = create_dic(user, token)
		dic_poplang.update(dic)
	keys = list(dic_lang.keys())
	values = list(dic_lang.values())
	maxim = 0
	maxim_ind = 0
	for i in range(len(values)):
		if values[i] > maxim:
			maxim_ind = i
	print('Самый популярный язык - это ' + keys[maxim_ind])

def main(userlist, token):
	user = input('Введите имя пользователя: ')
	if user not in userlist:
		print('Данного пользователя нет в списке')
	else:
		maxpage = findpagenum(user, token)
		name_and_desc(user, token)
		dic_lang = create_dic(user, token)
		language(dic_lang, user)
		max_rep(userlist, token)
		pop_lang(userlist, token)

main(userlist, token)
