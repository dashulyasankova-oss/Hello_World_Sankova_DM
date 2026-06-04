fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(
    2, 2,
    figsize=(14, 10)   # ширина × высота в дюймах
)
fig.suptitle("Анализ учебной базы данных", fontsize=16, fontweight="bold", y=1.01)