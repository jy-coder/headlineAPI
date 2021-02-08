from database.models import *


def save_subscription(records, user):
	for k,v in records.items():
		category = Category.objects.get(category_id =k)

		subscription = Subscription.objects.filter(user=user,category=category)
		# print(subscription)
	
		if v and not subscription:
			subscription = Subscription(user=user, category=category)
			subscription.save()

		elif not v and subscription:
			subscription = Subscription.objects.get(user=user,category=category)
			subscription.delete()


def get_subscription(user):
	records = []
	subscription = Subscription.objects.filter(user=user)
	# print(subscription)
	category_id_list = list(subscription.values_list("category",flat=True))
	# print(category_id_list)
	categories = list(Category.objects.values())
	# print(categories)
	for category in categories:
		category_id = category["category_id"]

		if(category_id in category_id_list):
			category["checked"] = True
		else:
			category["checked"] = False

		records.append(category)
		# print(records)
	

	return records 