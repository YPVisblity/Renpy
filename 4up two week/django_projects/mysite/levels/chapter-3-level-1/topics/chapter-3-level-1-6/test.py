plot = create_pie_chart()
ax = plot.gca()

count = len(ax.patches)
labels = [text.get_text() for text in ax.texts if text.get_text()]
title = ax.get_title()

count_results = ("chapter-3-level-1-4:count", count)
labels_results = ("chapter-3-level-1-4:labels", labels)
title_results = ("chapter-3-level-1-4:title", title)
