plot = create_scatter_plot()
ax = plot.gca()

count = sum(len(collection.get_offsets()) for collection in ax.collections)
points = []
for collection in ax.collections:
    points.extend([tuple(point) for point in collection.get_offsets().tolist()])

title = ax.get_title()
xlabel = ax.get_xlabel()
ylabel = ax.get_ylabel()

count_results = ("chapter-3-level-1-3:count", count)
points_results = ("chapter-3-level-1-3:points", points)
title_results = ("chapter-3-level-1-3:title", title)
xlabel_results = ("chapter-3-level-1-3:xlabel", xlabel)
ylabel_results = ("chapter-3-level-1-3:ylabel", ylabel)
