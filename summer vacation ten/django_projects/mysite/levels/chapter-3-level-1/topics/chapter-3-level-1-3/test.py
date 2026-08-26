plot = create_plot()
ax = plot.gca()

line_count = len(ax.lines)

line = ax.lines[0] if ax.lines else None
x_data = list(line.get_xdata()) if line else []
y_data = list(line.get_ydata()) if line else []

plot_title = ax.get_title()
x_label = ax.get_xlabel()
y_label = ax.get_ylabel()

line_count_signature = ("chapter-3-level-1-1:line_count", line_count)
x_data_signature = ("chapter-3-level-1-1:x_data", x_data)
y_data_signature = ("chapter-3-level-1-1:y_data", y_data)
title_signature = ("chapter-3-level-1-1:title", plot_title)
xlabel_signature = ("chapter-3-level-1-1:xlabel", x_label)
ylabel_signature = ("chapter-3-level-1-1:ylabel", y_label)
