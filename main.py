import os
import csv
import datetime


def check_hypothesis(csv_file_path):
	"""
	Проверить гипотезу, что пользователи, которые 
	выбирают больше двух комплектов приборов, 
	оставляют больше чаевых, чем остальные

	:param csv_file_path: str - пусть к файлу с данными

	:return True: если гипотеза верна
	:return False: если гипотеза НЕ верна
	"""

	more_cutlery_rows = []  # Строки, где больше 2х столовых приборов
	less_cutlery_rows = []  # Строки, где больше 2х столовых приборов

	with open(csv_file_path, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

		for i, row in enumerate(spamreader):
			# print(row)

			if i == 0: 
				continue

			if int(row[1]) > 2:
				more_cutlery_rows.append(row)
			else:
				less_cutlery_rows.append(row)

	print(len(more_cutlery_rows))
	print(len(less_cutlery_rows))

	# Сумма чаевых у тех, кто брал больше 2х приборов
	more_cutlery_tips_sum = sum([int(x[2]) for x in more_cutlery_rows])
	# Сумма чаевых у тех, кто брал 2 и меньше приборов
	less_cutlery_tips_sum = sum([int(x[2]) for x in less_cutlery_rows])

	print(more_cutlery_tips_sum)
	print(less_cutlery_tips_sum)

	# Средняя сумма чаевых у тех, кто брал больше 2х приборов
	average_cutlery_more = more_cutlery_tips_sum / len(more_cutlery_rows)
	# Средняя сумма чаевых у тех, кто брал больше 2х приборов
	average_cutlery_less = less_cutlery_tips_sum / len(less_cutlery_rows)

	print(average_cutlery_more)
	print(average_cutlery_less)

	if average_cutlery_more > average_cutlery_less:
		return True
	else:
		return False


def gather_users_segment(csv_file_path):
	"""
	Соберите сегмент пользователей
	Все uid пользователей, которые добавляли в заказ больше двух 
	комплектов столовых приборов и делали заказ не в январские 
	праздники на сумму больше 800p

	:param csv_file_path: str - пусть к файлу с данными

	:return: массив uid
	"""

	arr = []

	with open(csv_file_path, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

		for i, row in enumerate(spamreader):
			# print(row)

			if i == 0: 
				continue
			
			if int(row[1]) > 2 and int(row[3]) > 800:
				order_dt = datetime.datetime(
					int(row[0].split(' ')[0].split('-')[0]),
					int(row[0].split(' ')[0].split('-')[1]),
					int(row[0].split(' ')[0].split('-')[2]),
				)

				# Проверка на январские праздники
				if order_dt.month == 1:
					if order_dt.day >= 1 and order_dt.day <= 10:
						continue

				arr.append(int(row[4]))

	return list(set(arr))


def main():
	csv_file_path = os.path.join(os.path.dirname(__file__), 'shmya_final_version.csv')

	if check_hypothesis(csv_file_path):
		print('Гипотеза верна')
	else:
		print('Гипотеза НЕ верна')

	users_uids = gather_users_segment(csv_file_path)
	print('Сегмент пользователей:', users_uids)
	print('Количество пользователей:', len(users_uids))


if __name__ == '__main__':
	main()
