set terminal pngcairo size 1000,600
set output 'data/status_categories_generated.png'

set title 'HTTP Status Category Distribution'
set xlabel 'HTTP Status Category'
set ylabel 'Number of Requests'

set xrange [-0.5:4.5]
set yrange [0:*]

set xtics ('1xx' 0, '2xx' 1, '3xx' 2, '4xx' 3, '5xx' 4)
set ytics auto
set grid ytics
set boxwidth 0.6
set style fill solid 0.7
set key off

plot 'data/status_categories.dat' using (column(0)):2 with boxes, \
     'data/status_categories.dat' using (column(0)):($2+0.2):(sprintf('%g',$2)) with labels notitle

