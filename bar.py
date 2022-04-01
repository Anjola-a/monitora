import matplotlib.pyplot as plt
# fig, ax = plt.subplots()
# ax = fig.add_axes([0,0,1,1])
langs = ['C', 'C++', 'Java', 'Python', 'PHP']
students = [23,17,35,29,12]
plt.bar(langs,students)
plt.show()