# TODO: your reusable plotting functions here
import matplotlib.pyplot as plt
import utils

def bar_chart(mypy, col_name):
    x, y = utils.get_freq_str(mypy, col_name)
    plt.figure()
    fig, ax = plt.subplots()
#     print(y)
#     print(x)
    plt.bar(x, y)
    plt.xlabel(col_name)
    plt.ylabel('count')
    ax.set_xticklabels(x, rotation=90)
    plt.show()
    
def pie_chart_example(x, y):
    plt.figure()
    plt.pie(y, labels=x, autopct="%1.1f%%")
    plt.show()