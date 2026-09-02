plot = create_bar_chart()
ax = plot.gca()

count = len(ax.patches)
price = [bar.get_height() for bar in ax.patches]
fruit = [label.get_text() for label in ax.get_xticklabels()]

title = ax.get_title()
xlabel = ax.get_xlabel()
ylabel = ax.get_ylabel()

count_results = ("chapter-3-level-1-2:count", count)
price_results = ("chapter-3-level-1-2:price", price)
fruit_results = ("chapter-3-level-1-2:fruit", fruit)
title_results = ("chapter-3-level-1-2:title", title)
xlabel_results = ("chapter-3-level-1-2:xlabel", xlabel)
ylabel_results = ("chapter-3-level-1-2:ylabel", ylabel)